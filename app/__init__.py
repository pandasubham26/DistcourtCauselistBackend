import os
from flask import Flask
from flask_cors import CORS
from sqlalchemy import MetaData

from app.api.auth_api import authentication_bp
from app.api.casefile.casefile_upload_api import bulkupload_casefile_bp
from app.api.causelist.causelist_api import causelist_bp
from app.api.master.dop_master_api import dop_master_bp
from app.api.master.master_api import master_bp
from app.api.search.global_search_api import search_bp
from app.cli import create_superadmin
from app.config import config
from app.errors import register_error_handlers
from app.extensions import db, jwt, ma, migrate, bcrypt
from app.logger import setup_logging
from app.utils import success_response


def _create_main_db_tables(app, allowed_tables=None):
    """
        Create only the tables explicitly allowed by configuration.
        If allowed_tables is empty or None → do nothing.
    """

    if not allowed_tables:
        app.logger.info("Table creation skipped (no allowed tables provided)")
        return

    with app.app_context():
        engine = db.get_engine()

        metadata = MetaData()
        tables_to_create = []

        for table in db.metadata.sorted_tables:
            if table.name in allowed_tables:
                table.tometadata(metadata)
                tables_to_create.append(table.name)

        if tables_to_create:
            metadata.create_all(bind=engine)
            app.logger.info(f"Created allowed tables: {tables_to_create}")
        else:
            app.logger.info("No matching tables found to create")


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    # CORS for Angular frontend
    CORS(app,
         resources={r"/api/*": {"origins": ["http://localhost:4200"]}},
         supports_credentials=True,
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"]
         )

    # setup logging early
    setup_logging(app)

    # initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    app.cli.add_command(create_superadmin)

    # ___________________________________
    # Register Blueprint
    #____________________________________
    app.register_blueprint(authentication_bp, url_prefix='/api/auth')
    app.register_blueprint(master_bp, url_prefix='/api/<estcode>/master')
    app.register_blueprint(bulkupload_casefile_bp, url_prefix='/api/<estcode>/casefile')
    app.register_blueprint(dop_master_bp, url_prefix='/api/<estcode>/cis')
    app.register_blueprint(causelist_bp, url_prefix='/api/<estcode>/causelist')
    app.register_blueprint(search_bp, url_prefix='/api/<estcode>/global/search')

    register_error_handlers(app)

    # ----------------------------------------
    # FIX: Run table creation ONLY in main process
    # ----------------------------------------
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        with app.app_context():
            try:
                _create_main_db_tables(app, allowed_tables=["users", "casefile_header", "casefile_detail", "causelist"])
            except Exception:
                app.logger.exception('Failed to auto-create main DB tables')

    @app.route('/')
    def index():
        return success_response(message='Flask + Postgres API is up')

    return app
