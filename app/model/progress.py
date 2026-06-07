from app import db

class Progress(db.Model):
    __tablename__ = 'progress'

    id = db.Column(db.Integer, primary_key=True)

    id_user = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    progres_value = db.Column(
        db.Float,   # bisa persen (0–100)
        default=0
    )

    last_updated = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now()
    )
