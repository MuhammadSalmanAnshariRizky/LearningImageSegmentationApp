from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import click
from flask.cli import with_appcontext

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(
        __name__,
        template_folder='../resources/views',
        static_folder='../resources/static'
    )

    # =========================
    # CONFIG DATABASE
    # =========================
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3307/db_segmind'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # =========================
    # IMPORT MODEL (PENTING!)
    # =========================
    from app.model.activity import Activity
    from app.model.question import Question
    from app.model.activity_question import ActivityQuestion

    # =========================
    # REGISTER BLUEPRINT
    # =========================
    from app.controller.user_controller import user_bp
    app.register_blueprint(user_bp)

    # =========================
    # REGISTER CLI COMMAND
    # =========================
    app.cli.add_command(db_fresh)

    return app


# =========================
# DB FRESH COMMAND (LIKE LARAVEL)
# =========================
@click.command("db_fresh")
@with_appcontext
def db_fresh():
    from app import db
    from app.seeder.soal import seed_question, seed_activity,seed_activity_question,seed_question_kuis,seed_kuis

    print("🔥 Dropping all tables...")
    db.drop_all()

    print("🚀 Creating all tables...")
    db.create_all()

    print("🌱 Seeding data...")
    seed_activity()
    seed_question()
    seed_question_kuis()
    seed_kuis()
    seed_activity_question()
    

    print("✅ Database fresh + seed done!")