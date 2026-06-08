import cv2
from flask import Blueprint, abort, current_app, render_template, jsonify,flash, session
from flask import request, redirect, url_for
from datetime import datetime
from app import db
from app.model.activity_answer import ActivityAnswer
from app.model.activity_result import ActivityResult
from app.model.question import Question
from app.model.activity_question import ActivityQuestion
from app.model.activity import Activity
from app.model.user import User
from app.model.classes import Class
from app.model.student_class import StudentClass
from app.model.teacher_class import TeacherClass
from app.model.topic import Topic
from app.model.subtopic import SubTopic
from app.model.progress import Progress
from app.model.historyprogress import HistoryProgress
from app.model.settings import Setting
from werkzeug.security import check_password_hash, generate_password_hash
import json
import random
from datetime import datetime
import pandas as pd
from flask import send_file
import io
import pandas as pd
import re
from io import BytesIO
from sqlalchemy.orm import joinedload
from app.decorator.auth import student_required, teacher_required
import subprocess
import tempfile
import os
import glob
import uuid
from flask import send_from_directory
from sqlalchemy import func

from app.seeder.klaimpaket import generate_learning_package

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def index():
    return render_template('index.html')

@user_bp.route('/perihal')
def perihal():
    return render_template('perihal.html')
# =========================
# ROUTE SUBTOPIC
# =========================
SUBTOPIC_ROUTE = {

    # TOPIC 1
    1: "/materi1/pengantarcitradigital",
    2: "/materi1/jeniscitra",
    3: "/materi1/rangkuman",
    4: "/materi1/kuis",

    # TOPIC 2
    5: "/materi2/pengantarsegmentasi",
    6: "/materi2/metodesegmentasi",
    7: "/materi2/rangkuman",
    8: "/materi2/kuis",

    # TOPIC 3
    9: "/materi3/pengantaredgebased",
    10: "/materi3/tahapanedgebased",
    11: "/materi3/praktekedgebased",
    12: "/materi3/rangkuman",
    13: "/materi3/kuis",

    # TOPIC 4
    14: "/materi4/pengantarthresholdbased",
    15: "/materi4/histogram",
    16: "/materi4/metodethresholding",
    17: "/materi4/rangkuman",
    18: "/materi4/kuis",

    # TOPIC 5
    19: "/materi5/pengantarregionbased",
    20: "/materi5/regiongrowing",
    21: "/materi5/splitandmerge",
    22: "/materi5/rangkuman",
    23: "/materi5/kuis",

    # EVALUASI
    24: "/evaluasi"
}


@user_bp.route('/dashboard')
@student_required
def dashboard():

    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # =========================
    # KELAS SISWA
    # =========================
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return render_template(
            'dashboard.html',
            kelas=None,
            total_materi=0,
            selesai=0,
            progress_percent=0,
            materi_list=[],
            hasil_belajar=[]
        )

    kelas = Class.query.get(student_class.id_class)

    # =========================
    # AMBIL SEMUA TOPIC
    # =========================
    topics = (
        Topic.query
        .order_by(Topic.id.asc())
        .all()
    )

    # =========================
    # TOTAL SUBTOPIC
    # =========================
    total_subtopic = SubTopic.query.count()

    # =========================
    # HISTORY SISWA
    # =========================
    histories = (
        HistoryProgress.query
        .filter_by(id_user=user_id)
        .all()
    )

    completed_subtopic_ids = [
        h.id_subtopic
        for h in histories
        if h.id_subtopic is not None
    ]

    # =========================
    # TOTAL SELESAI
    # =========================
    selesai = len(completed_subtopic_ids)

    # =========================
    # PROGRESS %
    # =========================
    progress_percent = 0

    if total_subtopic > 0:
        progress_percent = round(
            (selesai / total_subtopic) * 100
        )

    # =========================
    # LIST DASHBOARD
    # =========================
    materi_list = []

    next_unlock = True

    for topic in topics:

        # =========================
        # SUBTOPIC PER TOPIC
        # =========================
        subtopics = (
            SubTopic.query
            .filter_by(id_topic=topic.id)
            .order_by(SubTopic.id.asc())
            .all()
        )

        total_sub = len(subtopics)

        subtopic_ids = [
            s.id for s in subtopics
        ]

        # =========================
        # HITUNG YANG SELESAI
        # =========================
        selesai_sub = sum(
            1 for sid in subtopic_ids
            if sid in completed_subtopic_ids
        )

        # =========================
        # PERSEN TOPIC
        # =========================
        persen = 0

        if total_sub > 0:
            persen = round(
                (selesai_sub / total_sub) * 100
            )

        # =========================
        # SUBTOPIC BERIKUTNYA
        # =========================
        next_subtopic_id = None

        for sid in subtopic_ids:

            if sid not in completed_subtopic_ids:
                next_subtopic_id = sid
                break

        # kalau topic selesai
        if next_subtopic_id is None and subtopic_ids:
            next_subtopic_id = subtopic_ids[0]

        # =========================
        # HREF
        # =========================
        href = SUBTOPIC_ROUTE.get(
            next_subtopic_id,
            "#"
        )

        # =========================
        # DEFAULT STATUS
        # =========================
        status = "locked"

        button_text = "Terkunci"
        button_class = "btn-secondary"

        badge_class = "bg-secondary bg-opacity-10 text-secondary"

        card_class = "locked locked-card"

        # =========================
        # TOPIC SELESAI
        # =========================
        if persen == 100:

            status = "done"

            button_text = "Pelajari Lagi"
            button_class = "btn-outline-success"

            badge_class = "bg-success bg-opacity-10 text-success"

            card_class = "success"

            next_unlock = True

        # =========================
        # TOPIC YANG AKTIF
        # =========================
        elif next_unlock:

            status = "current"

            button_text = "Lanjutkan"
            button_class = "btn-primary"

            badge_class = "bg-primary bg-opacity-10 text-primary"

            card_class = "primary"

            next_unlock = False

        # =========================
        # SIMPAN KE LIST
        # =========================
        materi_list.append({

            "id": topic.id,
            "title": topic.topic_name,

            "status": status,
            "progress": persen,

            "selesai_sub": selesai_sub,
            "total_sub": total_sub,

            "button_text": button_text,
            "button_class": button_class,

            "badge_class": badge_class,
            "card_class": card_class,

            "href": href
        })

    # =========================
    # HASIL BELAJAR SISWA
    # =========================
    hasil_belajar = []

    # AMBIL SEMUA ACTIVITY
    activities = (

        Activity.query

        .filter(
            Activity.type.in_(["kuis", "evaluasi"])
        )

        .order_by(Activity.id.asc())

        .all()
    )

    # LOOP ACTIVITY
    for activity in activities:

        # =========================
        # AMBIL RESULT TERBARU
        # =========================
        latest_result = (

            ActivityResult.query

            .filter_by(
                id_user=user_id,
                id_activity=activity.id
            )

            .order_by(
                ActivityResult.id.desc()
            )

            .first()
        )

        # JIKA ADA RESULT
        if latest_result:

            hasil_belajar.append({

                "title": activity.title,

                "nilai": latest_result.nilai_akhir,

                "status": latest_result.result_status,

                "benar": latest_result.total_benar,

                "salah": latest_result.total_salah
            })

    return render_template(
        'dashboard.html',
        kelas=kelas,
        total_materi=len(topics),
        selesai=selesai,
        progress_percent=progress_percent,
        materi_list=materi_list,
        hasil_belajar=hasil_belajar
    )

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    # 1. Ambil data 'old' dari session jika ada (hasil titipan dari redirect sebelumnya)
    old = session.pop('old_form', {})

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        id_other = request.form.get('id_other')
        type_id_other = request.form.get('type_id_other')
        class_code = request.form.get('class_code')

        # 2. Siapkan data yang akan "dititipkan" jika terjadi error
        old_data = request.form.to_dict()
        old_data.pop('password', None) # KEAMANAN: Jangan pernah simpan password yang diketik user!

        # VALIDASI 1: Cek apakah ada field yang kosong
        if not all([name, email, password, role, id_other, type_id_other]):
            session['old_form'] = old_data # Titipkan data
            return redirect(url_for(
                'user.register',
                status='error',
                message='Semua field wajib diisi!'
            ))

        # VALIDASI 2: Password minimal 8 karakter
        if len(password) < 8:
            session['old_form'] = old_data 
            return redirect(url_for(
                'user.register',
                status='error',
                message='Password terlalu pendek! Minimal 8 karakter.'
            ))

        # VALIDASI 3: Cek apakah Email sudah terdaftar
        if User.query.filter_by(email=email).first():
            session['old_form'] = old_data 
            return redirect(url_for(
                'user.register',
                status='error',
                message='Email sudah terdaftar! Gunakan email lain.'
            ))

        # VALIDASI 4: Cek apakah Nomor ID (NIM/NIDN) sudah terdaftar
        if User.query.filter_by(id_other=id_other).first():
            session['old_form'] = old_data 
            return redirect(url_for(
                'user.register',
                status='error',
                message=f'Nomor ID ({id_other}) sudah terdaftar di sistem!'
            ))

        try:
            # 🔐 HASH PASSWORD
            hashed_password = generate_password_hash(password)

            # 💾 BUAT USER (BELUM COMMIT)
            user = User(
                name=name,
                email=email,
                password=hashed_password,
                role=role,
                id_other=id_other,
                type_id_other=type_id_other
            )

            db.session.add(user)
            db.session.flush()  # ambil user.id tanpa commit

            # =============================
            # 🔗 VALIDASI & HUBUNGKAN KELAS
            # =============================
            if class_code:
                kelas = Class.query.filter_by(token=class_code).first()

                if not kelas:
                    db.session.rollback()
                    session['old_form'] = old_data 
                    return redirect(url_for(
                        'user.register',
                        status='error',
                        message='Kode kelas tidak valid atau tidak ditemukan!'
                    ))

                if role == 'Student':
                    rel = StudentClass(
                        id_student=user.id,
                        id_class=kelas.id
                    )
                    db.session.add(rel)

                elif role == 'Teacher':
                    rel = TeacherClass(
                        id_teacher=user.id,
                        id_class=kelas.id
                    )
                    db.session.add(rel)

            # COMMIT SEKALI SAJA
            db.session.commit()

            # SUKSES: Arahkan ke halaman login membawa trigger SweetAlert
            return redirect(url_for(
                'user.login',
                status='success',
                message='Akun berhasil dibuat! Silakan login.'
            ))

        except Exception as e:
            db.session.rollback()
            print(e) # Untuk debugging di terminal
            session['old_form'] = old_data 
            return redirect(url_for(
                'user.register',
                status='error',
                message='Terjadi kesalahan sistem saat registrasi!'
            ))

    # Untuk request GET (Saat user pertama kali buka halaman)
    # Tidak akan ada pesan error yang muncul karena kode post dan validasi dilewati
    return render_template('register.html', old=old)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():

    old = session.pop('old_login_form', {})

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        session['old_login_form'] = {
            'email': email
        }

        # VALIDASI INPUT
        if not email or not password:
            return redirect(
                url_for(
                    'user.login',
                    status='error',
                    message='Email dan Password wajib diisi!'
                )
            )

        # CARI USER
        user = User.query.filter_by(email=email).first()

        # VALIDASI LOGIN
        if user and check_password_hash(user.password, password):

            # SESSION DASAR
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role

            # HAPUS OLD FORM
            session.pop('old_login_form', None)

            # =========================
            # ARAHKAN BERDASARKAN ROLE
            # =========================
            if user.role == 'Student':
                
                # Ambil kelas siswa jika rolenya Student
                kelas_siswa = StudentClass.query.filter_by(
                    id_student=user.id
                ).first()

                session['id_class'] = kelas_siswa.id_class if kelas_siswa else None
                
                return redirect(url_for('user.dashboard'))

            elif user.role == 'Teacher':
                
                # Jika rolenya Teacher, arahkan ke dashboard dosen
                return redirect(url_for('user.dashboard_dosen'))

            else:
                # Default fallback jika ada role lain (Admin, dsb)
                return redirect(url_for('user.dashboard'))

        else:

            return redirect(
                url_for(
                    'user.login',
                    status='error',
                    message='Email atau Password salah!'
                )
            )

    return render_template(
        'login.html',
        old=old
    )

@user_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')

@user_bp.app_template_filter('from_json')
def from_json(value):
    return json.loads(value)


# materi 1
@user_bp.route('/materi1/pengantarcitradigital')
@student_required
def pengantarcitradigital():

    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ambil subtopic dulu
    subtopic = SubTopic.query.filter_by(
        sub_topic_name="Pengertian Citra Digital"
    ).first()

    if not subtopic:
        return "Subtopik tidak ditemukan"

    id_subtopic = subtopic.id

    # ambil activity berdasarkan kelas + subtopic
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_subtopic=id_subtopic
    ).first()

    if not activity:
        return "Activity tidak ditemukan"

    id_activity = activity.id

    # ambil progress
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0

    return render_template(
        'mahasiswa/sub1/pengertiancitradigital.html',
        id_activity=id_activity,
        progress=progress_percent
    )
    
@user_bp.route('/materi1/jeniscitra')
@student_required
def jeniscitra():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ambil subtopic dulu
    subtopic = SubTopic.query.filter_by(
        sub_topic_name="Jenis Citra"
    ).first()

    if not subtopic:
        return "Subtopik tidak ditemukan"

    id_subtopic = subtopic.id

    # ambil activity berdasarkan kelas + subtopic
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_subtopic=id_subtopic
    ).first()

    if not activity:
        return "Activity tidak ditemukan"

    id_activity = activity.id

    # ambil progress
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0

    return render_template(
        'mahasiswa/sub1/jeniscitra.html',
        id_activity=id_activity,
        progress=progress_percent)

@user_bp.route('/materi1/rangkuman')
@student_required
def rangkuman1():

    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas (opsional, kalau mau validasi)
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    # ambil progress user (GLOBAL / keseluruhan)
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0

    return render_template(
        'mahasiswa/sub1/rangkuman1.html',
        progress=progress_percent
    )

@user_bp.route('/materi1/kuis')
@student_required
def kuis1():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ===============================
    # AMBIL KELAS USER
    # ===============================
    student_class = StudentClass.query.filter_by(id_student=user_id).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ===============================
    # AMBIL TOPIC & SUBTOPIC
    # ===============================
    topic = Topic.query.filter_by(topic_name="Pengantar Citra Digital").first()
    if not topic:
        return "Topic tidak ditemukan"

    subtopic = SubTopic.query.filter_by(sub_topic_name="Kuis-1").first()
    if not subtopic:
        return "Subtopik tidak ditemukan"

    # ===============================
    # AMBIL ACTIVITY
    # ===============================
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_topic=topic.id,
        id_subtopic=subtopic.id,
        type="kuis"
    ).first()

    if not activity:
        return "Activity kuis tidak ditemukan"

    id_activity = activity.id

    # ===============================
    # AMBIL RIWAYAT HASIL (Diurutkan dari percobaan terbaru)
    # ===============================
    results = ActivityResult.query.filter_by(
        id_user=user_id,
        id_activity=id_activity
    ).order_by(ActivityResult.percobaan_ke.desc()).all()

    result = results[0] if results else None

    # ===============================
    # AMBIL DETAIL JAWABAN (GROUP BY PERCOBAAN)
    # ===============================
    # Kita menggunakan list agar mudah di-looping di Jinja2
    grouped_details = []

    if results:
        # Kita urutkan ascending (1, 2, 3...) khusus untuk tampilan Tab Modal
        results_asc = sorted(results, key=lambda x: x.percobaan_ke)
        
        for r in results_asc:
            # Ambil jawaban khusus untuk ActivityResult ini saja
            answers = ActivityAnswer.query.filter_by(
                id_activity_result=r.id
            ).order_by(ActivityAnswer.id.asc()).all()

            attempt_details = []
            for ans in answers:
                q = Question.query.get(ans.id_question)
                if not q:
                    continue

                try:
                    soal_json = json.loads(q.question)
                    text = soal_json.get("text", "")
                except:
                    text = q.question

                attempt_details.append({
                    "soal": text,
                    "jawaban_user": ans.user_answer,
                    "status": ans.status
                })

            grouped_details.append({
                "percobaan_ke": r.percobaan_ke,
                "details": attempt_details
            })

    # ===============================
    # PROGRESS
    # ===============================
    progress_data = Progress.query.filter_by(id_user=user_id).first()
    progress_percent = progress_data.progres_value if progress_data else 0

    # ===============================
    # RENDER
    # ===============================
    return render_template(
        'mahasiswa/sub1/kuis1.html',
        activity=activity,
        result=result,
        grouped_details=grouped_details, # Pass data yang sudah dikelompokkan
        results=results,
        progress=progress_percent
    )
    
# materi 2
@user_bp.route('/materi2/pengantarsegmentasi')
@student_required
def pengantarsegmentasi():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ambil subtopic dulu
    subtopic = SubTopic.query.filter_by(
        sub_topic_name="Segmentasi Citra"
    ).first()

    if not subtopic:
        return "Subtopik tidak ditemukan"

    id_subtopic = subtopic.id

    # ambil activity berdasarkan kelas + subtopic
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_subtopic=id_subtopic
    ).first()

    if not activity:
        return "Activity tidak ditemukan"

    id_activity = activity.id

    # ambil progress
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0
    return render_template(
        'mahasiswa/sub2/pengantarsegmentasi.html', 
        id_activity=id_activity,
        progress=progress_percent)
    

@user_bp.route('/materi2/metodesegmentasi')
@student_required
def metodesegmentasi():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ambil subtopic dulu
    subtopic = SubTopic.query.filter_by(
        sub_topic_name="Metode Segmentasi Citra"
    ).first()

    if not subtopic:
        return "Subtopik tidak ditemukan"

    id_subtopic = subtopic.id

    # ambil activity berdasarkan kelas + subtopic
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_subtopic=id_subtopic
    ).first()

    if not activity:
        return "Activity tidak ditemukan"

    id_activity = activity.id

    # ambil progress
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()
    progress_percent = progress_data.progres_value if progress_data else 0
    return render_template(
        'mahasiswa/sub2/metodesegmentasi.html', 
        id_activity=id_activity,
        progress=progress_percent)

@user_bp.route('/materi2/rangkuman')
@student_required
def rangkuman2():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas (opsional, kalau mau validasi)
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    # ambil progress user (GLOBAL / keseluruhan)
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0
    return render_template('mahasiswa/sub2/rangkuman2.html',progress=progress_percent)

@user_bp.route('/materi2/kuis')
@student_required
def kuis2():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ===============================
    # AMBIL KELAS USER
    # ===============================
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ===============================
    # AMBIL TOPIC
    # ===============================
    topic = Topic.query.filter_by(
        topic_name="Pengantar Segmentasi Citra"
    ).first()

    if not topic:
        return "Topic tidak ditemukan"

    # ===============================
    # AMBIL SUBTOPIC
    # ===============================
    subtopic = SubTopic.query.filter_by(
        sub_topic_name="Kuis-2"
    ).first()

    if not subtopic:
        return "Subtopik tidak ditemukan"

    # ===============================
    # AMBIL ACTIVITY (PALING PENTING)
    # ===============================
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_topic=topic.id,
        id_subtopic=subtopic.id,
        type="kuis"
    ).first()

    if not activity:
        return "Activity kuis tidak ditemukan"

    id_activity = activity.id

    # ===============================
    # AMBIL RIWAYAT HASIL (Diurutkan dari percobaan terbaru)
    # ===============================
    results = ActivityResult.query.filter_by(
        id_user=user_id,
        id_activity=id_activity
    ).order_by(ActivityResult.percobaan_ke.desc()).all()

    result = results[0] if results else None

    # ===============================
    # AMBIL DETAIL JAWABAN (GROUP BY PERCOBAAN)
    # ===============================
    grouped_details = []

    if results:
        # Urutkan ascending khusus untuk tampilan Tab Modal (1, 2, 3...)
        results_asc = sorted(results, key=lambda x: x.percobaan_ke)
        
        for r in results_asc:
            # Ambil jawaban khusus untuk ActivityResult ini saja
            answers = ActivityAnswer.query.filter_by(
                id_activity_result=r.id
            ).order_by(ActivityAnswer.id.asc()).all()

            attempt_details = []
            for ans in answers:
                q = Question.query.get(ans.id_question)

                if not q:
                    continue

                try:
                    soal_json = json.loads(q.question)
                    text = soal_json.get("text", "")
                except:
                    text = q.question

                attempt_details.append({
                    "soal": text,
                    "jawaban_user": ans.user_answer,
                    "status": ans.status
                })

            grouped_details.append({
                "percobaan_ke": r.percobaan_ke,
                "details": attempt_details
            })

    # ===============================
    # PROGRESS (FIX)
    # ===============================
    progress_data = Progress.query.filter_by(
        id_user=user_id,
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0

    # ===============================
    # RENDER
    # ===============================
    return render_template(
        'mahasiswa/sub2/kuis2.html',
        activity=activity,
        result=result,
        grouped_details=grouped_details, # Pass data yang sudah dikelompokkan
        results=results,
        progress=progress_percent
    )
# materi 3
@user_bp.route('/materi3/pengantaredgebased')
@student_required
def pengantaredgebased():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ambil subtopic dulu
    subtopic = SubTopic.query.filter_by(
        sub_topic_name="Pengantar Edge-based segmentation"
    ).first()

    if not subtopic:
        return "Subtopik tidak ditemukan"

    id_subtopic = subtopic.id

    # ambil activity berdasarkan kelas + subtopic
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_subtopic=id_subtopic
    ).first()

    if not activity:
        return "Activity tidak ditemukan"

    id_activity = activity.id

    # ambil progress
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0
    return render_template(
        'mahasiswa/sub3/pengantaredgebased.html',
        id_activity=id_activity,
        progress=progress_percent
    )

@user_bp.route('/materi3/tahapanedgebased')
@student_required
def tahapanedgebased():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ambil subtopic dulu
    subtopic = SubTopic.query.filter_by(
        sub_topic_name="Tahapan Edge Based Segmentation"
    ).first()

    if not subtopic:
        return "Subtopik tidak ditemukan"

    id_subtopic = subtopic.id

    # ambil activity berdasarkan kelas + subtopic
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_subtopic=id_subtopic
    ).first()

    if not activity:
        return "Activity tidak ditemukan"

    id_activity = activity.id

    # ambil progress
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0
    return render_template(
        'mahasiswa/sub3/tahapanedgebased.html',
        id_activity=id_activity,
        progress=progress_percent
    )

@user_bp.route('/materi3/praktekedgebased')
@student_required
def praktekedgebased():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ambil subtopic dulu
    subtopic = SubTopic.query.filter_by(
        sub_topic_name="Praktek Edge-based Segmentation"
    ).first()

    if not subtopic:
        return "Subtopik tidak ditemukan"

    id_subtopic = subtopic.id

    # ambil activity berdasarkan kelas + subtopic
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_subtopic=id_subtopic
    ).first()

    if not activity:
        return "Activity tidak ditemukan"

    id_activity = activity.id

    # ambil progress
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0
    return render_template(
        'mahasiswa/sub3/praktekedgebased.html',
        id_activity=id_activity,
        progress=progress_percent
    )

@user_bp.route('/materi3/rangkuman')
@student_required
def rangkuman3():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas (opsional, kalau mau validasi)
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    # ambil progress user (GLOBAL / keseluruhan)
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0
    return render_template('mahasiswa/sub3/rangkuman3.html',progress=progress_percent)

@user_bp.route('/materi3/kuis')
@student_required
def kuis3():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ===============================
    # AMBIL KELAS USER
    # ===============================
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ===============================
    # AMBIL TOPIC
    # ===============================
    topic = Topic.query.filter_by(
        topic_name="Edge-Based Segmentation"
    ).first()

    if not topic:
        return "Topic tidak ditemukan"

    # ===============================
    # AMBIL SUBTOPIC
    # ===============================
    subtopic = SubTopic.query.filter_by(
        sub_topic_name="Kuis-3"
    ).first()

    if not subtopic:
        return "Subtopik tidak ditemukan"

    # ===============================
    # AMBIL ACTIVITY (PALING PENTING)
    # ===============================
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_topic=topic.id,
        id_subtopic=subtopic.id,
        type="kuis"
    ).first()

    if not activity:
        return "Activity kuis tidak ditemukan"

    id_activity = activity.id

    # ===============================
    # AMBIL RIWAYAT HASIL (Diurutkan dari percobaan terbaru)
    # ===============================
    results = ActivityResult.query.filter_by(
        id_user=user_id,
        id_activity=id_activity
    ).order_by(ActivityResult.percobaan_ke.desc()).all()

    result = results[0] if results else None

    # ===============================
    # AMBIL DETAIL JAWABAN (GROUP BY PERCOBAAN)
    # ===============================
    grouped_details = []

    if results:
        # Urutkan ascending khusus untuk tampilan Tab Modal (1, 2, 3...)
        results_asc = sorted(results, key=lambda x: x.percobaan_ke)
        
        for r in results_asc:
            # Ambil jawaban khusus untuk ActivityResult ini saja
            answers = ActivityAnswer.query.filter_by(
                id_activity_result=r.id
            ).order_by(ActivityAnswer.id.asc()).all()

            attempt_details = []
            for ans in answers:
                q = Question.query.get(ans.id_question)

                if not q:
                    continue

                try:
                    soal_json = json.loads(q.question)
                    text = soal_json.get("text", "")
                except:
                    text = q.question

                attempt_details.append({
                    "soal": text,
                    "jawaban_user": ans.user_answer,
                    "status": ans.status
                })

            grouped_details.append({
                "percobaan_ke": r.percobaan_ke,
                "details": attempt_details
            })

    # ===============================
    # PROGRESS (FIX)
    # ===============================
    progress_data = Progress.query.filter_by(
        id_user=user_id,
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0

    return render_template(
        'mahasiswa/sub3/kuis3.html',
        activity=activity,
        result=result,
        grouped_details=grouped_details, # Pass data yang sudah dikelompokkan
        results=results,
        progress=progress_percent
    )
    
# materi 4
@user_bp.route('/materi4/pengantarthresholdbased')
@student_required
def pengantarthresholdbased():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ambil subtopic dulu
    subtopic = SubTopic.query.filter_by(
        sub_topic_name="Pengantar Thresholding"
    ).first()

    if not subtopic:
        return "Subtopik tidak ditemukan"

    id_subtopic = subtopic.id

    # ambil activity berdasarkan kelas + subtopic
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_subtopic=id_subtopic
    ).first()

    if not activity:
        return "Activity tidak ditemukan"

    id_activity = activity.id

    # ambil progress
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0
    return render_template('mahasiswa/sub4/pengantarthresholdbased.html',id_activity=id_activity, progress=progress_percent)

@user_bp.route("/materi4/histogram")
@student_required
def histogram():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ambil subtopic dulu
    subtopic = SubTopic.query.filter_by(
        sub_topic_name="Histogram"
    ).first()

    if not subtopic:
        return "Subtopik tidak ditemukan"

    id_subtopic = subtopic.id

    # ambil activity berdasarkan kelas + subtopic
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_subtopic=id_subtopic
    ).first()

    if not activity:
        return "Activity tidak ditemukan"

    id_activity = activity.id

    # ambil progress
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0
    return render_template('mahasiswa/sub4/histogram.html',id_activity=id_activity, progress=progress_percent)

@user_bp.route("/materi4/metodethresholding")
@student_required
def metodethresholding():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ambil subtopic dulu
    subtopic = SubTopic.query.filter_by(
        sub_topic_name="Metode Thresholding"
    ).first()

    if not subtopic:
        return "Subtopik tidak ditemukan"

    id_subtopic = subtopic.id

    # ambil activity berdasarkan kelas + subtopic
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_subtopic=id_subtopic
    ).first()

    if not activity:
        return "Activity tidak ditemukan"

    id_activity = activity.id

    # ambil progress
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0
    return render_template('mahasiswa/sub4/metodethresholding.html', id_activity=id_activity, progress=progress_percent)

@user_bp.route("/materi4/rangkuman")
@student_required
def rangkuman4():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas (opsional, kalau mau validasi)
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    # ambil progress user (GLOBAL / keseluruhan)
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0
    return render_template('mahasiswa/sub4/rangkuman4.html', progress=progress_percent)

@user_bp.route('/materi4/kuis')
@student_required
def kuis4():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ===============================
    # AMBIL KELAS USER
    # ===============================
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ===============================
    # AMBIL TOPIC
    # ===============================
    topic = Topic.query.filter_by(
        topic_name="Threshold-Based Segmentation"
    ).first()

    if not topic:
        return "Topic tidak ditemukan"

    # ===============================
    # AMBIL SUBTOPIC
    # ===============================
    subtopic = SubTopic.query.filter_by(
        sub_topic_name="Kuis-4"
    ).first()

    if not subtopic:
        return "Subtopik tidak ditemukan"

    # ===============================
    # AMBIL ACTIVITY (PALING PENTING)
    # ===============================
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_topic=topic.id,
        id_subtopic=subtopic.id,
        type="kuis"
    ).first()

    if not activity:
        return "Activity kuis tidak ditemukan"

    id_activity = activity.id

    # ===============================
    # AMBIL RIWAYAT HASIL (Diurutkan dari percobaan terbaru)
    # ===============================
    results = ActivityResult.query.filter_by(
        id_user=user_id,
        id_activity=id_activity
    ).order_by(ActivityResult.percobaan_ke.desc()).all()

    result = results[0] if results else None

    # ===============================
    # AMBIL DETAIL JAWABAN (GROUP BY PERCOBAAN)
    # ===============================
    grouped_details = []

    if results:
        # Urutkan ascending khusus untuk tampilan Tab Modal (1, 2, 3...)
        results_asc = sorted(results, key=lambda x: x.percobaan_ke)
        
        for r in results_asc:
            # Ambil jawaban khusus untuk ActivityResult ini saja
            answers = ActivityAnswer.query.filter_by(
                id_activity_result=r.id
            ).order_by(ActivityAnswer.id.asc()).all()

            attempt_details = []
            for ans in answers:
                q = Question.query.get(ans.id_question)

                if not q:
                    continue

                try:
                    soal_json = json.loads(q.question)
                    text = soal_json.get("text", "")
                except:
                    text = q.question

                attempt_details.append({
                    "soal": text,
                    "jawaban_user": ans.user_answer,
                    "status": ans.status
                })

            grouped_details.append({
                "percobaan_ke": r.percobaan_ke,
                "details": attempt_details
            })

    # ===============================
    # PROGRESS (FIX)
    # ===============================
    progress_data = Progress.query.filter_by(
        id_user=user_id,
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0

    return render_template(
        'mahasiswa/sub4/kuis4.html',
        activity=activity,
        result=result,
        grouped_details=grouped_details, # Pass data yang sudah dikelompokkan
        results=results,
        progress=progress_percent
    )
#materi 5
@user_bp.route('/materi5/pengantarregionbased')
@student_required
def pengantarregionbased():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ambil subtopic dulu
    subtopic = SubTopic.query.filter_by(
        sub_topic_name="Pengantar Region-Based Segmentation"
    ).first()

    if not subtopic:
        return "Subtopik tidak ditemukan"

    id_subtopic = subtopic.id

    # ambil activity berdasarkan kelas + subtopic
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_subtopic=id_subtopic
    ).first()

    if not activity:
        return "Activity tidak ditemukan"

    id_activity = activity.id

    # ambil progress
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0
    return render_template('mahasiswa/sub5/pengantarregionbased.html',id_activity=id_activity, progress=progress_percent)

@user_bp.route('/materi5/regiongrowing')
@student_required
def regiongrowing():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ambil subtopic dulu
    subtopic = SubTopic.query.filter_by(
        sub_topic_name="Region Growing"
    ).first()

    if not subtopic:
        return "Subtopik tidak ditemukan"

    id_subtopic = subtopic.id

    # ambil activity berdasarkan kelas + subtopic
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_subtopic=id_subtopic
    ).first()

    if not activity:
        return "Activity tidak ditemukan"

    id_activity = activity.id

    # ambil progress
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0
    return render_template('mahasiswa/sub5/regiongrowing.html',id_activity=id_activity, progress=progress_percent)

@user_bp.route('/materi5/splitandmerge')
@student_required
def splitandmerge():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ambil subtopic dulu
    subtopic = SubTopic.query.filter_by(
        sub_topic_name="Split and Merge"
    ).first()

    if not subtopic:
        return "Subtopik tidak ditemukan"

    id_subtopic = subtopic.id

    # ambil activity berdasarkan kelas + subtopic
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_subtopic=id_subtopic
    ).first()

    if not activity:
        return "Activity tidak ditemukan"

    id_activity = activity.id

    # ambil progress
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0
    return render_template('mahasiswa/sub5/splitandmerge.html',id_activity=id_activity, progress=progress_percent)

@user_bp.route("/materi5/rangkuman")
@student_required
def rangkuman5():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ambil kelas (opsional, kalau mau validasi)
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    # ambil progress user (GLOBAL / keseluruhan)
    progress_data = Progress.query.filter_by(
        id_user=user_id
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0
    return render_template('mahasiswa/sub5/rangkuman5.html', progress=progress_percent)
@user_bp.route('/materi5/kuis')
@student_required
def kuis5():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # ===============================
    # AMBIL KELAS USER
    # ===============================
    student_class = StudentClass.query.filter_by(
        id_student=user_id
    ).first()

    if not student_class:
        return "User belum masuk kelas"

    kelas_id = student_class.id_class

    # ===============================
    # AMBIL TOPIC
    # ===============================
    topic = Topic.query.filter_by(
        topic_name="Region-Based Segmentation"
    ).first()

    if not topic:
        return "Topic tidak ditemukan"

    # ===============================
    # AMBIL SUBTOPIC
    # ===============================
    subtopic = SubTopic.query.filter_by(
        sub_topic_name="Kuis-5"
    ).first()

    if not subtopic:
        return "Subtopik tidak ditemukan"

    # ===============================
    # AMBIL ACTIVITY (PALING PENTING)
    # ===============================
    activity = Activity.query.filter_by(
        id_class=kelas_id,
        id_topic=topic.id,
        id_subtopic=subtopic.id,
        type="kuis"
    ).first()

    if not activity:
        return "Activity kuis tidak ditemukan"

    id_activity = activity.id

    # ===============================
    # AMBIL RIWAYAT HASIL (Diurutkan dari percobaan terbaru)
    # ===============================
    results = ActivityResult.query.filter_by(
        id_user=user_id,
        id_activity=id_activity
    ).order_by(ActivityResult.percobaan_ke.desc()).all()

    result = results[0] if results else None

    # ===============================
    # AMBIL DETAIL JAWABAN (GROUP BY PERCOBAAN)
    # ===============================
    grouped_details = []

    if results:
        # Urutkan ascending khusus untuk tampilan Tab Modal (1, 2, 3...)
        results_asc = sorted(results, key=lambda x: x.percobaan_ke)
        
        for r in results_asc:
            # Ambil jawaban khusus untuk ActivityResult ini saja
            answers = ActivityAnswer.query.filter_by(
                id_activity_result=r.id
            ).order_by(ActivityAnswer.id.asc()).all()

            attempt_details = []
            for ans in answers:
                q = Question.query.get(ans.id_question)

                if not q:
                    continue

                try:
                    soal_json = json.loads(q.question)
                    text = soal_json.get("text", "")
                except:
                    text = q.question

                attempt_details.append({
                    "soal": text,
                    "jawaban_user": ans.user_answer,
                    "status": ans.status
                })

            grouped_details.append({
                "percobaan_ke": r.percobaan_ke,
                "details": attempt_details
            })

    # ===============================
    # PROGRESS (FIX)
    # ===============================
    progress_data = Progress.query.filter_by(
        id_user=user_id,
    ).first()

    progress_percent = progress_data.progres_value if progress_data else 0

    return render_template(
        'mahasiswa/sub5/kuis5.html',
        activity=activity,
        result=result,
        grouped_details=grouped_details, # Pass data yang sudah dikelompokkan
        results=results,
        progress=progress_percent
    )

# Aktivitas
@user_bp.route('/api/soal/<int:id_activity>')
def get_soal(id_activity):

    relations = ActivityQuestion.query.filter_by(
        id_activity=id_activity
    ).all()

    hasil = []

    for rel in relations:
        q = Question.query.get(rel.id_question)

        question_data = json.loads(q.question)

        hasil.append({
            "soal": question_data["text"],

            # TAMBAHKAN INI
            "URL": question_data.get("URL"),

            "jawaban": q.MC_Answer,

            "opsi": {
                k: v["teks"]
                for opt in json.loads(q.MC_option)
                for k, v in opt.items()
            }
        })

    return jsonify(hasil)

# Load Soal
@user_bp.route('/api/kuis/<string:title>')
def api_kuis(title):
    import json, random
    from app.model.activity import Activity
    from app.model.activity_question import ActivityQuestion
    from app.model.question import Question

    activity = Activity.query.filter_by(title=title).first_or_404()

    relasi = ActivityQuestion.query.filter_by(id_activity=activity.id).all()
    question_ids = [r.id_question for r in relasi]

    questions = Question.query.filter(Question.id.in_(question_ids)).all()

    result = []

    for q in questions:
        soal = json.loads(q.question)
        opsi = json.loads(q.MC_option)

        # 🔹 cari teks jawaban benar SEBELUM shuffle
        correct_text = None
        for opt in opsi:
            for k, v in opt.items():
                if k.lower() == q.MC_Answer.lower():
                    correct_text = v["teks"]

        # 🔹 shuffle opsi
        random.shuffle(opsi)

        letters = ['a', 'b', 'c', 'd', 'e']
        new_options = []
        correct_key = None  #  kunci jawaban setelah shuffle

        for i, opt in enumerate(opsi):
            key = letters[i]
            val = list(opt.values())[0]['teks']

            if val == correct_text:
                correct_key = key

            new_options.append({
                "key": key,
                "text": val
            })

        result.append({
            "id": q.id,
            "text": soal["text"],
            "URL": soal.get("URL", ""),
            "options": new_options,
            "correct_key": correct_key  #  WAJIB
        })

    # 🔹 shuffle soal
    random.shuffle(result)

    return jsonify(result)

# load soal kuis
@user_bp.route('/kuis/mulai/<slug>')
def mulai_kuis(slug):

    title = slug.replace('-', ' ')

    activity = Activity.query.filter_by(title=title).first_or_404()

    return render_template(
        'layouts/kuis.html',
        activity=activity
    )

@user_bp.route('/evaluasi')
@student_required # Pastikan decorator ini dipasang agar session aman
def evaluasi():
    # 1. Ambil dari session, JANGAN di-hardcode angka 1
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    # 2. Cari activity evaluasi
    activity = Activity.query.filter_by(
        type="evaluasi",
        id_topic=6
    ).first()

    if not activity:
        return "Aktivitas Evaluasi tidak ditemukan"

    # 3. Ambil semua riwayat berdasarkan user_id yang login (Urutkan dari percobaan terbaru)
    results = ActivityResult.query.filter_by(
        id_user=user_id,
        id_activity=activity.id
    ).order_by(ActivityResult.percobaan_ke.desc()).all()

    result = results[0] if results else None

    # ===============================
    # 4. AMBIL DETAIL JAWABAN (GROUP BY PERCOBAAN)
    # ===============================
    grouped_details = []

    if results:
        # Urutkan ascending khusus untuk tampilan Tab Modal (1, 2, 3...)
        results_asc = sorted(results, key=lambda x: x.percobaan_ke)
        
        for r in results_asc:
            # Ambil jawaban khusus untuk ActivityResult ini saja
            answers = ActivityAnswer.query.filter_by(
                id_activity_result=r.id
            ).order_by(ActivityAnswer.id.asc()).all()

            attempt_details = []
            for ans in answers:
                q = Question.query.get(ans.id_question)
                
                if not q:
                    continue

                try:
                    soal = json.loads(q.question)
                    text_soal = soal.get("text", "")
                except:
                    text_soal = q.question

                attempt_details.append({
                    "soal": text_soal,
                    "jawaban_user": ans.user_answer,
                    "status": ans.status
                })

            grouped_details.append({
                "percobaan_ke": r.percobaan_ke,
                "details": attempt_details
            })

    return render_template(
        'mahasiswa/evaluasi_mahasiswa.html',
        activity=activity,
        result=result,
        grouped_details=grouped_details, # Pass data yang sudah dikelompokkan
        results=results
    )

@user_bp.route('/submit-kuis-evaluasi', methods=['POST'])
def submit_kuis_evaluasi():

    user_id = session.get('user_id')
    activity_id = request.form.get('activity_id')

    # =========================
    # AMBIL DATA
    # =========================
    answers = json.loads(request.form.get('answers', '{}'))
    correct_map = json.loads(request.form.get('correct_map', '{}'))

    start_time = datetime.now()

    activity = Activity.query.get(activity_id)

    if not activity:
        return redirect('/')

    total_waktu = activity.durasi_pengerjaan * 60

    # =========================
    # AMBIL KKM BERDASARKAN KELAS
    # =========================
    setting = Setting.query.filter_by(id_class=activity.id_class).first()

    # DEFAULT
    kkm = 60
    if setting:
        if activity.type == 'kuis' and setting.nilai_kkm_kuis:
            kkm = setting.nilai_kkm_kuis
        elif activity.type == 'evaluasi' and setting.nilai_kkm_evaluasi:
            kkm = setting.nilai_kkm_evaluasi

    # =========================
    # CEK PERCOBAAN KE-BERAPA (UPDATE BARU)
    # =========================
    last_attempt = ActivityResult.query.filter_by(
        id_user=user_id,
        id_activity=activity_id
    ).order_by(
        ActivityResult.percobaan_ke.desc() # Ambil data percobaan terakhir
    ).first()

    if last_attempt:
        is_retry = True
        percobaan_ke = last_attempt.percobaan_ke + 1
    else:
        is_retry = False
        percobaan_ke = 1

    # =========================
    # WAKTU
    # =========================
    try:
        sisa_waktu = int(request.form.get('time_left', 0))
    except:
        sisa_waktu = 0

    if sisa_waktu < 0:
        sisa_waktu = 0
    if sisa_waktu > total_waktu:
        sisa_waktu = total_waktu

    waktu_mengerjakan = total_waktu - sisa_waktu

    # =========================
    # CEK JAWABAN (SIMPAN SEMENTARA DULU)
    # =========================
    activity_questions = ActivityQuestion.query.filter_by(id_activity=activity_id).all()
    total_soal = len(activity_questions)
    
    total_benar = 0
    total_salah = 0
    
    # List untuk menyimpan jawaban sementara sebelum disimpan ke DB
    temp_answers = [] 

    for aq in activity_questions:
        q_id = str(aq.id_question)
        user_ans = answers.get(q_id, "")
        question = Question.query.get(aq.id_question)
        is_correct = False

        if user_ans:
            if question.type == 'mc':
                correct_key = correct_map.get(q_id)
                if correct_key and (user_ans.lower() == correct_key.lower()):
                    is_correct = True
            else:
                if (user_ans.strip().lower() == question.SA_Answer.strip().lower()):
                    is_correct = True

        # Status & Kalkulasi
        if is_correct:
            total_benar += 1
            status = 'benar'
        else:
            total_salah += 1
            status = 'salah'

        # Masukkan ke list sementara
        temp_answers.append({
            'id_question': aq.id_question,
            'user_answer': user_ans,
            'status': status
        })

    # =========================
    # HITUNG NILAI AKHIR
    # =========================
    nilai_asli = ((total_benar / total_soal) * 100) if total_soal > 0 else 0
    nilai_final = nilai_asli

    # JIKA SUDAH PERNAH MENGERJAKAN DAN NILAI MELEBIHI KKM MAKA NILAI DIJADIKAN KKM
    if is_retry and nilai_asli >= kkm:
        nilai_final = kkm

    end_time = datetime.now()
    result_status = 'lulus' if nilai_final >= kkm else 'tidak lulus'

    # =========================
    # 1. SIMPAN RESULT DULU (UPDATE BARU)
    # =========================
    result = ActivityResult(
        id_user=user_id,
        id_activity=activity_id,
        percobaan_ke=percobaan_ke, # Kolom baru
        nilai_akhir=nilai_final,
        result_status=result_status,
        waktu_mengerjakan=waktu_mengerjakan,
        start_time=start_time,
        end_time=end_time,
        total_benar=total_benar,
        total_salah=total_salah
    )

    db.session.add(result)
    db.session.flush() # Penting! Flush agar `result` mendapat ID dari database sebelum di-commit

    # =========================
    # 2. SIMPAN JAWABAN (UPDATE BARU)
    # =========================
    for ans_data in temp_answers:
        answer = ActivityAnswer(
            id_activity_result=result.id, # Ambil ID dari result yang baru saja di-flush
            id_activity=activity_id,
            id_user=user_id,
            id_question=ans_data['id_question'],
            user_answer=ans_data['user_answer'],
            status=ans_data['status']
        )
        db.session.add(answer)

    # Commit semua data (Result & Answers) secara bersamaan
    db.session.commit()

    # ==================================================
    # UPDATE HISTORY PROGRESS
    # ==================================================
    existing = HistoryProgress.query.filter_by(
        id_user=user_id,
        id_topic=activity.id_topic,
        id_subtopic=activity.id_subtopic
    ).first()

    if not existing:
        history = HistoryProgress(
            id_user=user_id,
            id_topic=activity.id_topic,
            id_subtopic=activity.id_subtopic,
            updated_at=datetime.now()
        )
        db.session.add(history)
        db.session.commit()

        # =========================
        # UPDATE TOTAL PROGRESS
        # =========================
        total_subtopic = SubTopic.query.count()
        completed = HistoryProgress.query.filter_by(id_user=user_id).count()
        progress_value = round((completed / total_subtopic) * 100)

        progress = Progress.query.filter_by(id_user=user_id).first()

        if progress:
            progress.progres_value = progress_value
            progress.last_updated = datetime.now()
        else:
            progress = Progress(
                id_user=user_id,
                progres_value=progress_value,
                last_updated=datetime.now()
            )
            db.session.add(progress)

        db.session.commit()

    # =========================
    # REDIRECT
    # =========================
    topic = Topic.query.get(activity.id_topic)

    if activity.type == 'evaluasi':
        return redirect('/evaluasi')

    if topic.topic_name == 'Pengantar Citra Digital':
        return redirect('/materi1/kuis')
    elif topic.topic_name == 'Segmentasi Citra':
        return redirect('/materi2/kuis')
    elif topic.topic_name == 'Edge-Based Segmentation':
        return redirect('/materi3/kuis')
    elif topic.topic_name == 'Threshold-Based Segmentation':
        return redirect('/materi4/kuis')
    elif topic.topic_name == 'Region-Based Segmentation':
        return redirect('/materi5/kuis')

    return redirect('/')

@user_bp.route('/update-progress', methods=['POST'])
@student_required
def update_progress():

    user_id = session.get('user_id')

    data = request.get_json()

    activity_id = data.get('activity_id')

    # =========================
    # JIKA DARI EVALUASI / QUIZ / ACTIVITY
    # =========================
    if activity_id:

        activity = Activity.query.get(activity_id)

        if not activity:
            return jsonify({
                'success': False,
                'message': 'Activity tidak ditemukan'
            }), 404

        id_topic = activity.id_topic
        id_subtopic = activity.id_subtopic

    # =========================
    # JIKA DARI RANGKUMAN
    # =========================
    else:

        id_topic = data.get('id_topic')
        id_subtopic = data.get('id_subtopic')

    # =========================
    # VALIDASI
    # =========================
    if not id_topic or not id_subtopic:
        return jsonify({
            'success': False,
            'message': 'Data tidak lengkap'
        }), 400

    # =========================
    # CEK HISTORY
    # =========================
    existing = HistoryProgress.query.filter_by(
        id_user=user_id,
        id_topic=id_topic,
        id_subtopic=id_subtopic
    ).first()

    # =========================
    # JIKA BELUM ADA
    # =========================
    if not existing:

        history = HistoryProgress(
            id_user=user_id,
            id_topic=id_topic,
            id_subtopic=id_subtopic,
            updated_at=datetime.now()
        )

        db.session.add(history)

        db.session.commit()

        # =========================
        # TOTAL SUBTOPIC
        # =========================
        total_subtopic = SubTopic.query.count()

        # =========================
        # TOTAL COMPLETED
        # =========================
        completed = HistoryProgress.query.filter_by(
            id_user=user_id
        ).count()

        # =========================
        # HITUNG PROGRESS
        # =========================
        progress_value = round(
            (completed / total_subtopic) * 100
        )

        # =========================
        # CEK PROGRESS
        # =========================
        progress = Progress.query.filter_by(
            id_user=user_id
        ).first()

        if progress:

            progress.progres_value = progress_value
            progress.last_updated = datetime.now()

        else:

            progress = Progress(
                id_user=user_id,
                progres_value=progress_value,
                last_updated=datetime.now()
            )

            db.session.add(progress)

        db.session.commit()

    return jsonify({
        'success': True
    })

# guru / pengajar
@user_bp.route('/dashboard-dosen')
# @dosen_required  <-- Pastikan ini diaktifkan nanti
def dashboard_dosen():
    # Ambil ID dosen yang sedang login
    dosen_id = session.get('user_id')

    if not dosen_id:
        return redirect(url_for('user.login'))

    # ==========================================
    # 1. AMBIL KELAS MILIK DOSEN INI SAJA
    # ==========================================
    # Asumsi: kelas yang dimiliki dosen dicatat di kolom 'created_by' pada tabel Classes.
    # Jika kamu menggunakan tabel TeacherClass, ubah query-nya menyesuaikan relasi tersebut.
    kelas_dosen = Class.query.filter_by(created_by=dosen_id).all()
    
    total_kelas = len(kelas_dosen)
    
    # Kumpulkan semua ID kelas milik dosen ini ke dalam list
    kelas_ids = [k.id for k in kelas_dosen]

    # ==========================================
    # 2. HITUNG TOTAL SISWA DI KELAS DOSEN INI
    # ==========================================
    if kelas_ids:
        # Ambil data StudentClass HANYA yang id_class-nya ada di daftar kelas dosen ini
        siswa_di_kelas_dosen = StudentClass.query.filter(StudentClass.id_class.in_(kelas_ids)).all()
        # Gunakan set() agar jika 1 siswa ikut 2 kelas milik dosen ini, tetap dihitung 1 siswa unik
        total_siswa = len(set([sc.id_student for sc in siswa_di_kelas_dosen]))
    else:
        total_siswa = 0

    # ==========================================
    # 3. HITUNG TOTAL SOAL
    # ==========================================
    # Total seluruh soal di database (Jika ingin difilter milik dosen ini saja, 
    # ganti jadi: Question.query.filter_by(created_by=dosen_id).count() )
    total_soal = Question.query.count()

    # ==========================================
    # 4. HITUNG RATA-RATA PROGRESS PER KELAS (MILIK DOSEN SAJA)
    # ==========================================
    progress_kelas = []

    for kelas in kelas_dosen:
        siswa_di_kelas = StudentClass.query.filter_by(id_class=kelas.id).all()
        jumlah_siswa = len(siswa_di_kelas)
        
        rata_rata_progress = 0
        
        if jumlah_siswa > 0:
            total_progress_kelas = 0
            for sk in siswa_di_kelas:
                prog = Progress.query.filter_by(id_user=sk.id_student).first()
                if prog:
                    total_progress_kelas += prog.progres_value
            
            rata_rata_progress = round(total_progress_kelas / jumlah_siswa)

        # Tentukan warna bar
        if rata_rata_progress >= 75:
            color = "primary"
        elif rata_rata_progress >= 50:
            color = "warning"
        else:
            color = "danger"

        progress_kelas.append({
            'nama_kelas': kelas.name,
            'deskripsi': kelas.description,
            'jumlah_siswa': jumlah_siswa,
            'rata_progress': rata_rata_progress,
            'color': color
        })

    return render_template(
        'dashboard-dosen.html',
        total_kelas=total_kelas,
        total_siswa=total_siswa,
        total_soal=total_soal,
        progress_kelas=progress_kelas
    )
@user_bp.route('/datasiswa')
def data_siswa():

    # AMBIL ID DOSEN YANG LOGIN
    teacher_id = session.get('user_id')

    # VALIDASI LOGIN
    if not teacher_id:
        return redirect(url_for('user.login'))

    # AMBIL KELAS DOSEN
    kelas = db.session.query(Class)\
        .join(TeacherClass, Class.id == TeacherClass.id_class)\
        .filter(TeacherClass.id_teacher == teacher_id)\
        .all()

    # CLASS YANG DIPILIH
    selected_class = request.args.get('class_id', type=int)

    siswa = []
    nama_kelas = None

    # JIKA ADA KELAS DIPILIH
    if selected_class:

        # VALIDASI KELAS MILIK DOSEN
        valid_class = db.session.query(TeacherClass)\
            .filter(
                TeacherClass.id_teacher == teacher_id,
                TeacherClass.id_class == selected_class
            ).first()

        # JIKA BUKAN KELAS DOSEN
        if not valid_class:
            abort(403)

        # AMBIL SISWA
        siswa = db.session.query(User, Class)\
            .join(StudentClass, User.id == StudentClass.id_student)\
            .join(Class, Class.id == StudentClass.id_class)\
            .filter(
                StudentClass.id_class == selected_class,
                User.role == 'Student'
            ).all()

        # NAMA KELAS
        kelas_terpilih = Class.query.get(selected_class)

        if kelas_terpilih:
            nama_kelas = kelas_terpilih.name

    return render_template(
        'dosen/datasiswa.html',
        kelas=kelas,
        siswa=siswa,
        selected_class=selected_class,
        nama_kelas=nama_kelas
    )
# edit data siswa
@user_bp.route('/update_siswa/<int:id>', methods=['POST'])
def update_siswa(id):
    data = request.get_json()

    user = User.query.get(id)

    if not user:
        return jsonify({'message': 'User tidak ditemukan'}), 404

    user.name = data.get('name')
    user.email = data.get('email')

    # password optional
    if data.get('password'):
        user.password = generate_password_hash(data.get('password'))

    db.session.commit()

    return jsonify({'message': 'Data berhasil diperbarui'})

@user_bp.route('/export_siswa')
def export_siswa():
    class_id = request.args.get('class_id', type=int)

    # =========================
    # JIKA PILIH KELAS
    # =========================
    if class_id:
        data = db.session.query(User, Class)\
            .join(StudentClass, User.id == StudentClass.id_student)\
            .join(Class, Class.id == StudentClass.id_class)\
            .filter(
                StudentClass.id_class == class_id,
                User.role == 'Student'
            ).all()

        nama_kelas = Class.query.get(class_id).name

        filename = f"data_siswa_kelas_{nama_kelas}.xlsx"

    # =========================
    # JIKA TIDAK PILIH (SEMUA)
    # =========================
    else:
        data = db.session.query(User, Class)\
            .join(StudentClass, User.id == StudentClass.id_student)\
            .join(Class, Class.id == StudentClass.id_class)\
            .filter(User.role == 'Student')\
            .all()

        filename = "data_semua_siswa.xlsx"

    # =========================
    # FORMAT DATA
    # =========================
    rows = []
    for i, (user, kelas) in enumerate(data, start=1):
        rows.append({
            "No": i,
            "Nama Siswa": user.name,
            "Email": user.email,
            "Kelas": kelas.name
        })

    df = pd.DataFrame(rows)

    # =========================
    # EXPORT
    # =========================
    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return send_file(
        output,
        download_name=filename,
        as_attachment=True
    )

@user_bp.route('/datakelas')
def data_kelas():

    # AMBIL USER LOGIN
    user_id = session.get('user_id')

    # VALIDASI LOGIN
    if not user_id:
        return redirect(url_for('user.login'))

    # AMBIL SEMUA KELAS DOSEN
    classes = db.session.query(Class)\
        .join(TeacherClass, Class.id == TeacherClass.id_class)\
        .filter(TeacherClass.id_teacher == user_id)\
        .all()

    data = []

    for k in classes:

        # AMBIL SEMUA ACTIVITY KELAS
        activities = Activity.query.filter_by(
            id_class=k.id,
            status='aktif'
        ).all()

        # FILTER KUIS
        kuis_list = [
            a for a in activities
            if a.type == 'kuis'
        ]

        # FILTER AKTIVITAS
        aktivitas_list = [
            a for a in activities
            if a.type in ['kuis', 'evaluasi']
        ]

        # AMBIL UNIQUE TOPIC ID
        topic_ids = list(set([
            a.id_topic for a in kuis_list
            if a.id_topic
        ]))

        # AMBIL TOPIC
        topics = []

        if topic_ids:
            topics = Topic.query.filter(
                Topic.id.in_(topic_ids)
            ).all()

        data.append({
            "class": k,
            "activities": activities,
            "topics": topics,
            "aktivitas_list": aktivitas_list
        })

    return render_template(
        'dosen/datakelas.html',
        data=data
    )

@user_bp.route('/tambah-kelas', methods=['POST'])
def tambah_kelas():

    from flask import request, redirect, url_for, session
    import random
    import string

    # AMBIL USER LOGIN
    user_id = session.get('user_id')

    # VALIDASI LOGIN
    if not user_id:
        return redirect(url_for('user.login'))

    # AMBIL DATA FORM
    name = request.form.get('name')
    semester = request.form.get('semester')
    tahun = request.form.get('tahun')
    description = request.form.get('description')

    # GENERATE TOKEN UNIK
    while True:

        token = ''.join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=6
            )
        )

        # cek apakah token sudah ada
        existing = Class.query.filter_by(token=token).first()

        if not existing:
            break

    # SIMPAN KELAS
    kelas = Class(
        name=name,
        semester=semester,
        tahun=tahun,
        description=description,
        token=token,
        created_by=user_id
    )

    db.session.add(kelas)
    db.session.flush()  
    # flush agar kelas.id langsung ada tanpa commit

    # HUBUNGKAN DOSEN KE KELAS
    relasi = TeacherClass(
        id_teacher=user_id,
        id_class=kelas.id
    )

    db.session.add(relasi)

    # COMMIT SEKALI
    db.session.commit()

    return redirect(url_for('user.data_kelas'))

@user_bp.route('/gabung-kelas', methods=['POST'])
def gabung_kelas():

    # USER LOGIN (MAHASISWA)
    user_id = session.get('user_id')

    # VALIDASI LOGIN
    if not user_id:
        return redirect(url_for('user.login'))

    # AMBIL TOKEN
    token = request.form.get('token')

    if not token:
        return "Token kelas wajib diisi"

    # CARI KELAS
    kelas = Class.query.filter_by(token=token).first()

    if not kelas:
        return "Token tidak valid"

    # CEK SUDAH JOIN ATAU BELUM
    exists = StudentClass.query.filter_by(
        id_student=user_id,
        id_class=kelas.id
    ).first()

    if exists:
        return "Kamu sudah bergabung di kelas ini"

    # SIMPAN RELASI
    join = StudentClass(
        id_student=user_id,
        id_class=kelas.id,
        progress=0
    )

    db.session.add(join)
    db.session.commit()

    return redirect(url_for('user.data_kelas'))

@user_bp.route('/claim_package', methods=['POST'])
def claim_package():
    from flask import request, redirect, url_for, flash

    class_id = request.form.get('id_class')

    if not class_id:
        flash("ID Kelas tidak ditemukan.", "danger")
        return redirect(url_for('user.data_kelas'))

    class_id = int(class_id)

    # cek apakah sudah pernah di-claim
    existing = Activity.query.filter_by(id_class=class_id).first()

    if existing:
        flash("Paket pembelajaran sudah pernah diklaim.", "warning")
        return redirect(url_for('user.data_kelas'))

    # jalankan generator (semua seeder kamu)
    generate_learning_package(class_id)

    flash("Berhasil menginisiasi paket pembelajaran!", "success")

    return redirect(url_for('user.data_kelas'))

@user_bp.route('/datanilai')
def data_nilai():

    from flask import session, redirect, url_for

    # USER LOGIN
    user_id = session.get('user_id')

    # VALIDASI LOGIN
    if not user_id:
        return redirect(url_for('user.login'))

    # =========================
    # AMBIL SEMUA KELAS DOSEN
    # =========================
    classes = db.session.query(Class)\
        .join(
            TeacherClass,
            Class.id == TeacherClass.id_class
        )\
        .filter(
            TeacherClass.id_teacher == user_id
        )\
        .all()

    data = []

    for cls in classes:

        # =========================
        # TOTAL SISWA
        # =========================
        total_siswa = StudentClass.query.filter_by(
            id_class=cls.id
        ).count()

        # =========================
        # AMBIL ACTIVITY
        # =========================
        activities = Activity.query.filter(
            Activity.id_class == cls.id,
            Activity.status == 'aktif',
            Activity.type.in_(['kuis', 'evaluasi'])
        ).all()

        activity_list = []

        for act in activities:

            # =========================
            # TOTAL SISWA YANG MENGERJAKAN
            # =========================
            total = db.session.query(
                ActivityResult.id_user
            ).filter(
                ActivityResult.id_activity == act.id
            ).distinct().count()

            # =========================
            # TOPIC
            # =========================
            topic = Topic.query.get(
                act.id_topic
            )

            activity_list.append({

                "id": act.id,

                "title": (
                    topic.topic_name
                    if topic
                    else act.title
                ),

                "total": total
            })

        data.append({

            "class_name": cls.name,

            "total_activity": len(activity_list),

            "total_siswa": total_siswa,

            "activities": activity_list
        })

    return render_template(
        'dosen/datanilai.html',
        data=data
    )

@user_bp.route('/detailnilai')
def detail_nilai():

    activity_id = request.args.get('activity_id', type=int)
    user_id = request.args.get('user_id', type=int)

    if not activity_id:
        return "Activity tidak ditemukan"

    activity = Activity.query.get(activity_id)

    if not activity:
        return "Activity tidak ditemukan"

    # ambil topic & subtopic
    topic = Topic.query.get(activity.id_topic)
    subtopic = SubTopic.query.get(activity.id_subtopic)

    topic_name = topic.topic_name if topic else "-"
    subtopic_name = subtopic.sub_topic_name if subtopic else "-"

    # ====================================
    # MODE 1: MODAL (DETAIL USER)
    # ====================================
    if user_id:

        results = ActivityResult.query.filter_by(
            id_activity=activity_id,
            id_user=user_id
        ).order_by(ActivityResult.start_time.desc()).all()

        user = User.query.get(user_id)

        rows = ""

        for i, res in enumerate(results, start=1):
            tanggal = res.start_time.strftime('%d %b %Y') if res.start_time else "-"
            waktu = res.start_time.strftime('%H:%M') if res.start_time else "-"

            rows += f"""
            <tr>
                <td>{i}</td>
                <td>{tanggal}</td>
                <td>{waktu}</td>
                <td>{res.total_benar}</td>
                <td>{res.total_salah}</td>
                <td>{res.nilai_akhir}</td>
                <td>{"Ya" if res.result_status == "lulus" else "Tidak"}</td>
            </tr>
            """

        return f"""
        <h5 class="mb-1">{user.name}</h5>
        <small class="text-muted">{topic_name} - {subtopic_name}</small>

        <table class="table table-striped mt-3">
            <thead>
                <tr>
                    <th>No</th>
                    <th>Tanggal</th>
                    <th>Waktu</th>
                    <th>Benar</th>
                    <th>Salah</th>
                    <th>Nilai</th>
                    <th>Tuntas</th>
                </tr>
            </thead>
            <tbody>
                {rows if rows else '<tr><td colspan="7" class="text-center">Tidak ada data</td></tr>'}
            </tbody>
        </table>
        """

    # ====================================
    # MODE 2: HALAMAN UTAMA
    # ====================================
    results = db.session.query(ActivityResult, User)\
        .join(User, User.id == ActivityResult.id_user)\
        .filter(ActivityResult.id_activity == activity_id)\
        .order_by(ActivityResult.start_time.desc())\
        .all()

    latest_per_user = {}

    for res, user in results:
        if user.id not in latest_per_user:
            latest_per_user[user.id] = (res, user)

    data_siswa = []
    total_nilai = 0

    for res, user in latest_per_user.values():
        nilai = res.nilai_akhir or 0
        total_nilai += nilai

        if res.result_status == "lulus":
            status_label = "Lulus"
            badge = "badge-lulus"
        else:
            status_label = "Tidak Lulus"
            badge = "badge-remedial"

        data_siswa.append({
            "id_user": user.id,
            "nama": user.name,
            "nilai": nilai,
            "status": status_label,
            "badge": badge
        })

    rata = round(total_nilai / len(data_siswa), 2) if data_siswa else 0

    return render_template(
        'dosen/detailnilai.html',
        activity=activity,
        topic_name=topic_name,
        subtopic_name=subtopic_name,
        data_siswa=data_siswa,
        total_siswa=len(data_siswa),
        rata=rata,
        activity_id=activity_id
    )

@user_bp.route('/export_nilai')
def export_nilai():
    activity_id = request.args.get('activity_id', type=int)

    if not activity_id:
        return "Activity tidak ditemukan"

    activity = Activity.query.get(activity_id)

    if not activity:
        return "Activity tidak ditemukan"

    # ambil data
    results = db.session.query(User, ActivityResult)\
        .join(ActivityResult, User.id == ActivityResult.id_user)\
        .filter(ActivityResult.id_activity == activity_id)\
        .all()

    data = []

    for user, result in results:
        data.append({
            "Nama Siswa": user.name,
            "Nilai": result.nilai_akhir,
            "Status": result.result_status,
            "Total Benar": result.total_benar,
            "Total Salah": result.total_salah,
            "Durasi (detik)": result.waktu_mengerjakan
        })

    # buat dataframe
    df = pd.DataFrame(data)

    # simpan ke memory
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)

    # bikin nama file aman
    safe_title = re.sub(r'[^\w\s-]', '', activity.title).strip().replace(' ', '_')
    filename = f"nilai_mahasiswa_{safe_title}.xlsx"

    return send_file(
        output,
        download_name=filename,
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
@user_bp.route('/export_semua_nilai')
def export_semua_nilai():

    # ambil semua data (join lengkap)
    results = db.session.query(Class, Activity, User, ActivityResult)\
        .join(Activity, Activity.id_class == Class.id)\
        .join(ActivityResult, ActivityResult.id_activity == Activity.id)\
        .join(User, User.id == ActivityResult.id_user)\
        .all()

    data = []

    for kelas, activity, user, result in results:
        data.append({
            "Kelas": kelas.name,
            "Nama Aktivitas": activity.title,
            "Nama Siswa": user.name,
            "Nilai": result.nilai_akhir,
            "Status": result.result_status,
            "Total Benar": result.total_benar,
            "Total Salah": result.total_salah,
            "Durasi (detik)": result.waktu_mengerjakan
        })

    df = pd.DataFrame(data)

    # simpan ke memory
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)

    # nama file
    filename = "nilai_semua_kelas.xlsx"

    return send_file(
        output,
        download_name=filename,
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
@user_bp.route('/datasoal')
def data_soal():

    # =========================
    # AMBIL USER LOGIN
    # =========================
    user_id = session.get('user_id')

    if not user_id:
        return redirect('/login')

    # =========================
    # AMBIL KELAS MILIK GURU
    # =========================
    classes = Class.query.filter_by(
        created_by=user_id
    ).all()

    # =========================
    # CACHE TOPIC
    # =========================
    topics = {
        t.id: t.topic_name
        for t in Topic.query.all()
    }

    subtopics = {
        s.id: s.sub_topic_name
        for s in SubTopic.query.all()
    }

    data_per_class = {}

    # =========================
    # LOOP SETIAP KELAS
    # =========================
    for c in classes:

        results = db.session.query(
            Question.id,
            Question.type,
            Question.question,
            Question.MC_option,
            Question.tingkat_kesulitan,
            Activity.id_topic,
            Activity.id_subtopic
        ).join(
            ActivityQuestion,
            ActivityQuestion.id_question == Question.id
        ).join(
            Activity,
            Activity.id == ActivityQuestion.id_activity
        ).filter(
            Activity.id_class == c.id
        ).distinct().all()

        soal_list = []

        # =========================
        # LOOP SOAL
        # =========================
        for r in results:

            # -------------------------
            # PARSE QUESTION JSON
            # -------------------------
            question_text = ""
            question_image = None

            try:

                q_json = json.loads(r.question)

                question_text = q_json.get("text", "")
                question_image = q_json.get("URL")

            except:

                question_text = r.question
                question_image = None

            # -------------------------
            # BERSIHKAN HTML
            # -------------------------
            clean_text = re.sub(
                r'<br\s*/?>',
                '\n',
                question_text
            )

            clean_text = re.sub(
                r'<[^>]*>',
                '',
                clean_text
            )

            clean_text = clean_text.strip()

            # -------------------------
            # PARSE MC OPTION
            # -------------------------
            mc_options = []

            try:

                if r.mc_option:
                    mc_options = json.loads(r.mc_option)

            except:
                mc_options = []

            # -------------------------
            # TOPIC & SUBTOPIC
            # -------------------------
            topic_name = topics.get(
                r.id_topic,
                "-"
            )

            subtopic_name = subtopics.get(
                r.id_subtopic,
                "-"
            )

            # -------------------------
            # APPEND DATA
            # -------------------------
            soal_list.append({

                "id": r.id,
                "type": r.type,

                # QUESTION
                "question": clean_text,
                "question_image": question_image,

                # OPTION
                "mc_option": mc_options,

                # META
                "topic": topic_name,
                "subtopic": subtopic_name,
                "level": r.tingkat_kesulitan

            })

        # =========================
        # GROUP PER CLASS
        # =========================
        data_per_class[c.id] = {

            "nama_kelas": c.name,
            "soal": soal_list

        }

    # =========================
    # RENDER
    # =========================
    return render_template(
        'dosen/datasoal.html',
        data_per_class=data_per_class,
        classes=classes
    )

@user_bp.route('/detail_soal')
def detail_soal():

    import json

    soal_id = request.args.get('id', type=int)

    soal = Question.query.get(soal_id)

    if not soal:
        return "<div class='text-danger'>Soal tidak ditemukan</div>"

    # ===============================
    # FUNCTION FORMAT LATEX
    # ===============================
    def format_math(text):

        if not text:
            return ""

        # sudah format latex
        if "\\[" in text or "\\(" in text:
            return f"<div class='mathjax'>{text}</div>"

        latex_keywords = [
            "\\frac",
            "\\begin",
            "\\sum",
            "\\int",
            "^",
            "_"
        ]

        # auto wrap latex
        if any(k in text for k in latex_keywords):
            return f"<div class='mathjax'>\\({text}\\)</div>"

        return text

    # ===============================
    # AMBIL QUESTION
    # ===============================
    try:

        data = json.loads(soal.question)

        question_text = data.get("text", "")
        question_image = data.get("URL")

    except:

        question_text = soal.question
        question_image = None

    question_text = format_math(question_text)

    # ===============================
    # AMBIL OPSI
    # ===============================
    try:

        options_raw = json.loads(soal.MC_option)

    except:

        options_raw = []

    # ===============================
    # JAWABAN
    # ===============================
    answer = (soal.MC_Answer or "").strip()

    # ===============================
    # HTML HEADER
    # ===============================
    html = f"""
    <div class="mb-4">

        <h5 class="fw-bold mb-3">
            Pertanyaan
        </h5>

        <div class="mb-3">
            {question_text}
        </div>
    """

    # ===============================
    # GAMBAR SOAL
    # ===============================
    if question_image:

        html += f"""
        <div class="mb-3">
            <img src="{question_image}"
                 class="img-fluid rounded border"
                 style="max-height:300px;">
        </div>
        """

    html += "</div><hr>"

    # ===============================
    # RENDER OPSI
    # ===============================
    if options_raw:

        html += """
        <h5 class="fw-bold mb-3">
            Pilihan Jawaban
        </h5>
        """

        for opt in options_raw:

            huruf = list(opt.keys())[0]

            isi = opt[huruf].get("teks", "")
            gambar_opsi = opt[huruf].get("url")

            isi = format_math(isi)

            is_correct = (
                answer.lower() == huruf.lower()
            )

            html += f"""
            <div class="border rounded p-3 mb-3 {'bg-success text-white' if is_correct else ''}">

                <div class="fw-bold mb-2">
                    {huruf.upper()}.
                </div>

                <div>
                    {isi}
                </div>
            """

            # ===============================
            # GAMBAR OPSI
            # ===============================
            if gambar_opsi:

                html += f"""
                <div class="mt-3">
                    <img src="{gambar_opsi}"
                         class="img-fluid rounded border"
                         style="max-height:220px;">
                </div>
                """

            html += "</div>"

    else:

        html += """
        <div class='text-muted'>
            Tidak ada pilihan jawaban
        </div>
        """

    # ===============================
    # JAWABAN BENAR
    # ===============================
    html += f"""
    <hr>

    <div>
        <b>Jawaban Benar:</b><br>

        <span class="text-success fw-bold">
            {answer.upper()}
        </span>
    </div>
    """

    return html

@user_bp.route('/tambahsoal', methods=['GET', 'POST'])
def tambah_soal():

    from flask import request, redirect, url_for, session
    from sqlalchemy.orm import joinedload
    import json

    # USER LOGIN
    user_id = session.get('user_id')

    # VALIDASI LOGIN
    if not user_id:
        return redirect(url_for('user.login'))

    # ================= POST =================
    if request.method == 'POST':

        try:

            tipe = request.form.get('tipe')
            kesulitan = request.form.get('kesulitan')
            id_activity = request.form.get('id_activity', type=int)
            pertanyaan = request.form.get('pertanyaan')

            # VALIDASI
            if not tipe or not pertanyaan or not id_activity:
                return "Field belum lengkap!"

            # ================= VALIDASI ACTIVITY =================
            activity = db.session.query(Activity)\
                .join(
                    TeacherClass,
                    TeacherClass.id_class == Activity.id_class
                )\
                .filter(
                    Activity.id == id_activity,
                    TeacherClass.id_teacher == user_id
                ).first()

            # JIKA ACTIVITY BUKAN MILIK DOSEN
            if not activity:
                return "❌ Activity tidak valid"

            # ================= MULTIPLE CHOICE =================
            if tipe == 'mc':

                opsi = [
                    {
                        "a": {
                            "teks": request.form.get('opsi_a'),
                            "url": request.form.get('url_a')
                        }
                    },
                    {
                        "b": {
                            "teks": request.form.get('opsi_b'),
                            "url": request.form.get('url_b')
                        }
                    },
                    {
                        "c": {
                            "teks": request.form.get('opsi_c'),
                            "url": request.form.get('url_c')
                        }
                    },
                    {
                        "d": {
                            "teks": request.form.get('opsi_d'),
                            "url": request.form.get('url_d')
                        }
                    },
                    {
                        "e": {
                            "teks": request.form.get('opsi_e'),
                            "url": request.form.get('url_e')
                        }
                    }
                ]

                soal = Question(
                    type='mc',
                    question=pertanyaan,
                    MC_option=json.dumps(opsi),
                    MC_Answer=request.form.get('jawaban'),
                    tingkat_kesulitan=kesulitan,
                    created_by=user_id
                )

            # ================= ISIAN =================
            else:

                soal = Question(
                    type='isian',
                    question=pertanyaan,
                    SA_Answer=request.form.get('jawaban_isian'),
                    tingkat_kesulitan=kesulitan,
                    created_by=user_id
                )

            # SIMPAN SOAL
            db.session.add(soal)
            db.session.flush()

            # RELASI KE ACTIVITY
            relasi = ActivityQuestion(
                id_activity=id_activity,
                id_question=soal.id
            )

            db.session.add(relasi)

            # COMMIT SEKALI
            db.session.commit()

            return redirect(url_for('user.tambah_soal'))

        except Exception as e:

            db.session.rollback()
            return f"Error: {str(e)}"

    # ================= GET =================

    # HANYA ACTIVITY MILIK DOSEN
    activities = db.session.query(Activity)\
        .join(
            TeacherClass,
            TeacherClass.id_class == Activity.id_class
        )\
        .options(
            joinedload(Activity.topic),
            joinedload(Activity.subtopic)
        )\
        .filter(
            TeacherClass.id_teacher == user_id
        )\
        .all()

    return render_template(
        'dosen/kelolaSoal/tambahsoal.html',
        activities=activities
    )

# edit soal
@user_bp.route('/editsoal/<int:id>', methods=['GET', 'POST'])
def editsoal(id):
    import json
    from sqlalchemy.orm import joinedload

    try:
        soal = Question.query.get_or_404(id)
        relasi = ActivityQuestion.query.filter_by(id_question=id).first()

        # ================= POST =================
        if request.method == 'POST':

            kesulitan = request.form.get('kesulitan')
            pertanyaan = request.form.get('pertanyaan')
            id_activity = request.form.get('id_activity')

            if not pertanyaan or not id_activity:
                return "Field belum lengkap!"

            # simpan dalam JSON (FIX UTAMA)
            soal.question = json.dumps({
                "text": pertanyaan,
                "URL": None
            })

            soal.tingkat_kesulitan = kesulitan

            # ================= MC =================
            if soal.type == 'mc':
                opsi = [
                    {"a": {"teks": request.form.get('opsi_a'), "url": request.form.get('url_a')}},
                    {"b": {"teks": request.form.get('opsi_b'), "url": request.form.get('url_b')}},
                    {"c": {"teks": request.form.get('opsi_c'), "url": request.form.get('url_c')}},
                    {"d": {"teks": request.form.get('opsi_d'), "url": request.form.get('url_d')}},
                    {"e": {"teks": request.form.get('opsi_e'), "url": request.form.get('url_e')}},
                ]

                soal.MC_option = json.dumps(opsi)
                soal.MC_Answer = request.form.get('jawaban')

            # ================= ISIAN =================
            else:
                soal.SA_Answer = request.form.get('jawaban_isian')

            # update relasi
            if relasi:
                relasi.id_activity = id_activity

            db.session.commit()
            return redirect(url_for('user.data_soal'))

    except Exception as e:
        db.session.rollback()
        return f"Error: {str(e)}"

    # ================= GET =================
    activities = Activity.query.options(
        joinedload(Activity.topic),
        joinedload(Activity.subtopic)
    ).all()

    # parsing QUESTION (FIX UTAMA)
    try:
        parsed = json.loads(soal.question)
        question_text = parsed.get("text", "")
        question_url = parsed.get("URL", None)
    except:
        question_text = soal.question
        question_url = None

    # parsing opsi MC (ANTI ERROR)
    opsi_data = {
        "a": {"teks": "", "url": ""},
        "b": {"teks": "", "url": ""},
        "c": {"teks": "", "url": ""},
        "d": {"teks": "", "url": ""},
        "e": {"teks": "", "url": ""},
    }

    if soal.type == 'mc' and soal.MC_option:
        try:
            data = json.loads(soal.MC_option)
            for item in data:
                for key, val in item.items():
                    opsi_data[key] = val
        except:
            pass

    return render_template(
        'dosen/kelolaSoal/editsoal.html',
        soal=soal,
        activities=activities,
        opsi=opsi_data,
        relasi=relasi,
        question_text=question_text,
        question_url=question_url
    )

# hapus soal
@user_bp.route('/hapussoal/<int:id>')
def hapus_soal(id):
    try:
        # ambil soal
        soal = Question.query.get_or_404(id)

        # hapus relasi dulu (penting)
        ActivityQuestion.query.filter_by(id_question=id).delete()

        # hapus soal utama
        db.session.delete(soal)
        db.session.commit()

        return redirect(url_for('user.data_soal'))

    except Exception as e:
        db.session.rollback()
        return f"Error: {str(e)}"
    
    
@user_bp.route('/dataprogress')
def data_progress():

    from flask import session, redirect, url_for

    # USER LOGIN
    dosen_id = session.get('user_id')

    # VALIDASI LOGIN
    if not dosen_id:
        return redirect(url_for('user.login'))

    # AMBIL KELAS DOSEN
    kelas_list = db.session.query(Class)\
        .join(
            TeacherClass,
            TeacherClass.id_class == Class.id
        )\
        .filter(
            TeacherClass.id_teacher == dosen_id
        )\
        .all()

    kelas_ids = [k.id for k in kelas_list]

    # JIKA DOSEN BELUM PUNYA KELAS
    if not kelas_ids:
        return render_template(
            'dosen/dataprogress.html',
            data=[],
            kelas_list=[]
        )

    # QUERY DATA PROGRESS
    data = db.session.query(
        User.id,
        User.name.label("user_name"),
        Class.name.label("kelas_name"),
        db.func.coalesce(
            Progress.progres_value,
            0
        ).label("progres_value")
    )\
    .join(
        StudentClass,
        User.id == StudentClass.id_student
    )\
    .join(
        Class,
        StudentClass.id_class == Class.id
    )\
    .outerjoin(
        Progress,
        User.id == Progress.id_user
    )\
    .filter(
        User.role == 'Student',
        StudentClass.id_class.in_(kelas_ids)
    )\
    .all()

    return render_template(
        'dosen/dataprogress.html',
        data=data,
        kelas_list=kelas_list
    )
# modal detail progress
@user_bp.route('/progress-detail/<int:user_id>')
def progress_detail(user_id):

    data = db.session.query(
        HistoryProgress.id_topic,
        HistoryProgress.id_subtopic,
        HistoryProgress.updated_at,
        Topic.topic_name,
        SubTopic.sub_topic_name
    ).join(
        Topic, HistoryProgress.id_topic == Topic.id
    ).join(
        SubTopic, HistoryProgress.id_subtopic == SubTopic.id
    ).filter(
        HistoryProgress.id_user == user_id
    ).order_by(
        HistoryProgress.id_topic.asc(),
        HistoryProgress.id_subtopic.asc()
    ).all()

    result = []
    for d in data:
        result.append({
            "topic": d.topic_name,
            "subtopic": d.sub_topic_name,
            "tanggal": d.updated_at.strftime("%d-%m-%Y %H:%M")
        })

    return jsonify(result)

@user_bp.route('/dataaktivitas')
def data_aktivitas():

    from flask import session, redirect, url_for

    # USER LOGIN
    user_id = session.get('user_id')

    # VALIDASI LOGIN
    if not user_id:
        return redirect(url_for('user.login'))

    # AMBIL KELAS DOSEN
    classes = db.session.query(Class)\
        .join(
            TeacherClass,
            TeacherClass.id_class == Class.id
        )\
        .filter(
            TeacherClass.id_teacher == user_id
        )\
        .all()

    # TOPIC & SUBTOPIC
    topics = Topic.query.all()
    subtopics = SubTopic.query.all()

    data_per_class = {}

    for c in classes:

        # AMBIL ACTIVITY PER KELAS
        activities = db.session.query(
            Activity.id,
            Activity.title,
            Activity.type,
            Activity.status,
            Activity.durasi_pengerjaan,
            Activity.id_topic,
            Activity.id_subtopic,
            Topic.topic_name
        )\
        .join(
            Topic,
            Topic.id == Activity.id_topic
        )\
        .filter(
            Activity.id_class == c.id
        )\
        .all()

        aktivitas_list = []

        for a in activities:

            aktivitas_list.append({
                "id": a.id,
                "title": a.title,
                "type": a.type,
                "status": a.status,
                "topic": a.topic_name,
                "durasi_pengerjaan": a.durasi_pengerjaan,
                "id_topic": a.id_topic,
                "id_subtopic": a.id_subtopic
            })

        data_per_class[c.id] = {
            "nama_kelas": c.name,
            "semester": c.semester,
            "tahun": c.tahun,
            "data": aktivitas_list
        }

    return render_template(
        'dosen/dataaktivitas.html',
        data_per_class=data_per_class,
        topics=topics,
        subtopics=subtopics
    )
    
@user_bp.route('/update-status-aktivitas', methods=['POST'])
def update_status_aktivitas():
    data = request.get_json()

    aktivitas_id = data.get('id')
    status = data.get('status')  # 'aktif' / 'tidak aktif'

    # validasi sederhana
    if status not in ['aktif', 'tidak aktif']:
        return jsonify({"success": False, "message": "Status tidak valid"})

    aktivitas = Activity.query.get(aktivitas_id)

    if not aktivitas:
        return jsonify({"success": False, "message": "Data tidak ditemukan"})

    aktivitas.status = status
    db.session.commit()

    return jsonify({"success": True})

@user_bp.route('/update-aktivitas', methods=['POST'])
def update_aktivitas():

    data = request.get_json()

    # VALIDASI WAJIB
    if not data:
        return jsonify({
            "success": False,
            "message": "No data"
        }), 400

    aktivitas = Activity.query.get(data.get('id'))

    if not aktivitas:
        return jsonify({
            "success": False,
            "message": "Aktivitas tidak ditemukan"
        }), 404

    try:

        # ====================================
        # TYPE
        # ====================================
        if data.get('type') in [
            'aktivitas',
            'kuis',
            'evaluasi'
        ]:
            aktivitas.type = data.get('type')

        # ====================================
        # DURASI
        # ====================================
        durasi = data.get('durasi')

        if durasi == "" or durasi is None:
            aktivitas.durasi_pengerjaan = None
        else:
            aktivitas.durasi_pengerjaan = int(durasi)

        # ====================================
        # TOPIC
        # ====================================
        if data.get('topic'):
            aktivitas.id_topic = int(
                data.get('topic')
            )

        # ====================================
        # SUBTOPIC
        # ====================================
        if data.get('subtopic'):
            aktivitas.id_subtopic = int(
                data.get('subtopic')
            )

        # ====================================
        # STATUS
        # ====================================
        if data.get('status') in [
            'aktif',
            'tidak aktif'
        ]:
            aktivitas.status = data.get('status')

        # ====================================
        # AUTO HITUNG JUMLAH SOAL
        # ====================================
        jumlah = db.session.query(
            ActivityQuestion
        ).filter_by(
            id_activity=aktivitas.id
        ).count()

        aktivitas.jumlah_soal = jumlah

        # ====================================
        # SAVE
        # ====================================
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Berhasil update",
            "jumlah_soal": jumlah
        })

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
        
#render keseluruhan soal aktivitas pada halaman guru berdasarkan id activity
@user_bp.route('/get-soal-guru/<int:id>')
def get_soal_guru(id):

    soal = db.session.query(Question).join(
        ActivityQuestion,
        ActivityQuestion.id_question == Question.id
    ).filter(
        ActivityQuestion.id_activity == id
    ).all()

    html = ""

    if not soal:
        return """
        <div class='text-center text-muted'>
            Tidak ada soal
        </div>
        """

    # =========================================
    # FUNCTION FORMAT LATEX
    # =========================================
    def format_math(text):

        if not text:
            return ""

        if "\\[" in text or "\\(" in text:
            return f"<div class='mathjax'>{text}</div>"

        latex_keywords = [
            "\\frac",
            "\\begin",
            "\\sum",
            "\\int",
            "^",
            "_"
        ]

        if any(k in text for k in latex_keywords):
            return f"<div class='mathjax'>\\({text}\\)</div>"

        return text

    # =========================================
    # LOOP SOAL
    # =========================================
    for i, s in enumerate(soal, start=1):

        # =========================================
        # PARSE QUESTION
        # =========================================
        try:

            q = json.loads(s.question)

            question_text = q.get("text", "")
            question_image = q.get("URL")

        except:

            question_text = s.question
            question_image = None

        question_text = format_math(question_text)

        # =========================================
        # PARSE OPTIONS
        # =========================================
        try:

            options = json.loads(s.MC_option) if s.MC_option else []

        except:

            options = []

        # =========================================
        # HEADER CARD
        # =========================================
        html += f"""
        <div class="card mb-4 shadow-sm border-0">

            <div class="card-body">

                <div class="d-flex justify-content-between align-items-center mb-3">

                    <h6 class="fw-bold mb-0">
                        Soal {i}
                    </h6>

                    <span class="badge bg-primary">
                        {s.type.upper()}
                    </span>

                </div>

                <div class="mb-3">
                    {question_text}
                </div>
        """

        # =========================================
        # GAMBAR SOAL
        # =========================================
        if question_image:

            html += f"""
            <div class="mb-3">
                <img src="{question_image}"
                     class="img-fluid rounded border"
                     style="max-height:320px;">
            </div>
            """

        # =========================================
        # PILIHAN GANDA
        # =========================================
        if isinstance(options, list) and options:

            html += """
            <div class="mt-4">
            """

            for item in options:

                for key, val in item.items():

                    text = val.get("teks", "")
                    image = val.get("url")

                    text = format_math(text)

                    is_answer = (
                        str(key).lower()
                        ==
                        str(s.MC_Answer).lower()
                    )

                    active = (
                        "bg-success text-white border-success"
                        if is_answer
                        else
                        ""
                    )

                    html += f"""
                    <div class="border rounded p-3 mb-3 {active}">

                        <div class="fw-bold mb-2">
                            {key.upper()}.
                        </div>

                        <div>
                            {text}
                        </div>
                    """

                    # =========================================
                    # GAMBAR OPSI
                    # =========================================
                    if image:

                        html += f"""
                        <div class="mt-3">
                            <img src="{image}"
                                 class="img-fluid rounded border"
                                 style="max-height:220px;">
                        </div>
                        """

                    html += "</div>"

            html += "</div>"

        # =========================================
        # SOAL ISIAN
        # =========================================
        else:

            jawaban = s.SA_Answer or "-"

            html += f"""
            <div class="alert alert-success mt-3">

                <b>Jawaban:</b><br>

                {jawaban}

            </div>
            """

        # =========================================
        # PENUTUP CARD
        # =========================================
        html += """
            </div>
        </div>
        """

    return html

@user_bp.route('/aturaktivitas/<int:id>')
def atur_aktivitas(id):
    import json
    import re

    # 🔹 ambil relasi activity -> question (yang sudah dipilih)
    aq = db.session.query(ActivityQuestion.id_question).filter(
        ActivityQuestion.id_activity == id
    ).all()

    question_ids = [q.id_question for q in aq]

    # 🔹 ambil soal yang SUDAH TERPILIH
    soal_list = []

    if question_ids:
        results = db.session.query(
            Question.id,
            Question.type,
            Question.question,
            Question.tingkat_kesulitan
        ).filter(
            Question.id.in_(question_ids)
        ).all()

        for r in results:
            try:
                raw = json.loads(r.question).get("text", "")
            except:
                raw = r.question

            clean = re.sub(r'<br\s*/?>', '\n', raw)
            clean = re.sub(r'<[^>]*>', '', clean).strip()

            soal_list.append({
                "id": r.id,
                "type": "MultipleChoice" if r.type == "mc" else "Isian",
                "question": clean,
                "level": r.tingkat_kesulitan
            })

    # ambil SEMUA soal (untuk modal)
    all_results = db.session.query(
        Question.id,
        Question.type,
        Question.question,
        Question.tingkat_kesulitan
    ).all()

    all_soal = []

    for r in all_results:
        try:
            raw = json.loads(r.question).get("text", "")
        except:
            raw = r.question

        clean = re.sub(r'<br\s*/?>', '\n', raw)
        clean = re.sub(r'<[^>]*>', '', clean).strip()

        all_soal.append({
            "id": r.id,
            "type": "MultipleChoice" if r.type == "mc" else "Isian",
            "question": clean,
            "level": r.tingkat_kesulitan
        })

    # ID yang sudah dipilih
    selected_ids = [s["id"] for s in soal_list]

    # 🔹 statistik
    total = len(soal_list)
    mudah = len([s for s in soal_list if s['level'] == 'mudah'])
    sedang = len([s for s in soal_list if s['level'] == 'sedang'])
    sulit = len([s for s in soal_list if s['level'] == 'sulit'])

    return render_template(
        'dosen/kelolaAktivitas/aturaktivitas.html',
        soal_list=soal_list,        # atas (terpilih)
        all_soal=all_soal,          # modal (semua soal)
        selected_ids=selected_ids,  # penanda tombol
        total=total,
        mudah=mudah,
        sedang=sedang,
        sulit=sulit
    )
    
@user_bp.route('/simpan_soal', methods=['POST'])
def simpan_soal():
    data = request.get_json()

    id_activity = data.get('id_activity')
    soal_ids = data.get('soal_ids')

    for qid in soal_ids:

        # cek apakah sudah ada
        exists = ActivityQuestion.query.filter_by(
            id_activity=id_activity,
            id_question=qid
        ).first()

        if not exists:
            new_rel = ActivityQuestion(
                id_activity=id_activity,
                id_question=qid
            )
            db.session.add(new_rel)

    db.session.commit()

    return {"status": "success"}
    
@user_bp.route('/hapus_semua_soal/<int:id>', methods=['POST'])
def hapus_semua_soal(id):

    ActivityQuestion.query.filter_by(id_activity=id).delete()
    db.session.commit()

    return {"status": "success"}


@user_bp.route('/settings-kelas')
def settings_kelas():

    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    classes = Class.query.filter_by(
        created_by=user_id
    ).all()

    settings_data = []

    for kelas in classes:

        setting = Setting.query.filter_by(
            id_class=kelas.id
        ).first()

        # otomatis buat setting jika belum ada
        if not setting:

            setting = Setting(
                id_class=kelas.id,
                nilai_kkm_kuis=70,
                nilai_kkm_evaluasi=75
            )

            db.session.add(setting)
            db.session.commit()

        settings_data.append({
            'id_class': kelas.id,
            'nama_kelas': kelas.name,
            'nilai_kkm_kuis': setting.nilai_kkm_kuis,
            'nilai_kkm_evaluasi': setting.nilai_kkm_evaluasi
        })

    return render_template(
        'dosen/settings_kelas.html',
        settings_data=settings_data
    )
    
@user_bp.route('/update-settings-kelas', methods=['POST'])
def update_settings_kelas():

    id_class = request.form.get('id_class')

    nilai_kkm_kuis = request.form.get('nilai_kkm_kuis')
    nilai_kkm_evaluasi = request.form.get('nilai_kkm_evaluasi')

    setting = Setting.query.filter_by(
        id_class=id_class
    ).first()

    if not setting:

        setting = Setting(
            id_class=id_class
        )

        db.session.add(setting)

    setting.nilai_kkm_kuis = nilai_kkm_kuis
    setting.nilai_kkm_evaluasi = nilai_kkm_evaluasi

    db.session.commit()

    flash('Setting berhasil diperbarui!', 'success')

    return redirect(
        url_for('user.settings_kelas')
    )

#eksperimen praktek

# =========================================
# FOLDER SETUP
# =========================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "..", "uploads")
RESULT_FOLDER = os.path.join(BASE_DIR, "..", "static", "results")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# =========================================
# RUN PYTHON CODE
# =========================================
@user_bp.route("/run-code", methods=["POST"])
def run_code():

    data = request.get_json()

    code = data.get("code", "")
    image_path = data.get("image_path", "")

    # =====================================
    # DEFAULT IMAGE
    # =====================================
    if not image_path:
        image_path = os.path.join(
            UPLOAD_FOLDER,
            "bunga.jpg"
        )

    output = ""
    output_image = None

    try:

        before_files = set(
            os.listdir(RESULT_FOLDER)
        )

        # =====================================
        # INJECT VARIABLE KE USER CODE
        # =====================================
        injected_code = f"""
# pindah working directory ke uploads
import os
os.chdir(r'''{UPLOAD_FOLDER}''')

# variable bawaan
image_path = r'''{image_path}'''
output_dir = r'''{RESULT_FOLDER}'''

# =====================================
# USER CODE
# =====================================
{code}
"""

        # =====================================
        # TEMP PYTHON FILE
        # =====================================
        temp_name = f"{uuid.uuid4()}.py"

        temp_path = os.path.join(
            tempfile.gettempdir(),
            temp_name
        )

        with open(
            temp_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(injected_code)

        # =====================================
        # RUN PROCESS
        # =====================================
        result = subprocess.run(
            ["python", temp_path],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=current_app.root_path
        )

        output = result.stdout + result.stderr

        # =====================================
        # HAPUS TEMP FILE
        # =====================================
        if os.path.exists(temp_path):
            os.remove(temp_path)

        # =====================================
        # DETEKSI FILE GAMBAR TERBARU
        # =====================================
        image_files = []

        for file in os.listdir(RESULT_FOLDER):

            if file.lower().endswith(
                (
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".bmp"
                )
            ):

                full_path = os.path.join(
                    RESULT_FOLDER,
                    file
                )

                image_files.append(
                    (
                        file,
                        os.path.getmtime(full_path)
                    )
                )

        # =====================================
        # AMBIL FILE TERBARU
        # =====================================
        if image_files:

            image_files.sort(
                key=lambda x: x[1],
                reverse=True
            )

            output_image = image_files[0][0]

        # =====================================
        # RESPONSE
        # =====================================
        return jsonify({

            "output": output,

            "before_image":
                url_for(
                    "user.uploaded_file",
                    filename=os.path.basename(image_path)
                ),

            "after_image":
                url_for(
                    "user.serve_results",
                    filename=output_image
                ) if output_image else None
        })

    except Exception as e:

        return jsonify({

            "output": f"Server Error:\\n{str(e)}",

            "before_image":
                url_for(
                    "user.uploaded_file",
                    filename=os.path.basename(image_path)
                ),

            "after_image": None
        })
# =========================================
# UPLOAD IMAGE
# =========================================
@user_bp.route("/upload-image", methods=["POST"])
def upload_image():

    if "image" not in request.files:

        return jsonify({
            "error": "No image uploaded"
        }), 400

    file = request.files["image"]

    if file.filename == "":

        return jsonify({
            "error": "Empty filename"
        }), 400

    filename = file.filename

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(filepath)

    return jsonify({

        "filename": filename,

        "path": filepath
    })


# =========================================
# SERVE UPLOADED IMAGE
# =========================================
@user_bp.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )


# =========================================
# SERVE RESULT IMAGE
# =========================================
@user_bp.route("/static/results/<filename>")
def serve_results(filename):

    return send_from_directory(
        RESULT_FOLDER,
        filename
    )
    
    
