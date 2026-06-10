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
        2: [21, 24, 28, 32, 36, 37]       # Kelas 2
    }
    
    # Gabung semua valid ID untuk ditarik dari database sekaligus
    all_valid_ids = class_activity_ids[1] + class_activity_ids[2]
    activities_pool = Activity.query.filter(Activity.id.in_(all_valid_ids)).all()
    
    # Ubah menjadi dictionary agar gampang dicari & langsung pakai id_subtopic bawaan db
    activities_dict = {act.id: act for act in activities_pool}

    student_classes = StudentClass.query.all()
    student_to_class = {sc.id_student: sc.id_class for sc in student_classes}

    all_subtopics = SubTopic.query.order_by(SubTopic.id.asc()).all()
    total_sub = len(all_subtopics)

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
        
        # Tentukan batas progres simulasi siswa
        if index == 0:
            jumlah_history = total_sub # Siswa pertama 100% tembus sampai akhir
        else:
            jumlah_history = random.randint(5, total_sub) 
            
        max_subtopic_id = all_subtopics[jumlah_history - 1].id if jumlah_history > 0 else 0

        # 🎯 4. Looping aktivitas
        for act_id in valid_activity_ids:
            activity = activities_dict.get(act_id)
            if not activity:
                continue

            # FIX: Ambil langsung dari tabel Activity, bukan dari map manual!
            required_subtopic = activity.id_subtopic
            
            # GATE 1: Pengecekan Progres Berlapis
            if required_subtopic > max_subtopic_id:
                # Jika subtopik kuis ini lebih besar dari batas progres siswa, hentikan eksekusi
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
                # Jika progres siswa sudah melampaui kuis ini (required_subtopic < max_subtopic_id),
                # mustahil dia tidak lulus. Jadi kita paksa "Lulus" (minimal nilai 60).
                if required_subtopic < max_subtopic_id:
                    benar = random.randint(int(total_soal * 0.6), total_soal) 
                else:
                    # Jika kuis ini adalah pemberhentian terakhirnya, nilainya bisa Lulus / Tidak Lulus
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
                db.session.flush()

            # GATE 2: Anti-Bocor
            if status_terakhir == "tidak lulus":
                # Jika siswa gagal di kuis ini, pastikan dia TIDAK BISA lanjut mengerjakan kuis berikutnya
                break 

    if data_to_insert:
        db.session.commit()
        print(f"✅ Seeder ActivityResult sukses! Progres terjamin tidak bocor.")
    else:
        print("⚠️ Tidak ada data baru yang ditambahkan.")