"""Database utilities for App Tracker."""

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
        # overall PC usage
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS pc_usage(
                date TEXT PRIMARY KEY,
                seconds INTEGER NOT NULL
            )
            """
        )

        # per program usage
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS program_usage(
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                seconds INTEGER NOT NULL,
                PRIMARY KEY(name, date)
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

    def add_program_usage(self, name: str, date: str, seconds: int) -> None:
        """Add seconds of usage for a program on a date."""
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO program_usage(name, date, seconds) VALUES(?,?,?) "
            "ON CONFLICT(name, date) DO UPDATE SET "
            "seconds=seconds+excluded.seconds",
            (name, date, seconds),
        )
        self.conn.commit()

    def get_pc_usage(self, date: str) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT seconds FROM pc_usage WHERE date=?", (date,))
        row = cur.fetchone()
        return row[0] if row else 0

    def get_program_usage(self, date: str) -> List[tuple[str, int]]:
        """Return list of (program name, seconds) for a date."""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT name, seconds FROM program_usage "
            "WHERE date=? ORDER BY name",
            (date,),
        )
        return cur.fetchall()

    def list_dates(self) -> List[str]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT DISTINCT date FROM ("
            " SELECT date FROM pc_usage"
            " UNION SELECT date FROM program_usage"
            ") ORDER BY date DESC"
        )
        return [row[0] for row in cur.fetchall()]
