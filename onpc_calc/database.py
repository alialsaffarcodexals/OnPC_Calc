"""Database utilities for OnPC_Calc."""

import sqlite3
from pathlib import Path
from typing import List

DB_FILE = Path.home() / ".onpc_calc.db"

class Database:
    """Simple SQLite wrapper to store usage data."""

    def __init__(self, path: Path = DB_FILE) -> None:
        self.path = path
        self.conn = sqlite3.connect(self.path)
        self._create_tables()

    def _create_tables(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS pc_usage(
                date TEXT PRIMARY KEY,
                seconds INTEGER NOT NULL
            )
            """
        )
        self.conn.commit()

    def add_pc_usage(self, date: str, seconds: int) -> None:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO pc_usage(date, seconds) VALUES(?,?) "
            "ON CONFLICT(date) DO UPDATE SET seconds=seconds+excluded.seconds",
            (date, seconds),
        )
        self.conn.commit()

    def get_pc_usage(self, date: str) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT seconds FROM pc_usage WHERE date=?", (date,))
        row = cur.fetchone()
        return row[0] if row else 0

    def list_dates(self) -> List[str]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT date FROM pc_usage ORDER BY date DESC"
        )
        return [row[0] for row in cur.fetchall()]
