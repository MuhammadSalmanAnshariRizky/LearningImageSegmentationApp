from app import db
from app.model.user import User
from werkzeug.security import generate_password_hash

def seed_user():
    # ==========================================
    # DATA NAMA MAHASISWA & DOSEN
    # ==========================================
    nama_mahasiswa = [
        "Ahmad Fauzi", "Siti Nurhaliza", "Muhammad Rizky", "Putri Rahmawati",
        "Budi Santoso", "Ayu Lestari", "Dimas Pratama", "Rina Sari",
        "Hendra Saputra", "Maya Indah", "Reza Aditya", "Dinda Permata",
        "Rahmat Hidayat", "Fitriani", "Ade Putra", "Siska Amalia",
        "Irfan Hakim", "Nia Ramadhani", "Fajar Ramadhan", "Mega Pertiwi",
        "Gusti Arya", "Noor Hasanah", "Muhammad Iqbal", "Siti Aisyah",
        "Andi Wijaya", "Riska Amelia", "Surya Dharma", "Nurul Huda",
        "Bayu Anggara", "Dina Marlina", "Kevin Sanjaya", "Nisa Safitri",
        "Aris Munandar", "Wulan Purnamasari", "Dedi Kusuma", "Tika Kartika",
        "Rendi Juliansyah", "Intan Nuraini", "Gilang Saputra", "Aulia Zahra"
    ]

    users = []

    # 1. Buat 40 Mahasiswa
    for i, nama in enumerate(nama_mahasiswa, start=1):
        user = User(
            id_other=f"1000{i:02d}",
            type_id_other="NIM",
            name=nama,
            email=f"mhs_{i}@example.com",
            password=generate_password_hash("password123"),
            role="Student"
        )
        users.append(user)

    # 2. Buat 2 Dosen
    dosen_1 = User(
        id_other="198805122015041001", 
        type_id_other="NIP",
        name="Nuruddin Wiranda, S.Kom., M.Cs.",
        email="dosen1@example.com",
        password=generate_password_hash("password123"),
        role="Teacher"
    )

    dosen_2 = User(
        id_other="198507232010121002", 
        type_id_other="NIP",
        name="Rizky Pamuji, S.Kom., M.Kom.",
        email="dosen2@example.com",
        password=generate_password_hash("password123"),
        role="Teacher"
    )
    
    users.extend([dosen_1, dosen_2])

    # 3. Simpan semua User sekaligus
    db.session.add_all(users)
    db.session.commit()

    print("✅ Seeder User berhasil! 40 Mahasiswa dan 2 Dosen telah ditambahkan.")