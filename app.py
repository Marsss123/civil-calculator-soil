
import streamlit as st
import pandas as pd
import math

# ==================================
# CIVIL CALCULATOR
# ==================================

st.set_page_config(
    page_title="Civil Calculator",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ CIVIL CALCULATOR")
st.subheader("Soil Engineering & Land Cost Analysis")

st.info(
    "Aplikasi perhitungan teknik sipil untuk "
    "analisis tanah, luas lahan, dan estimasi biaya."
)

# ==================================
# FUNGSI FORMAT RUPIAH
# ==================================

def rupiah(nilai):
    return "Rp {:,.0f}".format(nilai).replace(",", ".")

# ==================================
# MENU APLIKASI
# ==================================

menu = st.sidebar.selectbox(
    "Pilih Menu",
    [
        "Dashboard",
        "Analisis Tekanan Tanah",
        "Perhitungan Luas Tanah",
        "Jenis Tanah",
        "Estimasi Biaya",
        "Laporan"
    ]
)

# ==================================
# PENYIMPANAN DATA
# ==================================

if "hasil" not in st.session_state:
    st.session_state.hasil = {}

# ==================================
# DASHBOARD
# ==================================

if menu == "Dashboard":

    st.header("Dashboard Teknik Sipil")

    col1, col2, col3 = st.columns(3)

    col1.metric("Aplikasi", "Civil Calculator")
    col2.metric("Satuan", "SI")
    col3.metric("Mata Uang", "Rupiah")

    st.markdown("""
    ### Fitur aplikasi

    - Analisis tekanan kontak tanah.
    - Analisis tekanan tanah lateral Rankine.
    - Perhitungan luas lahan.
    - Klasifikasi awal jenis tanah.
    - Estimasi harga tanah.
    - Estimasi biaya galian dan urugan.
    - Laporan hasil perhitungan.
    """)

# ==================================
# TEKANAN TANAH
# ==================================

elif menu == "Analisis Tekanan Tanah":

    st.header("Analisis Tekanan Tanah")

    st.markdown("### A. Tekanan kontak tanah")

    beban = st.number_input(
        "Total beban struktur (kN)",
        min_value=0.0,
        value=500.0
    )

    panjang = st.number_input(
        "Panjang pondasi (m)",
        min_value=0.1,
        value=2.0
    )

    lebar = st.number_input(
        "Lebar pondasi (m)",
        min_value=0.1,
        value=2.0
    )

    daya_izin = st.number_input(
        "Daya dukung tanah izin (kN/m²)",
        min_value=0.0,
        value=150.0
    )

    if st.button("Hitung Tekanan Kontak"):

        luas_pondasi = panjang * lebar

        tekanan = beban / luas_pondasi

        st.session_state.hasil["Tekanan kontak"] = tekanan
        st.session_state.hasil["Luas pondasi"] = luas_pondasi

        st.metric(
            "Tekanan kontak tanah",
            f"{tekanan:.2f} kN/m²"
        )

        st.metric(
            "Luas pondasi",
            f"{luas_pondasi:.2f} m²"
        )

        if daya_izin > 0:
            if tekanan <= daya_izin:
                st.success(
                    "Tekanan kontak tidak melebihi "
                    "daya dukung tanah izin."
                )
            else:
                st.error(
                    "Tekanan kontak melebihi "
                    "daya dukung tanah izin."
                )

        st.write(
            f"Rumus: q = P / A = "
            f"{beban} / {luas_pondasi} "
            f"= {tekanan:.2f} kN/m²"
        )

    st.divider()

    # Tekanan tanah lateral Rankine

    st.markdown("### B. Tekanan tanah lateral Rankine")

    gamma = st.number_input(
        "Berat isi tanah γ (kN/m³)",
        min_value=0.0,
        value=18.0
    )

    phi = st.number_input(
        "Sudut geser dalam φ (derajat)",
        min_value=0.0,
        max_value=89.0,
        value=30.0
    )

    tinggi = st.number_input(
        "Tinggi dinding penahan (m)",
        min_value=0.1,
        value=3.0
    )

    surcharge = st.number_input(
        "Beban merata permukaan q (kN/m²)",
        min_value=0.0,
        value=0.0
    )

    if st.button("Hitung Tekanan Lateral"):

        sudut = math.radians(phi)

        ka = (1 - math.sin(sudut)) / (
            1 + math.sin(sudut)
        )

        tekanan_dasar = ka * gamma * tinggi
        tekanan_surcharge = ka * surcharge

        resultan_tanah = (
            0.5 * ka * gamma * tinggi**2
        )

        resultan_surcharge = (
            ka * surcharge * tinggi
        )

        total_resultan = (
            resultan_tanah + resultan_surcharge
        )

        st.session_state.hasil[
            "Koefisien aktif Rankine"
        ] = ka

        st.session_state.hasil[
            "Resultan lateral"
        ] = total_resultan

        col1, col2, col3 = st.columns(3)

        col1.metric("Ka", f"{ka:.3f}")
        col2.metric(
            "Tekanan dasar",
            f"{tekanan_dasar + tekanan_surcharge:.2f} kN/m²"
        )
        col3.metric(
            "Resultan",
            f"{total_resultan:.2f} kN/m"
        )

        st.write(
            "Resultan tekanan lateral: "
            f"{total_resultan:.2f} kN/m"
        )

# ==================================
# LUAS TANAH
# ==================================

elif menu == "Perhitungan Luas Tanah":

    st.header("Perhitungan Luas Tanah")

    bentuk = st.selectbox(
        "Pilih bentuk tanah",
        [
            "Persegi Panjang",
            "Trapesium"
        ]
    )

    if bentuk == "Persegi Panjang":

        p = st.number_input(
            "Panjang tanah (m)",
            min_value=0.0,
            value=20.0
        )

        l = st.number_input(
            "Lebar tanah (m)",
            min_value=0.0,
            value=15.0
        )

        luas = p * l

    else:

        a = st.number_input(
            "Sisi sejajar pertama (m)",
            min_value=0.0,
            value=20.0
        )

        b = st.number_input(
            "Sisi sejajar kedua (m)",
            min_value=0.0,
            value=15.0
        )

        t = st.number_input(
            "Tinggi trapesium (m)",
            min_value=0.0,
            value=10.0
        )

        luas = ((a + b) / 2) * t

    if st.button("Hitung Luas"):

        st.session_state.hasil["Luas tanah"] = luas

        col1, col2 = st.columns(2)

        col1.metric("Luas tanah", f"{luas:.2f} m²")

        col2.metric(
            "Luas hektare",
            f"{luas / 10000:.4f} Ha"
        )

        st.success("Perhitungan luas berhasil.")

# ==================================
# JENIS TANAH
# ==================================

elif menu == "Jenis Tanah":

    st.header("Identifikasi Jenis Tanah")

    st.warning(
        "Pilih hasil identifikasi berdasarkan "
        "pengujian laboratorium atau data lapangan. "
        "Pemilihan ini bukan pengganti klasifikasi USCS."
    )

    jenis = st.selectbox(
        "Jenis tanah",
        [
            "GW - Kerikil bergradasi baik",
            "GP - Kerikil bergradasi buruk",
            "SW - Pasir bergradasi baik",
            "SP - Pasir bergradasi buruk",
            "GM - Kerikil berlanau",
            "GC - Kerikil berlempung",
            "SM - Pasir berlanau",
            "SC - Pasir berlempung",
            "ML - Lanau plastisitas rendah",
            "CL - Lempung plastisitas rendah",
            "MH - Lanau plastisitas tinggi",
            "CH - Lempung plastisitas tinggi",
            "OL - Tanah organik plastisitas rendah",
            "OH - Tanah organik plastisitas tinggi",
            "PT - Gambut"
        ]
    )

    deskripsi = {
        "GW": "Kerikil bergradasi baik",
        "GP": "Kerikil bergradasi buruk",
        "SW": "Pasir bergradasi baik",
        "SP": "Pasir bergradasi buruk",
        "GM": "Kerikil berlanau",
        "GC": "Kerikil berlempung",
        "SM": "Pasir berlanau",
        "SC": "Pasir berlempung",
        "ML": "Lanau plastisitas rendah",
        "CL": "Lempung plastisitas rendah",
        "MH": "Lanau plastisitas tinggi",
        "CH": "Lempung plastisitas tinggi",
        "OL": "Tanah organik plastisitas rendah",
        "OH": "Tanah organik plastisitas tinggi",
        "PT": "Gambut"
    }

    kode = jenis.split(" - ")[0]

    st.info(f"Kode klasifikasi: {kode}")

    st.write("Nama tanah:", deskripsi[kode])

    st.markdown("""
    ### Pengujian yang diperlukan

    - Analisis saringan.
    - Analisis hidrometer jika diperlukan.
    - Batas cair (Liquid Limit).
    - Batas plastis (Plastic Limit).
    - Indeks plastisitas (Plasticity Index).
    - Kadar bahan organik jika diperlukan.
    """)

    st.session_state.hasil["Jenis tanah"] = jenis

# ==================================
# ESTIMASI BIAYA
# ==================================

elif menu == "Estimasi Biaya":

    st.header("Estimasi Biaya Tanah dan Pekerjaan")

    luas = st.number_input(
        "Luas tanah (m²)",
        min_value=0.0,
        value=300.0
    )

    harga = st.number_input(
        "Harga tanah per m² (Rp)",
        min_value=0,
        value=1000000
    )

    biaya_pematangan = st.number_input(
        "Biaya pematangan lahan (Rp)",
        min_value=0,
        value=5000000
    )

    volume_galian = st.number_input(
        "Volume galian (m³)",
        min_value=0.0,
        value=10.0
    )

    harga_galian = st.number_input(
        "Harga galian per m³ (Rp)",
        min_value=0,
        value=75000
    )

    volume_urugan = st.number_input(
        "Volume urugan (m³)",
        min_value=0.0,
        value=10.0
    )

    harga_urugan = st.number_input(
        "Harga urugan per m³ (Rp)",
        min_value=0,
        value=100000
    )

    if st.button("Hitung Total Biaya"):

        total_tanah = luas * harga

        total_galian = volume_galian * harga_galian

        total_urugan = volume_urugan * harga_urugan

        total = (
            total_tanah
            + biaya_pematangan
            + total_galian
            + total_urugan
        )

        st.session_state.hasil.update({
            "Harga tanah": total_tanah,
            "Biaya pematangan": biaya_pematangan,
            "Biaya galian": total_galian,
            "Biaya urugan": total_urugan,
            "Total biaya": total
        })

        st.subheader("Rincian Biaya")

        data = pd.DataFrame({
            "Komponen": [
                "Pembelian tanah",
                "Pematangan lahan",
                "Pekerjaan galian",
                "Pekerjaan urugan"
            ],
            "Biaya (Rp)": [
                total_tanah,
                biaya_pematangan,
                total_galian,
                total_urugan
            ]
        })

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )

        st.success(
            f"TOTAL BIAYA: {rupiah(total)}"
        )

        st.bar_chart(
            data.set_index("Komponen")
        )

# ==================================
# LAPORAN
# ==================================

elif menu == "Laporan":

    st.header("Laporan Hasil Perhitungan")

    if st.session_state.hasil:

        for nama, nilai in st.session_state.hasil.items():

            if isinstance(nilai, float):
                st.write(f"**{nama}:** {nilai:.2f}")
            else:
                st.write(f"**{nama}:** {nilai}")

        isi = "LAPORAN CIVIL CALCULATOR\n\n"

        for nama, nilai in st.session_state.hasil.items():
            isi += f"{nama}: {nilai}\n"

        st.download_button(
            label="Download Laporan TXT",
            data=isi,
            file_name="laporan_civil_calculator.txt",
            mime="text/plain"
        )

    else:

        st.info(
            "Belum ada data. Silakan lakukan "
            "perhitungan terlebih dahulu."
        )

st.sidebar.divider()

st.sidebar.caption(
    "CIVIL CALCULATOR | Python & Streamlit"
)
