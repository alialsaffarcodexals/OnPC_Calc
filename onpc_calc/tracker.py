"""Process usage tracker."""

import threading
import time
from collections import defaultdict
from datetime import datetime
from typing import Dict

import psutil

class Tracker:
    """Track time spent in selected processes."""

    def __init__(self, paths: list[str] | None = None) -> None:
        self.running = False
        self.data: Dict[str, int] = defaultdict(int)
        self.total_seconds = 0
        self.thread: threading.Thread | None = None
        self.date = datetime.now().date().isoformat()
        self.paths = set(paths or [])

    def _run(self) -> None:
        while self.running:
            for proc in psutil.process_iter(['name', 'exe']):
                try:
                    exe = proc.info.get('exe') or ""
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                if exe not in self.paths:
                    continue
                name = proc.info.get('name') or exe or 'Unknown'
                self.data[name] += 1
            self.total_seconds += 1
            time.sleep(1)

    def start(self) -> None:
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self) -> Dict[str, int]:
        if not self.running:
            return {}
        self.running = False
        if self.thread:
            self.thread.join()
        return dict(self.data)
