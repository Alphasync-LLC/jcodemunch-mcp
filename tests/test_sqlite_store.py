"""Tests for the SQLite WAL storage backend."""

import sqlite3
from pathlib import Path

from jcodemunch_mcp.storage.sqlite_store import SQLiteIndexStore


def test_connect_creates_schema(tmp_path):
    """_connect creates tables and sets WAL pragmas."""
    store = SQLiteIndexStore(base_path=str(tmp_path))
    db_path = tmp_path / "test.db"
    conn = store._connect(db_path)

    # Check WAL mode
    mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
    assert mode == "wal"

    # Check tables exist
    tables = {row[0] for row in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()}
    assert tables >= {"meta", "symbols", "files"}

    conn.close()


def test_repo_slug(tmp_path):
    """_repo_slug produces a safe filesystem slug."""
    store = SQLiteIndexStore(base_path=str(tmp_path))
    slug = store._repo_slug("local", "my-project-abc123")
    assert "/" not in slug
    assert "\\" not in slug
    assert ".." not in slug


def test_db_path(tmp_path):
    """_db_path returns {base_path}/{slug}.db."""
    store = SQLiteIndexStore(base_path=str(tmp_path))
    path = store._db_path("local", "test-abc123")
    assert path.suffix == ".db"
    assert path.parent == tmp_path
