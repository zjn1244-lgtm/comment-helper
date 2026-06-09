import sqlite3
from pathlib import Path


DB_PATH = Path("data/app.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_comments_table():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment_id TEXT,
                username TEXT,
                content TEXT,
                likes INTEGER DEFAULT 0,
                replies INTEGER DEFAULT 0,
                created_at TEXT,
                system_tag TEXT,
                note TEXT,
                is_saved INTEGER DEFAULT 0,
                is_processed INTEGER DEFAULT 0,
                imported_at TEXT
            )
            """
        )


def insert_comments(comments):
    if not comments:
        return 0

    init_comments_table()

    with get_connection() as conn:
        for comment in comments:
            cursor = conn.execute(
                """
                INSERT INTO comments (
                    comment_id,
                    username,
                    content,
                    likes,
                    replies,
                    created_at,
                    system_tag,
                    note,
                    is_saved,
                    is_processed,
                    imported_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    comment.get("comment_id"),
                    comment.get("username"),
                    comment.get("content"),
                    comment.get("likes", 0),
                    comment.get("replies", 0),
                    comment.get("created_at"),
                    comment.get("system_tag"),
                    comment.get("note"),
                    comment.get("is_saved", 0),
                    comment.get("is_processed", 0),
                    comment.get("imported_at"),
                ),
            )
            comment["id"] = cursor.lastrowid

    return len(comments)


def get_comment_count():
    init_comments_table()

    with get_connection() as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM comments")
        return cursor.fetchone()[0]


def get_comments():
    init_comments_table()

    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            """
            SELECT
                id,
                comment_id,
                username,
                content,
                likes,
                replies,
                created_at,
                system_tag,
                note,
                is_saved,
                is_processed,
                imported_at
            FROM comments
            ORDER BY id ASC
            """
        )
        return [dict(row) for row in cursor.fetchall()]


def clear_comments():
    init_comments_table()

    with get_connection() as conn:
        conn.execute("DELETE FROM comments")


def update_comment_processed(comment_id, is_processed):
    init_comments_table()

    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE comments SET is_processed = ? WHERE id = ?",
            (1 if is_processed else 0, comment_id),
        )
        return cursor.rowcount > 0
