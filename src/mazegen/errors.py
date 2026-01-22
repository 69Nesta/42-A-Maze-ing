"""Custom exception types used by the maze generator.

This module defines specific exception classes raised during config
parsing and display setup. Each exception carries a helpful message and
optional attributes useful to callers and tests.
"""


class ConfigError(Exception):
    """Base class for configuration-related errors.

    Subclass this to represent any error encountered while parsing or
    validating configuration values.
    """
    pass


class DisplayError(Exception):
    """Base class for display-related errors.

    Use this as the parent for errors raised by the display/graphics
    subsystem.
    """
    pass


class ConfigFileNotFoundError(ConfigError):
    """Raised when the configured file cannot be found on disk.

    The exception message contains a short explanation and no extra
    attributes are attached.
    """

    def __init__(self) -> None:
        """Initialize the exception with a human-readable message.

        Returns:
            None
        """

        message = 'Config file not found.'
        super().__init__(message)


class ConfigFormatError(ConfigError):
    """Raised when a configuration line cannot be parsed.

    Attributes:
        at_key: Optional key name where the parsing failed.
        line_number: Line number (if available) where the error occurred.
    """

    def __init__(self, at_key: str = '', line_number: int = -1) -> None:
        """Create the error and compose a helpful message.

        Args:
            at_key: Key name that caused the formatting problem (optional).
            line_number: Line number where the error occurred (optional).

        Returns:
            None
        """

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
    """Raised when a required configuration key is not present.

    Attributes:
        missing_key: Name of the missing configuration key.
    """

    def __init__(self, missing_key: str) -> None:
        """Initialize with the missing key name and set the message.

        Args:
            missing_key: The configuration key that was not found.

        Returns:
            None
        """

        message = f'Config file is missing required key: "{missing_key}".'
        super().__init__(message)
        self.missing_key = missing_key


class ConfigValueError(ConfigError):
    """Raised when a configuration key contains an invalid value.

    Attributes:
        at_key: The configuration key name.
        invalid_value: The offending raw value as a string.
        line_number: Optional line number where the error was observed.
    """

    def __init__(self,
                 at_key: str,
                 invalid_value: str,
                 line_number: int = -1
                 ) -> None:
        """Create the error with a descriptive message and store extras.

        Args:
            at_key: The key associated with the invalid value.
            invalid_value: The raw string that failed validation.
            line_number: Line number where the value was read (optional).

        Returns:
            None
        """

        message = f'Invalid value "{invalid_value}" for key "{at_key}".'
        if line_number != -1:
            message += f' On line {line_number}.'
        super().__init__(message)
        self.at_key = at_key
        self.invalid_value = invalid_value
        self.line_number = line_number


class DisplayMazeToBig(DisplayError):
    """Raised when a maze's pixel dimensions exceed the display window.

    Attributes:
        maze_width: Width of the maze in cells/pixels as reported.
        maze_height: Height of the maze in cells/pixels as reported.
        window_width: Width of the target window in pixels.
        window_height: Height of the target window in pixels.
    """

    def __init__(self, maze_width: int, maze_height: int,
                 window_width: int, window_height: int) -> None:
        """Compose an informative message listing maze and window sizes.

        Args:
            maze_width: Maze width in pixels/cells.
            maze_height: Maze height in pixels/cells.
            window_width: Display window width in pixels.
            window_height: Display window height in pixels.

        Returns:
            None
        """

        message = (f'Maze size ({maze_width}x{maze_height}) exceeds '
                   f'window size ({window_width}x{window_height}).')
        super().__init__(message)
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.window_width = window_width
        self.window_height = window_height
