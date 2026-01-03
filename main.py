import simpy
import random
import statistics

WAKTU_SIMULASI = 180
JUMLAH_BARISTA = 1
WAKTU_BUAT_PER_CUP = 2 # menit
INTERVAL_PELANGGAN = 3 # Setiap 3 menit ada pelanggan baru

data_laporan = []