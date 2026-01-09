class ConfigError(Exception):
    """Base class for config file related errors."""
    pass


class ConfigFormatError(ConfigError):
    def __init__(self, at_key: str = '', line_number: int = None) -> None:
        message = 'Config file format error'
        if at_key:
            message += f' at key "{at_key}"'
        if line_number is not None:
            message += f' on line {line_number}'
        message += '. Expected format: <key>=<value>.'
        super().__init__(message)
        self.at_key = at_key
        self.line_number = line_number


class ConfigMissingError(ConfigError):
    def __init__(self, missing_key: str) -> None:
        message = f'Config file is missing required key: "{missing_key}".'
        super().__init__(message)
        self.missing_key = missing_key


class ConfigValueError(ConfigError):
    def __init__(self,
                 at_key: str,
                 invalid_value: str,
                 line_number: int = None
                 ) -> None:
        message = f'Invalid value "{invalid_value}" for key "{at_key}".'
        if line_number is not None:
            message += f' On line {line_number}.'
        super().__init__(message)
        self.at_key = at_key
        self.invalid_value = invalid_value
        self.line_number = line_number
