"""Configuration parsing utilities.

This module defines types and helpers to declaratively register expected
configuration keys, parse raw values from a file and retrieve typed
values. Errors raised during parsing are defined in
``src/mazegen/errors.py`` and include contextual information such as
the offending key or line number.
"""

from enum import Enum
from typing import Generic, TypeVar, cast, Type, Any
from .errors import (
    ConfigFormatError,
    ConfigMissingError,
    ConfigValueError,
    ConfigFileNotFoundError,
)


t_coords = tuple[int, int]
T = TypeVar('T')


class EConfig(Enum):
    """Enumeration of supported configuration keys.

    Each member's value is the textual key expected in the config file.
    """

    WIDTH = 'width'
    HEIGHT = 'height'
    ENTRY = 'entry'
    EXIT = 'exit'
    OUTPUT_FILE = 'output_file'
    PERFECT = 'perfect'
    DEBUG = 'debug_mode'
    MAZE_SEED = 'maze_seed'
    LOGO_FILE = 'logo_file'
    ANIMATE_MAZE_GENERATION = 'animate_maze_generation'
    MAZE_GENERATION_SPEED = 'maze_generation_speed'
    ANIMATE_MAZE_SOLVING = 'animate_maze_solving'
    MAZE_SOLVING_SPEED = 'maze_solving_speed'
    SHOW_FPS = 'show_fps'


class ConfigValue(Generic[T]):
    """Descriptor for a single configuration value.

    A ConfigValue knows how to parse a raw string into the expected
    Python type and stores the resulting value. It also tracks whether
    the value is required and a default may be provided.
    """

    def __init__(
        self,
        key: EConfig,
        value_type: Type[Any] | tuple[Type[Any], ...],
        default: T | None = None,
        required: bool = True,
    ) -> None:
        """Create a new ConfigValue.

        Args:
            key: The configuration key (EConfig) this entry represents.
            value_type: Expected Python type or tuple of types (for tuples).
            default: Optional default value used when not required.
            required: Whether the value must be present in the config.

        Returns:
            None
        """

        self.key: EConfig = key
        self.value_type: Type[Any] | tuple[Type[Any], ...] = value_type
        self.required: bool = required
        self.value: T | None = default

    def parse(self, raw_value: str, line: int) -> None:
        """Parse a raw configuration string into the expected type.

        The method dispatches to helper parsing functions depending on
        the declared ``value_type``. On failure it raises
        ``ConfigValueError`` with context.

        Args:
            raw_value: Raw string read from the configuration file.
            line: Line number where the value was read (used in errors).

        Returns:
            None
        """

        key = str(self.key.value)

        if self.value_type is int:
            self.value = cast(T, self.parse_int(raw_value, key, line))

        elif self.value_type is str:
            self.value = cast(T, self.parse_string(raw_value, key, line))

        elif isinstance(self.value_type, tuple):
            self.value = cast(
                T,
                self.parse_tuple(raw_value, self.value_type, key, line),
            )

        elif self.value_type is bool:
            self.value = cast(T, self.parse_bool(raw_value, key, line))

        elif self.value_type is float:
            self.value = cast(T, self.parse_float(raw_value, key, line))

        else:
            raise ConfigValueError(key, raw_value, line)

    def get_value(self) -> T:
        """Return the parsed value, or raise if not yet parsed.

        Returns:
            The parsed value of type ``T``.

        Raises:
            ValueError: If the value is still None (not parsed and no default).
        """

        if self.value is None:
            key = str(self.key.value)
            raise ValueError(f'Value for key "{key}" has not been parsed yet.')

        return self.value

    @staticmethod
    def parse_int(value: str, key: str, line: int = -1) -> int:
        """Parse an integer value or raise a ConfigValueError.

        Args:
            value: Raw string to parse.
            key: Configuration key name (for error messages).
            line: Line number where the value was read.

        Returns:
            The parsed integer.

        Raises:
            ConfigValueError: If conversion to int fails.
        """

        try:
            return int(value)
        except ValueError as exc:
            raise ConfigValueError(key, value, line) from exc

    @staticmethod
    def parse_string(value: str, key: str, line: int = -1) -> str:
        """Parse and validate a non-empty string value.

        Raises ``ConfigValueError`` when the trimmed string is empty.
        """

        value = value.strip()
        if not value:
            raise ConfigValueError(key, value, line)
        return value

    @staticmethod
    def parse_tuple(
        value: str,
        types: tuple[Type[Any], ...],
        key: str,
        line: int = -1,
    ) -> tuple[Any, ...]:
        """Parse a comma-separated tuple of values into the provided types.

        The number of items must match the length of ``types`` and each
        item is parsed according to its corresponding type.
        """

        values = value.split(",")

        if len(values) != len(types):
            raise ConfigValueError(key, value, line)

        parsed_values: list[Any] = []

        try:
            for raw, typ in zip(values, types):
                raw = raw.strip()

                if typ is int:
                    parsed_values.append(int(raw))
                elif typ is float:
                    parsed_values.append(float(raw))
                elif typ is str:
                    parsed_values.append(raw)
                elif typ is bool:
                    parsed_values.append(
                        ConfigValue.parse_bool(raw, key, line)
                    )
                else:
                    raise ConfigValueError(key, value, line)

        except ValueError as exc:
            raise ConfigValueError(key, value, line) from exc

        return tuple(parsed_values)

    @staticmethod
    def parse_bool(value: str, key: str, line: int = -1) -> bool:
        """Parse a boolean from text (true/false or 1/0).

        Raises ConfigValueError if the token is not a recognized boolean.
        """

        value = value.strip().lower()

        if value in {"true", "1"}:
            return True
        if value in {"false", "0"}:
            return False

        raise ConfigValueError(key, value, line)

    @staticmethod
    def parse_float(value: str, key: str, line: int = -1) -> float:
        """Parse a floating point value or raise ConfigValueError.

        Args:
            value: Raw string to parse.
            key: Configuration key name used in errors.
            line: Line number where the value was read.

        Returns:
            The parsed float.
        """

        try:
            return float(value)
        except ValueError as exc:
            raise ConfigValueError(key, value, line) from exc


class ConfigParser:
    """Low-level parser that reads raw key/value pairs from a file.

    The parser stores raw strings along with their line numbers and
    exposes a registration API used by higher-level components to
    request typed parsing.
    """

    def __init__(self, filename: str) -> None:
        """Read the file and populate raw_data with (value, line).

        Args:
            filename: Path to the configuration file to read.

        Raises:
            ConfigFileNotFoundError: If the file cannot be opened.
        """

        self.raw_data: dict[str, tuple[str, int]] = {}
        self.registered_values: dict[EConfig, ConfigValue[Any]] = {}
        try:
            with open(filename, 'r') as f:
                line_number = 0
                for line in f:
                    line_number += 1
                    if (line.strip() == '' or line.strip().startswith('#')):
                        continue
                    if '=' in line and '"' in line:
                        key_part, value_part = line.split('=', 1)
                        key = key_part.strip().lower()
                        value = value_part.strip()
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        self.raw_data[key] = (value, line_number)
                        continue
                    config_line = line.replace('\n', '').split('=')

                    if (len(config_line) != 2):
                        raise ConfigFormatError(line_number=line_number)

                    [key, value] = config_line
                    self.raw_data[key.lower().strip()] = (value, line_number)

        except FileNotFoundError:
            raise ConfigFileNotFoundError()

    def register(self, config_value: ConfigValue[T]) -> None:
        """Register a ConfigValue and attempt to parse it from raw_data.

        If the raw key exists its value is parsed and stored; if the key
        is required but missing a ConfigMissingError is raised.
        """

        key: str = config_value.key.value
        if key in self.raw_data:
            raw_value, line_number = self.raw_data[key]
            config_value.parse(raw_value, line_number)
            self.registered_values[config_value.key] = config_value
        elif config_value.required and config_value.value is None:
            raise ConfigMissingError(key)

    def get(self, key: EConfig) -> ConfigValue[T]:
        """Return a previously registered ConfigValue.

        Raises ConfigMissingError if the requested key was not registered
        or parsed successfully.
        """

        config_value = self.registered_values.get(key)
        if config_value is None:
            raise ConfigMissingError(str(key.value))
        return config_value


class Config:
    """Convenience wrapper exposing typed getters for parsed config.

    The constructor registers the known set of configuration keys and
    triggers parsing of the provided file.
    """

    def __init__(self, filename: str) -> None:
        """Parse the configuration file and prepare typed accessors.

        Args:
            filename: Path to the configuration file.

        Returns:
            None
        """

        parser = ConfigParser(filename)
        self.parser: ConfigParser = parser
        parser.register(ConfigValue[int](EConfig.WIDTH, int))
        parser.register(ConfigValue[int](EConfig.HEIGHT, int))
        parser.register(ConfigValue[t_coords](EConfig.ENTRY, (int, int)))
        parser.register(ConfigValue[t_coords](EConfig.EXIT, (int, int)))
        parser.register(ConfigValue[str](EConfig.OUTPUT_FILE, str))
        parser.register(ConfigValue[bool](EConfig.PERFECT, bool))
        parser.register(ConfigValue[str](EConfig.LOGO_FILE, str))
        parser.register(ConfigValue[bool](EConfig.DEBUG, bool, False, False))
        parser.register(ConfigValue[str](
            EConfig.MAZE_SEED, str, "0", False
        ))
        parser.register(ConfigValue[bool](
            EConfig.ANIMATE_MAZE_GENERATION, bool
        ))
        parser.register(ConfigValue[float](
            EConfig.MAZE_GENERATION_SPEED, float, 1.0, False
        ))
        parser.register(ConfigValue[bool](
            EConfig.ANIMATE_MAZE_SOLVING, bool
        ))
        parser.register(ConfigValue[float](
            EConfig.MAZE_SOLVING_SPEED, float, 1.0, False
        ))
        parser.register(ConfigValue[bool](
            EConfig.SHOW_FPS, bool, False, False
        ))

    def get(self, key: EConfig) -> ConfigValue[Any]:
        """Return the ConfigValue for the given key.

        Args:
            key: EConfig member identifying the requested value.

        Returns:
            The ConfigValue instance for the key.
        """

        return self.parser.get(key)

    def get_int(self, key: EConfig) -> ConfigValue[int]:
        """Return a ConfigValue typed as int for the given key."""

        return cast(ConfigValue[int], self.parser.get(key))

    def get_str(self, key: EConfig) -> ConfigValue[str]:
        """Return a ConfigValue typed as str for the given key."""

        return cast(ConfigValue[str], self.parser.get(key))

    def get_coords(self, key: EConfig) -> ConfigValue[t_coords]:
        """Return a ConfigValue typed as a tuple of two ints (coords)."""

        return cast(ConfigValue[t_coords], self.parser.get(key))

    def get_tuple(self, key: EConfig) -> ConfigValue[tuple[Any, ...]]:
        """Return a ConfigValue typed as a tuple for the given key."""

        return cast(ConfigValue[tuple[Any, ...]], self.parser.get(key))

    def get_bool(self, key: EConfig) -> ConfigValue[bool]:
        """Return a ConfigValue typed as bool for the given key."""

        return cast(ConfigValue[bool], self.parser.get(key))

    def get_float(self, key: EConfig) -> ConfigValue[float]:
        """Return a ConfigValue typed as float for the given key."""

        return cast(ConfigValue[float], self.parser.get(key))
