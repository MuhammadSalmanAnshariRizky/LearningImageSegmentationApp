from app import db
from app.model.settings import Setting

def seed_settings():
    # Cek apakah sudah ada pengaturan
    if Setting.query.first():
        print("⚠️ Tabel Settings sudah ada, skip...")
        return

    settings_data = [
        Setting(
            id_class=1, 
            nilai_kkm_kuis=60, 
            nilai_kkm_evaluasi=70
        ),
        Setting(
            id_class=2, 
            nilai_kkm_kuis=65, 
            nilai_kkm_evaluasi=75
        )
    ]

    db.session.add_all(settings_data)
    db.session.commit()
    print("✅ Seeder Settings (KKM untuk 2 kelas) berhasil!")