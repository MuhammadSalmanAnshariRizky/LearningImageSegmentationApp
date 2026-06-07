from app import db
from app.model.student_class import StudentClass
from app.model.user import User
from app.model.classes import Class

def seed_student_class():
    students = User.query.filter_by(role='Student').all()
    kelas = Class.query.all()

    if not students or not kelas:
        print("❌ Data student/class belum ada")
        return

    data = []

    for i, student in enumerate(students):
        k = kelas[i % len(kelas)]  # 🔥 bagi rata

        exists = StudentClass.query.filter_by(
            id_student=student.id,
            id_class=k.id
        ).first()

        if not exists:
            data.append(StudentClass(
                id_student=student.id,
                id_class=k.id,
            ))

    if not data:
        print("⚠️ Semua data sudah ada, skip")
        return

    db.session.add_all(data)
    db.session.commit()

    print("✅ Seeder StudentClass berhasil!")