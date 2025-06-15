"""Process usage tracker."""

import os
import threading
import time
from datetime import datetime

import psutil


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
    """Track usage of a program by its name."""

    def __init__(self, name: str) -> None:
        self.name = os.path.basename(name)
        self.running = False
        self.seconds = 0
        self.thread: threading.Thread | None = None
        self.date = datetime.now().date().isoformat()

    def _is_running(self) -> bool:
        """Return True if a process with matching name is running."""
        for proc in psutil.process_iter(["name"]):
            try:
                if proc.info.get("name") and proc.info["name"].lower() == self.name.lower():
                    return True
            except (psutil.Error, OSError):
                continue
        return False

    def _run(self) -> None:
        while self.running:
            if self._is_running():
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

