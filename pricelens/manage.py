import argparse

from app import create_app, _ensure_user_history_category


def main():
    parser = argparse.ArgumentParser(description="PriceLens management commands")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "migrate-user-history-category",
        help="Add user_history.category if missing and backfill when possible",
    )

    args = parser.parse_args()
    if args.command == "migrate-user-history-category":
        app = create_app(run_migrations=False)
        with app.app_context():
            _ensure_user_history_category()
        print("Migration complete: user_history.category ensured.")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
