from app import db

class Topic(db.Model):
    __tablename__ = 'topic'

    id = db.Column(db.Integer, primary_key=True)

    topic_name = db.Column(
        db.String(255),
        nullable=False
    )