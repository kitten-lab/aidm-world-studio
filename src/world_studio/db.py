"""SQLite connection and schema bootstrap."""

from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def connect(db_path: Path | str) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.executescript(sql)
    migrate_schema(conn)
    conn.commit()


def migrate_schema(conn: sqlite3.Connection) -> None:
    """Idempotent additive migrations for older world.db files."""
    cols = {
        row[1]
        for row in conn.execute("PRAGMA table_info(vens)").fetchall()
    }
    if cols and "parent_ven_id" not in cols:
        conn.execute(
            "ALTER TABLE vens ADD COLUMN parent_ven_id TEXT "
            "REFERENCES vens(id) ON DELETE SET NULL"
        )
    if cols:
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_vens_parent ON vens(parent_ven_id)"
        )
    # Compact VEN codes (RLM-001) — typeable handle alongside long cute slugs
    if cols and "code" not in cols:
        conn.execute("ALTER TABLE vens ADD COLUMN code TEXT")
    if cols or "code" in {
        row[1] for row in conn.execute("PRAGMA table_info(vens)").fetchall()
    }:
        from .ids import format_ven_code, kind_code_prefix, parse_ven_code

        rows = conn.execute(
            "SELECT id, kind, code FROM vens ORDER BY kind, created_at, id"
        ).fetchall()
        # Track max seq per prefix from existing codes, then fill gaps
        max_by_prefix: dict[str, int] = {}
        for r in rows:
            existing = parse_ven_code(r["code"] or "")
            if existing:
                pref, _, num = existing.partition("-")
                try:
                    max_by_prefix[pref] = max(max_by_prefix.get(pref, 0), int(num))
                except ValueError:
                    pass
        for r in rows:
            if parse_ven_code(r["code"] or ""):
                continue
            pref = kind_code_prefix(r["kind"] or "other")
            n = max_by_prefix.get(pref, 0) + 1
            max_by_prefix[pref] = n
            code = format_ven_code(pref, n)
            conn.execute("UPDATE vens SET code = ? WHERE id = ?", (code, r["id"]))
        conn.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_vens_code ON vens(code)"
        )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ven_parts (
            id              TEXT PRIMARY KEY,
            whole_ven_id    TEXT NOT NULL REFERENCES vens(id) ON DELETE CASCADE,
            part_ven_id     TEXT NOT NULL REFERENCES vens(id) ON DELETE CASCADE,
            role            TEXT NOT NULL DEFAULT 'part',
            ordinal         INTEGER NOT NULL DEFAULT 0,
            notes           TEXT NOT NULL DEFAULT '',
            created_at      TEXT NOT NULL DEFAULT (datetime('now')),
            UNIQUE (whole_ven_id, part_ven_id, role)
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_ven_parts_whole ON ven_parts(whole_ven_id)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_ven_parts_part ON ven_parts(part_ven_id)"
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS text_revisions (
            id              TEXT PRIMARY KEY,
            subject_type    TEXT NOT NULL,
            subject_id      TEXT NOT NULL,
            field           TEXT NOT NULL DEFAULT 'body',
            title           TEXT NOT NULL DEFAULT '',
            body            TEXT NOT NULL DEFAULT '',
            format          TEXT NOT NULL DEFAULT 'plain',
            author          TEXT NOT NULL DEFAULT 'builder',
            note            TEXT NOT NULL DEFAULT '',
            created_at      TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_text_rev_subject "
        "ON text_revisions(subject_type, subject_id, created_at)"
    )

    # Dialogs: cute typeable slug (FIRST-MEETING) alongside opaque dlg_ id
    dlg_info = conn.execute("PRAGMA table_info(dialogs)").fetchall()
    if dlg_info:
        dlg_cols = {row[1] for row in dlg_info}
        if "slug" not in dlg_cols:
            conn.execute("ALTER TABLE dialogs ADD COLUMN slug TEXT")
        from .ids import cute_name

        rows = conn.execute(
            "SELECT id, title, slug FROM dialogs ORDER BY created_at, id"
        ).fetchall()
        used: set[str] = set()
        for r in rows:
            existing = (r["slug"] or "").strip()
            if existing:
                used.add(existing.casefold())
                continue
            base = cute_name(r["title"] or "") or "DIALOG"
            if base in ("UNNAMED", ""):
                base = "DIALOG"
            candidate = base
            n = 2
            while candidate.casefold() in used:
                candidate = f"{base}-{n}"
                n += 1
            used.add(candidate.casefold())
            conn.execute(
                "UPDATE dialogs SET slug = ? WHERE id = ?",
                (candidate, r["id"]),
            )
        conn.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_dialogs_slug ON dialogs(slug)"
        )


def get_meta(conn: sqlite3.Connection, key: str, default: str | None = None) -> str | None:
    row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    if row is None:
        return default
    return row["value"]


def set_meta(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute(
        "INSERT INTO meta(key, value) VALUES(?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (key, value),
    )
    conn.commit()
