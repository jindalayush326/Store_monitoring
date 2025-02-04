from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from store.database import db
from sqlalchemy import create_engine
from store.routes import report_bp

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], connect_args={
        'foreign_keys': 'ON',
        'journal_mode': 'WAL',
        'page_size': 4096,
        'cache_size': 1000000,
        'temp_store': 'MEMORY',
        'mmap_size': 30000000000,
        'max_page_count': 2147483646
    })
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(report_bp)

    return app
