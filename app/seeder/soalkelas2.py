import json

from app import db
from app.model.activity import Activity
from app.model.question import Question
from app.model.activity_question import ActivityQuestion


def aktivitas1_2():

    # =========================
    # CREATE ACTIVITY
    # =========================
    activity = Activity(
        id_class=2,
        title='Aktivitas 1',
        type='aktivitas',
        durasi_pengerjaan=5,
        jumlah_soal=4,
        id_topic=1,
        id_subtopic=1,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": "Pernyataan yang paling tepat untuk menggambarkan citra digital adalah ....",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Gambar yang hanya dapat dilihat secara langsung tanpa perangkat elektronik",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Representasi visual dari dunia nyata dalam bentuk digital yang dapat dipahami dan diolah oleh komputer",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Gambar yang hanya tersimpan dalam bentuk cetakan kertas",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Kumpulan warna tanpa nilai numerik",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Gambar yang hanya dapat dibuat melalui lukisan tangan",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
                "text": "Berdasarkan matriks citra berikut ini, koordinat piksel yang memiliki nilai intensitas 100 adalah ....",

                # gambar matriks
                "URL": "/static/img/sub1/aktivitas1/soal_nomor2.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "f (0,0)",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "f (0,1)",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "f (1,1)",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "f (2,1)",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "f (2,2)",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": "Jika sebuah citra digital memiliki ukuran M × N, maka yang dimaksud dengan M adalah…",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Jumlah baris dalam citra",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Jumlah kolom dalam citra",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Nilai intensitas maksimum",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Jumlah warna dalam citra",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Jumlah total pixel dalam citra",
                        "url": None
                    }
                }

            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": "Diketahui suatu citra digital direpresentasikan sebagai f(x,y). Jika pada koordinat tertentu diperoleh nilai 150, maka angka 150 menunjukkan ....",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Posisi baris ke-150 pada citra",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Posisi kolom ke-150 pada citra",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Ukuran citra pada koordinat",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Nilai intensitas atau tingkat kecerahan piksel pada koordinat",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Jumlah piksel yang terdapat pada citra",
                        "url": None
                    }
                }

            ],

            "answer": "d"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            # question json
            question=json.dumps(item['question']),

            # options json
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='mudah',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Aktivitas 1 berhasil dibuat")
    
    
# aktivitas 2
def aktivitas2_2():

    # =========================
    # CREATE ACTIVITY
    # =========================
    activity = Activity(
        id_class=2,
        title='Aktivitas 2',
        type='aktivitas',
        durasi_pengerjaan=5,
        jumlah_soal=4,
        id_topic=1,
        id_subtopic=2,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": "Citra digital yang hanya memiliki satu kanal (channel) dan menampilkan tingkat terang–gelap tanpa informasi warna disebut …",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Citra RGB",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Citra biner",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Citra grayscales",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Citra vektor",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Citra multispektral",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
                "text": """
Pada citra RGB, setiap piksel umumnya terdiri dari tiga komponen warna \\( R \\), \\( G \\), dan \\( B \\).

Jika masing-masing komponen menggunakan 8 bit, maka jumlah bit dalam satu piksel adalah …
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "24 bit",
                        "url": None

                    }
                },

                {
                    "b": {
                        "teks": "16 bit",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "8 bit",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "32 bit",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "64 bit",
                        "url": None
                    }
                }

            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
Perhatikan karakteristik berikut:
<ul class="mt-2 mb-3 ms-3">
  <li>Hanya memiliki dua nilai piksel</li>
  <li>Biasanya direpresentasikan dengan 0 dan 1</li>
  <li>Digunakan pada dokumen hasil scan hitam-putih</li>
</ul>
Jenis citra yang sesuai adalah …
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Citra grayscales",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Citra RGB",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Citra 3D",
                        "url": None

                    }
                },

                {
                    "d": {
                        "teks": "Citra analog",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Citra biner",
                        "url": None
                    }
                }

            ],

            "answer": "e"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Diketahui sebuah citra RGB berukuran 2 × 2 piksel dengan nilai masing-masing kanal sebagai berikut.

Jika dilakukan konversi ke grayscales menggunakan Average Method dengan rumus:

\\[
Gray = \\frac{R + G + B}{3}
\\]

maka hasil grayscales pada \\( f(1,2) \\) yang benar adalah …
""",

                # gambar tabel RGB
                "URL": "/static/img/sub1/aktivitas2/soal_nomor4.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "190",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "185",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "200",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "180",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "165",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            # question json
            question=json.dumps(item['question']),

            # options json
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='mudah',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Aktivitas 2 berhasil dibuat")
    
def kuis1_2():

    # =========================
    # CREATE QUIZ
    # =========================
    activity = Activity(
        id_class=2,
        title='Kuis-1',
        type='kuis',
        durasi_pengerjaan=15,
        jumlah_soal=10,
        id_topic=1,
        id_subtopic=4,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": """
Citra digital disebut sebagai representasi dua dimensi karena…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Memiliki koordinat x dan y pada setiap piksel", "url": None}},
                {"b": {"teks": "Disusun dari tiga kanal warna", "url": None}},
                {"c": {"teks": "Memiliki warna yang beragam", "url": None} },
                {"d": {"teks": "Hanya dapat dilihat pada layar", "url": None}},
                {"e": {"teks": "Tidak memiliki ukuran tetap", "url": None}}

            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
                "text": """
Perbedaan utama antara citra digital dan citra analog adalah…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Citra digital tidak memiliki warna", "url": None}},
                {"b": {"teks": "Citra digital tersusun dari piksel dengan nilai diskrit", "url": None}},
                {"c": {"teks": "Citra analog hanya bisa disimpan di komputer", "url": None}},
                {"d": {"teks": "Citra digital tidak memiliki ukuran", "url": None}},
                {"e": {"teks": "Citra analog tidak dapat dilihat manusia", "url": None}}

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
Proses mengubah nilai kontinu menjadi nilai diskrit agar dapat diolah komputer disebut…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Sampling", "url": None}},
                {"b": {"teks": "Filtering", "url": None}},
                {"c": {"teks": "Discretization", "url": None}},
                {"d": {"teks": "Encoding", "url": None}},
                {"e": {"teks": "Transformasi", "url": None}}

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Jika suatu piksel memiliki nilai intensitas tinggi pada citra grayscales, maka tampilannya akan…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Semakin gelap", "url": None}},
                {"b": {"teks": "Semakin buram", "url": None}},
                {"c": {"teks": "Semakin terang", "url": None}},
                {"d": {"teks": "Semakin berwarna", "url": None}},
                {"e": {"teks": "Semakin tajam", "url": None}}

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 5
        # =====================================
        {
            "question": {
                "text": """
Pada citra grayscales 8-bit, jumlah kemungkinan nilai intensitas piksel adalah…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "2 nilai", "url": None}},
                {"b": {"teks": "8 nilai", "url": None}},
                {"c": {"teks": "128 nilai", "url": None}},
                {"d": {"teks": "256 nilai", "url": None}},
                {"e": {"teks": "512 nilai", "url": None}}

            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 6
        # =====================================
        {
            "question": {
                "text": """
Berikut ini yang merupakan karakteristik citra RGB adalah…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Menggunakan tiga kanal warna utama", "url": None}},
                {"b": {"teks": "Hanya memiliki dua nilai piksel", "url": None}},
                {"c": {"teks": "Hanya memiliki satu kanal", "url": None}},
                {"d": {"teks": "Tidak memiliki nilai intensitas", "url": None}},
                {"e": {"teks": "Tidak dapat menampilkan warna", "url": None}}

            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 7
        # =====================================
        {
            "question": {
                "text": """
Alasan utama citra grayscales sering digunakan dalam pengolahan citra adalah…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Memiliki lebih banyak warna", "url": None}},
                {"b": {"teks": "Lebih kompleks dari RGB", "url": None}},
                {"c": {"teks": "Menggunakan tiga kanal warna", "url": None}},
                {"d": {"teks": "Perhitungan lebih sederhana karena satu kanal", "url": None}},
                {"e": {"teks": "Tidak memiliki nilai numerik", "url": None}}

            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 8
        # =====================================
        {
            "question": {
                "text": """
Citra biner lebih efisien dalam penyimpanan karena…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Memiliki tiga kanal warna", "url": None}},
                {"b": {"teks": "Hanya memiliki dua kemungkinan nilai", "url": None}},
                {"c": {"teks": "Menggunakan 8 bit per piksel", "url": None}},
                {"d": {"teks": "Memiliki resolusi tinggi", "url": None}},
                {"e": {"teks": "Mengandung banyak informasi warna", "url": None}}

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 9
        # =====================================
        {
            "question": {
                "text": """
Dalam citra RGB, kombinasi nilai \\( (255,255,255) \\) menghasilkan warna…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Hitam", "url": None}},
                {"b": {"teks": "Merah", "url": None}},
                {"c": {"teks": "Hijau", "url": None}},
                {"d": {"teks": "Biru", "url": None}},
                {"e": {"teks": "Putih", "url": None}}

            ],

            "answer": "e"
        },

        # =====================================
        # SOAL 10
        # =====================================
        {
            "question": {
                "text": """
Diketahui sebuah citra RGB dengan masing-masing kanal sebagai berikut.

Jika dilakukan konversi ke grayscales menggunakan metode Luminosity:

\\[
Gray = 0.299R + 0.587G + 0.114B
\\]

maka nilai grayscales pada posisi \\( f(2,2) \\) adalah…
""",

                "URL": "/static/img/sub1/kuis1/soal_nomor10.png"
            },

            "options": [

                {"a": {"teks": "118", "url": None}},
                {"b": {"teks": "120", "url": None}},
                {"c": {"teks": "126", "url": None}},
                {"d": {"teks": "124", "url": None}},
                {"e": {"teks": "122", "url": None}}

            ],

            "answer": "e"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            question=json.dumps(item['question']),
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='sedang',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Kuis 1 berhasil dibuat")
    
# aktivitas 3
def aktivitas3_2():

    # =========================
    # CREATE ACTIVITY
    # =========================
    activity = Activity(
        id_class=2,
        title='Aktivitas 3',
        type='aktivitas',
        durasi_pengerjaan=5,
        jumlah_soal=4,
        id_topic=2,
        id_subtopic=5,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": """
Segmentasi citra membagi suatu citra menjadi beberapa wilayah.

Pernyataan yang tepat terkait hasil penggabungan seluruh wilayah tersebut adalah…
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Hanya sebagian citra yang terbentuk kembali",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menghasilkan citra baru yang berbeda",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Menghasilkan seluruh citra tanpa ada piksel yang tertinggal",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menghilangkan piksel yang tidak penting",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Mengubah ukuran citra",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
                "text": """
Dalam segmentasi citra, setiap wilayah harus merupakan connected set.

Artinya adalah…
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Setiap wilayah boleh terdiri dari piksel yang terpisah",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Piksel dalam satu wilayah harus saling terhubung",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Wilayah harus memiliki warna yang berbeda",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Setiap piksel harus memiliki nilai berbeda",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Wilayah harus berbentuk persegi",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
Perhatikan aturan segmentasi berikut:

\\[
R_i \\cap R_j = \\varnothing
\\]

Makna dari aturan tersebut adalah…
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Tidak boleh ada piksel yang menjadi anggota dua wilayah sekaligus",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Setiap wilayah harus memiliki ukuran yang sama",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Wilayah boleh saling beririsan sebagian",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Semua wilayah harus memiliki nilai intensitas sama",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Semua wilayah harus saling terhubung",
                        "url": None
                    }
                }

            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Dalam segmentasi citra, predikat digunakan sebagai kriteria homogenitas.

Jika suatu wilayah memiliki nilai piksel yang tidak seragam, maka…
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Segmentasi tetap valid",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Wilayah tersebut dianggap homogen",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Wilayah harus dipisahkan kembali",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Nilai predikat menjadi false",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Wilayah harus digabung dengan wilayah lain",
                        "url": None
                    }
                }

            ],

            "answer": "d"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            # question json
            question=json.dumps(item['question']),

            # options json
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='mudah',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Aktivitas 3 berhasil dibuat")


# aktivitas 4
def aktivitas4_2():

    # =========================
    # CREATE ACTIVITY
    # =========================
    activity = Activity(
        id_class=2,
        title='Aktivitas 4',
        type='aktivitas',
        durasi_pengerjaan=5,
        jumlah_soal=4,
        id_topic=2,
        id_subtopic=6,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": """
Pendekatan edge-based segmentation digunakan dengan cara…
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Mengelompokkan piksel berdasarkan warna yang sama",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Mengelompokkan piksel berdasarkan tekstur",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Menghitung rata-rata nilai piksel",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Membagi citra menjadi blok-blok kecil tanpa melihat intensitas",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Mendeteksi perubahan intensitas yang tajam sebagai batas wilayah",
                        "url": None
                    }
                }

            ],

            "answer": "e"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
                "text": """
Pada kondisi citra yang memiliki banyak tekstur dan perubahan intensitas kecil, metode yang lebih tepat digunakan adalah…
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Edge-based segmentation",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Thresholding sederhana",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Region-based segmentation",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Histogram equalization",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Filtering citra",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
Perbedaan utama antara edge-based dan region-based segmentation adalah…
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Edge-based menggunakan warna, region-based menggunakan bentuk",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Edge-based melihat batas perubahan intensitas, sedangkan region-based mengelompokkan piksel yang seragam",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Edge-based menggunakan blok piksel, region-based tidak",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Edge-based hanya untuk citra berwarna",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Region-based hanya untuk citra biner",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Dalam region-based segmentation, penggunaan standar deviasi bertujuan untuk…
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Mengidentifikasi wilayah bertekstur dan tidak bertekstur",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menentukan posisi tepi objek",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Mengukur perbedaan warna antar piksel",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Mengubah citra menjadi biner",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Mengurangi noise pada citra",
                        "url": None
                    }
                }

            ],

            "answer": "a"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            # question json
            question=json.dumps(item['question']),

            # options json
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='mudah',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Aktivitas 4 berhasil dibuat")


# kuis 2
def kuis2_2():

    # =========================
    # CREATE QUIZ
    # =========================
    activity = Activity(
        id_class=2,
        title='Kuis-2',
        type='kuis',
        durasi_pengerjaan=15,
        jumlah_soal=10,
        id_topic=2,
        id_subtopic=8,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": """
Segmentasi citra dilakukan pada ruang spasial.

Yang dimaksud ruang spasial adalah…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Ruang warna dalam citra", "url": None}},
                {"b": {"teks": "Ruang dua dimensi yang berisi posisi piksel", "url": None}},
                {"c": {"teks": "Ruang penyimpanan data citra", "url": None}},
                {"d": {"teks": "Ruang untuk menyimpan hasil segmentasi", "url": None}},
                {"e": {"teks": "Ruang untuk memproses noise", "url": None}}

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
                "text": """
Jika suatu citra dibagi menjadi beberapa wilayah \\( R_i \\), maka tujuan utama pembagian tersebut adalah…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Mengurangi ukuran citra", "url": None}},
                {"b": {"teks": "Mempermudah pengolahan dengan membagi citra menjadi bagian bermakna", "url": None}},
                {"c": {"teks": "Mengubah warna citra", "url": None}},
                {"d": {"teks": "Menghapus bagian citra tertentu", "url": None}},
                {"e": {"teks": "Menambah jumlah piksel", "url": None}}

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
Sebuah wilayah segmentasi memiliki dua bagian yang terpisah jauh tetapi masih dianggap satu region.

Kondisi ini berarti…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Segmentasi sudah benar", "url": None}},
                {"b": {"teks": "Segmentasi memenuhi aturan", "url": None}},
                {"c": {"teks": "Segmentasi tidak memenuhi konsep connected set", "url": None}},
                {"d": {"teks": "Segmentasi hanya berlaku pada citra berwarna", "url": None}},
                {"e": {"teks": "Segmentasi menjadi lebih akurat", "url": None}}

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Perbedaan utama antara 4-connected dan 8-connected terletak pada…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Nilai intensitas piksel", "url": None}},
                {"b": {"teks": "Jumlah wilayah dalam citra", "url": None}},
                {"c": {"teks": "Arah keterhubungan antar piksel", "url": None}},
                {"d": {"teks": "Ukuran citra", "url": None}},
                {"e": {"teks": "Warna piksel", "url": None}}

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 5
        # =====================================
        {
            "question": {
                "text": """
Jika suatu piksel termasuk ke dalam dua wilayah berbeda sekaligus, maka kondisi tersebut…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Melanggar aturan segmentasi citra", "url": None}},
                {"b": {"teks": "Diperbolehkan dalam segmentasi", "url": None}},
                {"c": {"teks": "Menunjukkan segmentasi yang optimal", "url": None}},
                {"d": {"teks": "Tidak berpengaruh pada hasil", "url": None}},
                {"e": {"teks": "Menunjukkan citra bertekstur", "url": None}}

            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 6
        # =====================================
        {
            "question": {
                "text": """
Suatu region memiliki piksel dengan nilai intensitas yang sangat beragam.

Berdasarkan konsep segmentasi, kondisi ini menunjukkan bahwa…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Region tersebut homogen", "url": None}},
                {"b": {"teks": "Region tersebut memenuhi kriteria", "url": None}},
                {"c": {"teks": "Segmentasi sudah sempurna", "url": None}},
                {"d": {"teks": "Region tersebut tidak memenuhi predikat Q", "url": None}},
                {"e": {"teks": "Region harus dipertahankan", "url": None}}

            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 7
        # =====================================
        {
            "question": {
                "text": """
Pendekatan edge-based segmentation paling tepat digunakan pada citra yang…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Memiliki banyak tekstur acak", "url": None}},
                {"b": {"teks": "Memiliki warna yang sama", "url": None}},
                {"c": {"teks": "Memiliki noise tinggi", "url": None}},
                {"d": {"teks": "Memiliki ukuran kecil", "url": None}},
                {"e": {"teks": "Memiliki perbedaan intensitas yang jelas antara objek dan latar", "url": None}}

            ],

            "answer": "e"
        },

        # =====================================
        # SOAL 8
        # =====================================
        {
            "question": {
                "text": """
Jika suatu citra memiliki banyak perubahan intensitas kecil yang tidak relevan, maka penggunaan edge-based segmentation akan…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Sangat akurat", "url": None}},
                {"b": {"teks": "Lebih cepat", "url": None}},
                {"c": {"teks": "Menghasilkan citra biner", "url": None}},
                {"d": {"teks": "Sulit menemukan batas yang jelas", "url": None}},
                {"e": {"teks": "Mengurangi jumlah piksel", "url": None}}

            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 9
        # =====================================
        {
            "question": {
                "text": """
Dalam region-based segmentation, citra dibagi menjadi subwilayah kecil.

Tujuan pembagian ini adalah…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Mengelompokkan piksel berdasarkan keseragaman karakteristik", "url": None}},
                {"b": {"teks": "Menghapus tepi objek", "url": None}},
                {"c": {"teks": "Menambah resolusi citra", "url": None}},
                {"d": {"teks": "Mengubah citra menjadi berwarna", "url": None}},
                {"e": {"teks": "Menghilangkan tekstur", "url": None}}

            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 10
        # =====================================
        {
            "question": {
                "text": """
Jika dua wilayah bertetangga memiliki karakteristik yang sama dan digabung masih homogen, maka…
""",
                "URL": None
            },

            "options": [

                {"a": {"teks": "Kedua wilayah harus dipisahkan", "url": None}},
                {"b": {"teks": "Segmentasi sudah salah total", "url": None}},
                {"c": {"teks": "Piksel harus dihapus", "url": None}},
                {"d": {"teks": "Nilai piksel harus diubah", "url": None}},
                {"e": {"teks": "Kedua wilayah sebenarnya satu region", "url": None}}

            ],

            "answer": "e"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            # question json
            question=json.dumps(item['question']),

            # options json
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='sedang',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Kuis 2 berhasil dibuat")


# aktivitas 5
def aktivitas5_2():

    # =========================
    # CREATE ACTIVITY
    # =========================
    activity = Activity(
        id_class=2,
        title='Aktivitas 5',
        type='aktivitas',
        durasi_pengerjaan=5,
        jumlah_soal=4,
        id_topic=3,
        id_subtopic=9,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": """
Konsep utama dari edge-based segmentation adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Mengelompokkan piksel berdasarkan warna yang sama",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menggunakan hasil deteksi tepi untuk membentuk batas objek pada citra",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Mengurangi jumlah piksel dalam citra",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Mengubah citra menjadi biner secara langsung",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Menghapus noise pada citra",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
                "text": """
Hasil deteksi tepi belum dapat langsung dianggap sebagai hasil segmentasi karena....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Hasilnya terlalu gelap",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Citra menjadi berwarna",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Ukuran citra berubah",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Tepi yang dihasilkan masih terpisah dan belum membentuk wilayah utuh",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Nilai piksel menjadi sama semua",
                        "url": None
                    }
                }

            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
Peran utama tepi (edge) dalam segmentasi citra adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Menunjukkan batas antara objek dengan latar belakang",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menambah jumlah piksel",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Mengubah warna objek",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Mengurangi resolusi citra",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Menentukan ukuran citra",
                        "url": None
                    }
                }

            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Edge chain tertutup dalam segmentasi citra berfungsi untuk....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Menghilangkan noise pada citra",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Mengubah citra menjadi grayscale",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Membentuk kontur lengkap yang mengelilingi objek",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menghubungkan piksel yang tidak berhubungan",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Mengurangi intensitas citra",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            # question json
            question=json.dumps(item['question']),

            # options json
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='mudah',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Aktivitas 5 berhasil dibuat")


# aktivitas 6
def aktivitas6_2():

    # =========================
    # CREATE ACTIVITY
    # =========================
    activity = Activity(
        id_class=2,
        title='Aktivitas 6',
        type='aktivitas',
        durasi_pengerjaan=5,
        jumlah_soal=4,
        id_topic=3,
        id_subtopic=10,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": """
Suatu sistem segmentasi citra telah berhasil mendeteksi sebagian besar tepi objek menggunakan metode Sobel.

Namun, hasil yang diperoleh masih berupa piksel-piksel tepi yang terputus-putus sehingga batas objek belum terbentuk secara utuh.

Berdasarkan tahapan edge-based segmentation, proses yang paling tepat dilakukan selanjutnya adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Melakukan region extraction untuk mengelompokkan objek dan latar belakang",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menghapus seluruh piksel tepi yang tidak saling terhubung",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Melakukan edge linking untuk menghubungkan piksel-piksel tepi yang berkaitan",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Mengubah citra menjadi grayscale agar tepi lebih mudah dideteksi",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Mengulangi proses edge detection dengan kernel yang berbeda",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
                "text": """
Perhatikan urutan proses berikut:

1. Objek dipisahkan dari latar belakang  
2. Perubahan intensitas piksel dideteksi untuk memperoleh tepi  
3. Piksel-piksel tepi yang berdekatan dihubungkan menjadi kontur yang lebih lengkap  

Apabila ketiga proses tersebut merupakan bagian dari edge-based segmentation, maka urutan yang benar adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "1 → 2 → 3",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "2 → 3 → 1",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "3 → 2 → 1",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "2 → 1 → 3",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "3 → 1 → 2",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
Sebuah citra telah melalui tahap edge detection dan menghasilkan edge map yang cukup baik.

Akan tetapi, beberapa bagian batas objek masih memiliki celah kecil akibat noise.

Jika proses segmentasi langsung dilanjutkan ke region extraction tanpa melakukan edge linking terlebih dahulu, dampak yang paling mungkin terjadi adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Nilai gradien objek menjadi lebih besar",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Seluruh noise pada citra akan hilang secara otomatis",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Waktu komputasi menjadi lebih cepat tanpa memengaruhi hasil segmentasi",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Wilayah objek dapat gagal diekstraksi secara tepat karena batas objek tidak tertutup sempurna",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Metode deteksi tepi berubah menjadi Hough Transform",
                        "url": None
                    }
                }

            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Dalam suatu proses edge linking menggunakan local processing, dua piksel tepi akan dihubungkan apabila memiliki magnitudo gradien dan arah gradien yang serupa.

Alasan utama penggunaan kedua kriteria tersebut adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Memastikan piksel yang dihubungkan kemungkinan berasal dari batas objek yang sama",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Mengurangi ukuran citra sebelum segmentasi dilakukan",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Mengubah citra grayscale menjadi citra biner",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menghilangkan kebutuhan proses region extraction",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Menggantikan fungsi edge detection dalam segmentasi",
                        "url": None
                    }
                }

            ],

            "answer": "a"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            # question json
            question=json.dumps(item['question']),

            # options json
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='sedang',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Aktivitas 6 berhasil dibuat")


# aktivitas 7
def aktivitas7_2():

    # =========================
    # CREATE ACTIVITY
    # =========================
    activity = Activity(
        id_class=2,
        title='Aktivitas 7',
        type='aktivitas',
        durasi_pengerjaan=5,
        jumlah_soal=4,
        id_topic=3,
        id_subtopic=11,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": """
Seorang mahasiswa ingin melakukan segmentasi objek menggunakan metode <i>Edge-Based Segmentation</i> pada citra berwarna.

Sebelum menjalankan fungsi 
<code class="code-python">cv2.Canny()</code>
citra terlebih dahulu dikonversi menjadi <i>grayscales</i> menggunakan perintah

<code class="code-python">cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)</code>

Tujuan utama langkah tersebut adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Mengurangi ukuran file citra agar lebih kecil",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Mengubah citra menjadi format yang dapat ditampilkan oleh Matplotlib",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Mengubah hasil segmentasi menjadi citra biner",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menghubungkan piksel-piksel tepi yang terputus",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Mempermudah proses deteksi tepi karena citra hanya memiliki satu kanal intensitas",
                        "url": None
                    }
                }

            ],

            "answer": "e"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
"text": """
Perhatikan urutan tahapan berikut:

<ol style="margin-top:10px; margin-bottom:15px;">
  <li class="mb-2">
    Menentukan kontur objek menggunakan 
    <code class="code-python">cv2.findContours()</code>
  </li>

  <li class="mb-2">
    Melakukan Edge Detection menggunakan 
    <code class="code-python">cv2.Canny()</code>
  </li>

  <li class="mb-2">
    Melakukan <i>Edge Linking</i> menggunakan Morphological Closing
  </li>

  <li class="mb-2">
    Melakukan Region Extraction menggunakan 
    <code class="code-python">cv2.drawContours()</code>
  </li>
</ol>

Urutan tahapan yang benar setelah citra berhasil dikonversi menjadi <i>grayscales</i> adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "1 → 2 → 3 → 4",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "2 → 3 → 1 → 4",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "3 → 2 → 1 → 4",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "2 → 1 → 4 → 3",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "1 → 3 → 2 → 4",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
Pada tahap <i>Edge Linking</i> digunakan operasi Morphological Closing dengan kernel berukuran 3×3.

Apabila tahap ini tidak dilakukan, dampak yang paling mungkin terjadi terhadap hasil segmentasi adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Kontur objek menjadi lebih efisien disimpan dalam memori",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Citra otomatis berubah menjadi citra biner",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Batas objek dapat tetap terputus sehingga proses segmentasi wilayah menjadi kurang optimal",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Nilai threshold pada Canny akan berubah secara otomatis",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Objek utama akan langsung terpisah sempurna dari latar belakang",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Hasil akhir segmentasi menunjukkan bahwa kendaraan berhasil diekstraksi sebagai wilayah berwarna putih.

Namun, beberapa objek kecil di sekitar kendaraan juga ikut tersegmentasi.

Berdasarkan penjelasan pada modul, kondisi tersebut terjadi karena....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Fungsi cv2.findContours() gagal mendeteksi kontur utama",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Nilai threshold pada Canny terlalu rendah sehingga citra menjadi gelap",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Operasi Morphological Closing menghapus sebagian objek utama",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Beberapa area latar belakang membentuk kontur tertutup sehingga dianggap sebagai objek oleh sistem",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Proses konversi grayscales menyebabkan hilangnya informasi warna",
                        "url": None
                    }
                }

            ],

            "answer": "d"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            # question json
            question=json.dumps(item['question']),

            # options json
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='sedang',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Aktivitas 7 berhasil dibuat")
    
    
def kuis3_2():
    # =========================
    # CREATE ACTIVITY
    # =========================
    activity = Activity(
        id_class=2,
        title='Kuis-3',
        type='kuis',
        durasi_pengerjaan=15,
        jumlah_soal=10,
        id_topic=3,
        id_subtopic=13,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": """
<i>Edge-Based Segmentation</i> merupakan metode segmentasi citra yang didasarkan pada....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Kesamaan warna antar piksel",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Kesamaan tekstur citra",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Informasi tepi yang menunjukkan batas objek",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Ukuran objek pada citra",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Posisi objek pada citra",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
                "text": """
Dalam <i>edge-based segmentation</i>, batas objek umumnya ditunjukkan oleh....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Kesamaan intensitas piksel",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Perubahan intensitas piksel yang signifikan",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Ukuran objek yang besar",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Banyaknya warna pada citra",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Jumlah piksel objek",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
Tujuan utama penggunaan <i>Edge-Based Segmentation</i> adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Mengurangi ukuran file citra",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Mengubah citra menjadi grayscales",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Membagi citra menjadi bagian-bagian bermakna berdasarkan batas objek",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menambah jumlah objek pada citra",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Menghilangkan seluruh noise pada citra",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Urutan tahapan yang benar pada <i>Edge-Based Segmentation</i> adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Edge linking → Edge Detection → Region Extraction",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Edge Detection → Edge linking → Region Extraction",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Region Extraction → Edge Detection → Edge Linking",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Region Extraction → Edge linking → Edge Detection",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Edge Detection → Region Extraction → Edge Linking",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 5
        # =====================================
        {
            "question": {
                "text": """
Setelah proses <i>Edge Detection</i> dilakukan, tahap <i>Edge linking</i> bertujuan untuk....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Menghubungkan piksel-piksel tepi yang terputus sehingga membentuk batas objek yang lebih lengkap",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Mengubah citra menjadi grayscales",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Menghitung gradien horizontal dan vertikal",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menentukan ukuran objek",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Mengubah citra menjadi RGB",
                        "url": None
                    }
                }

            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 6
        # =====================================
        {
            "question": {
                "text": """
Pada pendekatan <i>local processing</i>, dua piksel tepi dapat dihubungkan apabila....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Memiliki magnitudo gradien dan arah gradien yang serupa",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Berada pada koordinat yang sama",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Memiliki warna yang sama",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Memiliki ukuran yang sama",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Berasal dari citra yang sama",
                        "url": None
                    }
                }

            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 7
        # =====================================
        {
            "question": {
                "text": """
<i>Region Extraction</i> dilakukan setelah proses <i>Edge linking</i> karena....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Region Extraction digunakan untuk menghitung gradien citra",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Region Extraction digunakan untuk mendeteksi tepi",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Region Extraction digunakan untuk mengubah citra menjadi grayscales",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Region Extraction digunakan untuk menentukan kernel",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Region Extraction memerlukan batas objek yang kontinu dan tertutup",
                        "url": None
                    }
                }

            ],

            "answer": "e"
        },

        # =====================================
        # SOAL 8
        # =====================================
        {
            "question": {
                "text": """
Kode program yang tepat untuk mengubah citra menjadi <i>grayscales</i> adalah....
""",
                "URL": "/static/img/sub3/kuis3/soal_nomor8.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "<code class='code-python'>cv2.Canny(image,100,200)</code>",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "<code class='code-python'>cv2.drawContours(image)</code>",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "<code class='code-python'>cv2.findContours(image)</code>",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "<code class='code-python'>cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)</code>",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "<code class='code-python'>np.zeros(image.shape)</code>",
                        "url": None
                    }
                }

            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 9
        # =====================================
        {
            "question": {
                "text": """
Kode program yang tepat untuk melakukan deteksi tepi menggunakan metode Canny adalah....
""",
                "URL": "/static/img/sub3/kuis3/soal_nomor9.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "<code class='code-python'>cv2.drawContours(gray)</code>",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "<code class='code-python'>cv2.findContours(gray)</code>",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "<code class='code-python'>cv2.morphologyEx(gray)</code>",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "<code class='code-python'>cv2.Canny(gray,100,200)</code>",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "<code class='code-python'>np.zeros(gray.shape)</code>",
                        "url": None
                    }
                }

            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 10
        # =====================================
        {
            "question": {
                "text": """
Kode program yang tepat untuk melakukan <i>Edge linking</i> menggunakan Morphological Closing adalah....
""",
                "URL": "/static/img/sub3/kuis3/soal_nomor10.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "<code class='code-python'>cv2.CHAIN_APPROX_SIMPLE</code>",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "<code class='code-python'>cv2.RETR_EXTERNAL</code>",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "<code class='code-python'>cv2.Canny</code>",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "<code class='code-python'>cv2.COLOR_BGR2GRAY</code>",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "<code class='code-python'>cv2.MORPH_CLOSE</code>",
                        "url": None
                    }
                }

            ],

            "answer": "e"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            question=json.dumps(item['question']),

            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='sedang',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Kuis 3 berhasil dibuat")
    
# aktivitas 8
def aktivitas8_2():

    # =========================
    # CREATE ACTIVITY
    # =========================
    activity = Activity(
        id_class=2,
        title='Aktivitas 8',
        type='aktivitas',
        durasi_pengerjaan=5,
        jumlah_soal=4,
        id_topic=4,
        id_subtopic=14,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": """
<i>Graylevel Thresholding</i> digunakan untuk memisahkan objek dan latar belakang pada citra berdasarkan nilai intensitas piksel dengan bantuan nilai ambang (<i>threshold</i>)....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Mengubah citra menjadi berwarna",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Membandingkan nilai piksel dengan threshold",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Menghilangkan seluruh noise",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Memperbesar ukuran citra",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Mengubah format citra",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
                "text": """
Jika suatu piksel memiliki nilai intensitas lebih besar dari nilai threshold <code class="code-python">(T)</code>, maka pada citra biner hasil thresholding piksel tersebut akan bernilai....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "0 (background)",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "1 (objek)",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "255 (warna putih)",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Tetap seperti semula",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Tidak diproses",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
Metode <i>thresholding</i> sederhana banyak digunakan karena memiliki kelebihan utama yaitu....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Hasil selalu sempurna",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Proses sangat kompleks",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Cepat dan ringan secara komputasi",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Hanya untuk citra berwarna",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Membutuhkan data besar",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Jika nilai threshold 
<code class="code-python">T = 150</code>, 
maka piksel dengan nilai intensitas kurang dari atau sama dengan 150 akan diklasifikasikan sebagai....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Background (0)",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Objek (1)",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Objek (255)",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Tidak berubah",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Noise",
                        "url": None
                    }
                }

            ],

            "answer": "a"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            # question json
            question=json.dumps(item['question']),

            # options json
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='mudah',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Aktivitas 8 berhasil dibuat")
    
# aktivitas 9
def aktivitas9_2():

    # =========================
    # CREATE ACTIVITY
    # =========================
    activity = Activity(
        id_class=2,
        title='Aktivitas 9',
        type='aktivitas',
        durasi_pengerjaan=5,
        jumlah_soal=4,
        id_topic=4,
        id_subtopic=15,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": """
Pada histogram bimodal terdapat dua puncak yang mewakili objek dan <i>background</i>.

Nilai <i>threshold</i> umumnya dipilih pada....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Puncak histogram dengan frekuensi tertinggi",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Nilai intensitas maksimum citra",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Nilai intensitas minimum citra",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Lembah (<i>valley</i>) di antara dua puncak",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Rata-rata seluruh intensitas piksel",
                        "url": None
                    }
                }

            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
                "text": """
Sebuah histogram memiliki dua puncak yang terpisah dengan jelas.

Kondisi tersebut menunjukkan bahwa....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Objek dan background memiliki distribusi intensitas yang berbeda sehingga threshold lebih mudah ditentukan",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Histogram dipengaruhi oleh noise yang tinggi",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Segmentasi citra akan sulit dilakukan",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Seluruh piksel citra memiliki intensitas yang sama",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Citra harus menggunakan lebih dari satu threshold",
                        "url": None
                    }
                }

            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
<i>Noise</i> pada citra dapat memengaruhi proses penentuan threshold karena....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Mengurangi jumlah piksel citra",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Membuat distribusi intensitas objek dan background saling tumpang tindih pada histogram",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Mengubah citra grayscales menjadi RGB",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menambah ukuran objek pada citra",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Menghilangkan histogram citra",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Apabila histogram citra memiliki lebih dari dua puncak, maka pendekatan yang sesuai adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Edge Detection",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Thresholding Growing",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Multi-thresholding",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Local Thresholding",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Global Thresholding",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            # question json
            question=json.dumps(item['question']),

            # options json
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='mudah',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Aktivitas 9 berhasil dibuat")
    
# aktivitas 10
def aktivitas10_2():

    # =========================
    # CREATE ACTIVITY
    # =========================
    activity = Activity(
        id_class=2,
        title='Aktivitas 10',
        type='aktivitas',
        durasi_pengerjaan=5,
        jumlah_soal=4,
        id_topic=4,
        id_subtopic=16,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": """
Metode <i>Global Thresholding</i> menentukan nilai threshold dengan cara....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Menggunakan nilai threshold yang berbeda pada setiap piksel",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menggunakan satu nilai threshold untuk seluruh citra",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Menggunakan beberapa nilai threshold secara bersamaan",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menggunakan informasi tekstur sebagai dasar segmentasi",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Menggunakan koordinat piksel sebagai dasar segmentasi",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
                "text": """
Pada metode <i>Otsu Thresholding</i>, nilai threshold terbaik dipilih berdasarkan....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Nilai intensitas terbesar pada histogram",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Nilai rata-rata seluruh piksel citra",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Nilai threshold yang menghasilkan variansi total berbobot terbesar",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Nilai threshold yang menghasilkan variansi total berbobot terkecil",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Jumlah piksel objek yang paling banyak",
                        "url": None
                    }
                }

            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
Perhatikan potongan kode dibawah, Kode yang tepat untuk mengaktifkan metode <i>Otsu Thresholding</i> adalah....
""",
                "URL": "/static/img/sub4/aktivitas10/soal_nomor3.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "<code class='code-python'>cv2.THRESH_BINARY</code>",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "<code class='code-python'>cv2.THRESH_TRUNC</code>",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "<code class='code-python'>cv2.THRESH_BINARY + cv2.THRESH_OTSU</code>",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "<code class='code-python'>cv2.THRESH_BINARY_INV</code>",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "<code class='code-python'>cv2.THRESH_OTSU</code>",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Perhatikan potongan kode dibawah, Pada metode <i>Iterative Threshold Selection</i>, kode yang tepat untuk menghitung threshold baru adalah....
""",
                "URL": "/static/img/sub4/aktivitas10/soal_nomor4.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "<code class='code-python'>(m1 + m2) / 2</code>",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "<code class='code-python'>(m1 - m2) / 2</code>",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "<code class='code-python'>m1 * m2</code>",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "<code class='code-python'>max(m1, m2)</code>",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "<code class='code-python'>min(m1, m2)</code>",
                        "url": None
                    }
                }

            ],

            "answer": "a"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            # question json
            question=json.dumps(item['question']),

            # options json
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='sedang',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Aktivitas 10 berhasil dibuat")
    
# kuis 4
def kuis4_2():

    # =========================
    # CREATE QUIZ
    # =========================
    activity = Activity(
        id_class=2,
        title='Kuis-4',
        type='kuis',
        durasi_pengerjaan=15,
        jumlah_soal=10,
        id_topic=4,
        id_subtopic=18,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": """
Jika digunakan metode <i>thresholding</i>, sebuah citra memiliki objek berwarna gelap di atas latar belakang yang terang.

Tujuan utama proses tersebut adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Mengurangi ukuran citra",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Mengubah citra grayscales menjadi RGB",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Memisahkan objek dan background berdasarkan perbedaan intensitas piksel",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menghilangkan seluruh noise pada citra",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Menentukan posisi objek pada citra",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        },
# =====================================
# SOAL 2
# =====================================
{
    "question": {
        "text": """
Perhatikan aturan thresholding berikut.

\\[
g(x,y)=
\\begin{cases}
1, & f(x,y) > T \\\\
0, & f(x,y) \\leq T
\\end{cases}
\\]

Jika diketahui nilai piksel \\( f(x,y) > T \\), maka nilai keluaran adalah....
""",
        "URL": None
    },

    "options": [

        {
            "a": {
                "teks": "0",
                "url": None
            }
        },

        {
            "b": {
                "teks": "120",
                "url": None
            }
        },

        {
            "c": {
                "teks": "150",
                "url": None
            }
        },

        {
            "d": {
                "teks": "1",
                "url": None
            }
        },

        {
            "e": {
                "teks": "255",
                "url": None
            }
        }

    ],

    "answer": "d"
},
        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
Pada proses penentuan threshold menggunakan histogram, keberadaan lembah (<i>valley</i>) di antara dua puncak histogram menunjukkan bahwa....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Histogram mengandung noise yang tinggi",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Objek dan background sulit dibedakan",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Histogram tidak dapat digunakan untuk thresholding",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Terdapat batas yang berpotensi digunakan sebagai threshold",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Seluruh piksel memiliki intensitas yang sama",
                        "url": None
                    }
                }

            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Sebuah citra mengalami pencahayaan yang tidak merata sehingga bagian objek yang sama memiliki intensitas berbeda pada beberapa area.

Dampak kondisi tersebut terhadap histogram adalah….
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Histogram menjadi lebih sederhana",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Histogram hanya memiliki satu puncak",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Histogram menjadi lebih kompleks sehingga penentuan threshold lebih sulit",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Histogram tidak lagi memiliki nilai intensitas",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Histogram berubah menjadi citra biner",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 5
        # =====================================
        {
            "question": {
                "text": """
Pada metode <i>Iterative Threshold Selection</i>, tujuan pembagian piksel menjadi kelompok <code class="code-python">G1</code> dan <code class="code-python">G2</code> adalah….
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Mengubah citra menjadi histogram",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menghitung rata-rata intensitas masing-masing kelompok untuk memperbarui threshold",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Menentukan jumlah objek pada citra",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menghilangkan noise dari citra",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Menghitung ukuran citra",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        },

      # =====================================
# SOAL 6
# =====================================
{
    "question": {
        "text": """
Pada contoh perhitungan Iterative Threshold Selection diperoleh:

\\[
m_1 = 140
\\]

\\[
m_2 = 100
\\]

maka nilai threshold baru yang dihasilkan adalah....
""",
        "URL": None
    },

    "options": [

        {
            "a": {
                "teks": "120",
                "url": None
            }
        },

        {
            "b": {
                "teks": "95",
                "url": None
            }
        },

        {
            "c": {
                "teks": "70",
                "url": None
            }
        },

        {
            "d": {
                "teks": "140",
                "url": None
            }
        },

        {
            "e": {
                "teks": "190",
                "url": None
            }
        }

    ],

    "answer": "a"
},
        # =====================================
        # SOAL 7
        # =====================================
        {
            "question": {
                "text": """
Keunggulan utama metode <i>Otsu Thresholding</i> dibandingkan thresholding manual adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Menggunakan beberapa nilai threshold secara bersamaan",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Tidak memerlukan proses segmentasi",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Menghasilkan citra berwarna setelah segmentasi",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Dapat digunakan tanpa histogram citra",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Dapat menentukan nilai threshold secara otomatis berdasarkan histogram citra",
                        "url": None
                    }
                }

            ],

            "answer": "e"
        },

        # =====================================
        # SOAL 8
        # =====================================
        {
            "question": {
                "text": """
Pada algoritma <i>Otsu Thresholding</i>, histogram dinormalisasi terlebih dahulu agar....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Histogram berubah menjadi citra biner",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Jumlah piksel objek bertambah",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Nilai threshold menjadi nol",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Ukuran citra menjadi lebih kecil",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Setiap nilai histogram menyatakan probabilitas kemunculan intensitas piksel",
                        "url": None
                    }
                }

            ],

            "answer": "e"
        },

        # =====================================
        # SOAL 9
        # =====================================
        {
            "question": {
                "text": """
Perhatikan potongan gambar di bawah.Fungsi <code class="code-python">cv2.calcHist()</code> pada kode tersebut digunakan untuk....
""",
                "URL": "/static/img/sub4/kuis4/soal_nomor9.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "Melakukan thresholding citra",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menghitung distribusi frekuensi intensitas piksel",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Menentukan threshold otomatis",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menampilkan citra grayscales",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Mengubah citra menjadi biner",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 10
        # =====================================
        {
            "question": {
                "text": """
Perhatikan potongan gambar di bawah. Tujuan dari kondisi tersebut adalah....
""",
                "URL": "/static/img/sub4/kuis4/soal_nomor10.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "Menghentikan iterasi ketika nilai threshold telah konvergen",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menghentikan program jika citra tidak ditemukan",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Mengurangi noise pada citra",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menentukan jumlah histogram",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Mengubah citra menjadi biner",
                        "url": None
                    }
                }

            ],

            "answer": "a"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            # question json
            question=json.dumps(item['question']),

            # options json
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='sulit',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Kuis 4 berhasil dibuat")
    
# aktivitas 11
def aktivitas11_2():

    # =========================
    # CREATE ACTIVITY
    # =========================
    activity = Activity(
        id_class=2,
        title='Aktivitas 11',
        type='aktivitas',
        durasi_pengerjaan=5,
        jumlah_soal=4,
        id_topic=5,
        id_subtopic=19,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": """
<i>Region-Based Segmentation</i> merupakan metode segmentasi citra yang dilakukan dengan cara....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Mendeteksi perubahan intensitas untuk menemukan tepi objek",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menghitung histogram untuk menentukan threshold",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Mengubah citra berwarna menjadi citra grayscales",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menghilangkan noise menggunakan filter spasial",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Mengelompokkan piksel yang memiliki karakteristik serupa ke dalam suatu region",
                        "url": None
                    }
                }

            ],

            "answer": "e"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
                "text": """
Homogenitas suatu region pada <i>Region-Based Segmentation</i> dapat ditentukan berdasarkan....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Ukuran citra dan jumlah piksel",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Posisi objek pada citra",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Tingkat keabuan, warna, tekstur, atau karakteristik lainnya",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Jumlah region yang terbentuk",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Banyaknya tepi pada objek",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
Perhatikan pernyataan berikut.

<ol class="custom-number mt-2 mb-3">
  <li>Setiap region harus bersifat homogen.</li>
  <li>Region yang bertetangga harus selalu digabungkan.</li>
  <li>Dua region bertetangga tidak boleh digabung jika hasil penggabungannya tidak homogen.</li>
  <li>Homogenitas region dapat diuji menggunakan fungsi \\( P(R_i) \\).</li>
</ol>

Pernyataan yang sesuai dengan konsep <i>Region-Based Segmentation</i> adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "1 dan 2",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "1 dan 4",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "2 dan 3",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "1, 3, dan 4",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "1, 2, 3, dan 4",
                        "url": None
                    }
                }

            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Perbedaan utama antara <i>Region-Based Segmentation</i> dan <i>Edge-Based Segmentation</i> adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Region-Based Segmentation membentuk objek berdasarkan kesamaan karakteristik piksel, sedangkan Edge-Based Segmentation berfokus pada pencarian batas objek",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Region-Based Segmentation menggunakan histogram, sedangkan Edge-Based Segmentation tidak",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Region-Based Segmentation hanya digunakan pada citra grayscales, sedangkan Edge-Based Segmentation digunakan pada citra berwarna",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Region-Based Segmentation menggunakan threshold, sedangkan Edge-Based Segmentation menggunakan region",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Region-Based Segmentation tidak memerlukan kriteria homogenitas",
                        "url": None
                    }
                }

            ],

            "answer": "a"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            # question json
            question=json.dumps(item['question']),

            # options json
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='mudah',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Aktivitas 11 berhasil dibuat")
# aktivitas 12
def aktivitas12_2():

    # =========================
    # CREATE ACTIVITY
    # =========================
    activity = Activity(
        id_class=2,
        title='Aktivitas 12',
        type='aktivitas',
        durasi_pengerjaan=5,
        jumlah_soal=4,
        id_topic=5,
        id_subtopic=20,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": """
Pada <i>region growing</i>, suatu piksel dapat ditambahkan ke dalam region apabila....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Memiliki koordinat yang sama dengan <i>seed point</i>",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Memiliki ukuran yang sama dengan objek",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Berada pada baris yang sama dengan <i>seed point</i>",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Memenuhi <i>predicate</i> kesamaan dan terhubung dengan <i>seed point</i>",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Memiliki nilai intensitas terbesar",
                        "url": None
                    }
                }

            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
                "text": """
Seorang mahasiswa akan melakukan segmentasi citra menggunakan metode <i>Region Growing</i>.

Sebelum memeriksa kesamaan intensitas dan keterhubungan piksel, langkah yang harus dilakukan terlebih dahulu adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Memilih atau menentukan <i>seed point</i>",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menentukan nilai threshold untuk proses segmentasi",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Memberikan label pada region yang terbentuk",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Membentuk citra kandidat berdasarkan predicate",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Memeriksa hubungan 8-connectivity antar piksel",
                        "url": None
                    }
                }

            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
Jika nilai <i>threshold</i> diperbesar pada algoritma <i>Region Growing</i>, maka dampak yang paling mungkin terjadi adalah....
""",
                "URL": "/static/img/sub5/aktivitas12/soal_nomor3.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "Semakin sedikit piksel yang bergabung ke dalam region",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Tidak ada perubahan hasil segmentasi",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Semakin banyak piksel yang dapat bergabung ke dalam region",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "<i>Seed point</i> berpindah posisi",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Citra berubah menjadi citra biner",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Perhatikan potongan gambar di bawah. Potongan program tersebut digunakan untuk....
""",
                "URL": "/static/img/sub5/aktivitas12/soal_nomor4.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "Menentukan ukuran citra",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menentukan titik awal pertumbuhan region",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Menentukan jumlah region",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menentukan nilai histogram",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Menentukan warna objek",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            # question json
            question=json.dumps(item['question']),

            # options json
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='mudah',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Aktivitas 12 berhasil dibuat")

# aktivitas 13
def aktivitas13_2():

    # =========================
    # CREATE ACTIVITY
    # =========================
    activity = Activity(
        id_class=2,
        title='Aktivitas 13',
        type='aktivitas',
        durasi_pengerjaan=5,
        jumlah_soal=4,
        id_topic=5,
        id_subtopic=21,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": """
Pada metode <i>Region Splitting and Merging</i>, suatu region akan dipecah menjadi empat subregion apabila....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Region tidak memenuhi kriteria homogenitas",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Region memiliki rata-rata intensitas tinggi",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Region memiliki ukuran yang besar",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Region memiliki banyak tetangga",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Region berada pada level <i>pyramid</i> tertinggi",
                        "url": None
                    }
                }

            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
                "text": """
Perhatikan kriteria homogenitas berikut.

\\[
\\max(R) - \\min(R) < T
\\]

Jika suatu region memenuhi kondisi tersebut, maka kondisi region adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Tidak homogen sehingga harus di-<i>split</i>",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Harus dibagi menjadi delapan region",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Harus langsung di-<i>merge</i>",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Tidak dapat ditentukan",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Homogen sehingga tidak perlu di-<i>split</i>",
                        "url": None
                    }
                }

            ],

            "answer": "e"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
Perhatikan potongan kode dibawah, Program tersebut digunakan untuk....
""",
                "URL": "/static/img/sub5/aktivitas13/soal_nomor3.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "Menentukan posisi region",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menghitung ukuran region",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Mengecek homogenitas suatu region",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menghitung jumlah region",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Menentukan warna region",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Perhatikan potongan gambar di bawah, Tujuan dari kode tersebut adalah....
""",
                "URL": "/static/img/sub5/aktivitas13/soal_nomor4.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "Membagi region menjadi empat bagian",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menghapus region yang terlalu kecil",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Mengubah citra menjadi <i>grayscales</i>",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menggabungkan dua region yang memiliki karakteristik serupa",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Menghitung histogram citra",
                        "url": None
                    }
                }

            ],

            "answer": "d"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            # question json
            question=json.dumps(item['question']),

            # options json
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='mudah',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Aktivitas 13 berhasil dibuat")
    

# Kuis 5
def kuis5_2():

    # =========================
    # CREATE QUIZ
    # =========================
    activity = Activity(
        id_class=2,
        title='Kuis-5',
        type='kuis',
        durasi_pengerjaan=15,
        jumlah_soal=10,
        id_topic=5,
        id_subtopic=23,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": """
Perhatikan pernyataan berikut.

<ol class="custom-number mt-2 mb-3">
<li>Setiap region harus memenuhi kriteria homogenitas.</li>
<li>Region dapat dibentuk berdasarkan kesamaan warna atau tekstur.</li>
<li>Dua region yang tidak homogen dapat digabungkan menjadi satu region.</li>
</ol>

Pernyataan yang benar mengenai <i>Region-Based Segmentation</i> adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "1 saja",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "2 saja",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "1 dan 2",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "2 dan 3",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "1, 2, dan 3",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
                "text": """
Perhatikan hasil pengujian homogenitas berikut.

\\[
Q(R_1)=TRUE
\\]

\\[
Q(R_2)=TRUE
\\]

\\[
Q(R_1 \\cup R_2)=TRUE
\\]

Berdasarkan hasil tersebut, maka....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "R₁ dan R₂ harus dipecah menjadi empat subregion",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "R₁ dan R₂ dapat digabung menjadi satu region",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "R₁ harus dihapus",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "R₂ harus diberi label baru",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Region dianggap tidak homogen",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
Pada <i>Region Growing</i> digunakan <i>seed point</i> dengan intensitas 120 dan threshold sebesar 10.

Piksel yang memenuhi <i>predicate similarity</i> adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "132",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "135",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "125",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "106",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "104",
                        "url": None
                    }
                }

            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Perhatikan potongan gambar dibawah, Fungsi variabel <code class="code-python">seed_value</code> pada program tersebut adalah....
""",
                "URL": "/static/img/sub5/kuis5/soal_nomor4.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "Menyimpan ukuran citra",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menyimpan nilai intensitas acuan dari seed point",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Menyimpan koordinat seluruh piksel",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menentukan jumlah region",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Menentukan warna hasil segmentasi",
                        "url": None
                    }
                }

            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 5
        # =====================================
        {
            "question": {
                "text": """
Perhatikan potongan gambar di bawah. Variabel <code class="code-python">visited</code> digunakan untuk....
""",
                "URL": "/static/img/sub5/kuis5/soal_nomor5.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "Menyimpan citra hasil segmentasi",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menentukan seed point",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Menyimpan histogram citra",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menyimpan piksel yang sudah diperiksa selama proses Region Growing",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Menghitung nilai threshold",
                        "url": None
                    }
                }

            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 6
        # =====================================
        {
            "question": {
                "text": """
Pada metode <i>Split and Merge</i>, region akan terus dibagi sampai....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Region memenuhi kriteria homogenitas atau mencapai ukuran minimum",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Semua region memiliki label yang sama",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Ukuran citra menjadi 1×1",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Jumlah region mencapai empat",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Semua piksel memiliki nilai yang sama",
                        "url": None
                    }
                }

            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 7
        # =====================================
        {
            "question": {
                "text": """
Diketahui suatu region memiliki nilai piksel:

\\[
\\{120,122,121,123\\}
\\]

Jika digunakan kriteria homogenitas:

\\[
\\max(R)-\\min(R)<10
\\]

maka kondisi region tersebut adalah....
""",
                "URL": None
            },

            "options": [

                {
                    "a": {
                        "teks": "Homogen",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Tidak homogen",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Harus dihapus",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Harus digabung",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Tidak dapat ditentukan",
                        "url": None
                    }
                }

            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 8
        # =====================================
        {
            "question": {
                "text": """
Perhatikan potongan gambar di bawah. Kondisi tersebut digunakan untuk....
""",
                "URL": "/static/img/sub5/kuis5/soal_nomor8.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "Menggabungkan dua region",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menentukan seed point",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Mengubah citra menjadi biner",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menghitung rata-rata intensitas",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Menghentikan proses splitting pada suatu region",
                        "url": None
                    }
                }

            ],

            "answer": "e"
        },

        # =====================================
        # SOAL 9
        # =====================================
        {
            "question": {
                "text": """
Perhatikan potongan gambar di bawah, Nilai <code class="code-python">mean1</code> dan <code class="code-python">mean2</code> digunakan sebagai dasar untuk....
""",
                "URL": "/static/img/sub5/kuis5/soal_nomor9.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "Menentukan ukuran citra",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Menghitung jumlah piksel",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Menentukan posisi region",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Mengevaluasi kemungkinan penggabungan antar region",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Membentuk histogram",
                        "url": None
                    }
                }

            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 10
        # =====================================
        {
            "question": {
                "text": """
Perhatikan potongan gambar di bawah, Baris program tersebut berfungsi untuk....
""",
                "URL": "/static/img/sub5/kuis5/soal_nomor10.png"
            },

            "options": [

                {
                    "a": {
                        "teks": "Membaca citra grayscales",
                        "url": None
                    }
                },

                {
                    "b": {
                        "teks": "Membentuk seed point",
                        "url": None
                    }
                },

                {
                    "c": {
                        "teks": "Membagi citra menjadi empat subregion",
                        "url": None
                    }
                },

                {
                    "d": {
                        "teks": "Menampilkan hasil segmentasi",
                        "url": None
                    }
                },

                {
                    "e": {
                        "teks": "Menggabungkan region yang memiliki karakteristik serupa",
                        "url": None
                    }
                }

            ],

            "answer": "e"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            # question json
            question=json.dumps(item['question']),

            # options json
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='sulit',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Kuis 5 berhasil dibuat")
    
# evaluasi
def evaluasi2():

    # =========================
    # CREATE EVALUASI
    # =========================
    activity = Activity(
        id_class=2,
        title='Evaluasi',
        type='evaluasi',
        durasi_pengerjaan=20,
        jumlah_soal=20,
        id_topic=6,
        id_subtopic=24,
        status='aktif'
    )

    db.session.add(activity)
    db.session.commit()

    # =========================
    # QUESTIONS
    # =========================
    questions = [

        # =====================================
        # SOAL 1
        # =====================================
        {
            "question": {
                "text": """
Citra digital merupakan ....
""",
                "URL": None
            },

            "options": [
                {"a": {"teks": "Representasi visual suatu objek dalam bentuk piksel yang dapat diolah komputer", "url": None}},
                {"b": {"teks": "Kumpulan region hasil segmentasi", "url": None}},
                {"c": {"teks": "Kumpulan histogram citra", "url": None}},
                {"d": {"teks": "Hasil deteksi tepi", "url": None}},
                {"e": {"teks": "Kumpulan warna RGB", "url": None}}
            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 2
        # =====================================
        {
            "question": {
                "text": """
Perbedaan utama citra <i>grayscales</i> dan citra biner adalah ....
""",
                "URL": None
            },

            "options": [
                {"a": {"teks": "Citra biner memiliki tiga kanal warna", "url": None}},
                {"b": {"teks": "Citra grayscales memiliki rentang nilai keabuan, sedangkan citra biner hanya memiliki dua nilai intensitas", "url": None}},
                {"c": {"teks": "Citra grayscales memiliki lebih banyak piksel", "url": None}},
                {"d": {"teks": "Citra biner hanya digunakan pada segmentasi", "url": None}},
                {"e": {"teks": "Citra grayscales tidak memiliki intensitas", "url": None}}
            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 3
        # =====================================
        {
            "question": {
                "text": """
Tujuan utama segmentasi citra adalah ....
""",
                "URL": None
            },

            "options": [
                {"a": {"teks": "Mengubah citra menjadi RGB", "url": None}},
                {"b": {"teks": "Mengurangi ukuran file citra", "url": None}},
                {"c": {"teks": "Membagi citra menjadi bagian-bagian yang bermakna untuk mempermudah analisis", "url": None}},
                {"d": {"teks": "Menambah jumlah piksel", "url": None}},
                {"e": {"teks": "Memperbesar resolusi citra", "url": None}}
            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 4
        # =====================================
        {
            "question": {
                "text": """
Suatu segmentasi yang baik harus memenuhi syarat bahwa ....
""",
                "URL": None
            },

            "options": [
                {"a": {"teks": "Setiap region memiliki ukuran yang sama", "url": None}},
                {"b": {"teks": "Jumlah region harus genap", "url": None}},
                {"c": {"teks": "Setiap piksel harus memiliki intensitas berbeda", "url": None}},
                {"d": {"teks": "Setiap region memenuhi kriteria homogenitas yang ditentukan", "url": None}},
                {"e": {"teks": "Semua region harus berbentuk persegi", "url": None}}
            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 5
        # =====================================
        {
            "question": {
                "text": """
Pada <i>Edge-Based Segmentation</i>, objek dipisahkan dari background berdasarkan ....
""",
                "URL": None
            },

            "options": [
                {"a": {"teks": "Homogenitas warna", "url": None}},
                {"b": {"teks": "Nilai rata-rata histogram", "url": None}},
                {"c": {"teks": "Perubahan intensitas yang tajam pada batas objek", "url": None}},
                {"d": {"teks": "Posisi piksel", "url": None}},
                {"e": {"teks": "Jumlah region", "url": None}}
            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 6
        # =====================================
        {
            "question": {
                "text": """
Tahap pertama dalam <i>Edge-Based Segmentation</i> adalah ....
""",
                "URL": None
            },

            "options": [
                {"a": {"teks": "Edge Detection", "url": None}},
                {"b": {"teks": "Region Extraction", "url": None}},
                {"c": {"teks": "Thresholding", "url": None}},
                {"d": {"teks": "Region Growing", "url": None}},
                {"e": {"teks": "Region Merging", "url": None}}
            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 7
        # =====================================
        {
            "question": {
                "text": """
Proses yang bertujuan menghubungkan piksel-piksel tepi yang terputus sehingga membentuk batas objek yang lebih lengkap disebut....
""",
                "URL": None
            },

            "options": [
                {"a": {"teks": "Edge Detection", "url": None}},
                {"b": {"teks": "Region Extraction", "url": None}},
                {"c": {"teks": "Edge Linking", "url": None}},
                {"d": {"teks": "Thresholding", "url": None}},
                {"e": {"teks": "Region Growing", "url": None}}
            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 8
        # =====================================
        {
            "question": {
                "text": """
Hasil utama dari proses <i>Edge Detection</i> adalah ....
""",
                "URL": None
            },

            "options": [
                {"a": {"teks": "Histogram citra", "url": None}},
                {"b": {"teks": "Edge Map", "url": None}},
                {"c": {"teks": "Seed point", "url": None}},
                {"d": {"teks": "Label Region", "url": None}},
                {"e": {"teks": "Quadtree", "url": None}}
            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 9
        # =====================================
        {
            "question": {
                "text": """
Perhatikan potongan gambar di bawah. Variabel <code class="code-python">edges</code> digunakan untuk menyimpan ....
""",
                "URL": "/static/img/evaluasi/soal_nomor9.png"
            },

            "options": [
                {"a": {"teks": "Hasil segmentasi region", "url": None}},
                {"b": {"teks": "Hasil thresholding", "url": None}},
                {"c": {"teks": "Histogram citra", "url": None}},
                {"d": {"teks": "Hasil deteksi tepi", "url": None}},
                {"e": {"teks": "Seed point", "url": None}}
            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 10
        # =====================================
        {
            "question": {
                "text": """
Pada <i>Edge-Based Segmentation</i>, <i>region extraction</i> dilakukan setelah proses <i>edge linking</i> karena ....
""",
                "URL": None
            },

            "options": [
                {"a": {"teks": "Histogram harus dihitung terlebih dahulu", "url": None}},
                {"b": {"teks": "Seed point harus ditentukan terlebih dahulu", "url": None}},
                {"c": {"teks": "Edge map harus diubah menjadi RGB", "url": None}},
                {"d": {"teks": "Intensitas citra harus dinormalisasi", "url": None}},
                {"e": {"teks": "Batas objek perlu terbentuk terlebih dahulu sebelum wilayah objek diekstraksi", "url": None}}
            ],

            "answer": "e"
        },

        # =====================================
        # SOAL 11
        # =====================================
        {
            "question": {
                "text": """
<i>Threshold-Based Segmentation</i> memisahkan objek dan background berdasarkan ....
""",
                "URL": None
            },

            "options": [
                {"a": {"teks": "Perbandingan intensitas piksel terhadap nilai threshold", "url": None}},
                {"b": {"teks": "Bentuk objek", "url": None}},
                {"c": {"teks": "Posisi piksel", "url": None}},
                {"d": {"teks": "Jumlah tepi", "url": None}},
                {"e": {"teks": "Ukuran objek", "url": None}}
            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 12
        # =====================================
        {
            "question": {
                "text": """
Histogram digunakan dalam thresholding untuk ....
""",
                "URL": None
            },

            "options": [
                {"a": {"teks": "Menentukan seed point", "url": None}},
                {"b": {"teks": "Melihat distribusi intensitas piksel", "url": None}},
                {"c": {"teks": "Menghubungkan tepi", "url": None}},
                {"d": {"teks": "Menentukan connectivity", "url": None}},
                {"e": {"teks": "Membentuk region", "url": None}}
            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 13
        # =====================================
        {
            "question": {
                "text": """
Pada metode <i>Global Thresholding</i>, proses segmentasi dilakukan dengan cara ....
""",
                "URL": None
            },

            "options": [
                {"a": {"teks": "Menggunakan nilai threshold yang berbeda untuk setiap piksel", "url": None}},
                {"b": {"teks": "Menentukan nilai threshold berdasarkan seed point", "url": None}},
                {"c": {"teks": "Menggunakan satu nilai threshold yang sama untuk seluruh citra", "url": None}},
                {"d": {"teks": "Mengelompokkan piksel menggunakan region growing", "url": None}},
                {"e": {"teks": "Membagi citra menggunakan struktur quadtree", "url": None}}
            ],

            "answer": "c"
        },

        # =====================================
        # SOAL 14
        # =====================================
        {
            "question": {
                "text": """
Perhatikan potongan gambar di bawah. Nilai <code class="code-python">127</code> pada kode di bawah berfungsi sebagai ....
""",
                "URL": "/static/img/evaluasi/soal_nomor14.png"
            },

            "options": [
                {"a": {"teks": "Nilai maksimum piksel", "url": None}},
                {"b": {"teks": "Ukuran kernel", "url": None}},
                {"c": {"teks": "Jumlah iterasi", "url": None}},
                {"d": {"teks": "Nilai threshold", "url": None}},
                {"e": {"teks": "Nilai rata-rata histogram", "url": None}}
            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 15
        # =====================================
        {
            "question": {
                "text": """
Penggunaan <code class="code-python">cv2.THRESH_OTSU</code> bertujuan untuk ....
""",
                "URL": None
            },

            "options": [
                {"a": {"teks": "Menghubungkan tepi", "url": None}},
                {"b": {"teks": "Menentukan seed point", "url": None}},
                {"c": {"teks": "Membentuk region", "url": None}},
                {"d": {"teks": "Mengubah citra menjadi RGB", "url": None}},
                {"e": {"teks": "Menentukan threshold secara otomatis", "url": None}}
            ],

            "answer": "e"
        },

        # =====================================
        # SOAL 16
        # =====================================
        {
            "question": {
                "text": """
<i>Region-Based Segmentation</i> membentuk objek berdasarkan ....
""",
                "URL": None
            },

            "options": [
                {"a": {"teks": "Homogenitas karakteristik piksel dalam suatu region", "url": None}},
                {"b": {"teks": "Perubahan intensitas yang tajam", "url": None}},
                {"c": {"teks": "Histogram citra", "url": None}},
                {"d": {"teks": "Jumlah tepi", "url": None}},
                {"e": {"teks": "Ukuran objek", "url": None}}
            ],

            "answer": "a"
        },

        # =====================================
        # SOAL 17
        # =====================================
        {
            "question": {
                "text": """
Pada <i>Region Growing</i>, piksel dapat bergabung ke dalam region apabila ....
""",
                "URL": None
            },

            "options": [
                {"a": {"teks": "Memiliki intensitas terbesar", "url": None}},
                {"b": {"teks": "Memenuhi similarity dan connectivity", "url": None}},
                {"c": {"teks": "Berada pada baris yang sama dengan seed point", "url": None}},
                {"d": {"teks": "Berada di tepi citra", "url": None}},
                {"e": {"teks": "Memiliki ukuran yang sama dengan seed point", "url": None}}
            ],

            "answer": "b"
        },

        # =====================================
        # SOAL 18
        # =====================================
        {
            "question": {
                "text": """
Perhatikan potongan gambar di bawah. Variabel <code class="code-python">queue</code> digunakan untuk ....
""",
                "URL": "/static/img/evaluasi/soal_nomor18.png"
            },

            "options": [
                {"a": {"teks": "Menyimpan histogram", "url": None}},
                {"b": {"teks": "Menyimpan hasil segmentasi", "url": None}},
                {"c": {"teks": "Menyimpan label region", "url": None}},
                {"d": {"teks": "Menentukan threshold", "url": None}},
                {"e": {"teks": "Menyimpan piksel yang akan diperiksa selama pertumbuhan region", "url": None}}
            ],

            "answer": "e"
        },

        # =====================================
        # SOAL 19
        # =====================================
        {
            "question": {
                "text": """
Pada metode <i>Split and Merge</i>, suatu region akan di-<i>split</i> apabila ....
""",
                "URL": None
            },

            "options": [
                {"a": {"teks": "Berada pada tepi citra", "url": None}},
                {"b": {"teks": "Memiliki ukuran besar", "url": None}},
                {"c": {"teks": "Memiliki rata-rata intensitas tinggi", "url": None}},
                {"d": {"teks": "Tidak memenuhi kriteria homogenitas", "url": None}},
                {"e": {"teks": "Memiliki empat tetangga", "url": None}}
            ],

            "answer": "d"
        },

        # =====================================
        # SOAL 20
        # =====================================
        {
            "question": {
                "text": """
Perhatikan potongan gambar di bawah. Baris program tersebut digunakan untuk ....
""",
                "URL": "/static/img/evaluasi/soal_nomor20.png"
            },

            "options": [
                {"a": {"teks": "Membaca citra", "url": None}},
                {"b": {"teks": "Menentukan seed point", "url": None}},
                {"c": {"teks": "Membentuk histogram", "url": None}},
                {"d": {"teks": "Membagi region", "url": None}},
                {"e": {"teks": "Menggabungkan region yang memiliki karakteristik serupa", "url": None}}
            ],

            "answer": "e"
        }

    ]

    # =========================
    # INSERT QUESTIONS
    # =========================
    for item in questions:

        question = Question(
            type='mc',

            # question json
            question=json.dumps(item['question']),

            # options json
            MC_option=json.dumps(item['options']),

            MC_Answer=item['answer'],
            tingkat_kesulitan='sulit',
            created_by=41
        )

        db.session.add(question)
        db.session.commit()

        # =========================
        # RELASI ACTIVITY QUESTION
        # =========================
        activity_question = ActivityQuestion(
            id_activity=activity.id,
            id_question=question.id
        )

        db.session.add(activity_question)

    db.session.commit()

    print("✅ Evaluasi berhasil dibuat")