from app import db
from app.model.topic import Topic

def seed_topic():
    topics = [
        "Pengantar Citra Digital",
        "Pengantar Segmentasi Citra",
        "Edge-Based Segmentation",
        "Threshold-Based Segmentation",
        "Region-Based Segmentation",
        "Evaluasi"
    ]

    for t in topics:
        # biar tidak duplikat
        existing = Topic.query.filter_by(topic_name=t).first()
        if not existing:
            db.session.add(Topic(topic_name=t))

    db.session.commit()
    print("✅ Seed topic berhasil")