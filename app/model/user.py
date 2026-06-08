from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    id_other = db.Column(db.String(50))
    type_id_other = db.Column(db.Enum('NIM', 'NIDN','NIP', name='id_other_types'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Enum('Student', 'Teacher', name='user_roles'), nullable=False)
    password = db.Column(db.String(255), nullable=False)
