from app import db

class ActivityQuestion(db.Model):
    __tablename__ = 'activity_question'

    id_activity = db.Column(
        db.Integer,
        db.ForeignKey('activities.id'),
        primary_key=True
    )

    id_question = db.Column(
        db.Integer,
        db.ForeignKey('question.id'),
        primary_key=True
    )