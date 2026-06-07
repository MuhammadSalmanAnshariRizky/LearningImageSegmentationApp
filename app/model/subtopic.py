from app import db
class SubTopic(db.Model):
    __tablename__ = 'sub_topic'

    id = db.Column(db.Integer, primary_key=True)

    id_topic = db.Column(
        db.Integer,
        db.ForeignKey('topic.id'),
        nullable=False
    )

    sub_topic_name = db.Column(
        db.String(255),
        nullable=False
    )
