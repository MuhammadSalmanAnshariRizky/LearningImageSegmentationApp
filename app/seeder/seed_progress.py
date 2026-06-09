import random
from datetime import datetime
from app import db
from app.model.progress import Progress
from app.model.historyprogress import HistoryProgress
from app.model.activity_result import ActivityResult
from app.model.subtopic import SubTopic
from app.model.user import User

def seed_progress_history():
    # 1. Ambil semua siswa
    students = User.query.filter_by(role='Student').all()
    if not students:
        print("❌ Data student belum ada!")
        return

    # 2. Ambil semua subtopic
    all_subtopics = SubTopic.query.order_by(SubTopic.id.asc()).all()
    if not all_subtopics:
        print("❌ Subtopic belum ada!")
        return
    
    total_sub = len(all_subtopics)

    # Mapping: ID Aktivitas -> ID Subtopic terkait
    # SESUAIKAN ID ini dengan data di database Anda
    activity_subtopic_map = {
        3: 4, 
        6: 8, 
        10: 13, 
        14: 14, 
        18: 15, 
        19: 16
    }

    # 3. Reset data lama
    Progress.query.delete()
    HistoryProgress.query.delete()
    db.session.commit()

    # 4. Loop untuk setiap student
    for student in students:
        # Ambil hasil aktivitas siswa, urutkan berdasarkan ID aktivitas (sesuai urutan belajar)
        results = ActivityResult.query.filter_by(id_user=student.id)\
                                      .order_by(ActivityResult.id_activity.asc()).all()
        
        # Tentukan batas akhir subtopik yang bisa diakses
        max_subtopic_id = 0
        
        for res in results:
            if res.id_activity in activity_subtopic_map:
                if res.result_status == 'lulus':
                    # Jika lulus, update batas max subtopik ke subtopik aktivitas ini
                    max_subtopic_id = activity_subtopic_map[res.id_activity]
                else:
                    # Jika tidak lulus, progres berhenti tepat di aktivitas ini (break)
                    max_subtopic_id = activity_subtopic_map[res.id_activity]
                    break 

        # Jika siswa belum mengerjakan apapun, beri progress minimal (misal subtopik ke-1)
        if max_subtopic_id == 0:
            jumlah_history = 1 
        else:
            # Hitung berapa subtopik yang valid berdasarkan max_subtopic_id
            # Kita ambil subtopik yang ID-nya <= max_subtopic_id
            valid_subtopics = [s for s in all_subtopics if s.id <= max_subtopic_id]
            jumlah_history = len(valid_subtopics)

        # Hitung persentase progress
        progres_value = round((jumlah_history / total_sub) * 100)

        # Ambil subtopik yang sudah "dibuka"
        selected_subtopics = all_subtopics[:jumlah_history]

        # 5. Insert HistoryProgress
        for sub in selected_subtopics:
            history = HistoryProgress(
                id_user=student.id,
                id_topic=sub.id_topic,
                id_subtopic=sub.id,
                updated_at=datetime.now()
            )
            db.session.add(history)

        # 6. Insert Progress
        progress = Progress(
            id_user=student.id,
            progres_value=progres_value,
            last_updated=datetime.now()
        )
        db.session.add(progress)

    # Final commit
    db.session.commit()
    print(f"✅ Seeder Progress selaras berhasil untuk {len(students)} siswa!")