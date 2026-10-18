"""Lazy persistence: the application can start on a read-only serverless host."""
import sqlite3
from contextlib import closing, contextmanager
from pathlib import Path

SCHEMA = """CREATE TABLE IF NOT EXISTS enquiries (
reference TEXT PRIMARY KEY, created_at TEXT NOT NULL, name TEXT NOT NULL,
phone TEXT NOT NULL, email TEXT, city TEXT NOT NULL, kind TEXT NOT NULL,
message TEXT, items TEXT)"""


class StorageUnavailable(Exception):
    pass


@contextmanager
def connect_store(config):
    url = config.get("DATABASE_URL")
    path = config.get("DATABASE")
    if url:
        import psycopg
        try:
            with psycopg.connect(url, connect_timeout=8) as db:
                db.execute(SCHEMA)
                yield db, "%s"
        except psycopg.Error as error:
            raise StorageUnavailable("Remote enquiry storage is unavailable") from error
    elif path:
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with closing(sqlite3.connect(path, timeout=10)) as db:
                with db:
                    db.execute(SCHEMA)
                    yield db, "?"
        except (sqlite3.Error, OSError) as error:
            raise StorageUnavailable("Local enquiry storage is unavailable") from error
    else:
        raise StorageUnavailable("Enquiry storage has not been configured")


def save_enquiry(config, row):
    with connect_store(config) as (db, marker):
        db.execute(f"INSERT INTO enquiries VALUES ({', '.join([marker] * 9)})", row)


def list_enquiries(config):
    with connect_store(config) as (db, _):
        cursor = db.execute("SELECT * FROM enquiries ORDER BY created_at DESC")
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
