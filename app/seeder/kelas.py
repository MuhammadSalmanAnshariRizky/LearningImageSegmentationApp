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

    # ambil dosen
    teacher = User.query.filter_by(role='Teacher').first()

    if not teacher:
        print("❌ Tidak ada dosen, seed user dulu!")
        return

    classes = [
        Class(
            name="Pengolahan Citra Digital",
            description="Materi segmentasi citra",
            semester="ganjil",
            tahun=2025,
            token=generate_token(),
            created_by=teacher.id
        ),
        Class(
            name="Computer Vision",
            description="Dasar computer vision",
            semester="genap",
            tahun=2025,
            token=generate_token(),
            created_by=teacher.id
        )
    ]

    db.session.add_all(classes)
    db.session.commit()

    print("✅ Seeder Class berhasil!")