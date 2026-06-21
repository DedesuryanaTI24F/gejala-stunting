import streamlit as st

from knowledge_base import GEJALA, CF_USER_OPTIONS, SOLUSI, diagnosa

st.set_page_config(page_title="Deteksi Gejala Stunting", page_icon="🧒")

st.title("🧒 Sistem Pakar Deteksi Gejala Stunting pada Balita")
st.caption("Metode Forward Chaining + Certainty Factor — Tugas Kecerdasan Buatan")

st.markdown(
    "Aplikasi ini memberikan **indikasi awal** risiko stunting berdasarkan "
    "gejala yang dialami balita. Hasil diagnosis bukan pengganti pemeriksaan "
    "medis — tetap konsultasikan ke dokter atau ahli gizi untuk kepastian."
)

st.divider()
st.subheader("1. Data Balita")
col1, col2 = st.columns(2)
with col1:
    nama = st.text_input("Nama Balita")
    usia = st.number_input("Usia (bulan)", min_value=0, max_value=60, value=12)
with col2:
    tinggi = st.number_input("Tinggi badan (cm)", min_value=30.0, max_value=120.0, value=70.0)
    berat = st.number_input("Berat badan (kg)", min_value=1.0, max_value=30.0, value=8.0)

st.divider()
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

st.divider()

if st.button("🔍 Diagnosa Sekarang", type="primary"):
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
