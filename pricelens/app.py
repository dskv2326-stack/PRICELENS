from flask import Flask
from flask_login import LoginManager
from sqlalchemy import inspect, text

from config import Config
from models import User, db
from routes import init_extensions, main_bp
from scheduler import init_scheduler


login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message_category = "warning"


def create_app(run_migrations=True):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    init_extensions(app)

    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()
        if run_migrations:
            _ensure_user_history_category()

    init_scheduler(app)
    return app


def _ensure_user_history_category():
    engine = db.engine
    inspector = inspect(engine)
    if 'user_history' not in inspector.get_table_names():
        return
    columns = {col['name'] for col in inspector.get_columns('user_history')}
    if 'category' in columns:
        return

    with engine.begin() as conn:
        conn.execute(text('ALTER TABLE user_history ADD COLUMN category VARCHAR(80) NULL'))

    inspector = inspect(engine)
    index_names = {idx['name'] for idx in inspector.get_indexes('user_history')}
    if 'idx_user_history_category' not in index_names:
        with engine.begin() as conn:
            conn.execute(text('CREATE INDEX idx_user_history_category ON user_history (category)'))

    if 'products' not in inspector.get_table_names():
        return
    product_cols = {col['name'] for col in inspector.get_columns('products')}
    if 'category' not in product_cols:
        return

    if engine.dialect.name == 'mysql':
        sql = (
            'UPDATE user_history uh '
            'JOIN products p ON p.id = uh.product_id '
            'SET uh.category = p.category '
            'WHERE uh.category IS NULL'
        )
    else:
        sql = (
            'UPDATE user_history '
            'SET category = (SELECT category FROM products WHERE products.id = user_history.product_id) '
            'WHERE category IS NULL'
        )

    with engine.begin() as conn:
        conn.execute(text(sql))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=True)