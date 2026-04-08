from flask import Blueprint, render_template, jsonify
from app.model.activity_question import ActivityQuestion
from app.model.question import Question
import json
user_bp = Blueprint('user', __name__)

@user_bp.app_template_filter('from_json')
def from_json(value):
    return json.loads(value)

@user_bp.route('/')
def index():
    return render_template('index.html')

@user_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# materi 1
@user_bp.route('/materi1/pengantarcitradigital')
def pengantarcitradigital():
    return render_template(
        'mahasiswa/sub1/pengertiancitradigital.html',
        id_activity=1
    )

@user_bp.route('/materi1/jeniscitra')
def jeniscitra():
    return render_template(
        'mahasiswa/sub1/jeniscitra.html',
        id_activity=2)

@user_bp.route('/materi1/rangkuman')
def rangkuman1():
    return render_template('mahasiswa/sub1/rangkuman1.html')

@user_bp.route('/materi1/kuis')
def kuis1():
    from app.model.activity import Activity

    activity = Activity.query.filter_by(
        type="kuis",
        topic_name="Pengantar Citra Digital"
    ).first()

    return render_template(
        'mahasiswa/sub1/kuis1.html',
        activity=activity
    )
    



# materi 2
@user_bp.route('/materi2/pengantarsegmentasi')
def pengantarsegmentasi():
    return render_template(
        'mahasiswa/sub2/pengantarsegmentasi.html', 
        id_activity=3)
    

@user_bp.route('/materi2/metodesegmentasi')
def metodesegmentasi():
    return render_template(
        'mahasiswa/sub2/metodesegmentasi.html', 
        id_activity=4)

@user_bp.route('/materi2/rangkuman')
def rangkuman2():
    return render_template('mahasiswa/sub2/rangkuman2.html')

@user_bp.route('/materi2/kuis')
def kuis2():
    from app.model.activity import Activity

    activity = Activity.query.filter_by(
        type="kuis",
        topic_name="Segmentasi Citra"
    ).first()

    return render_template(
        'mahasiswa/sub2/kuis2.html',
        activity=activity
    )

# materi 3
@user_bp.route('/materi3/pengantaredgebased')
def pengantaredgebased():
    return render_template(
        'mahasiswa/sub3/pengantaredgebased.html',
        id_activity=5)

@user_bp.route('/materi3/edgethresholding')
def edgethresholding():
    return render_template(
        'mahasiswa/sub3/edgeimagethresholding.html',
        id_activity=6)

@user_bp.route('/materi3/bordertracing')
def bordertracing():
    return render_template(
        'mahasiswa/sub3/bordertracing.html',
        id_activity=7)

@user_bp.route('/materi3/rangkuman')
def rangkuman3():
    return render_template('mahasiswa/sub3/rangkuman3.html')

@user_bp.route('/materi3/kuis')
def kuis3():
    from app.model.activity import Activity

    activity = Activity.query.filter_by(
        type="kuis",
        topic_name="Edge-Based Segmentation"
    ).first()

    return render_template(
        'mahasiswa/sub3/kuis3.html',
        activity=activity
    )
    
# materi 4
@user_bp.route('/materi4/pengantarthresholdbased')
def pengantarthresholdbased():
    return render_template('mahasiswa/sub4/pengantarthresholdbased.html',id_activity=8)

@user_bp.route("/materi4/penerapanthresholding")
def penerapanthresholding():
    return render_template('mahasiswa/sub4/penerapanthreshold.html',id_activity=9)

@user_bp.route("/materi4/menentukanthreshold")
def menentukanthreshold():
    return render_template('mahasiswa/sub4/menentukanthreshold.html', id_activity=10)

@user_bp.route("/materi4/rangkuman")
def rangkuman4():
    return render_template('mahasiswa/sub4/rangkuman4.html')

@user_bp.route('/materi4/kuis')
def kuis4():
    from app.model.activity import Activity

    activity = Activity.query.filter_by(
        type="kuis",
        topic_name="Threshold-Based Segmentation"
    ).first()

    return render_template(
        'mahasiswa/sub4/kuis4.html',
        activity=activity
    )

#materi 5
@user_bp.route('/materi5/pengantarregionbased')
def pengantarregionbased():
    return render_template('mahasiswa/sub5/pengantarregionbased.html',id_activity=11)

@user_bp.route('/materi5/regionmerge')
def regionmerge():
    return render_template('mahasiswa/sub5/regionmerge.html',id_activity=12)

@user_bp.route('/materi5/splitandmerge')
def splitandmerge():
    return render_template('mahasiswa/sub5/splitandmerge.html',id_activity=13)

@user_bp.route('/materi5/postprocessing')
def postprocessing():
    return render_template('mahasiswa/sub5/postprocessing.html',id_activity=14)

@user_bp.route('/materi5/rangkuman')
def rangkuman5():       
    return render_template('mahasiswa/sub5/rangkuman5.html')

@user_bp.route('/materi5/kuis')
def kuis5():
    from app.model.activity import Activity

    activity = Activity.query.filter_by(
        type="kuis",
        topic_name="Region-Based Segmentation"
    ).first()

    return render_template(
        'mahasiswa/sub5/kuis5.html',
        activity=activity
    )

# Aktivitas
@user_bp.route('/api/soal/<int:id_activity>')
def get_soal(id_activity):
    relations = ActivityQuestion.query.filter_by(id_activity=id_activity).all()

    hasil = []

    for rel in relations:
        q = Question.query.get(rel.id_question)

        hasil.append({
            "soal": json.loads(q.question)["text"],
            "jawaban": q.MC_Answer,
            "opsi": {
                k: v["teks"]
                for opt in json.loads(q.MC_option)
                for k, v in opt.items()
            }
        })

    return jsonify(hasil)

# load soal kuis
@user_bp.route('/kuis/mulai/<string:title>')
def mulai_kuis(title):
    from app.model.activity import Activity
    from app.model.activity_question import ActivityQuestion
    from app.model.question import Question

    # cari activity berdasarkan title
    activity = Activity.query.filter_by(title=title).first_or_404()

    # ambil relasi
    relasi = ActivityQuestion.query.filter_by(id_activity=activity.id).all()

    question_ids = [r.id_question for r in relasi]

    questions = Question.query.filter(Question.id.in_(question_ids)).all()

    return render_template(
        'layouts/kuis.html',
        activity=activity,
        questions=questions
    )
