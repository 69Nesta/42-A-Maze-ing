from enum import Enum
from typing import Generic, TypeVar, Type, cast
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


class ConfigValue(Generic[T]):
    def __init__(
                self,
                key: EConfig,
                value_type: Type[T],
                required: bool = True
            ) -> None:
        self.key: EConfig = key
        self.value_type: Type[T] = value_type
        self.required: bool = required
        self.value: T | None = None

    def parse(self, raw_value: str, line: int) -> None:
        key = str(self.key.value)
        if self.value_type is int:
            self.value = cast(T, self.parse_int(raw_value, key, line))
        elif self.value_type is str:
            self.value = cast(T, self.parse_string(raw_value, key, line))
        elif self.value_type is tuple:
            self.value = cast(T, self.parse_coords(raw_value, key, line))
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
    def parse_coords(value: str, key: str, line: int = -1) -> tuple[int, int]:
        try:
            coords = value.split(',')
            if len(coords) != 2:
                raise ConfigValueError(key, value, line)
            x = int(coords[0].strip())
            y = int(coords[1].strip())
            return (x, y)
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
                    self.raw_data[key.lower()] = (value, line_number)

        except FileNotFoundError:
            print('Error: Config file not found!')

    def register(self, config_value: ConfigValue[T]) -> None:
        key: str = config_value.key.value
        if key in self.raw_data:
            raw_value, line_number = self.raw_data[key]
            config_value.parse(raw_value, line_number)
            self.registered_values[config_value.key] = config_value
        elif config_value.required:
            raise ConfigMissingError(key)

    def get(self, key: EConfig) -> ConfigValue:
        config_value = self.registered_values.get(key)
        if config_value is None:
            raise ConfigMissingError(str(key.value))
        return config_value


class Config:
    def __init__(self, filename: str) -> None:
        self.parser = ConfigParser(filename)
        self.parser.register(ConfigValue[int](EConfig.WIDTH, int))
        self.parser.register(ConfigValue[int](EConfig.HEIGHT, int))
        self.parser.register(ConfigValue[t_coords](EConfig.ENTRY, tuple))
        self.parser.register(ConfigValue[t_coords](EConfig.EXIT, tuple))
        self.parser.register(ConfigValue[str](EConfig.OUTPUT_FILE, str))
        self.parser.register(ConfigValue[bool](EConfig.PERFECT, bool))

    def get(self, key: EConfig) -> ConfigValue:
        config_value = self.parser.get(key)
        if config_value is None:
            raise ConfigMissingError(str(key.value))
        return config_value
