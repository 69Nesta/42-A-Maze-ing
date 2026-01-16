from src.errors import (
    ConfigFormatError,
    ConfigMissingError,
    ConfigValueError
    )


class ConfigParser:
    def __init__(self, filename: str) -> None:
        try:
            with open(filename, 'r') as f:
                idx = 0
                for line in f:
                    idx += 1
                    if (line.strip() == '' or line.strip().startswith('#')):
                        continue
                    config_line = line.replace('\n', '').split('=')

                    if (len(config_line) != 2):
                        raise ConfigFormatError(line_number=idx)

                    [key, value] = config_line
                    match key.strip().lower():
                        case 'width':
                            self.width = self.parse_int(value, 'WIDTH', idx)
                        case 'height':
                            self.height = self.parse_int(value, 'HEIGHT', idx)
                        case 'entry':
                            self.entry = self.parse_coords(value, 'ENTRY', idx)
                        case 'exit':
                            self.exit = self.parse_coords(value, 'EXIT', idx)
                        case 'output_file':
                            self.output_file = self.parse_string(
                                value, 'OUTPUT_FILE', idx
                            )
                        case 'perfect':
                            self.perfect = self.parse_bool(
                                value, 'PERFECT', idx
                            )

            required_attrs = [
                'width',
                'height',
                'entry',
                'exit',
                'output_file',
                'perfect'
            ]
            for attr in required_attrs:
                if not hasattr(self, attr):
                    raise ConfigMissingError(missing_key=attr.upper())

        except FileNotFoundError:
            print('Error: Config file not found!')

    @staticmethod
    def parse_int(value: str, key: str, line_number: int = None):
        try:
            return int(value)
        except ValueError:
            raise ConfigValueError(key, value, line_number)

    @staticmethod
    def parse_string(value: str, key: str, line_number: int = None):
        value = value.strip()
        if len(value) == 0:
            raise ConfigValueError(key, value, line_number)
        return value

    @staticmethod
    def parse_coords(value: str, key: str, line_number: int = None):
        try:
            coords = value.split(',')
            if len(coords) != 2:
                raise ConfigValueError(key, value, line_number)
            x = int(coords[0].strip())
            y = int(coords[1].strip())
            return (x, y)
        except ValueError:
            raise ConfigValueError(key, value, line_number)

    @staticmethod
    def parse_bool(value: str, key: str, line_number: int = None):
        value = value.strip().lower()
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            raise ConfigValueError(key, value, line_number)
