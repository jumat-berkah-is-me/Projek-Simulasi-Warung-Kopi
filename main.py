import simpy
import random
import statistics
import config
from entities import TomoroCoffee
from processes import generator_pelanggan

def jalankan_simulasi(skenario, data_laporan):
    random.seed(config.RANDOM_SEED)
    env = simpy.Environment()
    kedai = TomoroCoffee(env)
    env.process(generator_pelanggan(env, kedai, skenario, data_laporan))
    env.run(until=config.WAKTU_SIMULASI)

def cetak_laporan(data_laporan):
    print("\n" + "="*50)
    print(f"{'HASIL ANALISIS SIMULASI':^50}")
    print("="*50)
    
    for skenario in [config.SCENARIO_A, config.SCENARIO_B]:
        data_skenario = [d for d in data_laporan if d['Skenario'] == skenario]
        walk_in_times = [d['Waktu_Tunggu'] for d in data_skenario if d['Tipe'] == 'Walk-in']
        online_times = [d['Waktu_Tunggu'] for d in data_skenario if d['Tipe'] == 'Online']
        
        avg_walk_in = statistics.mean(walk_in_times) if walk_in_times else 0
        avg_online = statistics.mean(online_times) if online_times else 0
        
        print(f"\nSKENARIO: {skenario}")
        print(f"  > Rata-rata Waktu Tunggu Walk-in : {avg_walk_in:.2f} menit")
        print(f"  > Rata-rata Waktu Tunggu Online  : {avg_online:.2f} menit")
        print(f"  > Total Pelanggan Dilayani       : {len(data_skenario)} orang")
        print("-" * 30)

if __name__ == "__main__":
    data_laporan_global = []
    print("Memulai simulasi...")
    jalankan_simulasi(config.SCENARIO_A, data_laporan_global)
    jalankan_simulasi(config.SCENARIO_B, data_laporan_global)
    cetak_laporan(data_laporan_global)
