from app import db
from app.model.user import User
from werkzeug.security import generate_password_hash

def seed_user():
    users = [
        User(
            id_other="12345678",
            type_id_other="NIM",
            name="Mahasiswa 1",
            email="mhs1@example.com",
            password=generate_password_hash("password123"),
            role="Student"
        ),
        User(
            id_other="87654321",
            type_id_other="NIM",
            name="Mahasiswa 2",
            email="mhs2@example.com",
            password=generate_password_hash("password123"),
            role="Student"
        ),
        User(
            id_other="D001",
            type_id_other="NIDN",
            name="Dosen 1",
            email="dosen1@example.com",
            password=generate_password_hash("password123"),
            role="Teacher"
        )
    ]

    db.session.add_all(users)
    db.session.commit()

    print("✅ Seeder User berhasil!")