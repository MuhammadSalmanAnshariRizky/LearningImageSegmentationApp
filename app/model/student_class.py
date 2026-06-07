from app import db

class StudentClass(db.Model):
    __tablename__ = 'student_classes'

    id_student = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    )

    id_class = db.Column(
        db.Integer,
        db.ForeignKey('classes.id'),
        primary_key=True
    )
