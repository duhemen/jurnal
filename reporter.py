# reporter.py
import db_manager
from datetime import datetime

def generate_laporan_bulanan(bulan_angka, tahun):
    data = db_manager.load_json("keuangan.json")
    total_d = 0
    total_k = 0
    
    for item in data:
        dt = datetime.fromisoformat(item['timestamp'])
        if dt.month == bulan_angka and dt.year == tahun:
            total_d += item['debit']
            total_k += item['kredit']
            
    return total_d, total_k