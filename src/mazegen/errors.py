class ConfigError(Exception):
    """Base class for config file related errors."""
    pass


class DisplayError(Exception):
    """Base class for display related errors."""
    pass


class ConfigFileNotFoundError(ConfigError):
    '''Indicates that the config file was not found.'''
    def __init__(self) -> None:
        '''Indicates that the config file was not found.'''
        message = 'Config file not found.'
        super().__init__(message)


class ConfigFormatError(ConfigError):
    '''Indicates a formatting error in the config file.'''
    def __init__(self, at_key: str = '', line_number: int = -1) -> None:
        '''Indicates a formatting error in the config file.'''
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
    '''Indicates a missing required key in the config file.'''
    def __init__(self, missing_key: str) -> None:
        '''Indicates a missing required key in the config file.'''
        message = f'Config file is missing required key: "{missing_key}".'
        super().__init__(message)
        self.missing_key = missing_key


class ConfigValueError(ConfigError):
    '''Indicates an invalid value for a given key in the config file.'''
    def __init__(self,
                 at_key: str,
                 invalid_value: str,
                 line_number: int = -1
                 ) -> None:
        '''Indicates an invalid value for a given key in the config file.'''
        message = f'Invalid value "{invalid_value}" for key "{at_key}".'
        if line_number != -1:
            message += f' On line {line_number}.'
        super().__init__(message)
        self.at_key = at_key
        self.invalid_value = invalid_value
        self.line_number = line_number


class DisplayMazeToBig(DisplayError):
    '''Indicates that the maze is too big to be displayed in the window.'''
    def __init__(self, maze_width: int, maze_height: int,
                 window_width: int, window_height: int) -> None:
        '''Indicates that the maze is too big to be displayed in the window.'''
        message = (f'Maze size ({maze_width}x{maze_height}) exceeds '
                   f'window size ({window_width}x{window_height}).')
        super().__init__(message)
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.window_width = window_width
        self.window_height = window_height
