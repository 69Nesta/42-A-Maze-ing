from .config import Config, EConfig


class Debug:
    def __init__(self, config: Config) -> None:
        self.enabled: bool = config.get_bool(EConfig.DEBUG).get_value()

    def print(self, args: str) -> None:
        if (self.enabled):
            print(f'[DEBUG]: {args}')
