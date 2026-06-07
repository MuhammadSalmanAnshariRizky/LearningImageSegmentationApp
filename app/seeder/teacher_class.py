from app import db
from app.model.teacher_class import TeacherClass
from app.model.user import User
from app.model.classes import Class

def seed_teacher_class():
    if TeacherClass.query.first():
        print("⚠️ TeacherClass sudah ada, skip")
        return

    teachers = User.query.filter_by(role='Teacher').all()
    kelas = Class.query.all()

    if not teachers or not kelas:
        print("❌ Data teacher/class belum ada")
        return

    data = []

    for teacher in teachers:
        for k in kelas:
            data.append(TeacherClass(
                id_teacher=teacher.id,
                id_class=k.id
            ))

    db.session.add_all(data)
    db.session.commit()

    print("✅ Seeder TeacherClass berhasil!")