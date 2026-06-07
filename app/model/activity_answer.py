from app import db

class ActivityAnswer(db.Model):
    __tablename__ = 'activity_answer'

    id = db.Column(db.Integer, primary_key=True)
    id_activity = db.Column(db.Integer, nullable=False)
    id_user = db.Column(db.Integer, nullable=False)
    id_question = db.Column(db.Integer, nullable=False)
    user_answer = db.Column(db.Text)
    status = db.Column(db.Enum('benar','salah'))