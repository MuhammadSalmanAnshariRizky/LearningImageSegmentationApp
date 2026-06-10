import random
from app import db
from app.model.activity_result import ActivityResult
from app.model.activity_answer import ActivityAnswer
from app.model.activity_question import ActivityQuestion
from app.model.question import Question

def seed_activity_answer():
    # 1. Hapus semua jawaban lama agar data selalu fresh dan sinkron
    ActivityAnswer.query.delete()
    db.session.commit()
    print("🧹 Data jawaban lama telah dibersihkan.")

    # 2. Ambil semua hasil aktivitas yang sudah ada (Ini adalah sumber kebenaran)
    # Karena ActivityResult sudah disesuaikan untuk semua kelas, data yang ditarik pasti valid.
    results = ActivityResult.query.all()
    
    data_to_insert = []

    for result in results:
        # 3. Ambil semua soal untuk aktivitas ini
        questions = db.session.query(Question)\
            .join(ActivityQuestion, Question.id == ActivityQuestion.id_question)\
            .filter(ActivityQuestion.id_activity == result.id_activity).all()
        
        if not questions:
            continue

        # Acak urutan soal agar jawaban benar dan salah tersebar secara acak
        random.shuffle(questions)
        
        # Ambil target jumlah benar dari ActivityResult
        total_benar_target = result.total_benar or 0
        
        for idx, q in enumerate(questions):
            # Normalisasi kunci jawaban ke huruf kecil untuk mencegah ValueError (case-sensitive)
            kunci_jawaban = q.MC_Answer.lower() if q.MC_Answer else 'a'

            # 4. Tentukan status jawaban berdasarkan total_benar_target
            if idx < total_benar_target:
                status = 'benar'
                user_answer = kunci_jawaban
            else:
                status = 'salah'
                # Pilih jawaban salah dari opsi yang tersedia
                pilihan_jawaban = ['a', 'b', 'c', 'd', 'e']
                if kunci_jawaban in pilihan_jawaban:
                    pilihan_jawaban.remove(kunci_jawaban)
                user_answer = random.choice(pilihan_jawaban)
            
            # 5. Buat record Jawaban
            answer = ActivityAnswer(
                id_activity_result=result.id,
                id_activity=result.id_activity,
                id_user=result.id_user,
                id_question=q.id,
                user_answer=user_answer, 
                status=status
            )
            
            data_to_insert.append(answer)

    # 6. Eksekusi simpan massal
    if data_to_insert:
        db.session.add_all(data_to_insert)
        db.session.commit()
        print(f"✅ Seeder ActivityAnswer berhasil! {len(data_to_insert)} jawaban dibuat selaras dengan status kelulusan tiap kelas.")
    else:
        print("⚠️ Tidak ada data jawaban yang dibuat.")