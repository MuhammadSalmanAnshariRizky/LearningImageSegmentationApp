import random
from datetime import datetime
from app import db
from app.model.progress import Progress
from app.model.historyprogress import HistoryProgress
from app.model.subtopic import SubTopic
from app.model.user import User

def seed_progress_history():
    # 1. Ambil semua siswa
    students = User.query.filter_by(role='Student').all()
    if not students:
        print("❌ Data student belum ada!")
        return

    # 2. Ambil semua subtopic berurutan (Total 24)
    all_subtopics = SubTopic.query.order_by(SubTopic.id.asc()).all()
    if not all_subtopics:
        print("❌ Subtopic belum ada!")
        return
    
    total_sub = len(all_subtopics)

    # 3. Reset data lama
    Progress.query.delete()
    HistoryProgress.query.delete()
    db.session.commit()

    # 4. Loop untuk setiap student
    for index, student in enumerate(students):
        
        # Logika: Siswa pertama (index 0) pasti 100%, lainnya random
        if index == 0:
            jumlah_history = total_sub
        else:
            jumlah_history = random.randint(5, total_sub) 

        # Hitung persentase progress
        progres_value = round((jumlah_history / total_sub) * 100)

        # Ambil subtopik sesuai jumlah yang sudah selesai
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
    print(f"✅ Seeder Progress BERURUT berhasil untuk {len(students)} siswa!")