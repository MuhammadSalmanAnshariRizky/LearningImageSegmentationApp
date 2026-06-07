from app import db

class TeacherClass(db.Model):
    __tablename__ = 'teacher_classes'

    id_teacher = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    id_class = db.Column(db.Integer, db.ForeignKey('classes.id'), primary_key=True)