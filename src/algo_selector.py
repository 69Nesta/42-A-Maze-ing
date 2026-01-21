from enum import Enum
from .algo import Algo


class EAlgo(Enum):
    PRIM = 1
    BACKTRACK = 2


class AlgoSelector:
    def __init__(self) -> None:
        self.algo: dict[EAlgo, Algo] = {}
        self.current_algo: EAlgo | None = None

    def register_algo(
                self,
                key: EAlgo,
                algo: Algo,
                default: bool = False
            ) -> None:
        self.algo[key] = algo
        if default:
            self.current_algo = key

    def get(self) -> Algo | None:
        return self.algo.get(self.current_algo)

    def get_algo(self, key: EAlgo) -> Algo:
        return self.algo.get(key)

    def set_current_algo(self, key: EAlgo) -> None:
        self.current_algo = key
