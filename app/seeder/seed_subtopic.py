from app import db
from app.model.subtopic import SubTopic

def seed_subtopic_topic1():
    subtopics = [
        "Pengertian Citra Digital",
        "Jenis Citra",
        "Rangkuman",
        "Kuis-1"
    ]

    for s in subtopics:
        existing = SubTopic.query.filter_by(
            sub_topic_name=s,
            id_topic=1
        ).first()

        if not existing:
            db.session.add(SubTopic(
                sub_topic_name=s,
                id_topic=1
            ))

    db.session.commit()
    print("✅ SubTopic Topic 1 berhasil di-seed")

def seed_subtopic_topic2():
    subtopics = [
        "Segmentasi Citra",
        "Metode Segmentasi Citra",
        "Rangkuman",
        "Kuis-2"
    ]

    for s in subtopics:
        existing = SubTopic.query.filter_by(
            sub_topic_name=s,
            id_topic=2
        ).first()

        if not existing:
            db.session.add(SubTopic(
                sub_topic_name=s,
                id_topic=2
            ))

    db.session.commit()
    print("✅ SubTopic Topic 2 berhasil di-seed")
    

def seed_subtopic_topic3():
    subtopics = [
        "Pengantar Edge-based segmentation",
        "Tahapan Edge Based Segmentation",
        "Praktek Edge-based Segmentation",
        "Rangkuman",
        "Kuis-3"
    ]

    for s in subtopics:
        existing = SubTopic.query.filter_by(
            sub_topic_name=s,
            id_topic=3
        ).first()

        if not existing:
            db.session.add(SubTopic(
                sub_topic_name=s,
                id_topic=3
            ))

    db.session.commit()
    print("✅ SubTopic Topic 3 berhasil di-seed")
    

def seed_subtopic_topic4():
    subtopics = [
        "Pengantar Thresholding",
        "Histogram",
        "Metode Thresholding",
        "Rangkuman",
        "Kuis-4"
    ]

    for s in subtopics:
        existing = SubTopic.query.filter_by(
            sub_topic_name=s,
            id_topic=4
        ).first()

        if not existing:
            db.session.add(SubTopic(
                sub_topic_name=s,
                id_topic=4
            ))

    db.session.commit()
    print("✅ SubTopic Topic 4 berhasil di-seed")
    
def seed_subtopic_topic5():
    subtopics = [
        "Pengantar Region-Based Segmentation",
        "Region Growing",
        "Split and Merge",
        "Rangkuman",
        "Kuis-5"
    ]

    for s in subtopics:
        existing = SubTopic.query.filter_by(
            sub_topic_name=s,
            id_topic=5
        ).first()

        if not existing:
            db.session.add(SubTopic(
                sub_topic_name=s,
                id_topic=5
            ))

    db.session.commit()
    print("✅ SubTopic Topic 5 berhasil di-seed")
    
def seed_subtopic_topic6():
    subtopics = [
        "evaluasi akhir"
    ]

    for s in subtopics:
        existing = SubTopic.query.filter_by(
            sub_topic_name=s,
            id_topic=6
        ).first()

        if not existing:
            db.session.add(SubTopic(
                sub_topic_name=s,
                id_topic=6
            ))

    db.session.commit()
    print("✅ SubTopic Topic 6 berhasil di-seed")