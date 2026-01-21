from .config import Config, EConfig


class Debug:
    def __init__(self, config: Config):
        self.enabled: bool = config.get_bool(EConfig.DEBUG).get_value()

    def print(self, args: str):
        if (self.enabled):
            print(f'[DEBUG]: {args}')
