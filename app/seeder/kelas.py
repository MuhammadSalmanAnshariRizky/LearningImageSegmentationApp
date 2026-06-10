from app import db
from app.model.classes import Class
from app.model.user import User
import random
import string

def generate_token(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def seed_class():

    if Class.query.first():
        print("⚠️ Class sudah ada, skip")
        return

    teachers = User.query.filter_by(role='Teacher').all()

    if not teachers:
        print("❌ Tidak ada dosen")
        return

    for teacher in teachers:

        kelas = Class(
            name=f"Kelas {teacher.name}",
            description="Materi segmentasi citra",
            semester="ganjil",
            tahun=2025,
            token=generate_token(),
            created_by=teacher.id
        )

        db.session.add(kelas)

    db.session.commit()

    print("✅ Seeder Class berhasil!")