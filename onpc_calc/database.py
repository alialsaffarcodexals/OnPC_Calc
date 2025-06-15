"""Database utilities for OnPC_Calc."""

import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple

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
            CREATE TABLE IF NOT EXISTS usage(
                date TEXT NOT NULL,
                process_name TEXT NOT NULL,
                seconds INTEGER NOT NULL,
                PRIMARY KEY(date, process_name)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS totals(
                date TEXT PRIMARY KEY,
                seconds INTEGER NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS pc_usage(
                date TEXT PRIMARY KEY,
                seconds INTEGER NOT NULL
            )
            """
        )
        self.conn.commit()

    def add_usage(self, date: str, process_name: str, seconds: int) -> None:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO usage(date, process_name, seconds) VALUES(?,?,?) "
            "ON CONFLICT(date, process_name) DO UPDATE SET seconds=seconds+excluded.seconds",
            (date, process_name, seconds),
        )
        cur.execute(
            "INSERT INTO totals(date, seconds) VALUES(?,?) "
            "ON CONFLICT(date) DO UPDATE SET seconds=seconds+excluded.seconds",
            (date, seconds),
        )
        self.conn.commit()

    def get_usage_for_date(self, date: str) -> List[Tuple[str, int]]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT process_name, seconds FROM usage WHERE date=? ORDER BY seconds DESC",
            (date,),
        )
        return cur.fetchall()

    def get_total_for_date(self, date: str) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT seconds FROM totals WHERE date=?", (date,))
        row = cur.fetchone()
        return row[0] if row else 0

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
            "SELECT date FROM totals UNION SELECT date FROM pc_usage ORDER BY date DESC"
        )
        return [row[0] for row in cur.fetchall()]
