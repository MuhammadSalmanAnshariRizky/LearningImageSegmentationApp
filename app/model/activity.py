from app import db

class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)

    # Relasi ke kelas
    id_class = db.Column(
        db.Integer,
        db.ForeignKey('classes.id'),
        nullable=False
    )

    # Judul aktivitas
    title = db.Column(
        db.String(255),
        nullable=False
    )

    # Tipe aktivitas
    type = db.Column(
        db.Enum('aktivitas', 'kuis', 'evaluasi', name='activity_type'),
        nullable=False
    )

    # Durasi (menit)
    durasi_pengerjaan = db.Column(db.Integer)

    # Jumlah soal (khusus kuis/evaluasi)
    jumlah_soal = db.Column(db.Integer)

    # 🔥 GANTI topic_name → FK
    id_topic = db.Column(
        db.Integer,
        db.ForeignKey('topic.id'),
        nullable=True
    )

    # 🔥 Tambahin subtopic (biar granular)
    id_subtopic = db.Column(
        db.Integer,
        db.ForeignKey('sub_topic.id'),
        nullable=True
    )

    # Status aktif/tidak
    status = db.Column(
        db.Enum('aktif', 'tidak aktif', name='activity_status'),
        nullable=False,
        default='aktif'
    )
    
    # RELASI
    topic = db.relationship('Topic', backref='activities')
    subtopic = db.relationship('SubTopic', backref='activities')