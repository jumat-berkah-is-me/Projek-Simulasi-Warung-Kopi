import random
import config

def pelanggan(env, nama, tipe, jumlah_cup, kedai, jenis_skenario, data_laporan):
    waktu_datang = env.now
    
    prioritas = 10
    
    if jenis_skenario == config.SCENARIO_A:
        prioritas = 1
        
    elif jenis_skenario == config.SCENARIO_B:
        if jumlah_cup <= 2:
            prioritas = 1
        else:
            prioritas = 10

    with kedai.barista.request(priority=prioritas) as req:
        yield req
        
        lama_buat = jumlah_cup * config.WAKTU_BUAT_PER_CUP
        yield env.process(kedai.proses_buat_kopi(lama_buat))
        
    waktu_selesai = env.now
    waktu_tunggu = waktu_selesai - waktu_datang
    
    data_laporan.append({
        'Skenario': jenis_skenario,
        'Nama': nama,
        'Tipe': tipe,
        'Jumlah_Cup': jumlah_cup,
        'Waktu_Tunggu': waktu_tunggu
    })

def generator_pelanggan(env, kedai, skenario, data_laporan):
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / config.INTERVAL_PELANGGAN))
        i += 1
        
        if random.random() < 0.6:
            tipe = 'Online'
            jumlah_cup = random.randint(3, 8)
        else:
            tipe = 'Walk-in'
            jumlah_cup = random.randint(1, 2)
            
        env.process(pelanggan(env, f'Pelanggan_{i}', tipe, jumlah_cup, kedai, skenario, data_laporan))
