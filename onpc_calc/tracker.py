"""Simple timers for PC and app tracking."""

import threading
import time
from datetime import datetime


class PcTracker:
    """Simple timer to track overall PC usage."""

    def __init__(self) -> None:
        self.running = False
        self.seconds = 0
        self.thread: threading.Thread | None = None
        self.date = datetime.now().date().isoformat()

    def _run(self) -> None:
        while self.running:
            self.seconds += 1
            time.sleep(1)

    def start(self) -> None:
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self) -> int:
        if not self.running:
            return 0
        self.running = False
        if self.thread:
            self.thread.join()
        return self.seconds


class ProgramTracker:
    """Manual timer for a specific app name."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.running = False
        self.seconds = 0
        self.thread: threading.Thread | None = None
        self.date = datetime.now().date().isoformat()

    def _run(self) -> None:
        while self.running:
            self.seconds += 1
            time.sleep(1)

    def start(self) -> None:
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self) -> int:
        if not self.running:
            return 0
        self.running = False
        if self.thread:
            self.thread.join()
        return self.seconds

