import sqlite3
import json
from pathlib import Path
from core.base_module import module_result

DB_PATH = Path(__file__).parent.parent / "output" / "recon.db"

class Storage:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    module    TEXT NOT NULL,
                    target    TEXT NOT NULL,
                    success   INTEGER NOT NULL,
                    data      TEXT NOT NULL,
                    error     TEXT,
                    timestamp TEXT NOT NULL
                )
            """)

    def save(self, result: module_result):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO results (module, target, success, data, error, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                result.module_name,
                result.target,
                int(result.success),
                json.dumps(result.result_data),
                result.error,
                result.timestamp,
            ))

    def get(self, target: str = None, module: str = None) -> list[dict]:
        query = "SELECT * FROM results WHERE 1=1"
        params = []
        if target:
            query += " AND target = ?"
            params.append(target)
        if module:
            query += " AND module = ?"
            params.append(module)
        query += " ORDER BY timestamp DESC"

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(query, params).fetchall()

        results = []
        for row in rows:
            r = dict(row)
            r["data"] = json.loads(r["data"])
            r["success"] = bool(r["success"])
            results.append(r)
        return results

    def clear(self, target: str = None):
        with sqlite3.connect(self.db_path) as conn:
            if target:
                conn.execute("DELETE FROM results WHERE target = ?", (target,))
            else:
                conn.execute("DELETE FROM results")
