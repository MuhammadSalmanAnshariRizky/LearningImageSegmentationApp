import json
from app import create_app, db
from app.model.question import Question
from app.model.activity import Activity
from app.model.activity_question import ActivityQuestion


def seed_question():
    data = [
        {
            "question": {"text": "Pengertian citra digital adalah…", "URL": None},
            "options": [
                {"a": {"teks": "Gambar yang hanya dapat dilihat secara langsung tanpa perangkat elektronik", "url": None}},
                {"b": {"teks": "Representasi visual dari dunia nyata dalam bentuk digital yang dapat dipahami dan diolah oleh komputer", "url": None}},
                {"c": {"teks": "Gambar yang hanya tersimpan dalam bentuk cetakan kertas", "url": None}},
                {"d": {"teks": "Kumpulan warna tanpa nilai numerik", "url": None}},
                {"e": {"teks": "Gambar yang hanya dapat dibuat melalui lukisan tangan", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {"text": "Elemen terkecil yang menyusun sebuah citra digital disebut…", "URL": None},
            "options": [
                {"a": {"teks": "Bit", "url": None}},
                {"b": {"teks": "Layer", "url": None}},
                {"c": {"teks": "Frame", "url": None}},
                {"d": {"teks": "Pixel", "url": None}},
                {"e": {"teks": "Vector", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {"text": "Dalam representasi matematis citra digital f(x,y), nilai f(x,y) menunjukkan…", "URL": None},
            "options": [
                {"a": {"teks": "Ukuran citra digital", "url": None}},
                {"b": {"teks": "Posisi baris dan kolom citra", "url": None}},
                {"c": {"teks": "Nilai intensitas atau tingkat kecerahan pada suatu pixel", "url": None}},
                {"d": {"teks": "Jumlah pixel dalam citra", "url": None}},
                {"e": {"teks": "Jenis warna pada gambar", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {"text": "Jika sebuah citra digital memiliki ukuran M × N, maka yang dimaksud dengan M adalah…", "URL": None},
            "options": [
                {"a": {"teks": "Jumlah baris dalam citra", "url": None}},
                {"b": {"teks": "Jumlah kolom dalam citra", "url": None}},
                {"c": {"teks": "Nilai intensitas maksimum", "url": None}},
                {"d": {"teks": "Jumlah warna dalam citra", "url": None}},
                {"e": {"teks": "Jumlah total pixel dalam citra", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {"text": "Citra digital yang hanya memiliki satu kanal (channel) dan menampilkan tingkat terang–gelap tanpa informasi warna disebut …", "URL": None},
            "options": [
                {"a": {"teks": "Citra RGB", "url": None}},
                {"b": {"teks": "Citra biner", "url": None}},
                {"c": {"teks": "Citra grayscale", "url": None}},
                {"d": {"teks": "Citra vektor", "url": None}},
                {"e": {"teks": "Citra multispektral", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {"text": "Pada citra RGB, setiap piksel umumnya terdiri dari tiga komponen warna (R, G, B). Jika masing-masing komponen menggunakan 8 bit, maka jumlah bit dalam satu piksel adalah …", "URL": None},
            "options": [
                {"a": {"teks": "24 bit", "url": None}},
                {"b": {"teks": "32 bit", "url": None}},
                {"c": {"teks": "8 bit", "url": None}},
                {"d": {"teks": "16 bit", "url": None}},
                {"e": {"teks": "64 bit", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {"text": "Perhatikan karakteristik berikut: Hanya memiliki dua nilai piksel, biasanya direpresentasikan dengan 0 dan 1, digunakan pada dokumen hasil scan hitam-putih. Jenis citra yang sesuai adalah …", "URL": None},
            "options": [
                {"a": {"teks": "Citra grayscale", "url": None}},
                {"b": {"teks": "Citra RGB", "url": None}},
                {"c": {"teks": "Citra 3D", "url": None}},
                {"d": {"teks": "Citra analog", "url": None}},
                {"e": {"teks": "Citra biner", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {
                "text": """
                <p>Diketahui sebuah citra RGB berukuran 2×2 piksel dengan nilai sebagai berikut:</p>
                <p>
                \\[
                R =
                \\begin{bmatrix}
                100 & 150 \\\\
                200 & 50
                \\end{bmatrix}
                \\quad
                G =
                \\begin{bmatrix}
                120 & 130 \\\\
                180 & 60
                \\end{bmatrix}
                \\quad
                B =
                \\begin{bmatrix}
                80 & 110 \\\\
                160 & 40
                \\end{bmatrix}
                \\]
                </p>
                <p>Jika dilakukan konversi ke grayscale menggunakan metode rata-rata:</p>
                <p>
                \\[
                y = \\frac{R + G + B}{3}
                \\]
                </p>
                <p>Maka nilai grayscale pada f(1,0) adalah …</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "190", "url": None}},
                {"b": {"teks": "185", "url": None}},
                {"c": {"teks": "200", "url": None}},
                {"d": {"teks": "180", "url": None}},
                {"e": {"teks": "165", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {
                "text": """
                <p>Segmentasi citra membagi suatu citra menjadi beberapa wilayah \\( R_1, R_2, ..., R_n \\).</p>
                <p>Pernyataan yang tepat terkait hasil penggabungan seluruh wilayah tersebut adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Hanya sebagian citra yang terbentuk kembali", "url": None}},
                {"b": {"teks": "Menghasilkan citra baru yang berbeda", "url": None}},
                {"c": {"teks": "Menghasilkan seluruh citra tanpa ada piksel yang tertinggal", "url": None}},
                {"d": {"teks": "Menghilangkan piksel yang tidak penting", "url": None}},
                {"e": {"teks": "Mengubah ukuran citra", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {
                "text": """
                <p>Dalam segmentasi citra, setiap wilayah \\( R_i \\) harus merupakan <i>connected set</i>.</p>
                <p>Artinya adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Setiap wilayah boleh terdiri dari piksel yang terpisah", "url": None}},
                {"b": {"teks": "Piksel dalam satu wilayah harus saling terhubung", "url": None}},
                {"c": {"teks": "Wilayah harus memiliki warna yang berbeda", "url": None}},
                {"d": {"teks": "Setiap piksel harus memiliki nilai berbeda", "url": None}},
                {"e": {"teks": "Wilayah harus berbentuk persegi", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {
                "text": """
                <p>Perhatikan aturan segmentasi berikut:</p>
                <p>
                \\[
                R_i \\cap R_j = \\emptyset, \\quad i \\neq j
                \\]
                </p>
                <p>Makna dari aturan tersebut adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Tidak boleh ada piksel yang menjadi anggota dua wilayah sekaligus", "url": None}},
                {"b": {"teks": "Setiap wilayah harus memiliki ukuran yang sama", "url": None}},
                {"c": {"teks": "Wilayah boleh saling beririsan sebagian", "url": None}},
                {"d": {"teks": "Semua wilayah harus memiliki nilai intensitas sama", "url": None}},
                {"e": {"teks": "Semua wilayah harus saling terhubung", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {
                "text": """
                <p>Dalam segmentasi citra, predikat \\( Q(R_i) \\) digunakan sebagai kriteria homogenitas.</p>
                <p>Jika suatu wilayah memiliki nilai piksel yang tidak seragam, maka…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Segmentasi tetap valid", "url": None}},
                {"b": {"teks": "Wilayah tersebut dianggap homogen", "url": None}},
                {"c": {"teks": "Nilai Q(R_i) = TRUE", "url": None}},
                {"d": {"teks": "Nilai Q(R_i) = FALSE", "url": None}},
                {"e": {"teks": "Wilayah harus digabung dengan wilayah lain", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {
                "text": """
                <p>Pendekatan <i>edge-based segmentation</i> digunakan dengan cara…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Mengelompokkan piksel berdasarkan warna yang sama", "url": None}},
                {"b": {"teks": "Mengelompokkan piksel berdasarkan tekstur", "url": None}},
                {"c": {"teks": "Menghitung rata-rata nilai piksel", "url": None}},
                {"d": {"teks": "Membagi citra menjadi blok-blok kecil tanpa melihat intensitas", "url": None}},
                {"e": {"teks": "Mendeteksi perubahan intensitas yang tajam sebagai batas wilayah", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {
                "text": """
                <p>Pada kondisi citra yang memiliki banyak tekstur dan perubahan intensitas kecil, metode yang lebih tepat digunakan adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Edge-based segmentation", "url": None}},
                {"b": {"teks": "Thresholding sederhana", "url": None}},
                {"c": {"teks": "Region-based segmentation", "url": None}},
                {"d": {"teks": "Histogram equalization", "url": None}},
                {"e": {"teks": "Filtering citra", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {
                "text": """
                <p>Perbedaan utama antara <i>edge-based</i> dan <i>region-based segmentation</i> adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Edge-based menggunakan warna, region-based menggunakan bentuk", "url": None}},
                {"b": {"teks": "Edge-based melihat batas perubahan intensitas, sedangkan region-based mengelompokkan piksel yang seragam", "url": None}},
                {"c": {"teks": "Edge-based menggunakan blok piksel, region-based tidak", "url": None}},
                {"d": {"teks": "Edge-based hanya untuk citra berwarna", "url": None}},
                {"e": {"teks": "Region-based hanya untuk citra biner", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {
                "text": """
                <p>Dalam <i>region-based segmentation</i>, penggunaan standar deviasi bertujuan untuk…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Mengidentifikasi wilayah bertekstur dan tidak bertekstur", "url": None}},
                {"b": {"teks": "Menentukan posisi tepi objek", "url": None}},
                {"c": {"teks": "Mengukur perbedaan warna antar piksel", "url": None}},
                {"d": {"teks": "Mengubah citra menjadi biner", "url": None}},
                {"e": {"teks": "Mengurangi noise pada citra", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {
                "text": """
                <p>Konsep utama dari <i>edge-based segmentation</i> adalah….</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Mengelompokkan piksel berdasarkan warna yang sama", "url": None}},
                {"b": {"teks": "Menggunakan hasil deteksi tepi untuk membentuk batas objek pada citra", "url": None}},
                {"c": {"teks": "Mengurangi jumlah piksel dalam citra", "url": None}},
                {"d": {"teks": "Mengubah citra menjadi biner secara langsung", "url": None}},
                {"e": {"teks": "Menghapus noise pada citra", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {
                "text": """
                <p>Hasil deteksi tepi belum dapat langsung dianggap sebagai hasil segmentasi karena….</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Hasilnya terlalu gelap", "url": None}},
                {"b": {"teks": "Citra menjadi berwarna", "url": None}},
                {"c": {"teks": "Ukuran citra berubah", "url": None}},
                {"d": {"teks": "Tepi yang dihasilkan masih terpisah dan belum membentuk wilayah utuh", "url": None}},
                {"e": {"teks": "Nilai piksel menjadi sama semua", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {
                "text": """
                <p>Peran utama tepi (<i>edge</i>) dalam segmentasi citra adalah….</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Menunjukkan batas antara objek dengan latar belakang", "url": None}},
                {"b": {"teks": "Menambah jumlah piksel", "url": None}},
                {"c": {"teks": "Mengubah warna objek", "url": None}},
                {"d": {"teks": "Mengurangi resolusi citra", "url": None}},
                {"e": {"teks": "Menentukan ukuran citra", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {
                "text": """
                <p><i>Edge chain</i> tertutup dalam segmentasi citra berfungsi untuk….</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Menghilangkan noise pada citra", "url": None}},
                {"b": {"teks": "Mengubah citra menjadi grayscale", "url": None}},
                {"c": {"teks": "Membentuk kontur lengkap yang mengelilingi objek", "url": None}},
                {"d": {"teks": "Menghubungkan piksel yang tidak berhubungan", "url": None}},
                {"e": {"teks": "Mengurangi intensitas citra", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {
                "text": """
                <p>Pada proses <i>edge image thresholding</i>, tujuan utama penggunaan threshold adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Menambah jumlah piksel tepi", "url": None}},
                {"b": {"teks": "Mengubah citra grayscale menjadi RGB", "url": None}},
                {"c": {"teks": "Menghilangkan tepi dengan nilai kecil akibat noise", "url": None}},
                {"d": {"teks": "Menentukan arah gradien piksel", "url": None}},
                {"e": {"teks": "Menghitung magnitudo gradien", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {
                "text": """
                <p>Pada algoritma <i>Non-Maximal Suppression</i>, suatu piksel akan dihapus jika…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Bukan merupakan maksimum lokal pada arah tepi", "url": None}},
                {"b": {"teks": "Nilainya lebih besar dari semua tetangganya", "url": None}},
                {"c": {"teks": "Nilainya lebih kecil dari threshold rendah", "url": None}},
                {"d": {"teks": "Tidak memiliki arah gradien", "url": None}},
                {"e": {"teks": "Berada di tepi citra", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {
                "text": """
                <p>Jika suatu piksel memiliki arah gradien sebesar \\( 90^\\circ \\), maka piksel tersebut dibandingkan dengan…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Piksel kiri dan kanan", "url": None}},
                {"b": {"teks": "Piksel atas dan bawah", "url": None}},
                {"c": {"teks": "Piksel kanan atas dan kiri bawah", "url": None}},
                {"d": {"teks": "Piksel kiri atas dan kanan bawah", "url": None}},
                {"e": {"teks": "Semua tetangga (8 arah)", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {
                "text": """
                <p>Diketahui nilai threshold:</p>
                <p>
                \\[
                t_1 = 80 \\quad \\text{(threshold tinggi)}, \\quad
                t_0 = 40 \\quad \\text{(threshold rendah)}
                \\]
                </p>
                <p>Sebuah piksel memiliki nilai 50 dan tidak terhubung dengan piksel tepi kuat. Maka keputusan yang tepat adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Dipertahankan sebagai tepi kuat", "url": None}},
                {"b": {"teks": "Dipertahankan sebagai tepi lemah", "url": None}},
                {"c": {"teks": "Diubah menjadi tepi kuat", "url": None}},
                {"d": {"teks": "Dihapus (dianggap bukan tepi)", "url": None}},
                {"e": {"teks": "Diubah menjadi nilai maksimum", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {
                "text": """
                <p>Dalam algoritma <i>inner boundary tracing</i>, cara menentukan piksel awal \\( P_0 \\) adalah ....</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Piksel dengan nilai terbesar dalam region", "url": None}},
                {"b": {"teks": "Piksel pertama yang ditemukan secara acak", "url": None}},
                {"c": {"teks": "Piksel dengan kolom terkecil dan baris terkecil dalam region", "url": None}},
                {"d": {"teks": "Piksel yang berada di tengah region", "url": None}},
                {"e": {"teks": "Piksel dengan jumlah tetangga terbanyak", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {
                "text": """
                <p>Pada pencarian tetangga menggunakan <i>8-connectivity</i>, arah pencarian dilakukan dengan cara ....</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Searah jarum jam mulai dari atas", "url": None}},
                {"b": {"teks": "Berlawanan arah jarum jam mulai dari arah tertentu berdasarkan <i>dir</i>", "url": None}},
                {"c": {"teks": "Secara acak hingga menemukan piksel yang sesuai", "url": None}},
                {"d": {"teks": "Hanya ke arah horizontal dan vertikal", "url": None}},
                {"e": {"teks": "Selalu dimulai dari arah kanan", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {
                "text": """
                <p>Kondisi berhenti (<i>stopping condition</i>) pada <i>inner boundary tracing</i> terjadi ketika ....</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Semua piksel sudah diperiksa", "url": None}},
                {"b": {"teks": "Piksel saat ini sama dengan piksel awal", "url": None}},
                {"c": {"teks": "Tidak ditemukan piksel tetangga yang bernilai sama", "url": None}},
                {"d": {"teks": "Iterasi mencapai batas maksimum", "url": None}},
                {"e": {"teks": "Piksel saat ini sama dengan piksel kedua dan piksel sebelumnya sama dengan piksel awal", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {
                "text": """
                <p>Dalam <i>extended boundary</i>, perlakuan terhadap piksel <b>RIGHT</b> adalah ....</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Tidak mengalami perubahan posisi", "url": None}},
                {"b": {"teks": "Digeser ke atas satu piksel", "url": None}},
                {"c": {"teks": "Digeser ke kanan satu piksel", "url": None}},
                {"d": {"teks": "Digeser ke bawah satu piksel", "url": None}},
                {"e": {"teks": "Digeser ke bawah dan ke kanan", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {
                "text": """
                <p><i>Graylevel Thresholding</i> digunakan untuk memisahkan objek dan latar belakang pada citra berdasarkan nilai intensitas piksel dengan bantuan nilai ambang (<i>threshold</i>).</p>
                <p>Prinsip utama metode ini adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Mengubah citra menjadi berwarna", "url": None}},
                {"b": {"teks": "Membandingkan nilai piksel dengan threshold", "url": None}},
                {"c": {"teks": "Menghilangkan seluruh noise", "url": None}},
                {"d": {"teks": "Memperbesar ukuran citra", "url": None}},
                {"e": {"teks": "Mengubah format citra", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {
                "text": """
                <p>Jika suatu piksel memiliki nilai intensitas lebih besar dari threshold \\( T \\), maka pada citra biner hasil thresholding piksel tersebut akan bernilai…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "0 (background)", "url": None}},
                {"b": {"teks": "Tetap seperti semula", "url": None}},
                {"c": {"teks": "255 (warna putih)", "url": None}},
                {"d": {"teks": "1 (objek)", "url": None}},
                {"e": {"teks": "Tidak diproses", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {
                "text": """
                <p>Metode thresholding sederhana banyak digunakan karena memiliki kelebihan utama yaitu…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Hasil selalu sempurna", "url": None}},
                {"b": {"teks": "Proses sangat kompleks", "url": None}},
                {"c": {"teks": "Cepat dan ringan secara komputasi", "url": None}},
                {"d": {"teks": "Hanya untuk citra berwarna", "url": None}},
                {"e": {"teks": "Membutuhkan data besar", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {
                "text": """
                <p>Jika nilai threshold \\( T = 150 \\), maka piksel dengan nilai intensitas kurang dari atau sama dengan 150 akan diklasifikasikan sebagai…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Background (0)", "url": None}},
                {"b": {"teks": "Objek (255)", "url": None}},
                {"c": {"teks": "Objek (1)", "url": None}},
                {"d": {"teks": "Tidak berubah", "url": None}},
                {"e": {"teks": "Noise", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {
                "text": """
                <p>Dalam proses segmentasi citra, terdapat metode yang menggunakan satu nilai <i>threshold</i> untuk seluruh piksel pada citra tanpa membedakan posisi atau area tertentu.</p>
                <p>Metode tersebut dikenal sebagai…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Global thresholding", "url": None}},
                {"b": {"teks": "Multi-thresholding", "url": None}},
                {"c": {"teks": "Adaptive thresholding", "url": None}},
                {"d": {"teks": "Band thresholding", "url": None}},
                {"e": {"teks": "Edge detection", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {
                "text": """
                <p>Pada beberapa citra, pencahayaan tidak merata sehingga penggunaan satu nilai <i>threshold</i> tidak cukup baik.</p>
                <p>Oleh karena itu digunakan metode yang menentukan nilai threshold berdasarkan bagian tertentu dari citra. Metode ini disebut…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Global thresholding", "url": None}},
                {"b": {"teks": "Histogram equalization", "url": None}},
                {"c": {"teks": "Adaptive thresholding", "url": None}},
                {"d": {"teks": "Band thresholding", "url": None}},
                {"e": {"teks": "Filtering", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {
                "text": """
                <p>Suatu metode thresholding memilih piksel sebagai objek jika nilainya berada dalam suatu rentang intensitas tertentu, bukan hanya berdasarkan satu nilai ambang.</p>
                <p>Metode tersebut adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Global thresholding", "url": None}},
                {"b": {"teks": "Band thresholding", "url": None}},
                {"c": {"teks": "Adaptive thresholding", "url": None}},
                {"d": {"teks": "Binary thresholding", "url": None}},
                {"e": {"teks": "Edge detection", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {
                "text": """
                <p>Dalam segmentasi citra, terdapat metode yang membagi piksel ke dalam beberapa kelas berdasarkan beberapa rentang nilai intensitas, sehingga tidak hanya menghasilkan dua kelas saja.</p>
                <p>Metode ini dikenal sebagai…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Global thresholding", "url": None}},
                {"b": {"teks": "Band thresholding", "url": None}},
                {"c": {"teks": "Adaptive thresholding", "url": None}},
                {"d": {"teks": "Multi-thresholding", "url": None}},
                {"e": {"teks": "Smoothing", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {
                "text": """
                <p>Dalam menentukan nilai threshold menggunakan metode <i>p-tile</i>, diperlukan informasi awal mengenai proporsi objek terhadap keseluruhan citra.</p>
                <p>Informasi tersebut digunakan untuk…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Menentukan warna objek", "url": None}},
                {"b": {"teks": "Menentukan jumlah piksel citra", "url": None}},
                {"c": {"teks": "Memilih nilai threshold berdasarkan persentase piksel tertentu", "url": None}},
                {"d": {"teks": "Mengubah citra menjadi biner secara langsung", "url": None}},
                {"e": {"teks": "Menghapus noise pada citra", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {
                "text": """
                <p>Histogram citra sering digunakan untuk membantu menentukan nilai threshold. Jika histogram memiliki dua puncak yang jelas (<i>bimodal</i>), maka nilai threshold yang baik biasanya dipilih…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Pada nilai maksimum histogram", "url": None}},
                {"b": {"teks": "Pada salah satu puncak histogram", "url": None}},
                {"c": {"teks": "Di tengah salah satu kelompok piksel", "url": None}},
                {"d": {"teks": "Pada lembah di antara dua puncak", "url": None}},
                {"e": {"teks": "Pada nilai keabuan tertinggi", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {
                "text": """
                <p>Dalam beberapa kasus, bentuk histogram tidak jelas karena adanya piksel pada batas objek dan <i>background</i>.</p>
                <p>Salah satu cara mengatasinya adalah dengan…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Menghapus seluruh piksel batas", "url": None}},
                {"b": {"teks": "Memberikan bobot agar pengaruh piksel batas berkurang", "url": None}},
                {"c": {"teks": "Mengubah citra menjadi berwarna", "url": None}},
                {"d": {"teks": "Menggunakan satu threshold tetap", "url": None}},
                {"e": {"teks": "Mengabaikan histogram", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {
                "text": """
                <p>Algoritma Otsu menentukan nilai threshold secara otomatis dengan memilih nilai yang menghasilkan pemisahan terbaik antara objek dan <i>background</i>.</p>
                <p>Kriteria yang digunakan adalah…</p>
                <p>
                \\[
                \\text{Variansi dalam kelas (intra-class variance) dibuat sekecil mungkin}
                \\]
                </p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Variansi dalam setiap kelas sekecil mungkin", "url": None}},
                {"b": {"teks": "Nilai intensitas maksimum", "url": None}},
                {"c": {"teks": "Jumlah piksel terbanyak", "url": None}},
                {"d": {"teks": "Warna citra", "url": None}},
                {"e": {"teks": "Ukuran citra", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {
                "text": """
                <p>Tujuan utama dari <i>region-based segmentation</i> adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Mendeteksi tepi objek secara tajam", "url": None}},
                {"b": {"teks": "Membagi citra menjadi region dengan ukuran sama", "url": None}},
                {"c": {"teks": "Meningkatkan kontras citra", "url": None}},
                {"d": {"teks": "Menghilangkan noise pada citra", "url": None}},
                {"e": {"teks": "Membagi citra menjadi region yang homogen", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {
                "text": """
                <p>Metode <i>region growing</i> lebih efektif digunakan pada citra yang memiliki noise karena…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Tidak memerlukan perhitungan intensitas", "url": None}},
                {"b": {"teks": "Tidak bergantung pada batas objek", "url": None}},
                {"c": {"teks": "Dapat memperbesar ukuran citra", "url": None}},
                {"d": {"teks": "Hanya menggunakan warna sebagai parameter", "url": None}},
                {"e": {"teks": "Tidak memerlukan piksel awal", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {
                "text": """
                <p>Diketahui fungsi homogenitas \\( Q(R_i) \\).</p>
                <p>Pernyataan yang tepat untuk \\( Q(R_i) = TRUE \\) adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Region R_i dapat digabung dengan semua region lain", "url": None}},
                {"b": {"teks": "Region R_i tidak memiliki batas yang jelas", "url": None}},
                {"c": {"teks": "Region R_i memiliki ukuran terbesar dalam citra", "url": None}},
                {"d": {"teks": "Region R_i memenuhi kriteria homogenitas", "url": None}},
                {"e": {"teks": "Region R_i terdiri dari beberapa region kecil", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {
                "text": """
                <p>Diketahui dua region bertetangga \\( R_i \\) dan \\( R_j \\).</p>
                <p>Jika \\( Q(R_i \\cup R_j) = FALSE \\), maka…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Kedua region dapat digabung menjadi satu region", "url": None}},
                {"b": {"teks": "Kedua region memiliki nilai homogenitas yang sama", "url": None}},
                {"c": {"teks": "Penggabungan kedua region tidak memenuhi kriteria homogenitas", "url": None}},
                {"d": {"teks": "Kedua region tidak memiliki hubungan spasial", "url": None}},
                {"e": {"teks": "Kedua region harus dihapus dari citra", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {
                "text": """
                <p>Pada metode <i>region merging</i>, kondisi berikut harus dipenuhi agar suatu region valid:</p>
                <p>
                \\[
                Q(R_i) = TRUE
                \\]
                </p>
                <p>Makna dari kondisi tersebut adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Region tidak memiliki batas", "url": None}},
                {"b": {"teks": "Region dapat digabung dengan semua region lain", "url": None}},
                {"c": {"teks": "Region memiliki karakteristik homogen", "url": None}},
                {"d": {"teks": "Region memiliki ukuran terbesar", "url": None}},
                {"e": {"teks": "Region memiliki nilai acak", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {
                "text": """
                <p>Dua region \\( R_i \\) dan \\( R_j \\) dapat digabung jika memenuhi kriteria:</p>
                <p>
                \\[
                |\\mu_i - \\mu_j| \\le 5
                \\]
                </p>
                <p>Jika diketahui \\( \\mu_i = 20 \\) dan \\( \\mu_j = 24 \\), maka keputusan yang benar adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Tidak dapat digabung karena selisih terlalu besar", "url": None}},
                {"b": {"teks": "Dapat digabung karena selisih memenuhi kriteria", "url": None}},
                {"c": {"teks": "Tidak dapat digabung karena tidak bertetangga", "url": None}},
                {"d": {"teks": "Dapat digabung tanpa syarat", "url": None}},
                {"e": {"teks": "Harus dipecah menjadi region baru", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {
                "text": """
                <p>Dalam proses <i>region merging</i>, penggabungan hanya dilakukan pada region yang…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Memiliki ukuran yang sama", "url": None}},
                {"b": {"teks": "Memiliki bentuk yang sama", "url": None}},
                {"c": {"teks": "Memiliki warna berbeda", "url": None}},
                {"d": {"teks": "Bertetangga dan memenuhi kriteria homogenitas", "url": None}},
                {"e": {"teks": "Berada di posisi yang sama", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {
                "text": """
                <p>Berdasarkan hasil validasi, jika semua pasangan region bertetangga memiliki:</p>
                <p>
                \\[
                |\\mu_i - \\mu_j| > 5
                \\]
                </p>
                <p>Maka kesimpulan yang tepat adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Tidak ada region yang dapat digabung dan proses berhenti", "url": None}},
                {"b": {"teks": "Proses segmentasi dilanjutkan", "url": None}},
                {"c": {"teks": "Region harus dipecah kembali", "url": None}},
                {"d": {"teks": "Semua region harus digabung", "url": None}},
                {"e": {"teks": "Semua region dianggap tidak valid", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {
                "text": """
                <p>Pada metode <i>split and merge</i>, proses penggabungan (<i>merging</i>) antara dua region bertetangga dapat dilakukan apabila memenuhi kondisi…</p>
                <p>
                \\[
                Q(R_i \\cup R_j)
                \\]
                </p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Q(R_i \\cup R_j) = FALSE", "url": None}},
                {"b": {"teks": "Q(R_i \\cup R_j) = TRUE", "url": None}},
                {"c": {"teks": "Q(R_i) = FALSE", "url": None}},
                {"d": {"teks": "Kedua region memiliki ukuran berbeda", "url": None}},
                {"e": {"teks": "Salah satu region tidak homogen", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {
                "text": """
                <p>Dalam metode <i>split and merge</i>, apabila suatu region tidak memenuhi kriteria homogenitas, maka tindakan yang dilakukan terhadap region tersebut adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Menghapus region tersebut dari citra", "url": None}},
                {"b": {"teks": "Menggabungkan dengan semua region lain", "url": None}},
                {"c": {"teks": "Membagi region menjadi empat subregion", "url": None}},
                {"d": {"teks": "Mengubah nilai piksel menjadi sama", "url": None}},
                {"e": {"teks": "Mengabaikan region tersebut", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {
                "text": """
                <p>Dalam proses <i>merging</i>, empat region yang memiliki parent yang sama dapat digabungkan menjadi satu region apabila memenuhi kondisi…</p>
                <p>
                \\[
                Q(R_1 \\cup R_2 \\cup R_3 \\cup R_4)
                \\]
                </p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Q(R_1 \\cup R_2 \\cup R_3 \\cup R_4) = FALSE", "url": None}},
                {"b": {"teks": "Region berada pada level yang berbeda", "url": None}},
                {"c": {"teks": "Semua region memiliki ukuran berbeda", "url": None}},
                {"d": {"teks": "Tidak ada perbedaan nilai piksel", "url": None}},
                {"e": {"teks": "Q(R_1 \\cup R_2 \\cup R_3 \\cup R_4) = TRUE", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {
                "text": """
                <p>Struktur data yang digunakan untuk merepresentasikan hasil segmentasi pada metode <i>split and merge</i> dalam bentuk pohon adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Linked List", "url": None}},
                {"b": {"teks": "Stack", "url": None}},
                {"c": {"teks": "Binary Tree", "url": None}},
                {"d": {"teks": "Segmentation Quadtree", "url": None}},
                {"e": {"teks": "Array satu dimensi", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {
                "text": """
                <p>Pada tahap <i>post-processing</i> dalam segmentasi citra, tujuan utama dilakukan perbaikan hasil segmentasi adalah untuk…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Mengubah ukuran citra menjadi lebih kecil", "url": None}},
                {"b": {"teks": "Mengurangi kompleksitas algoritma utama", "url": None}},
                {"c": {"teks": "Memperbaiki hasil segmentasi yang terlalu banyak atau terlalu sedikit region", "url": None}},
                {"d": {"teks": "Menghilangkan seluruh noise tanpa proses tambahan", "url": None}},
                {"e": {"teks": "Mengganti metode segmentasi yang digunakan", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {
                "text": """
                <p>Pada metode <i>boundary elimination</i>, batas antar region akan dihilangkan berdasarkan…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Jumlah piksel pada setiap region", "url": None}},
                {"b": {"teks": "Warna dominan citra", "url": None}},
                {"c": {"teks": "Ukuran citra secara keseluruhan", "url": None}},
                {"d": {"teks": "Perbedaan kontras dan perubahan arah pada batas", "url": None}},
                {"e": {"teks": "Posisi region dalam citra", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {
                "text": """
                <p>Dalam algoritma <i>removal of small image regions</i>, langkah pertama yang dilakukan adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Mencari region dengan ukuran piksel paling kecil", "url": None}},
                {"b": {"teks": "Menentukan region dengan nilai intensitas tertinggi", "url": None}},
                {"c": {"teks": "Menggabungkan semua region bertetangga", "url": None}},
                {"d": {"teks": "Menghapus seluruh region kecil secara langsung", "url": None}},
                {"e": {"teks": "Mengurutkan region berdasarkan posisi", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {
                "text": """
                <p>Proses penggabungan region kecil dilakukan secara berulang hingga kondisi berikut terpenuhi, yaitu…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "Semua region memiliki ukuran yang sama", "url": None}},
                {"b": {"teks": "Tidak ada lagi region yang memenuhi kriteria homogenitas", "url": None}},
                {"c": {"teks": "Seluruh region telah digabung menjadi satu", "url": None}},
                {"d": {"teks": "Semua nilai piksel menjadi seragam", "url": None}},
                {"e": {"teks": "Tidak ada lagi region yang ukurannya lebih kecil dari batas minimum yang ditentukan", "url": None}}
            ],
            "answer": "e"
        }
    ]

    for item in data:
        q = Question(
            type="mc",
            question=json.dumps(item["question"]),
            MC_option=json.dumps(item["options"]),
            MC_Answer=item["answer"],
            tingkat_kesulitan="mudah",
            created_by=3
        )
        db.session.add(q)

    db.session.commit()
    print("✅ Seeder question berhasil!")


def seed_activity(class_id):
    data = [
        # Topic 1
        {"title": "aktivitas 1", "type": "aktivitas", "jumlah_soal": 4, "id_topic": 1, "id_subtopic": 1},
        {"title": "aktivitas 2", "type": "aktivitas", "jumlah_soal": 4, "id_topic": 1, "id_subtopic": 2},

        # Topic 2
        {"title": "aktivitas 3", "type": "aktivitas", "jumlah_soal": 4, "id_topic": 2, "id_subtopic": 5},
        {"title": "aktivitas 4", "type": "aktivitas", "jumlah_soal": 4, "id_topic": 2, "id_subtopic": 6},

        # Topic 3
        {"title": "aktivitas 5", "type": "aktivitas", "jumlah_soal": 4, "id_topic": 3, "id_subtopic": 9},
        {"title": "aktivitas 6", "type": "aktivitas", "jumlah_soal": 4, "id_topic": 3, "id_subtopic": 10},
        {"title": "aktivitas 7", "type": "aktivitas", "jumlah_soal": 4, "id_topic": 3, "id_subtopic": 11},

        # Topic 4
        {"title": "aktivitas 8", "type": "aktivitas", "jumlah_soal": 4, "id_topic": 4, "id_subtopic": 14},
        {"title": "aktivitas 9", "type": "aktivitas", "jumlah_soal": 4, "id_topic": 4, "id_subtopic": 15},
        {"title": "aktivitas 10", "type": "aktivitas", "jumlah_soal": 4, "id_topic": 4, "id_subtopic": 16},

        # Topic 5
        {"title": "aktivitas 11", "type": "aktivitas", "jumlah_soal": 4, "id_topic": 5, "id_subtopic": 19},
        {"title": "aktivitas 12", "type": "aktivitas", "jumlah_soal": 4, "id_topic": 5, "id_subtopic": 20},
        {"title": "aktivitas 13", "type": "aktivitas", "jumlah_soal": 4, "id_topic": 5, "id_subtopic": 21},
        {"title": "aktivitas 14", "type": "aktivitas", "jumlah_soal": 4, "id_topic": 5, "id_subtopic": 22},
    ]

    for item in data:
        activity = Activity(
            id_class=class_id,
            title=item["title"],
            type=item["type"],
            durasi_pengerjaan=None,
            jumlah_soal=item["jumlah_soal"],
            id_topic=item["id_topic"],
            id_subtopic=item["id_subtopic"]
        )
        db.session.add(activity)

    db.session.commit()
    print(f"✅ Seeder activity berhasil untuk class_id: {class_id}")


def seed_question_kuis():
    data = [
        {
            "question": {"text": "Citra digital disebut sebagai representasi dua dimensi karena…", "URL": None},
            "options": [
                {"a": {"teks": "Memiliki koordinat x dan y pada setiap piksel", "url": None}},
                {"b": {"teks": "Disusun dari tiga kanal warna", "url": None}},
                {"c": {"teks": "Memiliki warna yang beragam", "url": None}},
                {"d": {"teks": "Hanya dapat dilihat pada layar", "url": None}},
                {"e": {"teks": "Tidak memiliki ukuran tetap", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {"text": "Perbedaan utama antara citra digital dan citra analog adalah…", "URL": None},
            "options": [
                {"a": {"teks": "Citra digital tidak memiliki warna", "url": None}},
                {"b": {"teks": "Citra digital tersusun dari piksel dengan nilai diskrit", "url": None}},
                {"c": {"teks": "Citra analog hanya bisa disimpan di komputer", "url": None}},
                {"d": {"teks": "Citra digital tidak memiliki ukuran", "url": None}},
                {"e": {"teks": "Citra analog tidak dapat dilihat manusia", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {"text": "Proses mengubah nilai kontinu menjadi nilai diskrit agar dapat diolah komputer disebut…", "URL": None},
            "options": [
                {"a": {"teks": "Sampling", "url": None}},
                {"b": {"teks": "Filtering", "url": None}},
                {"c": {"teks": "Discretization", "url": None}},
                {"d": {"teks": "Encoding", "url": None}},
                {"e": {"teks": "Transformasi", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {"text": "Jika suatu piksel memiliki nilai intensitas tinggi pada citra grayscale, maka tampilannya akan…", "URL": None},
            "options": [
                {"a": {"teks": "Semakin gelap", "url": None}},
                {"b": {"teks": "Semakin buram", "url": None}},
                {"c": {"teks": "Semakin terang", "url": None}},
                {"d": {"teks": "Semakin berwarna", "url": None}},
                {"e": {"teks": "Semakin tajam", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {"text": "Pada citra grayscale 8-bit, jumlah kemungkinan nilai intensitas piksel adalah…", "URL": None},
            "options": [
                {"a": {"teks": "2 nilai", "url": None}},
                {"b": {"teks": "8 nilai", "url": None}},
                {"c": {"teks": "128 nilai", "url": None}},
                {"d": {"teks": "256 nilai", "url": None}},
                {"e": {"teks": "512 nilai", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {"text": "Berikut ini yang merupakan karakteristik citra RGB adalah…", "URL": None},
            "options": [
                {"a": {"teks": "Menggunakan tiga kanal warna utama", "url": None}},
                {"b": {"teks": "Hanya memiliki dua nilai piksel", "url": None}},
                {"c": {"teks": "Hanya memiliki satu kanal", "url": None}},
                {"d": {"teks": "Tidak memiliki nilai intensitas", "url": None}},
                {"e": {"teks": "Tidak dapat menampilkan warna", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {"text": "Alasan utama citra grayscale sering digunakan dalam pengolahan citra adalah…", "URL": None},
            "options": [
                {"a": {"teks": "Memiliki lebih banyak warna", "url": None}},
                {"b": {"teks": "Lebih kompleks dari RGB", "url": None}},
                {"c": {"teks": "Menggunakan tiga kanal warna", "url": None}},
                {"d": {"teks": "Perhitungan lebih sederhana karena satu kanal", "url": None}},
                {"e": {"teks": "Tidak memiliki nilai numerik", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {"text": "Citra biner lebih efisien dalam penyimpanan karena…", "URL": None},
            "options": [
                {"a": {"teks": "Memiliki tiga kanal warna", "url": None}},
                {"b": {"teks": "Hanya memiliki dua kemungkinan nilai", "url": None}},
                {"c": {"teks": "Menggunakan 8 bit per piksel", "url": None}},
                {"d": {"teks": "Memiliki resolusi tinggi", "url": None}},
                {"e": {"teks": "Mengandung banyak informasi warna", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {"text": "Dalam citra RGB, kombinasi nilai (255, 255, 255) menghasilkan warna…", "URL": None},
            "options": [
                {"a": {"teks": "Hitam", "url": None}},
                {"b": {"teks": "Merah", "url": None}},
                {"c": {"teks": "Hijau", "url": None}},
                {"d": {"teks": "Biru", "url": None}},
                {"e": {"teks": "Putih", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {
                "text": """
                <p>Diketahui sebuah citra RGB dengan masing-masing kanal sebagai berikut:</p>
                \\[
                \\begin{array}{|c|c|c|}
                \\hline
                \\text{Kanal R} & \\text{Kanal G} & \\text{Kanal B} \\\\
                \\hline
                \\begin{array}{ccc}
                110 & 80 & 90 \\\\
                50 & 60 & 100 \\\\
                20 & 40 & 120
                \\end{array}
                &
                \\begin{array}{ccc}
                15 & 20 & 160 \\\\
                10 & 150 & 80 \\\\
                110 & 50 & 90
                \\end{array}
                &
                \\begin{array}{ccc}
                120 & 60 & 80 \\\\
                30 & 140 & 170 \\\\
                80 & 110 & 100
                \\end{array}
                \\\\
                \\hline
                \\end{array}
                \\]
                <p>Jika dilakukan konversi ke grayscale menggunakan metode Luminosity:</p>
                <p>
                \\[
                Gray = 0.3R + 0.59G + 0.11B
                \\]
                </p>
                <p>Maka nilai grayscale pada posisi f(2,2) adalah…</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "118", "url": None}},
                {"b": {"teks": "120", "url": None}},
                {"c": {"teks": "124", "url": None}},
                {"d": {"teks": "126", "url": None}},
                {"e": {"teks": "122", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {"text": "Segmentasi citra dilakukan pada ruang spasial. Yang dimaksud ruang spasial adalah…", "URL": None},
            "options": [
                {"a": {"teks": "Ruang warna dalam citra", "url": None}},
                {"b": {"teks": "Ruang dua dimensi yang berisi posisi piksel", "url": None}},
                {"c": {"teks": "Ruang penyimpanan data citra", "url": None}},
                {"d": {"teks": "Ruang untuk menyimpan hasil segmentasi", "url": None}},
                {"e": {"teks": "Ruang untuk memproses noise", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {"text": "Jika suatu citra dibagi menjadi beberapa wilayah R₁, R₂, ..., Rₙ, maka tujuan utama pembagian tersebut adalah…", "URL": None},
            "options": [
                {"a": {"teks": "Mengurangi ukuran citra", "url": None}},
                {"b": {"teks": "Mempermudah pengolahan dengan membagi citra menjadi bagian bermakna", "url": None}},
                {"c": {"teks": "Mengubah warna citra", "url": None}},
                {"d": {"teks": "Menghapus bagian citra tertentu", "url": None}},
                {"e": {"teks": "Menambah jumlah piksel", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {"text": "Sebuah wilayah segmentasi memiliki dua bagian yang terpisah jauh tetapi masih dianggap satu region. Kondisi ini berarti…", "URL": None},
            "options": [
                {"a": {"teks": "Segmentasi sudah benar", "url": None}},
                {"b": {"teks": "Segmentasi memenuhi aturan", "url": None}},
                {"c": {"teks": "Segmentasi tidak memenuhi konsep connected set", "url": None}},
                {"d": {"teks": "Segmentasi hanya berlaku pada citra berwarna", "url": None}},
                {"e": {"teks": "Segmentasi menjadi lebih akurat", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {"text": "Perbedaan utama antara 4-connected dan 8-connected terletak pada…", "URL": None},
            "options": [
                {"a": {"teks": "Nilai intensitas piksel", "url": None}},
                {"b": {"teks": "Jumlah wilayah dalam citra", "url": None}},
                {"c": {"teks": "Arah keterhubungan antar piksel", "url": None}},
                {"d": {"teks": "Ukuran citra", "url": None}},
                {"e": {"teks": "Warna piksel", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {"text": "Jika suatu piksel termasuk ke dalam dua wilayah berbeda sekaligus, maka kondisi tersebut…", "URL": None},
            "options": [
                {"a": {"teks": "Melanggar aturan segmentasi citra", "url": None}},
                {"b": {"teks": "Diperbolehkan dalam segmentasi", "url": None}},
                {"c": {"teks": "Menunjukkan segmentasi yang optimal", "url": None}},
                {"d": {"teks": "Tidak berpengaruh pada hasil", "url": None}},
                {"e": {"teks": "Menunjukkan citra bertekstur", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {"text": "Suatu region memiliki piksel dengan nilai intensitas yang sangat beragam. Berdasarkan konsep segmentasi, kondisi ini menunjukkan bahwa…", "URL": None},
            "options": [
                {"a": {"teks": "Region tersebut homogen", "url": None}},
                {"b": {"teks": "Region tersebut memenuhi kriteria", "url": None}},
                {"c": {"teks": "Segmentasi sudah sempurna", "url": None}},
                {"d": {"teks": "Region tersebut tidak memenuhi predikat Q", "url": None}},
                {"e": {"teks": "Region harus dipertahankan", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {"text": "Pendekatan edge-based segmentation paling tepat digunakan pada citra yang…", "URL": None},
            "options": [
                {"a": {"teks": "Memiliki banyak tekstur acak", "url": None}},
                {"b": {"teks": "Memiliki warna yang sama", "url": None}},
                {"c": {"teks": "Memiliki noise tinggi", "url": None}},
                {"d": {"teks": "Memiliki ukuran kecil", "url": None}},
                {"e": {"teks": "Memiliki perbedaan intensitas yang jelas antara objek dan latar", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {"text": "Jika suatu citra memiliki banyak perubahan intensitas kecil yang tidak relevan, maka penggunaan edge-based segmentation akan…", "URL": None},
            "options": [
                {"a": {"teks": "Sangat akurat", "url": None}},
                {"b": {"teks": "Lebih cepat", "url": None}},
                {"c": {"teks": "Menghasilkan citra biner", "url": None}},
                {"d": {"teks": "Sulit menemukan batas yang jelas", "url": None}},
                {"e": {"teks": "Mengurangi jumlah piksel", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {"text": "Dalam region-based segmentation, citra dibagi menjadi subwilayah kecil. Tujuan pembagian ini adalah…", "URL": None},
            "options": [
                {"a": {"teks": "Mengelompokkan piksel berdasarkan keseragaman karakteristik", "url": None}},
                {"b": {"teks": "Menghapus tepi objek", "url": None}},
                {"c": {"teks": "Menambah resolusi citra", "url": None}},
                {"d": {"teks": "Mengubah citra menjadi berwarna", "url": None}},
                {"e": {"teks": "Menghilangkan tekstur", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {"text": "Jika dua wilayah bertetangga memiliki karakteristik yang sama dan digabung masih homogen, maka…", "URL": None},
            "options": [
                {"a": {"teks": "Kedua wilayah harus dipisahkan", "url": None}},
                {"b": {"teks": "Segmentasi sudah salah total", "url": None}},
                {"c": {"teks": "Piksel harus dihapus", "url": None}},
                {"d": {"teks": "Nilai piksel harus diubah", "url": None}},
                {"e": {"teks": "Kedua wilayah sebenarnya satu region", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {"text": "Pada algoritma Non-Maximal Suppression, sebuah piksel tepi akan dipertahankan jika …", "URL": None},
            "options": [
                {"a": {"teks": "Nilainya lebih kecil dari tetangganya", "url": None}},
                {"b": {"teks": "Terletak pada pusat citra", "url": None}},
                {"c": {"teks": "Memiliki nilai gradien nol", "url": None}},
                {"d": {"teks": "Merupakan maksimum lokal pada arah tepi", "url": None}},
                {"e": {"teks": "Memiliki lebih dari empat tetangga", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {"text": "Jika suatu piksel memiliki arah gradien 0°, maka pada proses Non-Maximal Suppression piksel tersebut dibandingkan dengan …", "URL": None},
            "options": [
                {"a": {"teks": "Piksel atas dan bawah", "url": None}},
                {"b": {"teks": "Piksel kiri dan kanan", "url": None}},
                {"c": {"teks": "Piksel kiri atas dan kanan bawah", "url": None}},
                {"d": {"teks": "Piksel kanan atas dan kiri bawah", "url": None}},
                {"e": {"teks": "Semua piksel tetangga", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {"text": "Diketahui nilai t₁ = 90 dan t₀ = 40. Jika sebuah piksel memiliki nilai magnitudo 30, maka pada algoritma hysteresis thresholding piksel tersebut akan …", "URL": None},
            "options": [
                {"a": {"teks": "Dipertahankan sebagai tepi kuat", "url": None}},
                {"b": {"teks": "Dipertahankan sebagai tepi lemah", "url": None}},
                {"c": {"teks": "Dihapus karena dianggap noise", "url": None}},
                {"d": {"teks": "Dibandingkan dengan tetangga", "url": None}},
                {"e": {"teks": "Dijadikan nilai maksimum", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {"text": "Jika sebuah piksel memiliki magnitudo 65 dengan t₁ = 90 dan t₀ = 40, maka piksel tersebut dikategorikan sebagai …", "URL": None},
            "options": [
                {"a": {"teks": "Tepi kuat", "url": None}},
                {"b": {"teks": "Tepi lemah yang perlu diperiksa konektivitasnya", "url": None}},
                {"c": {"teks": "Noise", "url": None}},
                {"d": {"teks": "Piksel maksimum", "url": None}},
                {"e": {"teks": "Piksel latar belakang", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {"text": "Dalam algoritma inner boundary tracing, piksel awal P₀ ditentukan berdasarkan …", "URL": None},
            "options": [
                {"a": {"teks": "Piksel dengan intensitas terbesar", "url": None}},
                {"b": {"teks": "Piksel yang dipilih secara acak", "url": None}},
                {"c": {"teks": "Piksel dengan kolom terkecil dan baris terkecil pada region", "url": None}},
                {"d": {"teks": "Piksel yang berada di tengah region", "url": None}},
                {"e": {"teks": "Piksel yang memiliki tetangga terbanyak", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {"text": "Pada inner boundary tracing dengan 8-connectivity, pencarian piksel tetangga dilakukan dengan cara …", "URL": None},
            "options": [
                {"a": {"teks": "Berlawanan arah jarum jam dari arah tertentu", "url": None}},
                {"b": {"teks": "Searah jarum jam", "url": None}},
                {"c": {"teks": "Secara acak", "url": None}},
                {"d": {"teks": "Hanya ke arah horizontal", "url": None}},
                {"e": {"teks": "Hanya ke arah vertikal", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {"text": "Dalam proses outer boundary tracing, piksel yang termasuk outer boundary adalah …", "URL": None},
            "options": [
                {"a": {"teks": "Piksel background yang diperiksa di sekitar objek", "url": None}},
                {"b": {"teks": "Piksel objek yang memiliki nilai terbesar", "url": None}},
                {"c": {"teks": "Piksel objek yang berada di tengah region", "url": None}},
                {"d": {"teks": "Piksel dengan nilai gradien terbesar", "url": None}},
                {"e": {"teks": "Piksel yang berada di pusat citra", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {"text": "Perbedaan utama antara inner boundary dan outer boundary adalah …", "URL": None},
            "options": [
                {"a": {"teks": "Keduanya merupakan bagian dari objek", "url": None}},
                {"b": {"teks": "Keduanya merupakan bagian background", "url": None}},
                {"c": {"teks": "Outer boundary merupakan bagian dari objek sedangkan inner boundary bukan", "url": None}},
                {"d": {"teks": "Inner boundary merupakan bagian dari objek sedangkan outer boundary bukan", "url": None}},
                {"e": {"teks": "Keduanya tidak memiliki hubungan", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {"text": "Jika dua region pada citra saling bersebelahan, maka berdasarkan konsep inner boundary dan outer boundary …", "URL": None},
            "options": [
                {"a": {"teks": "Kedua region memiliki batas yang sama", "url": None}},
                {"b": {"teks": "Outer boundary berubah menjadi objek", "url": None}},
                {"c": {"teks": "Kedua region memiliki nilai piksel yang sama", "url": None}},
                {"d": {"teks": "Inner boundary akan hilang", "url": None}},
                {"e": {"teks": "Kedua region tidak memiliki batas yang sama", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {"text": "Dalam pembentukan extended boundary, piksel dengan kategori LEFT akan digeser ke posisi …", "URL": None},
            "options": [
                {"a": {"teks": "(i+1, j)", "url": None}},
                {"b": {"teks": "(i+1, j+1)", "url": None}},
                {"c": {"teks": "(i−1, j+1)", "url": None}},
                {"d": {"teks": "(i−1, j)", "url": None}},
                {"e": {"teks": "(i, j+1)", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {"text": "Dalam proses thresholding, perubahan dari citra grayscale ke citra biner bertujuan untuk menyederhanakan informasi citra sehingga....", "URL": None},
            "options": [
                {"a": {"teks": "Warna citra menjadi lebih banyak", "url": None}},
                {"b": {"teks": "Semua piksel memiliki nilai sama", "url": None}},
                {"c": {"teks": "Ukuran citra menjadi lebih besar", "url": None}},
                {"d": {"teks": "Nilai piksel menjadi acak", "url": None}},
                {"e": {"teks": "Objek dan latar belakang lebih mudah dibedakan", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {"text": "Jika sebuah citra memiliki perbedaan intensitas yang sangat kecil antara objek dan background, maka penggunaan thresholding sederhana kemungkinan akan menghasilkan....", "URL": None},
            "options": [
                {"a": {"teks": "Segmentasi yang sangat akurat", "url": None}},
                {"b": {"teks": "Semua piksel menjadi background", "url": None}},
                {"c": {"teks": "Semua piksel menjadi objek", "url": None}},
                {"d": {"teks": "Pemisahan yang kurang jelas", "url": None}},
                {"e": {"teks": "Tidak terjadi perubahan", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {"text": "Perhatikan data piksel berikut: {100, 120, 130, 140, 180} dengan T = 130. Piksel yang diklasifikasikan sebagai background adalah....", "URL": None},
            "options": [
                {"a": {"teks": "{100, 120}", "url": None}},
                {"b": {"teks": "{140, 180}", "url": None}},
                {"c": {"teks": "{130, 140}", "url": None}},
                {"d": {"teks": "{100, 120, 130}", "url": None}},
                {"e": {"teks": "Semua piksel", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {"text": "Dalam adaptive thresholding, jika suatu bagian citra memiliki pencahayaan lebih gelap dibanding bagian lain, maka nilai threshold pada bagian tersebut biasanya....", "URL": None},
            "options": [
                {"a": {"teks": "Sama dengan bagian lain", "url": None}},
                {"b": {"teks": "Diabaikan", "url": None}},
                {"c": {"teks": "Selalu lebih besar", "url": None}},
                {"d": {"teks": "Tidak digunakan", "url": None}},
                {"e": {"teks": "Lebih kecil atau menyesuaikan kondisi lokal", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {"text": "Band thresholding dapat digunakan untuk mengekstraksi bagian tertentu dari citra karena metode ini bekerja dengan....", "URL": None},
            "options": [
                {"a": {"teks": "Memilih piksel dalam rentang nilai intensitas tertentu", "url": None}},
                {"b": {"teks": "Mengelompokkan piksel berdasarkan posisi", "url": None}},
                {"c": {"teks": "Menggunakan satu nilai threshold global", "url": None}},
                {"d": {"teks": "Menghapus semua piksel terang", "url": None}},
                {"e": {"teks": "Mengubah citra menjadi warna", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {
                "text": """
                <p>Diberikan histogram sederhana:</p>
                <p>
                \\[
                i = \\{0,1,2,3,4\\}
                \\]
                </p>
                <p>
                \\[
                H(i) = \\{5, 10, 20, 10, 5\\}
                \\]
                </p>
                <p>Jika threshold \\( t = 2 \\), maka jumlah piksel background adalah....</p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "15", "url": None}},
                {"b": {"teks": "25", "url": None}},
                {"c": {"teks": "35", "url": None}},
                {"d": {"teks": "45", "url": None}},
                {"e": {"teks": "50", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {"text": "Pada histogram bimodal, nilai keabuan yang jarang muncul biasanya berasal dari....", "URL": None},
            "options": [
                {"a": {"teks": "Bagian tengah objek", "url": None}},
                {"b": {"teks": "Background saja", "url": None}},
                {"c": {"teks": "Batas antara objek dan background", "url": None}},
                {"d": {"teks": "Noise saja", "url": None}},
                {"e": {"teks": "Piksel maksimum", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {"text": "Dalam algoritma Otsu, jika nilai probabilitas background semakin besar, maka artinya....", "URL": None},
            "options": [
                {"a": {"teks": "Semua piksel menjadi foreground", "url": None}},
                {"b": {"teks": "Semakin banyak piksel termasuk background", "url": None}},
                {"c": {"teks": "Tidak ada piksel background", "url": None}},
                {"d": {"teks": "Semua piksel sama", "url": None}},
                {"e": {"teks": "Histogram tidak digunakan", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {
                "text": """
                <p>Diberikan data probabilitas:</p>
                <p>
                \\[
                \\omega_B = 0.4, \\quad \\omega_F = 0.6
                \\]
                </p>
                <p>
                \\[
                \\sigma_B = 0.5, \\quad \\sigma_F = 0.5
                \\]
                </p>
                <p>Maka variansi total adalah....</p>
                <p>
                \\[
                0.4 \\times 0.5 + 0.6 \\times 0.5 = 0.5
                \\]
                </p>
                """,
                "URL": None
            },
            "options": [
                {"a": {"teks": "0.4", "url": None}},
                {"b": {"teks": "0.5", "url": None}},
                {"c": {"teks": "0.6", "url": None}},
                {"d": {"teks": "1.0", "url": None}},
                {"e": {"teks": "0.25", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {"text": "Dalam algoritma Otsu, nilai threshold terbaik dipilih ketika nilai variansi total berbobot....", "URL": None},
            "options": [
                {"a": {"teks": "Paling kecil", "url": None}},
                {"b": {"teks": "Paling besar", "url": None}},
                {"c": {"teks": "Sama dengan nol", "url": None}},
                {"d": {"teks": "Tidak berubah", "url": None}},
                {"e": {"teks": "Tidak dihitung", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {"text": "Tujuan utama dari segmentasi berbasis region dalam pengolahan citra adalah untuk....", "URL": None},
            "options": [
                {"a": {"teks": "Mendeteksi tepi objek secara detail", "url": None}},
                {"b": {"teks": "Membagi citra menjadi region dengan ukuran sama", "url": None}},
                {"c": {"teks": "Membagi citra menjadi region yang homogen", "url": None}},
                {"d": {"teks": "Meningkatkan resolusi citra", "url": None}},
                {"e": {"teks": "Mengubah citra menjadi biner", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {"text": "Dalam segmentasi berbasis region, suatu region dikatakan homogen apabila....", "URL": None},
            "options": [
                {"a": {"teks": "Memiliki jumlah piksel yang sama", "url": None}},
                {"b": {"teks": "Memiliki karakteristik yang seragam", "url": None}},
                {"c": {"teks": "Berada pada posisi tertentu", "url": None}},
                {"d": {"teks": "Memiliki bentuk persegi", "url": None}},
                {"e": {"teks": "Memiliki ukuran besar", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {"text": "Pada metode region merging, proses penggabungan dua region bertetangga dilakukan jika....", "URL": None},
            "options": [
                {"a": {"teks": "Kedua region memiliki ukuran sama", "url": None}},
                {"b": {"teks": "Kedua region memiliki bentuk sama", "url": None}},
                {"c": {"teks": "Hasil penggabungan tetap memenuhi kriteria homogenitas", "url": None}},
                {"d": {"teks": "Kedua region memiliki warna berbeda", "url": None}},
                {"e": {"teks": "Jumlah piksel keduanya sama", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {"text": "Dalam algoritma region merging, proses penggabungan dihentikan apabila....", "URL": None},
            "options": [
                {"a": {"teks": "Semua region telah digabung menjadi satu", "url": None}},
                {"b": {"teks": "Tidak ada lagi region bertetangga yang memenuhi kriteria homogenitas", "url": None}},
                {"c": {"teks": "Semua region memiliki ukuran sama", "url": None}},
                {"d": {"teks": "Nilai piksel menjadi nol", "url": None}},
                {"e": {"teks": "Seluruh citra telah diubah", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {"text": "Pada metode split and merge, proses splitting dilakukan ketika suatu region....", "URL": None},
            "options": [
                {"a": {"teks": "Memiliki ukuran besar", "url": None}},
                {"b": {"teks": "Tidak memiliki tetangga", "url": None}},
                {"c": {"teks": "Berada di tengah citra", "url": None}},
                {"d": {"teks": "Memiliki warna dominan", "url": None}},
                {"e": {"teks": "Tidak memenuhi kriteria homogenitas", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {"text": "Dalam metode split and merge, empat subregion dapat digabungkan kembali menjadi satu region apabila....", "URL": None},
            "options": [
                {"a": {"teks": "Memenuhi kriteria homogenitas setelah digabung", "url": None}},
                {"b": {"teks": "Berada pada level berbeda", "url": None}},
                {"c": {"teks": "Memiliki ukuran yang berbeda", "url": None}},
                {"d": {"teks": "Memiliki jumlah piksel yang sama", "url": None}},
                {"e": {"teks": "Tidak memiliki batas", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {"text": "Struktur data yang digunakan dalam metode split and merge untuk merepresentasikan proses segmentasi adalah....", "URL": None},
            "options": [
                {"a": {"teks": "Linked list", "url": None}},
                {"b": {"teks": "Stack", "url": None}},
                {"c": {"teks": "Graph linear", "url": None}},
                {"d": {"teks": "Array satu dimensi", "url": None}},
                {"e": {"teks": "Segmentation quadtree", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {"text": "Pada tahap post-processing, penggabungan region kecil dilakukan dengan tujuan utama untuk....", "URL": None},
            "options": [
                {"a": {"teks": "Meningkatkan resolusi citra", "url": None}},
                {"b": {"teks": "Mengubah warna citra", "url": None}},
                {"c": {"teks": "Memperbesar ukuran objek", "url": None}},
                {"d": {"teks": "Mengurangi jumlah region yang tidak signifikan", "url": None}},
                {"e": {"teks": "Menghapus seluruh batas region", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {"text": "Dalam algoritma removal of small image regions, pemilihan region tetangga untuk digabungkan didasarkan pada....", "URL": None},
            "options": [
                {"a": {"teks": "Posisi region dalam citra", "url": None}},
                {"b": {"teks": "Ukuran region terbesar", "url": None}},
                {"c": {"teks": "Warna paling terang", "url": None}},
                {"d": {"teks": "Kemiripan berdasarkan kriteria homogenitas", "url": None}},
                {"e": {"teks": "Jumlah piksel genap", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {"text": "Salah satu tujuan penggunaan metode post-processing yang dikombinasikan dengan deteksi tepi adalah untuk....", "URL": None},
            "options": [
                {"a": {"teks": "Menyesuaikan kontur hasil segmentasi dengan tepi objek", "url": None}},
                {"b": {"teks": "Mempercepat proses thresholding", "url": None}},
                {"c": {"teks": "Mengurangi ukuran citra", "url": None}},
                {"d": {"teks": "Menghilangkan semua region kecil", "url": None}},
                {"e": {"teks": "Mengubah citra menjadi grayscale", "url": None}}
            ],
            "answer": "a"
        }
    ]

    for item in data:
        q = Question(
            type="mc",
            question=json.dumps(item["question"]),
            MC_option=json.dumps(item["options"]),
            MC_Answer=item["answer"],
            tingkat_kesulitan="mudah",
            created_by=3
        )
        db.session.add(q)

    db.session.commit()
    print("✅ Seeder citra digital berhasil!")

def seed_kuis(class_id):
    data = [
        {"title": "Kuis 1", "type": "kuis", "jumlah_soal": 10, "id_topic": 1, "id_subtopic": 4},
        {"title": "Kuis 2", "type": "kuis", "jumlah_soal": 10, "id_topic": 2, "id_subtopic": 8},
        {"title": "Kuis 3", "type": "kuis", "jumlah_soal": 10, "id_topic": 3, "id_subtopic": 13},
        {"title": "Kuis 4", "type": "kuis", "jumlah_soal": 10, "id_topic": 4, "id_subtopic": 18},
        {"title": "Kuis 5", "type": "kuis", "jumlah_soal": 10, "id_topic": 5, "id_subtopic": 24},
    ]

    for item in data:
        kuis = Activity(
            id_class=class_id,
            title=item["title"],
            type=item["type"],
            durasi_pengerjaan=30,
            jumlah_soal=item["jumlah_soal"],
            id_topic=item["id_topic"],
            id_subtopic=item["id_subtopic"]
        )
        db.session.add(kuis)

    db.session.commit()
    print(f"✅ Seeder kuis berhasil untuk class_id: {class_id}")

def seed_question_evaluasi():
    data = [
        {
            "question": {"text": "Dalam pengolahan citra digital, sebuah gambar direpresentasikan sebagai fungsi dua dimensi f(x,y). Pernyataan yang paling tepat terkait fungsi tersebut adalah…", "URL": None},
            "options": [
                {"a": {"teks": "f(x,y) hanya menunjukkan warna citra", "url": None}},
                {"b": {"teks": "x dan y menunjukkan nilai intensitas", "url": None}},
                {"c": {"teks": "f(x,y) menunjukkan nilai kecerahan pada koordinat tertentu", "url": None}},
                {"d": {"teks": "x dan y menunjukkan jumlah piksel", "url": None}},
                {"e": {"teks": "f(x,y) menunjukkan ukuran citra", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {"text": "Sebuah citra digital berukuran 256 × 256 piksel. Jika setiap piksel memiliki nilai intensitas tertentu, maka total jumlah piksel pada citra tersebut adalah…", "URL": None},
            "options": [
                {"a": {"teks": "256", "url": None}},
                {"b": {"teks": "512", "url": None}},
                {"c": {"teks": "65536", "url": None}},
                {"d": {"teks": "131072", "url": None}},
                {"e": {"teks": "100000", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {"text": "Pada citra grayscale 8-bit, jika nilai mendekati 0 maka tampilannya adalah…", "URL": None},
            "options": [
                {"a": {"teks": "Warna cerah", "url": None}},
                {"b": {"teks": "Warna merah", "url": None}},
                {"c": {"teks": "Warna gelap atau hitam", "url": None}},
                {"d": {"teks": "Warna putih", "url": None}},
                {"e": {"teks": "Warna abu terang", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {"text": "Dalam konversi RGB ke grayscale, metode luminosity lebih akurat karena…", "URL": None},
            "options": [
                {"a": {"teks": "Menggunakan rata-rata sederhana", "url": None}},
                {"b": {"teks": "Memberi bobot berbeda tiap kanal", "url": None}},
                {"c": {"teks": "Mengabaikan warna hijau", "url": None}},
                {"d": {"teks": "Menggunakan nilai maksimum", "url": None}},
                {"e": {"teks": "Menggunakan nilai minimum", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {"text": "Jika RGB menggunakan 8 bit tiap kanal, maka total bit per piksel adalah…", "URL": None},
            "options": [
                {"a": {"teks": "8 bit", "url": None}},
                {"b": {"teks": "16 bit", "url": None}},
                {"c": {"teks": "24 bit", "url": None}},
                {"d": {"teks": "32 bit", "url": None}},
                {"e": {"teks": "64 bit", "url": None}}
            ],
            "answer": "c"
        },
        {
            "question": {"text": "Citra biner sering digunakan karena…", "URL": None},
            "options": [
                {"a": {"teks": "Memiliki banyak warna", "url": None}},
                {"b": {"teks": "Hanya dua nilai sehingga efisien", "url": None}},
                {"c": {"teks": "Resolusi tinggi", "url": None}},
                {"d": {"teks": "3 kanal warna", "url": None}},
                {"e": {"teks": "Lebih kompleks", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {"text": "Jika piksel < threshold maka akan menjadi…", "URL": None},
            "options": [
                {"a": {"teks": "Objek", "url": None}},
                {"b": {"teks": "Background", "url": None}},
                {"c": {"teks": "Merah", "url": None}},
                {"d": {"teks": "Tidak berubah", "url": None}},
                {"e": {"teks": "Noise", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {"text": "Tujuan segmentasi citra adalah…", "URL": None},
            "options": [
                {"a": {"teks": "Menambah ukuran", "url": None}},
                {"b": {"teks": "Mempermudah analisis objek", "url": None}},
                {"c": {"teks": "Mengubah warna", "url": None}},
                {"d": {"teks": "Mengurangi resolusi", "url": None}},
                {"e": {"teks": "Menambah piksel", "url": None}}
            ],
            "answer": "b"
        },
        {
            "question": {"text": "Connected set berarti…", "URL": None},
            "options": [
                {"a": {"teks": "Piksel saling terhubung", "url": None}},
                {"b": {"teks": "Warna berbeda", "url": None}},
                {"c": {"teks": "Boleh terpisah", "url": None}},
                {"d": {"teks": "Ukuran sama", "url": None}},
                {"e": {"teks": "Bentuk lingkaran", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {"text": "Piksel masuk dua region berarti…", "URL": None},
            "options": [
                {"a": {"teks": "Benar", "url": None}},
                {"b": {"teks": "Optimal", "url": None}},
                {"c": {"teks": "Homogen", "url": None}},
                {"d": {"teks": "Melanggar aturan", "url": None}},
                {"e": {"teks": "Tidak berpengaruh", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {"text": "Edge-based segmentation berdasarkan…", "URL": None},
            "options": [
                {"a": {"teks": "Warna", "url": None}},
                {"b": {"teks": "Tekstur", "url": None}},
                {"c": {"teks": "Jumlah piksel", "url": None}},
                {"d": {"teks": "Ukuran", "url": None}},
                {"e": {"teks": "Perubahan intensitas tajam", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {"text": "Hasil edge belum jadi segmentasi karena…", "URL": None},
            "options": [
                {"a": {"teks": "Terlalu terang", "url": None}},
                {"b": {"teks": "Tidak berwarna", "url": None}},
                {"c": {"teks": "Terlalu kecil", "url": None}},
                {"d": {"teks": "Tidak bernilai", "url": None}},
                {"e": {"teks": "Masih garis terpisah", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {"text": "Tujuan Non-Maximal Suppression adalah…", "URL": None},
            "options": [
                {"a": {"teks": "Menipiskan tepi", "url": None}},
                {"b": {"teks": "Menghapus semua", "url": None}},
                {"c": {"teks": "Menebalkan tepi", "url": None}},
                {"d": {"teks": "RGB", "url": None}},
                {"e": {"teks": "Menambah noise", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {"text": "Gradien 90° dibandingkan dengan…", "URL": None},
            "options": [
                {"a": {"teks": "Atas dan bawah", "url": None}},
                {"b": {"teks": "Kiri kanan", "url": None}},
                {"c": {"teks": "Diagonal", "url": None}},
                {"d": {"teks": "Semua", "url": None}},
                {"e": {"teks": "Tidak dibandingkan", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {"text": "Hysteresis threshold piksel tengah akan…", "URL": None},
            "options": [
                {"a": {"teks": "Dihapus", "url": None}},
                {"b": {"teks": "Tepi kuat", "url": None}},
                {"c": {"teks": "Tidak diproses", "url": None}},
                {"d": {"teks": "Background", "url": None}},
                {"e": {"teks": "Dicek konektivitas", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {"text": "Global threshold kurang efektif jika…", "URL": None},
            "options": [
                {"a": {"teks": "Resolusi tinggi", "url": None}},
                {"b": {"teks": "Banyak piksel", "url": None}},
                {"c": {"teks": "Berwarna", "url": None}},
                {"d": {"teks": "Kecil", "url": None}},
                {"e": {"teks": "Pencahayaan tidak merata", "url": None}}
            ],
            "answer": "e"
        },
        {
            "question": {"text": "Histogram bimodal artinya…", "URL": None},
            "options": [
                {"a": {"teks": "Tidak ada objek", "url": None}},
                {"b": {"teks": "Semua sama", "url": None}},
                {"c": {"teks": "Rusak", "url": None}},
                {"d": {"teks": "Objek vs background jelas", "url": None}},
                {"e": {"teks": "Tidak bisa segmentasi", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {"text": "Otsu menentukan threshold dengan…", "URL": None},
            "options": [
                {"a": {"teks": "Nilai terbesar", "url": None}},
                {"b": {"teks": "Nilai terkecil", "url": None}},
                {"c": {"teks": "Ubah warna", "url": None}},
                {"d": {"teks": "Maksimalkan perbedaan kelas", "url": None}},
                {"e": {"teks": "Hapus piksel", "url": None}}
            ],
            "answer": "d"
        },
        {
            "question": {"text": "Region merging jika…", "URL": None},
            "options": [
                {"a": {"teks": "Homogen setelah digabung", "url": None}},
                {"b": {"teks": "Warna beda", "url": None}},
                {"c": {"teks": "Ukuran sama", "url": None}},
                {"d": {"teks": "Tidak bertetangga", "url": None}},
                {"e": {"teks": "Jumlah sama", "url": None}}
            ],
            "answer": "a"
        },
        {
            "question": {"text": "Split and merge jika tidak homogen maka…", "URL": None},
            "options": [
                {"a": {"teks": "Dihapus", "url": None}},
                {"b": {"teks": "Digabung semua", "url": None}},
                {"c": {"teks": "Ubah warna", "url": None}},
                {"d": {"teks": "Dipecah jadi subregion", "url": None}},
                {"e": {"teks": "Diabaikan", "url": None}}
            ],
            "answer": "d"
        }
    ]

    for item in data:
        q = Question(
            type="mc",
            question=json.dumps(item["question"]),
            MC_option=json.dumps(item["options"]),
            MC_Answer=item["answer"],
            tingkat_kesulitan="sedang",
            created_by=3
        )
        db.session.add(q)

    db.session.commit()
    print("✅ Seeder evaluasi (20 soal) berhasil!")

def seed_evaluasi(class_id):
    data = [
        {"title": "Evaluasi Akhir", "type": "evaluasi", "jumlah_soal": 20, "id_topic": 6, "id_subtopic": None},
    ]

    for item in data:
        evaluasi = Activity(
            id_class=class_id,
            title=item["title"],
            type=item["type"],
            durasi_pengerjaan=60,
            jumlah_soal=item["jumlah_soal"],
            id_topic=item["id_topic"],
            id_subtopic=item["id_subtopic"]
        )
        db.session.add(evaluasi)

    db.session.commit()
    print(f"✅ Seeder evaluasi berhasil untuk class_id: {class_id}")
    
def seed_activity_question(class_id):
    # 🔥 PENTING: Filter berdasarkan class_id agar tidak menabrak kelas lain
    activities = Activity.query.filter_by(id_class=class_id).order_by(Activity.id).all()

    offset = 0

    for i, activity in enumerate(activities, start=1):
        # Menggunakan pengecekan tipe aktivitas akan jauh lebih aman daripada urutan index
        if activity.type == "aktivitas":
            jumlah = 4
        elif activity.type == "kuis":
            jumlah = 10
        else:
            jumlah = 20

        questions = Question.query.offset(offset).limit(jumlah).all()

        if not questions:
            print(f"⚠️ Soal habis di activity ke-{i} untuk class_id {class_id}")
            break

        for q in questions:
            rel = ActivityQuestion(
                id_activity=activity.id,
                id_question=q.id
            )
            db.session.add(rel)

        offset += jumlah

    db.session.commit()
    print(f"✅ Seeder activity_question berhasil untuk class_id: {class_id}")
    
def generate_learning_package(id_class):
    # 1. HAPUS RELASI LAMA HANYA UNTUK KELAS INI (Mencegah terhapusnya soal kelas lain)
    activities = Activity.query.filter_by(id_class=id_class).all()
    activity_ids = [act.id for act in activities]
    
    if activity_ids:
        ActivityQuestion.query.filter(ActivityQuestion.id_activity.in_(activity_ids)).delete(synchronize_session=False)
        db.session.commit()

    # 2. HAPUS AKTIVITAS LAMA HANYA UNTUK KELAS INI (Mencegah aktivitas jadi dobel saat di-klaim ulang)
    Activity.query.filter_by(id_class=id_class).delete()
    db.session.commit()

    # 3. SEED SOAL HANYA JIKA BELUM ADA DI DATABASE (Mencegah duplikasi ribuan soal di DB)
    # Kita cek apakah tabel Question masih kosong
    if Question.query.count() == 0:
        seed_question()
        seed_question_kuis()
        seed_question_evaluasi()

    # 4. BUAT AKTIVITAS BARU UNTUK KELAS INI
    seed_activity(id_class)
    seed_kuis(id_class)
    seed_evaluasi(id_class)
    
    # 5. HUBUNGKAN SOAL DENGAN AKTIVITAS KELAS INI
    seed_activity_question(id_class)
        
    print(f"🎉 Semua paket pembelajaran berhasil di-generate untuk kelas {id_class}!")