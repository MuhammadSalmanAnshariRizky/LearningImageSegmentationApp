from app import db
from app.model.student_class import StudentClass
from app.model.user import User
from app.model.classes import Class

def seed_student_class():
    # Pastikan data diambil secara berurutan berdasarkan ID
    students = User.query.filter_by(role='Student').order_by(User.id.asc()).all()
    
    if not students:
        print("❌ Data student belum ada")
        return

    data = []

    for i, student in enumerate(students):
        # 🔥 Logika Baru: 20 siswa pertama (index 0-19) ke Kelas 1, sisanya ke Kelas 2
        target_class_id = 1 if i < 20 else 2

        exists = StudentClass.query.filter_by(
            id_student=student.id,
            id_class=target_class_id
        ).first()

        if not exists:
            data.append(StudentClass(
                id_student=student.id,
                id_class=target_class_id,
            ))

    if not data:
        print("⚠️ Semua data StudentClass sudah ada, skip")
        return

    db.session.add_all(data)
    db.session.commit()

    print("✅ Seeder StudentClass berhasil! (20 ke Kelas 1, 20 ke Kelas 2)")