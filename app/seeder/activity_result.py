import random
from datetime import datetime, timedelta
from app import db
from app.model.activity import Activity
from app.model.activity_result import ActivityResult
from app.model.user import User

def seed_activity_result():
    # 🎯 Ambil semua user dengan role Student
    students = User.query.filter_by(role='Student').all()

    # 🎯 Ambil activity kuis & evaluasi (ID: 3, 6, 10, 14, 18, 19)
    activities = Activity.query.filter(Activity.id.in_([3, 6, 10, 14, 18, 19])).all()

    if not students or not activities:
        print("❌ Data Student atau Activity tidak ditemukan")
        return

    data_to_insert = []

    # Looping untuk setiap siswa
    for student in students:
        # Looping untuk setiap aktivitas
        for activity in activities:

            # 🔥 CEK biar tidak double (Pengecekan spesifik ke percobaan 1)
            existing = ActivityResult.query.filter_by(
                id_user=student.id,
                id_activity=activity.id,
                percobaan_ke=1 
            ).first()

            if existing:
                continue

            # 🔢 Jumlah soal (default 10 kalau tidak ada field)
            total_soal = getattr(activity, 'jumlah_soal', 10)

            # 🎯 Hasil realistis (Misal: minimal betul 40% sampai 100%)
            benar = random.randint(int(total_soal * 0.4), total_soal)
            salah = total_soal - benar

            # 💯 Nilai
            nilai = (benar / total_soal) * 100

            # ⏱ Waktu (5–20 menit)
            waktu = random.randint(300, 1200)

            start_time = datetime.now() - timedelta(minutes=random.randint(10, 60))
            end_time = start_time + timedelta(seconds=waktu)

            # 📊 Status kelulusan (KKM default 60)
            status = "lulus" if nilai >= 60 else "tidak lulus"

            result = ActivityResult(
                id_user=student.id,
                id_activity=activity.id,
                percobaan_ke=1, # WAJIB DIISI karena tabel sudah diupdate
                nilai_akhir=round(nilai, 2),
                result_status=status,
                waktu_mengerjakan=waktu,
                start_time=start_time,
                end_time=end_time,
                total_benar=benar,
                total_salah=salah
            )

            data_to_insert.append(result)

    if not data_to_insert:
        print("⚠️ Semua data ActivityResult sudah ada, skip")
        return

    # Eksekusi insert massal agar lebih cepat
    db.session.add_all(data_to_insert)
    db.session.commit()
    
    print(f"✅ Seeder ActivityResult berhasil! Data ditambahkan untuk {len(students)} siswa pada aktivitas [3, 6, 10, 14, 18, 19].")