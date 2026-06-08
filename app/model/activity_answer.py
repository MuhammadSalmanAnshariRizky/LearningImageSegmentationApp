from app import db

class ActivityAnswer(db.Model):
    __tablename__ = 'activity_answer'

    id = db.Column(db.Integer, primary_key=True)
    
    # --- ATRIBUT BARU & FOREIGN KEY ---
    # Menghubungkan setiap jawaban dengan spesifik ke id_activity_result tertentu
    id_activity_result = db.Column(db.Integer, db.ForeignKey('activity_result.id'), nullable=False)
    
    id_activity = db.Column(db.Integer, nullable=False) # (Bisa dihapus jika ingin normalisasi ketat, tapi dipertahankan juga tidak apa-apa)
    id_user = db.Column(db.Integer, nullable=False)     # (Bisa dihapus jika ingin normalisasi ketat, tapi dipertahankan juga tidak apa-apa)
    id_question = db.Column(db.Integer, nullable=False)
    user_answer = db.Column(db.Text)
    status = db.Column(db.Enum('benar', 'salah'))