from app import db
from app.model.teacher_class import TeacherClass
from app.model.user import User
from app.model.classes import Class

def seed_teacher_class():
    # Ambil dosen berurutan (Dosen 1 lalu Dosen 2)
    teachers = User.query.filter_by(role='Teacher').order_by(User.id.asc()).all()

    if len(teachers) < 2:
        print("❌ Data teacher minimal harus ada 2 untuk skenario ini")
        return

    data = []

    # 🔥 Mapping eksplisit: Dosen Pertama -> Kelas 1, Dosen Kedua -> Kelas 2
    mappings = [
        (teachers[0].id, 1),
        (teachers[1].id, 2)
    ]

    for teacher_id, class_id in mappings:
        exists = TeacherClass.query.filter_by(
            id_teacher=teacher_id,
            id_class=class_id
        ).first()

        if not exists:
            data.append(TeacherClass(
                id_teacher=teacher_id,
                id_class=class_id
            ))

    if not data:
        print("⚠️ Semua data TeacherClass sudah ada, skip")
        return

    db.session.add_all(data)
    db.session.commit()

    print("✅ Seeder TeacherClass berhasil! (Dosen dipetakan ke kelas masing-masing)")