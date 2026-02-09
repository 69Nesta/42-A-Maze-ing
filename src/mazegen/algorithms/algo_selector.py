from enum import Enum
from .algo import Algo


class EAlgo(Enum):
    """Enumeration of available maze generation algorithms.

    Members:
        PRIM: Use Prim's algorithm.
        BACKTRACK: Use backtrack algorithm.
    """
    PRIM = 1
    BACKTRACK = 2


class AlgoSelector:
    """
    Register and select a maze generation algorithm.
    """

    def __init__(self) -> None:
        """Create an AlgoSelector with no registered algorithms.

        Returns:
            None
        """
        self.algo: dict[EAlgo, Algo] = {}
        self.current_algo: EAlgo | None = None

    def register_algo(
                self,
                key: EAlgo,
                algo: Algo,
                default: bool = False
            ) -> None:
        """Register an algorithm under the provided key.

        Args:
            key (EAlgo): Enum key for the algorithm.
            algo (Algo): Algorithm instance to register.
            default (bool): If True, mark this algorithm as the default
                current algorithm.

        Returns:
            None
        """
        self.algo[key] = algo
        if default:
            self.current_algo = key

    def get(self) -> Algo | None:
        """Return the currently selected algorithm instance.

        Returns:
            Algo | None: The selected algorithm, or None if none is set.
        """
        if self.current_algo is None:
            return None
        return self.algo.get(self.current_algo)

    def get_algo(self, key: EAlgo) -> Algo | None:
        """Retrieve a registered algorithm by its key.

        Args:
            key (EAlgo): Enum key identifying the algorithm.

        Returns:
            Algo | None: The registered algorithm instance or None if
                not found.
        """
        return self.algo.get(key)

    def set_current_algo(self, key: EAlgo) -> None:
        """Set the provided algorithm as the current selection.

        Args:
            key (EAlgo): Enum key to set as current.

        Returns:
            None
        """
        self.current_algo = key
