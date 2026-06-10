import random
from datetime import datetime, timedelta
from app import db
from app.model.activity import Activity
from app.model.activity_result import ActivityResult
from app.model.user import User
from app.model.subtopic import SubTopic
from app.model.student_class import StudentClass  # Pastikan di-import untuk cek kelas siswa

def seed_activity_result():
    # 🎯 1. Ambil semua user dengan role Student
    students = User.query.filter_by(role='Student').all()
    
    # 🎯 2. Definisikan ID Activity berdasarkan Kelas
    class_activity_ids = {
        1: [3, 6, 10, 14, 18, 19],        # ID Activity untuk Kelas 1
        2: [21, 24, 28, 32, 36, 37]       # ID Activity untuk Kelas 2 (Sesuai database kamu)
    }
    
    # 🎯 3. Mapping: ID Aktivitas (Kedua Kelas) -> ID Subtopic terkait
    # Urutan subtopik milestone: Kuis-1 (4), Kuis-2 (8), Kuis-3 (13), Aktivitas 8 (14), Aktivitas 9 (15), Aktivitas 10 (16)
    activity_subtopic_map = {
        # Kelas 1
        3: 4, 6: 8, 10: 13, 14: 14, 18: 15, 19: 16,
        # Kelas 2
        21: 4, 24: 8, 28: 13, 32: 14, 36: 15, 37: 16
    }

    # Ambil semua ID aktivitas yang digabung dari Kelas 1 dan Kelas 2
    all_valid_ids = class_activity_ids[1] + class_activity_ids[2]
    activities_pool = Activity.query.filter(Activity.id.in_(all_valid_ids)).all()
    
    # Ubah menjadi dictionary pool agar pencarian object di dalam loop lebih cepat (menghemat query)
    activities_dict = {act.id: act for act in activities_pool}

    # Ambil data kelas semua siswa sekaligus
    student_classes = StudentClass.query.all()
    student_to_class = {sc.id_student: sc.id_class for sc in student_classes}

    # Ambil semua subtopic untuk menghitung batas progres
    all_subtopics = SubTopic.query.order_by(SubTopic.id.asc()).all()
    total_sub = len(all_subtopics)

    if not students or not activities_pool:
        print("❌ Data Student atau Activity tidak ditemukan")
        return

    data_to_insert = []
    
    # 🎯 4. Looping data siswa
    for index, student in enumerate(students):
        # Dapatkan ID kelas si siswa
        kelas_id = student_to_class.get(student.id)
        if not kelas_id:
            continue  # Lewati jika siswa tidak terdaftar di kelas manapun
            
        # Ambil daftar ID aktivitas yang sah khusus untuk kelas siswa ini
        valid_activity_ids = class_activity_ids.get(kelas_id, [])
        
        # Tentukan batas progres simulasi siswa
        if index == 0:
            jumlah_history = total_sub # Siswa pertama disimulasikan lulus 100%
        else:
            jumlah_history = random.randint(5, total_sub) 
            
        # ID subtopik terakhir yang dicapai
        max_subtopic_id = all_subtopics[jumlah_history - 1].id if jumlah_history > 0 else 0

        # 🎯 5. Looping aktivitas secara runtut sesuai urutan ID Kelasnya
        for act_id in valid_activity_ids:
            activity = activities_dict.get(act_id)
            if not activity:
                continue

            # GATE 1: Apakah siswa sudah mencapai subtopik yang dibutuhkan?
            required_subtopic = activity_subtopic_map.get(activity.id, 0)
            
            if max_subtopic_id < required_subtopic:
                # Progres belum sampai, jangan buat record hasil
                continue

            # Cek apakah data hasil sudah ada di database
            existing = ActivityResult.query.filter_by(
                id_user=student.id,
                id_activity=activity.id,
                percobaan_ke=1 
            ).first()

            if existing:
                status_terakhir = existing.result_status
            else:
                # 🎯 6. Buat data hasil baru
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
                db.session.add(new_result)
                db.session.flush() # Amankan instance ID ke session

            # GATE 2: Jika siswa tidak lulus, patahkan loop agar tidak mengerjakan aktivitas berikutnya
            if status_terakhir == "tidak lulus":
                break 

    # Eksekusi simpan data massal ke database
    if data_to_insert:
        db.session.commit()
        print(f"✅ Seeder ActivityResult sukses! Data Kelas 1 & Kelas 2 telah disinkronkan.")
    else:
        print("⚠️ Tidak ada data baru yang ditambahkan.")