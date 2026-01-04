import streamlit as st
import pandas as pd
import simpy
import random
import altair as alt
import config
from entities import TomoroCoffee
from processes import generator_pelanggan

st.set_page_config(
    page_title="Dashboard Simulasi Kopi",
    page_icon="",
    layout="wide"
)

st.title("Analisis Antrean: Tomoro Coffee Kemang")

with st.sidebar:
    st.header("Parameter Simulasi")
    
    durasi_sim = st.slider("Durasi Buka Toko (Menit)", 60, 480, 180, step=30)
    config.WAKTU_SIMULASI = durasi_sim
    
    interval_pel = st.slider("Interval Kedatangan (Menit)", 1.0, 5.0, 3.0, step=0.5)
    config.INTERVAL_PELANGGAN = interval_pel
    
    kecepatan_barista = st.slider("Kecepatan Barista (Menit/Cup)", 0.5, 3.0, 1.5, step=0.1)
    config.WAKTU_BUAT_PER_CUP = kecepatan_barista
    
    tombol_run = st.button("JALANKAN SIMULASI", type="primary")

def run_simulation(skenario_name):
    random.seed(config.RANDOM_SEED)
    env = simpy.Environment()
    kedai = TomoroCoffee(env)
    data_log = []
    
    env.process(generator_pelanggan(env, kedai, skenario_name, data_log))
    env.run(until=config.WAKTU_SIMULASI)
    
    df = pd.DataFrame(data_log)
    df['Urutan_Pelanggan'] = df.index + 1
    return df

if tombol_run:
    with st.spinner('Sedang memproses antrean...'):
        df_a = run_simulation(config.SCENARIO_A)
        df_b = run_simulation(config.SCENARIO_B)

    st.subheader("1. Ringkasan Hasil (Rata-rata)")
    
    wait_a_walkin = df_a[df_a['Tipe'] == 'Walk-in']['Waktu_Tunggu'].mean()
    wait_b_walkin = df_b[df_b['Tipe'] == 'Walk-in']['Waktu_Tunggu'].mean()
    delta = wait_a_walkin - wait_b_walkin
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Walk-in: Skenario A (FIFO)", f"{wait_a_walkin:.1f} menit")
    with col2:
        st.metric("Walk-in: Skenario B (Prioritas)", f"{wait_b_walkin:.1f} menit", 
                    delta=f"{delta:.1f} menit lebih cepat", delta_color="normal")
    with col3:
        wait_a_online = df_a[df_a['Tipe'] == 'Online']['Waktu_Tunggu'].mean()
        wait_b_online = df_b[df_b['Tipe'] == 'Online']['Waktu_Tunggu'].mean()
        st.metric("Impact ke Online", f"{wait_b_online:.1f} menit", 
                    delta=f"{(wait_a_online - wait_b_online):.1f} menit", delta_color="off")

    st.divider()

    tab1, tab2 = st.tabs(["Grafik Time-Series", "Data Mentah"])

    with tab1:
        st.markdown("### Bagaimana antrean terbentuk seiring waktu?")
        st.caption("Grafik ini menunjukkan pengalaman setiap pelanggan dari urutan pertama sampai terakhir.")
        
        
        plot_a = df_a.copy()
        plot_b = df_b.copy()

        plot_a['Skenario'] = 'A (FIFO)'
        plot_b['Skenario'] = 'B (Solusi)'
        combined_df = pd.concat([plot_a, plot_b])

        chart = alt.Chart(combined_df).mark_line(point=True).encode(
            x=alt.X('Urutan_Pelanggan', title='Urutan Kedatangan Pelanggan'),
            y=alt.Y('Waktu_Tunggu', title='Waktu Tunggu (Menit)'),
            color=alt.Color('Skenario', scale=alt.Scale(domain=['A (FIFO)', 'B (Solusi)'], range=['#ff4b4b', '#00c0f2'])),
            tooltip=['Nama', 'Tipe', 'Jumlah_Cup', 'Waktu_Tunggu']
        ).properties(height=400).interactive()
        
        st.altair_chart(chart, width='stretch')
        st.info("Garis Merah (A) yang menanjak tinggi menunjukkan terjadinya Bottleneck. Garis Biru (B) yang rendah menunjukkan antrean terkendali.")

    with tab2:
        st.markdown("### Log Data Detail")
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("#### Data Skenario A (FIFO)")
            st.dataframe(df_a[['Nama', 'Tipe', 'Jumlah_Cup', 'Waktu_Tunggu']], height=300)
            
        with col_t2:
            st.markdown("#### Data Skenario B (Solusi)")
            st.dataframe(df_b[['Nama', 'Tipe', 'Jumlah_Cup', 'Waktu_Tunggu']], height=300)

else:
    st.warning("Hasil simulasi belum tersedia. Silakan atur parameter di sidebar dan klik tombol 'JALANKAN SIMULASI'.")
