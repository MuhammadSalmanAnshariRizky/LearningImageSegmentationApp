import random
from app import db
from app.model.activity import Activity
from app.model.activity_result import ActivityResult
from app.model.activity_answer import ActivityAnswer
from app.model.activity_question import ActivityQuestion
from app.model.user import User

def seed_activity_answer():
    # 1. Ambil semua siswa
    students = User.query.filter_by(role='Student').all()
    
    # 2. Ambil aktivitas yang relevan
    activity_ids = [3, 6, 10, 14, 18, 19]
    
    data_to_insert = []

    for student in students:
        for act_id in activity_ids:
            
            # 3. Ambil semua hasil (ActivityResult) siswa ini untuk aktivitas ini
            # (Agar jawaban terikat ke percobaan ke-1, ke-2, dst)
            results = ActivityResult.query.filter_by(
                id_user=student.id, 
                id_activity=act_id
            ).all()

            for result in results:
                # 4. Ambil semua soal untuk aktivitas ini
                questions = ActivityQuestion.query.filter_by(id_activity=act_id).all()
                
                for q in questions:
                    # Cek apakah jawaban sudah ada agar tidak duplikat
                    existing = ActivityAnswer.query.filter_by(
                        id_activity_result=result.id,
                        id_question=q.id_question
                    ).first()
                    
                    if existing:
                        continue

                    # 5. Simulasi Jawaban
                    # Pilih status acak, tapi sesuaikan dengan total_benar/salah di ActivityResult
                    # (Opsional: agar lebih simpel, kita buat status acak saja)
                    status = random.choice(['benar', 'salah'])
                    
                    # Isi jawaban dummy
                    answer = ActivityAnswer(
                        id_activity_result=result.id,
                        id_activity=act_id,
                        id_user=student.id,
                        id_question=q.id_question,
                        user_answer="Jawaban Dummy", 
                        status=status
                    )
                    
                    data_to_insert.append(answer)

    if not data_to_insert:
        print("⚠️ Tidak ada data baru untuk di-seed (mungkin sudah terisi).")
        return

    db.session.add_all(data_to_insert)
    db.session.commit()
    print(f"✅ Seeder ActivityAnswer berhasil! {len(data_to_insert)} jawaban dibuat.")