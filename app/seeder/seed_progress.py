import random
from datetime import datetime
from app import db
from app.model.progress import Progress
from app.model.historyprogress import HistoryProgress
from app.model.activity_result import ActivityResult
from app.model.subtopic import SubTopic
from app.model.user import User
from app.model.activity import Activity 

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

    # 🎯 Mapping Dinamis ID Aktivitas -> ID Subtopic
    milestone_subtopics = [4, 8, 13, 18, 23, 24]
    
    gate_activities = Activity.query.filter(Activity.id_subtopic.in_(milestone_subtopics)).all()
    
    activity_subtopic_map = {act.id: act.id_subtopic for act in gate_activities}

    # 3. Reset data lama
    Progress.query.delete()
    HistoryProgress.query.delete()
    db.session.commit()

    # 4. Loop untuk setiap student
    for student in students:
        results = ActivityResult.query.filter_by(id_user=student.id)\
                                      .order_by(ActivityResult.id_activity.asc()).all()
        
        max_subtopic_id = 0
        
        for res in results:
            if res.id_activity in activity_subtopic_map:
                subtopic_terkait = activity_subtopic_map[res.id_activity]
                
                if res.result_status == 'lulus':
                    # JIKA LULUS: Update progres ke subtopik kuis ini
                    max_subtopic_id = max(max_subtopic_id, subtopic_terkait)
                else:
                    # JIKA TIDAK LULUS: 
                    # Jangan update max_subtopic_id! Langsung hentikan pengecekan.
                    # Progres akan otomatis tertahan di titik kelulusan terakhir.
                    break 

        # Jika siswa belum mengerjakan apapun (atau gagal di kuis pertama)
        if max_subtopic_id == 0:
            jumlah_history = 1 
        else:
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
    print(f"✅ Seeder Progress selaras berhasil untuk {len(students)} siswa! Progres mandek jika tidak lulus.")