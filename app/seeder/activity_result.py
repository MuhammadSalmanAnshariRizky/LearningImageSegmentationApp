import random
from datetime import datetime, timedelta
from app import db
from app.model.activity import Activity
from app.model.activity_result import ActivityResult
from app.model.user import User

def seed_activity_result():
    # 🎯 ambil user tertentu
    user = User.query.get(1)

    # 🎯 ambil activity ID 16 - 20
    activities = Activity.query.filter(Activity.id.in_([15,16, 17, 18, 19, 20])).all()

    if not user or not activities:
        print("❌ User atau Activity tidak ditemukan")
        return

    for activity in activities:

        # 🔥 CEK biar tidak double (opsional)
        existing = ActivityResult.query.filter_by(
            id_user=user.id,
            id_activity=activity.id
        ).first()

        if existing:
            continue

        # 🔢 jumlah soal (default 10 kalau tidak ada field)
        total_soal = getattr(activity, 'jumlah_soal', 10)

        # 🎯 hasil realistis
        benar = random.randint(int(total_soal * 0.5), total_soal)
        salah = total_soal - benar

        # 💯 nilai
        nilai = (benar / total_soal) * 100

        # ⏱ waktu (5–20 menit)
        waktu = random.randint(300, 1200)

        start_time = datetime.now() - timedelta(minutes=random.randint(10, 60))
        end_time = start_time + timedelta(seconds=waktu)

        # 📊 status
        status = "lulus" if nilai >= 60 else "tidak lulus"

        result = ActivityResult(
            id_user=user.id,
            id_activity=activity.id,
            nilai_akhir=round(nilai, 2),
            result_status=status,
            waktu_mengerjakan=waktu,
            start_time=start_time,
            end_time=end_time,
            total_benar=benar,
            total_salah=salah
        )

        db.session.add(result)

    db.session.commit()
    print("✅ Seeder ActivityResult (ID 16–20, User 1) berhasil!")