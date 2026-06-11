import random
from datetime import datetime, timedelta
from app import db
from app.model.activity import Activity
from app.model.activity_result import ActivityResult
from app.model.user import User
from app.model.subtopic import SubTopic
from app.model.student_class import StudentClass  

def seed_activity_result():
    # 🎯 1. Ambil semua user dengan role Student
    students = User.query.filter_by(role='Student').all()
    
    # 🎯 2. Definisikan ID Activity berdasarkan Kelas
    class_activity_ids = {
        1: [3, 6, 10, 14, 18, 19],        # Kelas 1
        2: [22, 25, 29, 33, 37, 38]       # Kelas 2
    }
    
    # Gabung semua valid ID untuk ditarik dari database sekaligus
    all_valid_ids = class_activity_ids[1] + class_activity_ids[2]
    activities_pool = Activity.query.filter(Activity.id.in_(all_valid_ids)).all()
    
    # Ubah menjadi dictionary agar gampang dicari
    activities_dict = {act.id: act for act in activities_pool}

    student_classes = StudentClass.query.all()
    student_to_class = {sc.id_student: sc.id_class for sc in student_classes}

    if not students or not activities_pool:
        print("❌ Data Student atau Activity tidak ditemukan")
        return

    data_to_insert = []
    
    # 🎯 3. Looping data siswa
    for index, student in enumerate(students):
        kelas_id = student_to_class.get(student.id)
        if not kelas_id:
            continue
            
        valid_activity_ids = class_activity_ids.get(kelas_id, [])
        if not valid_activity_ids:
            continue

        # 🚀 PERBAIKAN DI SINI: Cari subtopik yang relevan HANYA untuk kelas siswa ini
        current_class_activities = [activities_dict[aid] for aid in valid_activity_ids if aid in activities_dict]
        if not current_class_activities:
            continue
            
        # Ambil semua daftar id_subtopic unik untuk kelas ini dan urutkan
        class_subtopic_ids = sorted(list(set(act.id_subtopic for act in current_class_activities)))
        total_sub_kelas = len(class_subtopic_ids)

        # Tentukan batas progres simulasi siswa berdasarkan subtopik kelasnya sendiri
        if index == 0:
            # Siswa pertama dijamin lulus semua kuis di kelasnya
            max_subtopic_id = class_subtopic_ids[-1] 
        else:
            # Siswa lain akan berhenti di subtopik acak khusus di kelas mereka (misal dari subtopik ke-1 sampai terakhir kelas itu)
            dapat_kuis_ke = random.randint(1, total_sub_kelas)
            max_subtopic_id = class_subtopic_ids[dapat_kuis_ke - 1]

        # 🎯 4. Looping aktivitas sesuai kelas siswa
        for act_id in valid_activity_ids:
            activity = activities_dict.get(act_id)
            if not activity:
                continue

            required_subtopic = activity.id_subtopic
            
            # GATE 1: Pengecekan Progres Berlapis
            if required_subtopic > max_subtopic_id:
                # Jika subtopik kuis ini melampaui batas batas acak siswa, lewati kuis ini dan setelahnya
                continue

            existing = ActivityResult.query.filter_by(
                id_user=student.id,
                id_activity=activity.id,
                percobaan_ke=1 
            ).first()

            if existing:
                status_terakhir = existing.result_status
            else:
                total_soal = getattr(activity, 'jumlah_soal', 10)
                
                # LOGIKA REALISTIS:
                # Jika kuis ini berada di bawah batas maksimalnya, dia dipaksa lulus
                if required_subtopic < max_subtopic_id:
                    benar = random.randint(int(total_soal * 0.6), total_soal) 
                else:
                    # Jika kuis ini adalah batas maksimalnya, buat nilainya random (bisa lulus / gagal)
                    benar = random.randint(int(total_soal * 0.3), total_soal)
                    
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

            # GATE 2: Anti-Bocor
            if status_terakhir == "tidak lulus":
                # Jika terhenti karena tidak lulus, kuis berikutnya otomatis tidak dikerjakan
                break 

    if data_to_insert:
        db.session.commit()
        print(f"✅ Seeder ActivityResult sukses! Data Kelas 1 dan Kelas 2 sekarang bervariasi proporsional.")
    else:
        print("⚠️ Tidak ada data baru yang ditambahkan.")