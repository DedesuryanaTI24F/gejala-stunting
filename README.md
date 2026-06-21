# Sistem Pakar Deteksi Gejala Stunting pada Balita

Aplikasi web sederhana untuk mendeteksi indikasi stunting pada balita
menggunakan metode **Forward Chaining + Certainty Factor (CF)**, dibangun
dengan Python + Streamlit.

## Struktur File

- `knowledge_base.py` — basis pengetahuan (daftar gejala, nilai CF, dan
  fungsi forward chaining + certainty factor)
- `app.py` — tampilan web (Streamlit)
- `requirements.txt` — daftar dependency

## Menjalankan di Laptop (Lokal)

1. Pastikan Python sudah terinstal.
2. Install dependency:
   ```
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```
   streamlit run app.py
   ```
4. Browser akan otomatis terbuka di `http://localhost:8501`.

## Deploy Online Gratis (Tanpa Domain) — Streamlit Community Cloud

1. Buat repository baru di GitHub, lalu upload ketiga file di atas
   (`knowledge_base.py`, `app.py`, `requirements.txt`).
2. Buka [share.streamlit.io](https://share.streamlit.io), login dengan akun
   GitHub.
3. Klik **"Create app"** → pilih repository, branch, dan file utama
   (`app.py`).
4. Klik **Deploy**. Dalam beberapa menit, kamu akan mendapat link publik
   seperti `https://nama-app.streamlit.app` yang bisa langsung dibagikan ke
   dosen.
5. Setelah penilaian/presentasi selesai, aplikasi bisa dihapus kapan saja
   dari dashboard Streamlit Community Cloud — tidak ada biaya domain atau
   hosting yang perlu dibayar.

## Catatan untuk Laporan

Nilai Certainty Factor (CF) pada `knowledge_base.py` disusun dengan
menggabungkan dua referensi (lihat komentar di bagian atas file tersebut).
Sebagian nilai diambil langsung dari contoh perhitungan manual pada jurnal
referensi, sebagian merupakan adaptasi peneliti. Cantumkan penjelasan ini
di bagian metodologi laporan agar transparan dan dapat dipertanggungjawabkan.

## Referensi

1. Zailani, D. A., Lubis, I., & Aulia, R. (2025). Analisis Penerapan Metode
   Forward Chaining dan Certainty Factor pada Sistem Diagnosa Penyakit
   Stunting pada Balita Berbasis Web. *JUKTISI*, 4(2), 1153-1160.
2. Suherman, P. A., & Tahel, F. (2023). Metode Case-Based Reasoning dalam
   Diagnosa Penyakit Stunting pada Balita. *Jurnal InSeDS*, 2(1), 90-97.
