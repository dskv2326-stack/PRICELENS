from apscheduler.schedulers.background import BackgroundScheduler

from models import db


scheduler = BackgroundScheduler(timezone="Asia/Kolkata")


def refresh_prices_job():
    # Prices are managed directly in the database tables.
    return


def init_scheduler(app):
    if scheduler.running:
        return

    def run_with_context():
        with app.app_context():
            refresh_prices_job()

    scheduler.add_job(
        func=run_with_context,
        trigger="cron",
        hour=0,
        minute=0,
        id="daily_price_refresh",
        replace_existing=True,
    )
    scheduler.start()
