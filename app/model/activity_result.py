from app import db

class ActivityResult(db.Model):
    __tablename__ = 'activity_result'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, nullable=False)
    id_activity = db.Column(db.Integer, nullable=False)
    
    # --- ATRIBUT BARU ---
    percobaan_ke = db.Column(db.Integer, nullable=False, default=1) 
    
    nilai_akhir = db.Column(db.Float)
    result_status = db.Column(db.String(50))
    waktu_mengerjakan = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    total_benar = db.Column(db.Integer)
    total_salah = db.Column(db.Integer)

    # --- RELASI ORM (Sangat Disarankan) ---
    # Memudahkan kamu memanggil jawaban dari sebuah hasil ujian
    # Contoh penggunaan: result.answers
    answers = db.relationship('ActivityAnswer', backref='result_reference', lazy=True, cascade="all, delete-orphan")