from app import db

class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    type = db.Column(db.Enum('aktivitas','kuis', 'evaluasi'))
    durasi_pengerjaan = db.Column(db.Integer)
    deadline = db.Column(db.DateTime)
    jumlah_soal = db.Column(db.Integer)
    topic_name = db.Column(db.String(255))