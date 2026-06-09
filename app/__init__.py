from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import click
import os
from flask.cli import with_appcontext


# 🔥 BARIS IMPOR MODEL DI SINI SUDAH DIHAPUS AGAR TIDAK ERROR CIRCULAR IMPORT

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(
        __name__,
        template_folder='../resources/views',
        static_folder='../resources/static'
    )
    app.config['SECRET_KEY'] = os.urandom(24)
    # =========================
    # CONFIG DATABASE
    # =========================
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://researc4_salman:MsalmanAr13@localhost/researc4_segmentasi'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,  # Jurus ampuh: Cek nyawa database sebelum kirim query
    'pool_recycle': 280,    # Daur ulang koneksi setiap 280 detik
    'pool_timeout': 20,
    }
    db.init_app(app)
    migrate.init_app(app, db)

    # =========================
    # IMPORT MODEL (PENTING!)
    # =========================
    # Semua model diimpor di sini setelah db diinisialisasi
    from app.model.activity import Activity
    from app.model.question import Question
    from app.model.activity_question import ActivityQuestion
    from app.model.activity_result import ActivityResult
    from app.model.activity_answer import ActivityAnswer
    from app.model.settings import Setting
    from app.model.user import User
    from app.model.classes import Class
    from app.model.student_class import StudentClass
    from app.model.teacher_class import TeacherClass
    from app.model.topic import Topic
    from app.model.subtopic import SubTopic
    from app.model.progress import Progress
    from app.model.historyprogress import HistoryProgress
        
# Di dalam create_app()
    @app.context_processor
    def inject_sidebar():
        user_id = session.get('user_id')
        user_role = session.get('user_role')

        # 1. Ambil objek User dari database (untuk current_user)
        user = User.query.get(user_id) if user_id else None

        # Jika user tidak ada atau bukan student, kirim None untuk sidebar
        if not user_id or user_role != 'Student':
            return dict(
                current_user=user, # Masih tetap dikirim walaupun None/Guest
                aktif_materi=[],
                completed_materi=[]
            )

        # =========================
        # AMBIL KELAS SISWA
        # =========================
        kelas_siswa = StudentClass.query.filter_by(id_student=user_id).all()
        kelas_ids = [k.id_class for k in kelas_siswa]

        if not kelas_ids:
            return dict(
                current_user=user,
                aktif_materi=[],
                completed_materi=[]
            )

        # =========================
        # AMBIL ACTIVITY AKTIF
        # =========================
        activities = Activity.query.filter(
            Activity.id_class.in_(kelas_ids),
            Activity.status == 'aktif'
        ).all()

        aktif_materi = [(a.id_class, a.id_topic, a.id_subtopic) for a in activities]

        # =========================
        # HISTORY PROGRESS
        # =========================
        histories = HistoryProgress.query.filter_by(id_user=user_id).all()
        completed_materi = [(h.id_topic, h.id_subtopic) for h in histories]

        # Return semua variabel termasuk current_user
        return dict(
            current_user=user, # <--- INI KUNCI ERROR ANDA
            aktif_materi=aktif_materi,
            completed_materi=completed_materi
        )

    # REGISTER BLUEPRINT
    from app.controller.user_controller import user_bp
    app.register_blueprint(user_bp)

    app.cli.add_command(db_fresh)
    return app
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
    # from app.seeder.soal import seed_question, seed_activity,seed_activity_question,seed_question_kuis,seed_kuis,seed_question_evaluasi,seed_evaluasi
    from app.seeder.user import seed_user
    from app.seeder.kelas import seed_class
    from app.seeder.student_class import seed_student_class
    from app.seeder.teacher_class import seed_teacher_class
    from app.seeder.activity_result import seed_activity_result
    from app.seeder.seed_topic import seed_topic
    from app.seeder.seed_subtopic import seed_subtopic_topic1, seed_subtopic_topic2, seed_subtopic_topic3, seed_subtopic_topic4, seed_subtopic_topic5,seed_subtopic_topic6
    from app.seeder.seed_progress import seed_progress_history
    from app.seeder.soal_soal import aktivitas1,aktivitas2,kuis1,aktivitas3,aktivitas4,kuis2,aktivitas5,aktivitas6,aktivitas7,kuis3,aktivitas8,aktivitas9,aktivitas10,kuis4,aktivitas11,aktivitas12,aktivitas13,kuis5,evaluasi
    from app.seeder.setting import seed_settings
    from app.seeder.activity_answer import seed_activity_answer
    
    print("🔥 Dropping all tables...")
    db.drop_all()

    print("🚀 Creating all tables...")
    db.create_all()

    print("🌱 Seeding data...")   
    seed_user()          
    seed_class() 
        
    seed_teacher_class()  
    seed_student_class()  
    
    seed_topic()
    seed_subtopic_topic1()
    seed_subtopic_topic2()
    seed_subtopic_topic3()
    seed_subtopic_topic4()
    seed_subtopic_topic5()
    seed_subtopic_topic6()
    
    #bab 1
    aktivitas1()
    aktivitas2()
    kuis1()
    #bab 2
    aktivitas3()
    aktivitas4()
    kuis2()
    #bab 3
    aktivitas5()
    aktivitas6()
    aktivitas7()
    kuis3()
    #bab4
    aktivitas8()
    aktivitas9()
    aktivitas10()
    kuis4()
    #bab5
    aktivitas11()
    aktivitas12()   
    aktivitas13()
    kuis5()
    
    #evaluasi
    evaluasi()
    # seed_activity()
    # seed_question()
    # seed_question_kuis()
    # seed_kuis()
    # seed_question_evaluasi()
    # seed_evaluasi()
    # seed_activity_question()
    seed_activity_result() 
    seed_activity_answer()
    seed_progress_history()
    seed_settings()
    
    
    print("✅ Database fresh + seed done!")