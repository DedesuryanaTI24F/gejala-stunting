"""
Basis Pengetahuan - Sistem Pakar Deteksi Gejala Stunting pada Balita
Metode: Forward Chaining + Certainty Factor (CF)

Gejala dan nilai CF disusun dengan menggabungkan dua referensi:
1. Zailani, D. A., Lubis, I., & Aulia, R. (2025). Analisis Penerapan Metode
   Forward Chaining dan Certainty Factor pada Sistem Diagnosa Penyakit
   Stunting pada Balita Berbasis Web. JUKTISI, 4(2), 1153-1160.
2. Suherman, P. A., & Tahel, F. (2023). Metode Case-Based Reasoning dalam
   Diagnosa Penyakit Stunting pada Balita. Jurnal InSeDS, 2(1), 90-97.

CATATAN METODOLOGI (penting untuk dicantumkan di laporan kamu):
Sebagian nilai CF pada tabel di bawah diambil langsung dari contoh
perhitungan manual pada referensi [1] (gejala: pertumbuhan gigi melambat,
tinggi badan di bawah rata-rata, pertumbuhan melambat, sering lemas, sesak
napas, gangguan belajar, BB cenderung turun, sulit fokus). Gejala lain
merupakan hasil adaptasi peneliti dari daftar gejala pada referensi [2],
dengan bobot disesuaikan mengikuti pola tingkat keparahan (gejala fisik
seperti tubuh membiru atau sesak napas diberi bobot lebih tinggi pada
kategori Berat; gejala umum/dini seperti nafsu makan turun diberi bobot
lebih tinggi pada kategori Ringan). Disarankan nilai ini divalidasi lebih
lanjut bersama dosen pembimbing atau tenaga ahli gizi jika memungkinkan.
"""

KATEGORI = ["Stunting Ringan", "Stunting Sedang", "Stunting Berat"]

# Struktur: { kode: {"teks": gejala, "cf": {kategori: nilai CF pakar}} }
GEJALA = {
    "G01": {
        "teks": "Berat badan balita cenderung turun",
        "cf": {"Stunting Ringan": 0.6, "Stunting Sedang": 0.5, "Stunting Berat": 0.4},
    },
    "G02": {
        "teks": "Tinggi/panjang badan di bawah rata-rata usia (TB/U rendah)",
        "cf": {"Stunting Ringan": 0.2, "Stunting Sedang": 0.1, "Stunting Berat": 0.1},
    },
    "G03": {
        "teks": "Pertumbuhan gigi melambat",
        "cf": {"Stunting Ringan": 0.5, "Stunting Sedang": 0.7, "Stunting Berat": 0.9},
    },
    "G04": {
        "teks": "Wajah tampak lebih muda dari usianya",
        "cf": {"Stunting Ringan": 0.4, "Stunting Sedang": 0.6, "Stunting Berat": 0.8},
    },
    "G05": {
        "teks": "Pertumbuhan fisik melambat secara umum",
        "cf": {"Stunting Ringan": 0.5, "Stunting Sedang": 0.6, "Stunting Berat": 0.5},
    },
    "G06": {
        "teks": "Sulit fokus, daya ingat buruk, atau ada gangguan belajar",
        "cf": {"Stunting Ringan": 0.4, "Stunting Sedang": 0.3, "Stunting Berat": 0.2},
    },
    "G07": {
        "teks": "Mudah terserang infeksi berulang",
        "cf": {"Stunting Ringan": 0.3, "Stunting Sedang": 0.5, "Stunting Berat": 0.7},
    },
    "G08": {
        "teks": "Tidak aktif bermain / cenderung pendiam dan kurang kontak mata",
        "cf": {"Stunting Ringan": 0.3, "Stunting Sedang": 0.5, "Stunting Berat": 0.6},
    },
    "G09": {
        "teks": "Sering terlihat lemas",
        "cf": {"Stunting Ringan": 0.3, "Stunting Sedang": 0.4, "Stunting Berat": 0.4},
    },
    "G10": {
        "teks": "Sesak napas",
        "cf": {"Stunting Ringan": 0.1, "Stunting Sedang": 0.2, "Stunting Berat": 0.3},
    },
    "G11": {
        "teks": "Balita tidak dapat menyusu dengan baik / enggan disusui",
        "cf": {"Stunting Ringan": 0.2, "Stunting Sedang": 0.4, "Stunting Berat": 0.7},
    },
    "G12": {
        "teks": "Tubuh anak tampak membiru saat menangis",
        "cf": {"Stunting Ringan": 0.1, "Stunting Sedang": 0.3, "Stunting Berat": 0.8},
    },
    "G13": {
        "teks": "Mudah sakit, kekebalan tubuh melemah, atau lama sembuh",
        "cf": {"Stunting Ringan": 0.4, "Stunting Sedang": 0.5, "Stunting Berat": 0.6},
    },
    "G14": {
        "teks": "Kehilangan selera makan / kurang nafsu makan",
        "cf": {"Stunting Ringan": 0.5, "Stunting Sedang": 0.4, "Stunting Berat": 0.3},
    },
    "G15": {
        "teks": "Mudah menangis tanpa sebab yang jelas",
        "cf": {"Stunting Ringan": 0.3, "Stunting Sedang": 0.3, "Stunting Berat": 0.2},
    },
}

# Tingkat keyakinan user terhadap gejala yang dipilih (CF user)
CF_USER_OPTIONS = {
    "Tidak yakin": 0.4,
    "Cukup yakin": 0.7,
    "Yakin": 1.0,
}

SOLUSI = {
    "Stunting Ringan": "Pantau tumbuh kembang anak secara rutin di Posyandu/Puskesmas.",
    "Stunting Sedang": "Penuhi kebutuhan gizi anak dengan menu seimbang dan konsultasikan ke ahli gizi.",
    "Stunting Berat": "Dampingi ASI/susu eksklusif dan MPASI sehat, segera konsultasikan ke dokter anak.",
}


def hitung_cf_kombinasi(daftar_cf):
    """Menggabungkan beberapa nilai CF gejala menjadi satu CF akhir.

    Rumus kombinasi Certainty Factor (mengikuti referensi [1]):
        CF(R1,R2) = CF(R1) + CF(R2) * (1 - CF(R1))
    Dihitung berantai untuk gejala ketiga, keempat, dst.
    """
    if not daftar_cf:
        return 0.0
    cf_gabungan = daftar_cf[0]
    for cf in daftar_cf[1:]:
        cf_gabungan = cf_gabungan + cf * (1 - cf_gabungan)
    return cf_gabungan


def diagnosa(gejala_terpilih, cf_user=1.0):
    """Menjalankan forward chaining + certainty factor.

    Parameter:
        gejala_terpilih: list kode gejala, misal ["G01", "G03", "G09"]
        cf_user: tingkat keyakinan user terhadap gejala yang dipilih (0-1)

    Mengembalikan dict {kategori: CF akhir (0-1)}, diurutkan dari yang
    tertinggi ke terendah.
    """
    hasil = {}
    for kategori in KATEGORI:
        nilai_cf = []
        for kode in gejala_terpilih:
            if kode in GEJALA:
                cf_pakar = GEJALA[kode]["cf"][kategori]
                nilai_cf.append(cf_user * cf_pakar)
        hasil[kategori] = hitung_cf_kombinasi(nilai_cf)

    return dict(sorted(hasil.items(), key=lambda item: item[1], reverse=True))
