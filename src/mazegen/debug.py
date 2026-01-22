"""Small helper for conditional debug printing.

The Debug class wraps a configuration flag and exposes a `print`
method that only emits output when debugging is enabled.
"""

from .config import Config, EConfig


class Debug:
    """Conditional debug printer driven by configuration.

    Args:
        config: Config instance used to read the debug flag.
    """

    def __init__(self, config: Config) -> None:
        """Initialize the helper and read the debug flag from config.

        Returns:
            None
        """

        self.enabled: bool = config.get_bool(EConfig.DEBUG).get_value()

    def print(self, args: str) -> None:
        """Print a debug message if debugging is enabled.

        Args:
            args: The string to print (will be prefixed with a [DEBUG] tag).

        Returns:
            None
        """

        if (self.enabled):
            print(f'[DEBUG]: {args}')
