from app import db

class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    semester = db.Column(db.Enum('ganjil', 'genap', name='semester_enum'))
    tahun = db.Column(db.Integer)
    token = db.Column(db.String(50))

    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))