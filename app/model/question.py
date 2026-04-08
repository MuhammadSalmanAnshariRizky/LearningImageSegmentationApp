from app import db

class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    question = db.Column(db.Text)
    MC_option = db.Column(db.Text)
    MC_Answer = db.Column(db.String(10))
    SA_Answer = db.Column(db.Text)
    tingkat_kesulitan = db.Column(db.Enum('mudah', 'sedang', 'sulit'))
    created_by = db.Column(db.Integer)

