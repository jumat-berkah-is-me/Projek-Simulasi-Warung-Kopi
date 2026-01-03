from simpy import PriorityResource
from config import JUMLAH_BARISTA

class TomoroCoffee:
    def __init__(self, env):
        self.env = env
        self.barista = PriorityResource(env, capacity=JUMLAH_BARISTA)
    
    def proses_buat_kopi(self, lama_waktu):
        yield self.env.timeout(lama_waktu)