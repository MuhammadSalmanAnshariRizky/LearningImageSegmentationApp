import random
from datetime import datetime, timedelta
from app import db
from app.model.activity import Activity
from app.model.activity_result import ActivityResult
from app.model.user import User
from app.model.subtopic import SubTopic

def seed_activity_result():
    # 🎯 Ambil semua user dengan role Student
    students = User.query.filter_by(role='Student').all()
    
    # 🎯 Ambil activity kuis & evaluasi, urutkan berdasarkan ID agar alur belajarnya urut
    activities = Activity.query.filter(Activity.id.in_([3, 6, 10, 14, 18, 19])).order_by(Activity.id.asc()).all()
    
    # Mapping: ID Aktivitas -> ID Subtopic terkait
    activity_subtopic_map = {
        3: 4, 6: 8, 10: 13, 14: 14, 18: 15, 19: 16
    }

    if not students or not activities:
        print("❌ Data Student atau Activity tidak ditemukan")
        return

    data_to_insert = []
    
    # Ambil semua subtopic untuk menghitung batas progres
    all_subtopics = SubTopic.query.order_by(SubTopic.id.asc()).all()
    total_sub = len(all_subtopics)

    for index, student in enumerate(students):
        # 1. Tentukan batas progres siswa (Samakan dengan logika seed_progress_history)
        if index == 0:
            jumlah_history = total_sub # Siswa pertama 100%
        else:
            jumlah_history = random.randint(5, total_sub) 
            
        # ID subtopik terakhir yang dicapai
        max_subtopic_id = all_subtopics[jumlah_history - 1].id if jumlah_history > 0 else 0

        # 2. Looping aktivitas
        for activity in activities:
            # GATE 1: Apakah siswa sudah mencapai subtopik yang dibutuhkan?
            required_subtopic = activity_subtopic_map.get(activity.id, 0)
            
            if max_subtopic_id < required_subtopic:
                # Progres belum sampai, jangan buat record hasil
                continue

            # Cek apakah data sudah ada
            existing = ActivityResult.query.filter_by(
                id_user=student.id,
                id_activity=activity.id,
                percobaan_ke=1 
            ).first()

            if existing:
                # Jika sudah ada, kita tetap harus cek statusnya untuk logika "Tidak Lulus"
                status_terakhir = existing.result_status
            else:
                # 3. Buat data baru
                total_soal = getattr(activity, 'jumlah_soal', 10)
                benar = random.randint(int(total_soal * 0.4), total_soal)
                salah = total_soal - benar
                nilai = (benar / total_soal) * 100
                waktu = random.randint(300, 1200)

                start_time = datetime.now() - timedelta(minutes=random.randint(10, 60))
                end_time = start_time + timedelta(seconds=waktu)

                status_terakhir = "lulus" if nilai >= 60 else "tidak lulus"

                new_result = ActivityResult(
                    id_user=student.id,
                    id_activity=activity.id,
                    percobaan_ke=1,
                    nilai_akhir=round(nilai, 2),
                    result_status=status_terakhir,
                    waktu_mengerjakan=waktu,
                    start_time=start_time,
                    end_time=end_time,
                    total_benar=benar,
                    total_salah=salah
                )
                data_to_insert.append(new_result)
                # Tambahkan ke DB session sementara untuk pengecekan berikutnya
                db.session.add(new_result)
                db.session.flush() # Agar id tersedia untuk pengecekan/relasi

            # GATE 2: Jika siswa tidak lulus, hentikan aktivitas selanjutnya untuk siswa ini
            if status_terakhir == "tidak lulus":
                break 

    # Eksekusi insert massal
    if data_to_insert:
        db.session.commit()
        print(f"✅ Seeder ActivityResult berhasil! Data diselaraskan dengan progres siswa.")
    else:
        print("⚠️ Tidak ada data baru atau siswa belum mencapai subtopik yang diperlukan.")