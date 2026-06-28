import random
from datetime import datetime

import streamlit as st

from knowledge_base import GEJALA, CF_USER_OPTIONS, SOLUSI, diagnosa

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

st.set_page_config(page_title="Deteksi Gejala Stunting", page_icon="🌱", layout="centered")

# ---------- Custom styling ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700&family=Nunito:wght@400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Nunito', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Baloo 2', sans-serif !important;
        color: #2C6E5E;
    }
    .hero-banner {
        background: linear-gradient(135deg, #4FA98B 0%, #7FC9A8 100%);
        border-radius: 18px;
        padding: 1.75rem 1.5rem;
        margin-bottom: 1.25rem;
        text-align: center;
        color: white;
    }
    .hero-banner h1 {
        color: white !important;
        font-size: 1.6rem;
        margin: 0 0 0.4rem 0;
    }
    .hero-banner p {
        margin: 0;
        font-size: 0.95rem;
        opacity: 0.95;
    }
    .sidebar-tip {
        background-color: #EAF1EA;
        border-radius: 12px;
        padding: 0.9rem 1rem;
        font-size: 0.88rem;
        line-height: 1.45;
        border-left: 4px solid #3E8E7E;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header banner ----------
st.markdown(
    """
    <div class="hero-banner">
        <h1>🌱 Sistem Pakar Deteksi Gejala Stunting</h1>
        <p>Bantu kenali tanda-tanda stunting pada balita lebih dini, dengan metode Forward Chaining &amp; Certainty Factor</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "Aplikasi ini memberikan **indikasi awal** risiko stunting berdasarkan "
    "gejala yang dialami balita. Hasil diagnosis bukan pengganti pemeriksaan "
    "medis — tetap konsultasikan ke dokter atau ahli gizi untuk kepastian."
)

# ---------- Sidebar: tip ramah tentang stunting ----------
TIPS_STUNTING = [
    "Periode 0–24 bulan disebut <b>1000 Hari Pertama Kehidupan</b>, masa paling kritis untuk mencegah stunting.",
    "Stunting <b>bukan hanya soal genetik</b> — gizi, sanitasi, dan pola asuh berperan lebih besar.",
    "Pemberian <b>ASI eksklusif</b> 6 bulan pertama membantu menurunkan risiko stunting.",
    "Pantau tumbuh kembang balita secara rutin di <b>Posyandu</b> terdekat.",
    "Target pemerintah RPJMN adalah menurunkan prevalensi stunting nasional menjadi <b>14%</b>.",
]
if "tip_hari_ini" not in st.session_state:
    st.session_state.tip_hari_ini = random.choice(TIPS_STUNTING)

with st.sidebar:
    st.markdown("### 🌿 Tahukah kamu?")
    st.markdown(f'<div class="sidebar-tip">{st.session_state.tip_hari_ini}</div>', unsafe_allow_html=True)
    st.markdown("")
    st.caption("Sumber: Kementerian Kesehatan RI, Survei Status Gizi Indonesia (SSGI) 2024")

# ---------- Data Balita ----------
with st.container(border=True):
    st.subheader("1. Data Balita")
    col1, col2 = st.columns(2)
    with col1:
        nama = st.text_input("Nama Balita")
        usia = st.number_input("Usia (bulan)", min_value=0, max_value=60, value=12)
    with col2:
        tinggi = st.number_input("Tinggi badan (cm)", min_value=30.0, max_value=120.0, value=70.0)
        berat = st.number_input("Berat badan (kg)", min_value=1.0, max_value=30.0, value=8.0)

st.write("")

# ---------- Gejala ----------
with st.container(border=True):
    st.subheader("2. Pilih Gejala yang Dialami")

    tingkat_keyakinan = st.select_slider(
        "Seberapa yakin Anda terhadap gejala yang dipilih?",
        options=list(CF_USER_OPTIONS.keys()),
        value="Cukup yakin",
    )

    gejala_terpilih = []
    for kode, data in GEJALA.items():
        if st.checkbox(data["teks"], key=kode):
            gejala_terpilih.append(kode)

st.write("")

if st.button("🔍 Diagnosa Sekarang", type="primary", use_container_width=True):
    if not gejala_terpilih:
        st.warning("Pilih minimal satu gejala terlebih dahulu.")
    else:
        cf_user = CF_USER_OPTIONS[tingkat_keyakinan]
        hasil = diagnosa(gejala_terpilih, cf_user)
        kategori_teratas, cf_teratas = next(iter(hasil.items()))

        st.subheader("3. Hasil Diagnosa")
        if nama:
            st.write(f"**Nama Balita:** {nama} ({usia} bulan)")

        if cf_teratas < 0.3:
            st.success(
                "Tidak terindikasi kuat mengalami stunting berdasarkan gejala "
                "yang dipilih."
            )
        else:
            st.error(f"**Indikasi: {kategori_teratas}** — tingkat keyakinan {cf_teratas * 100:.1f}%")
            st.info(f"**Rekomendasi:** {SOLUSI[kategori_teratas]}")

        with st.expander("Lihat detail tingkat keyakinan semua kategori"):
            for kategori, cf in hasil.items():
                st.write(f"- {kategori}: {cf * 100:.1f}%")

        st.caption(
            "⚠️ Hasil ini hanya diagnosis awal. Diperlukan konsultasi lanjutan "
            "ke dokter atau ahli gizi untuk kepastian dan penanganan yang tepat."
        )

        st.session_state.riwayat.append(
            {
                "Nama": nama if nama else "(tanpa nama)",
                "Usia (bulan)": usia,
                "Tinggi (cm)": tinggi,
                "Berat (kg)": berat,
                "Hasil": kategori_teratas if cf_teratas >= 0.3 else "Tidak terindikasi",
                "Keyakinan (%)": round(cf_teratas * 100, 1),
                "Waktu": datetime.now().strftime("%d-%m-%Y %H:%M"),
            }
        )

st.divider()
st.subheader("4. Riwayat Diagnosa (sesi ini)")
if st.session_state.riwayat:
    st.dataframe(list(reversed(st.session_state.riwayat)), use_container_width=True)
    if st.button("🗑️ Hapus riwayat"):
        st.session_state.riwayat = []
        st.rerun()
else:
    st.caption("Belum ada balita yang didiagnosa pada sesi ini.")

st.divider()
with st.expander("ℹ️ Tentang Metode & Referensi"):
    st.markdown(
        """
**Metode:** Forward Chaining + Certainty Factor (CF)

**Referensi:**
1. Zailani, D. A., Lubis, I., & Aulia, R. (2025). *Analisis Penerapan Metode
   Forward Chaining dan Certainty Factor pada Sistem Diagnosa Penyakit
   Stunting pada Balita Berbasis Web.* JUKTISI, 4(2), 1153-1160.
2. Suherman, P. A., & Tahel, F. (2023). *Metode Case-Based Reasoning dalam
   Diagnosa Penyakit Stunting pada Balita.* Jurnal InSeDS, 2(1), 90-97.
        """
    )
