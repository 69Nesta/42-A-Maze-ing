from enum import Enum
from typing import Generic, TypeVar, cast
from src.errors import (
    ConfigFormatError,
    ConfigMissingError,
    ConfigValueError
)

t_coords = tuple[int, int]
T = TypeVar('T', int, str, tuple, bool, float)


class EConfig(Enum):
    WIDTH = 'width'
    HEIGHT = 'height'
    ENTRY = 'entry'
    EXIT = 'exit'
    OUTPUT_FILE = 'output_file'
    PERFECT = 'perfect'
    DEBUG = 'debug_mode'
    MAZE_SEED = 'maze_seed'
    ANIMATE_MAZE_GENERATION = 'animate_maze_generation'
    MAZE_GENERATION_SPEED = 'maze_generation_speed'
    ANIMATE_MAZE_SOLVING = 'animate_maze_solving'
    MAZE_SOLVING_SPEED = 'maze_solving_speed'


class ConfigValue(Generic[T]):
    def __init__(
                self,
                key: EConfig,
                value_type: type,
                default: T | None = None,
                required: bool = True
            ) -> None:
        self.key: EConfig = key
        self.value_type: type = value_type
        self.required: bool = required
        self.value: T | None = default

    def parse(self, raw_value: str, line: int) -> None:
        key = str(self.key.value)
        if self.value_type is int:
            self.value = cast(T, self.parse_int(raw_value, key, line))
        elif self.value_type is str:
            self.value = cast(T, self.parse_string(raw_value, key, line))
        elif type(self.value_type) is tuple:
            self.value = cast(T, self.parse_tuple(
                raw_value,
                self.value_type,
                key,
                line
            ))
        elif self.value_type is bool:
            self.value = cast(T, self.parse_bool(raw_value, key, line))
        elif self.value_type is float:
            self.value = cast(T, self.parse_float(raw_value, key, line))
        else:
            raise ConfigValueError(key, raw_value, line)

    def get_value(self) -> T:
        key = str(self.key.value)
        if self.value is None:
            raise ValueError(f'Value for key "{key}" has not been parsed yet.')
        return self.value

    @staticmethod
    def parse_int(value: str, key: str, line: int = -1) -> int:
        try:
            return int(value)
        except ValueError:
            raise ConfigValueError(key, value, line)

    @staticmethod
    def parse_string(value: str, key: str, line: int = -1) -> str:
        value = value.strip()
        if len(value) == 0:
            raise ConfigValueError(key, value, line)
        return value

    @staticmethod
    def parse_tuple(
            value: str,
            types_tuple: tuple,
            key: str,
            line: int = -1) -> tuple:
        try:
            values = value.split(',')
            if len(values) != len(types_tuple):
                raise ConfigValueError(key, value, line)
            parsed_values = []
            for i in range(len(values)):
                val = values[i].strip()
                typ = types_tuple[i]
                if typ is int:
                    parsed_values.append(int(val))
                elif typ is float:
                    parsed_values.append(float(val))
                elif typ is str:
                    parsed_values.append(val)
                elif typ is bool:
                    parsed_values.append(
                        ConfigValue.parse_bool(val, key, line)
                    )
                else:
                    raise ConfigValueError(key, value, line)
            return tuple(parsed_values)
        except ValueError:
            raise ConfigValueError(key, value, line)

    @staticmethod
    def parse_bool(value: str, key: str, line: int = -1) -> bool:
        value = value.strip().lower()
        if value == 'true' or value == '1':
            return True
        elif value == 'false' or value == '0':
            return False
        else:
            raise ConfigValueError(key, value, line)

    @staticmethod
    def parse_float(value: str, key: str, line: int = -1) -> float:
        try:
            return float(value)
        except ValueError:
            raise ConfigValueError(key, value, line)


class ConfigParser:
    def __init__(self, filename: str) -> None:
        self.raw_data: dict[str, tuple[str, int]] = {}
        self.registered_values: dict[EConfig, ConfigValue] = {}
        try:
            with open(filename, 'r') as f:
                line_number = 0
                for line in f:
                    line_number += 1
                    if (line.strip() == '' or line.strip().startswith('#')):
                        continue
                    config_line = line.replace('\n', '').split('=')

                    if (len(config_line) != 2):
                        raise ConfigFormatError(line_number=line_number)

                    [key, value] = config_line
                    self.raw_data[key.lower().strip()] = (value, line_number)

        except FileNotFoundError:
            print('Error: Config file not found!')

    def register(self, config_value: ConfigValue[T]) -> None:
        key: str = config_value.key.value
        if key in self.raw_data:
            raw_value, line_number = self.raw_data[key]
            config_value.parse(raw_value, line_number)
            self.registered_values[config_value.key] = config_value
        elif config_value.required and config_value.value is None:
            raise ConfigMissingError(key)

    def get(self, key: EConfig) -> ConfigValue:
        config_value = self.registered_values.get(key)
        if config_value is None:
            raise ConfigMissingError(str(key.value))
        return config_value


class Config:
    def __init__(self, filename: str) -> None:
        parser = ConfigParser(filename)
        self.parser = parser
        parser.register(ConfigValue[int](EConfig.WIDTH, int))
        parser.register(ConfigValue[int](EConfig.HEIGHT, int))
        parser.register(ConfigValue[tuple](EConfig.ENTRY, (int, int)))
        parser.register(ConfigValue[tuple](EConfig.EXIT, (int, int)))
        parser.register(ConfigValue[str](EConfig.OUTPUT_FILE, str))
        parser.register(ConfigValue[bool](EConfig.PERFECT, bool))
        parser.register(ConfigValue[bool](EConfig.DEBUG, bool, False, False))
        parser.register(ConfigValue[int](
            EConfig.MAZE_SEED, int, 0, False
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

    def get(self, key: EConfig) -> ConfigValue:
        config_value = self.parser.get(key)
        return config_value

    def get_int(self, key: EConfig) -> ConfigValue[int]:
        return cast(ConfigValue[int], self.parser.get(key))

    def get_str(self, key: EConfig) -> ConfigValue[str]:
        return cast(ConfigValue[str], self.parser.get(key))

    def get_coords(self, key: EConfig) -> ConfigValue[tuple]:
        return cast(ConfigValue[tuple], self.parser.get(key))

    def get_tuple(self, key: EConfig) -> ConfigValue[tuple]:
        return cast(ConfigValue[tuple], self.parser.get(key))

    def get_bool(self, key: EConfig) -> ConfigValue[bool]:
        return cast(ConfigValue[bool], self.parser.get(key))

    def get_float(self, key: EConfig) -> ConfigValue[float]:
        return cast(ConfigValue[float], self.parser.get(key))
