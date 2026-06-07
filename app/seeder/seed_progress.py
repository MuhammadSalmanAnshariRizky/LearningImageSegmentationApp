from datetime import datetime

from app import db
from app.model.progress import Progress
from app.model.historyprogress import HistoryProgress
from app.model.subtopic import SubTopic


def seed_progress_history():
    # ========================
    # Ambil subtopic berurutan
    # ========================
    all_subtopics = SubTopic.query.order_by(
        SubTopic.id_topic.asc(),
        SubTopic.id.asc()
    ).all()

    if not all_subtopics:
        print("❌ Subtopic belum ada!")
        return

    total_sub = len(all_subtopics)

    # contoh progress user
    users_progress = [
        {"id": 1, "progress": 20},
        {"id": 2, "progress": 50},
    ]

    # reset
    Progress.query.delete()
    HistoryProgress.query.delete()
    db.session.commit()

    # ========================
    # Loop user
    # ========================
    for u in users_progress:
        id_user = u["id"]
        progres_value = u["progress"]

        # hitung jumlah subtopic yang selesai
        jumlah_history = int((progres_value / 100) * total_sub)

        # ambil BERURUT (bukan random)
        selected_subtopics = all_subtopics[:jumlah_history]

        # ========================
        # Insert history
        # ========================
        for sub in selected_subtopics:
            history = HistoryProgress(
                id_user=id_user,
                id_topic=sub.id_topic,
                id_subtopic=sub.id,
                updated_at=datetime.utcnow()
            )
            db.session.add(history)

        # ========================
        # Simpan progress
        # ========================
        progress = Progress(
            id_user=id_user,
            progres_value=progres_value,
            last_updated=datetime.utcnow()
        )
        db.session.add(progress)

    db.session.commit()
    print("✅ Seeder BERURUT berhasil")