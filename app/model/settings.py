from app import db

class Setting(db.Model):
    __tablename__ = 'settings'

    id_class = db.Column(
        db.Integer,
        db.ForeignKey('classes.id'),
        primary_key=True
    )

    nilai_kkm_kuis = db.Column(
        db.Integer,
        nullable=False,
        default=70
    )

    nilai_kkm_evaluasi = db.Column(
        db.Integer,
        nullable=False,
        default=75
    )
    
    