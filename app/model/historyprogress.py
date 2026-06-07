from app import db

class HistoryProgress(db.Model):
    __tablename__ = 'history_progress'

    id = db.Column(db.Integer, primary_key=True)

    id_user = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    id_topic = db.Column(
        db.Integer,
        db.ForeignKey('topic.id'),
        nullable=False
    )

    id_subtopic = db.Column(
        db.Integer,
        db.ForeignKey('sub_topic.id'),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now()
    )