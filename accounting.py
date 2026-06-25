import db_manager
from datetime import datetime

def simpan_transaksi(deskripsi, kategori, diterima, pengeluaran, sumber, lampiran):
    diterima = float(diterima or 0)
    pengeluaran = float(pengeluaran or 0)
    selisih = diterima - pengeluaran
    
    # Menghitung kelebihan dan kekurangan
    kelebihan = selisih if selisih > 0 else 0
    kekurangan = abs(selisih) if selisih < 0 else 0

    data = db_manager.load_json("keuangan.json")
    transaksi = {
        "timestamp": datetime.now().isoformat(),
        "deskripsi": deskripsi,
        "kategori": kategori,
        "diterima": diterima,
        "pengeluaran": pengeluaran,
        "kelebihan": kelebihan,
        "kekurangan": kekurangan,
        "sumber": sumber,
        "lampiran": lampiran
    }
    data.append(transaksi)
    db_manager.save_json("keuangan.json", data)
    return "Berhasil", selisih, kelebihan, kekurangan

def simpan_kegiatan(nama, detail, sumber, diterima, pengeluaran, lampiran):
    diterima = float(diterima or 0)
    pengeluaran = float(pengeluaran or 0)
    selisih = diterima - pengeluaran
    kelebihan = selisih if selisih > 0 else 0
    kekurangan = abs(selisih) if selisih < 0 else 0

    data = db_manager.load_json("kegiatan.json")
    kegiatan = {
        "timestamp": datetime.now().isoformat(),
        "nama_aktivitas": nama,
        "detail": detail,
        "sumber": sumber,
        "diterima": diterima,
        "pengeluaran": pengeluaran,
        "kelebihan": kelebihan, # Penting ditambahkan
        "kekurangan": kekurangan, # Penting ditambahkan
        "lampiran": lampiran
    }
    data.append(kegiatan)
    db_manager.save_json("kegiatan.json", data)
    return "Berhasil", selisih, kelebihan, kekurangan

def filter_data_by_periode(data, periode):
    if periode == "Semua": return data
    
    today = datetime.now()
    filtered = []
    
    for item in data:
        dt = datetime.fromisoformat(item['timestamp'])
        
        if periode == "Harian" and dt.date() == today.date():
            filtered.append(item)
        elif periode == "Mingguan" and dt.isocalendar()[1] == today.isocalendar()[1] and dt.year == today.year:
            filtered.append(item)
        elif periode == "Bulanan" and dt.month == today.month and dt.year == today.year:
            filtered.append(item)
        elif periode == "Tahunan" and dt.year == today.year:
            filtered.append(item)
            
    return filtered

# Update fungsi get_data Anda:
def get_data_keuangan(periode):
    data = db_manager.load_json("keuangan.json")
    return filter_data_by_periode(data, periode)

def get_data_kegiatan(periode):
    data = db_manager.load_json("kegiatan.json")
    return filter_data_by_periode(data, periode)

def hitung_saldo():
    keu = db_manager.load_json("keuangan.json")
    keg = db_manager.load_json("kegiatan.json")
    total = {"APBN DIPA": 0, "Patungan Pegawai": 0}
    for item in keu + keg:
        sumber = item.get('sumber')
        if sumber in total:
            total[sumber] += (item.get('diterima', 0) - item.get('pengeluaran', 0))
    return total

# Tambahkan fungsi pembantu untuk menghitung selisih
def hitung_selisih(diterima, pengeluaran):
    selisih = float(diterima or 0) - float(pengeluaran or 0)
    return selisih, max(0, selisih), abs(min(0, selisih)) # selisih, kelebihan, kekurangan

def delete_data_by_index(filename, index):
    data = db_manager.load_json(filename)
    if 0 <= index < len(data):
        data.pop(index)
        db_manager.save_json(filename, data)