import streamlit as st
import pandas as pd
import simpy
import random
import config
from entities import TomoroCoffee
from processes import generator_pelanggan

st.set_page_config(page_title="Simulasi Kopi Senja", layout="wide")

st.title("Simulasi Antrean 'Kopi Senja'")
st.markdown("""
Aplikasi ini mensimulasikan perbandingan efisiensi antara **Sistem FIFO** (Kondisi Saat Ini) 
dan **Sistem Prioritas** (Solusi Usulan) untuk mengatasi penumpukan antrean.
""")

st.sidebar.header("Pengaturan Simulasi")

durasi_simulasi = st.sidebar.slider("Durasi Simulasi (Menit)", 60, 480, 180)
config.WAKTU_SIMULASI = durasi_simulasi

interval_pelanggan = st.sidebar.slider("Rata-rata Kedatangan (Menit)", 1.0, 10.0, 3.0)
config.INTERVAL_PELANGGAN = interval_pelanggan

kecepatan_barista = st.sidebar.slider("Kecepatan Bikin Kopi (Menit/Cup)", 0.5, 5.0, 1.5)
config.WAKTU_BUAT_PER_CUP = kecepatan_barista

st.sidebar.markdown("---")
tombol_run = st.sidebar.button("Jalankan Simulasi")

def run_scenario(skenario):
    random.seed(config.RANDOM_SEED)
    env = simpy.Environment()
    kedai = TomoroCoffee(env)
    
    data_laporan = []
    env.process(generator_pelanggan(env, kedai, skenario, data_laporan))
    env.run(until=config.WAKTU_SIMULASI)
    
    return data_laporan

if tombol_run:
    with st.spinner('Sedang mensimulasikan antrean...'):
        data_A = run_scenario(config.SCENARIO_A)
        data_B = run_scenario(config.SCENARIO_B)

    df_A = pd.DataFrame(data_A)
    df_B = pd.DataFrame(data_B)

    avg_wait_A = df_A[df_A['Tipe'] == 'Walk-in']['Waktu_Tunggu'].mean()
    avg_wait_B = df_B[df_B['Tipe'] == 'Walk-in']['Waktu_Tunggu'].mean()
    
    improvement = avg_wait_A - avg_wait_B
    percent_imp = (improvement / avg_wait_A) * 100 if avg_wait_A > 0 else 0

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Waktu Tunggu (Skenario A - FIFO)", 
            value=f"{avg_wait_A:.2f} menit",
            help="Rata-rata waktu tunggu pelanggan Walk-in saat ini"
        )
    
    with col2:
        st.metric(
            label="Waktu Tunggu (Skenario B - Solusi)", 
            value=f"{avg_wait_B:.2f} menit",
            delta=f"-{improvement:.2f} menit (Lebih Cepat)",
            delta_color="normal"
        )

    with col3:
        st.metric(
            label="Efisiensi Meningkat",
            value=f"{percent_imp:.1f}%"
        )

    st.markdown("---")

    st.subheader("Analisis Visual")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("**Perbandingan Rata-rata Waktu Tunggu (Semua Tipe)**")
        avg_data = pd.DataFrame({
            'Skenario': ['A (FIFO)', 'B (Solusi)'],
            'Rata-rata Waktu Tunggu (Menit)': [
                df_A['Waktu_Tunggu'].mean(), 
                df_B['Waktu_Tunggu'].mean()
            ]
        })
        st.bar_chart(avg_data.set_index('Skenario'))
        
    with col_chart2:
        st.markdown("**Detail Distribusi Pelanggan Walk-in**")
        st.write("Sampel data Walk-in (Skenario B):")
        st.dataframe(df_B[df_B['Tipe'] == 'Walk-in'].tail(5))

else:
    st.info("Silakan atur parameter di sebelah kiri dan tekan tombol 'Jalankan Simulasi'")
