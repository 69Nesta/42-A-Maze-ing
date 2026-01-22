"""Animation helper used to drive time-based rendering steps.

This module contains :class:`AnimationState`, a small helper that tracks
whether an animation is started/finished, advances a step index over time
and provides timing logic to decide when to progress the animation.

The timing unit for `speed` is milliseconds and the :meth:`update` method
expects a POSIX-style timestamp (as returned by :func:`time.time`).
"""


class AnimationState:
    """Track and advance a discrete animation over time.

    The instance keeps an integer index which advances from 0 up to
    ``max_step - 1``. Use :meth:`start` to begin the animation, call
    :meth:`update` frequently with the current time to check if the next
    step should be applied, and use :meth:`get_next_step` to consume the
    next index when moving the animation forward.

    Attributes:
        finished (bool): True when the animation has completed all steps.
        started (bool): True when the animation is running.
        started_at (float): Timestamp when the animation started.
        speed (float): Per-step duration in milliseconds.
        last_update_time (float): Timestamp of last update callback.
        max_step (int): Number of discrete steps in the animation.
        index (int): Next index to be returned by :meth:`get_next_step`.
    """

    def __init__(self, speed: float, max_step: int) -> None:
        """Initialize an AnimationState.

        Args:
            speed (float): Duration of each step in milliseconds.
            max_step (int): Total number of steps for the animation.
        """

        self.finished: bool = False
        self.started: bool = False
        self.started_at: float = 0.0
        self.speed: float = speed
        self.last_update_time: float = 0.0
        self.max_step: int = max_step
        self.index: int = 0

    def start(self, current_time: float) -> None:
        """Begin the animation at the provided timestamp.

        Args:
            current_time (float): Current time (e.g. from :func:`time.time`).
        """

        self.started = True
        self.finished = False
        self.last_update_time = current_time
        self.started_at = self.last_update_time

    def stop(self) -> None:
        """Stop the animation and mark it as finished."""

        self.started = False
        self.finished = True
        self.last_update_time = 0.0
        self.started_at = self.last_update_time

    def update(self, current_time: float) -> bool:
        """Check whether the animation should advance a step.

        This method performs a timing check against the configured per-step
        duration. It does not change the step index; it only returns ``True``
        when the consumer should request the next step via
        :meth:`get_next_step`.

        Args:
            current_time (float): Current time (e.g. from :func:`time.time`).

        Returns:
            bool: ``True`` if the next step should be processed, otherwise
            ``False``.
        """

        if not self.started or self.finished:
            return False
        elapsed_time = current_time - self.started_at
        if elapsed_time >= (self.speed / 1000) * (self.index + 1):
            self.last_update_time = current_time
            return True
        return False

    def reset(self) -> None:
        """Reset the animation to the initial state without starting it."""

        self.finished = False
        self.started = False
        self.started_at = 0.0
        self.last_update_time = 0.0
        self.index = 0

    def get_next_step(self) -> int | None:
        """Return the next step index and advance the internal counter.

        If the returned index would exceed :attr:`max_step`, the animation is
        marked finished and ``None`` is returned.

        Returns:
            int | None: The next step index, or ``None`` if the animation is
            complete.
        """

        index = self.index
        self.index += 1
        if index >= self.max_step:
            self.finished = True
            return None
        return index
