class AnimationState:
    def __init__(self, speed: float, max_step: int) -> None:
        self.finished: bool = False
        self.started: bool = False
        self.started_at: float = 0.0
        self.speed: float = speed
        self.last_update_time: float = 0.0
        self.max_step: int = max_step
        self.index: int = 0

    def start(self, current_time) -> None:
        self.started = True
        self.finished = False
        self.last_update_time = current_time
        self.started_at = self.last_update_time

    def stop(self) -> None:
        self.started = False
        self.finished = True
        self.last_update_time = 0.0
        self.started_at = self.last_update_time

    def update(self, current_time) -> bool:
        if not self.started or self.finished:
            return False
        elapsed_time = current_time - self.started_at
        if elapsed_time >= (self.speed / 1000) * (self.index + 1):
            self.last_update_time = current_time
            return True
        return False

    def reset(self) -> None:
        self.finished = False
        self.started = False
        self.started_at = 0.0
        self.last_update_time = 0.0
        self.index = 0

    def get_next_step(self) -> int | None:
        index = self.index
        self.index += 1
        if index >= self.max_step:
            self.finished = True
            return None
        return index
