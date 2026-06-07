from app import db

class ActivityResult(db.Model):
    __tablename__ = 'activity_result'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer)
    id_activity = db.Column(db.Integer)
    nilai_akhir = db.Column(db.Float)
    result_status = db.Column(db.String(50))
    waktu_mengerjakan = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    total_benar = db.Column(db.Integer)
    total_salah = db.Column(db.Integer)