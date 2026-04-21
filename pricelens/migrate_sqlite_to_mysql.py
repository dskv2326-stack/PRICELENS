import os
import sqlite3

from sqlalchemy import text

from app import create_app
from models import db


def get_sqlite_path():
    return os.getenv("SQLITE_PATH", os.path.join("instance", "pricelens.db"))


def load_rows(conn, table):
    cur = conn.execute(f"SELECT * FROM {table}")
    cols = [d[0] for d in cur.description]
    rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    return cols, rows


def insert_rows(engine, table, cols, rows):
    if not rows:
        return 0
    col_list = ", ".join(f"`{c}`" for c in cols)
    placeholders = ", ".join(f":{c}" for c in cols)
    sql = text(f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})")
    with engine.begin() as conn:
        conn.execute(sql, rows)
    return len(rows)


def main():
    sqlite_path = get_sqlite_path()
    if not os.path.exists(sqlite_path):
        raise FileNotFoundError(
            f"SQLite DB not found at '{sqlite_path}'. "
            "Set SQLITE_PATH to the correct location."
        )

    app = create_app()
    with app.app_context():
        db.create_all()
        engine = db.get_engine()

    wipe = os.getenv("WIPE_MYSQL", "0") == "1"
    table_order = ["users", "products", "prices", "user_history"]

    with sqlite3.connect(sqlite_path) as sqlite_conn:
        sqlite_conn.row_factory = sqlite3.Row

        if wipe:
            with engine.begin() as mysql_conn:
                mysql_conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
                for table in reversed(table_order):
                    mysql_conn.execute(text(f"TRUNCATE TABLE {table}"))
                mysql_conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))

        total = 0
        for table in table_order:
            cols, rows = load_rows(sqlite_conn, table)
            count = insert_rows(engine, table, cols, rows)
            print(f"{table}: {count} rows")
            total += count

        print(f"Total rows copied: {total}")


if __name__ == "__main__":
    main()
