from typing import Generic, TypeVar, Type, cast
from src.errors import (
    ConfigFormatError,
    ConfigMissingError,
    ConfigValueError
    )

t_coords = tuple[int, int]

T = TypeVar('T', int, str, t_coords, bool)


class ConfigValue(Generic[T]):
    def __init__(self, key: str, value_type: Type[T], required: bool = True) -> None:
        self.key: str = key
        self.value_type: Type[T] = value_type
        self.required: bool = required
        self.value: T | None = None

    def parse(self, raw_value: str, line: int) -> None:
        if self.value_type is int:
            self.value = cast(T, self.parse_int(raw_value, self.key, line))
        elif self.value_type is str:
            self.value = cast(T, self.parse_string(raw_value, self.key, line))
        elif self.value_type is t_coords:
            self.value = cast(T, self.parse_coords(raw_value, self.key, line))
        elif self.value_type is bool:
            self.value = cast(T, self.parse_bool(raw_value, self.key, line))
        else:
            raise ConfigValueError(self.key, raw_value, line)

    def get_value(self) -> T:
        if self.value is None:
            raise ValueError(f'Value for key "{self.key}" has not been parsed yet.')
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


class ConfigParser:
    def __init__(self, filename: str) -> None:
        self.raw_data: dict[str, tuple[str, int]] = {}
        # self.registered_values = []
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
                    self.raw_data[key] = (value, line_number)

                    # match key.strip().lower():
                    #     case 'width':
                    #         self.width = self.parse_int(value, 'WIDTH', idx)
                    #     case 'height':
                    #         self.height = self.parse_int(value, 'HEIGHT', idx)
                    #     case 'entry':
                    #         self.entry = self.parse_coords(value, 'ENTRY', idx)
                    #     case 'exit':
                    #         self.exit = self.parse_coords(value, 'EXIT', idx)
                    #     case 'output_file':
                    #         self.output_file = self.parse_string(
                    #             value, 'OUTPUT_FILE', idx
                    #         )
                    #     case 'perfect':
                    #         self.perfect = self.parse_bool(
                    #             value, 'PERFECT', idx
                    #         )

            # required_attrs = [
            #     'width',
            #     'height',
            #     'entry',
            #     'exit',
            #     'output_file',
            #     'perfect'
            # ]
            # for attr in required_attrs:
            #     if not hasattr(self, attr):
            #         raise ConfigMissingError(missing_key=attr.upper())

        except FileNotFoundError:
            print('Error: Config file not found!')

    def register(self, config_value: ConfigValue[T]) -> None:
        if config_value.key in self.raw_data:
            raw_value, line_number = self.raw_data[config_value.key]
            config_value.parse(raw_value, line_number)
        elif config_value.required:
            raise ConfigMissingError(missing_key=config_value.key)


class Config:
    def __init__(self, filename: str) -> None:
        self.parser = ConfigParser(filename)
        self.parser.register(ConfigValue[int]('width', int))
