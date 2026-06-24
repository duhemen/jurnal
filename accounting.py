import db_manager
from datetime import datetime

def simpan_transaksi(deskripsi, kategori, diterima, pengeluaran, sumber, lampiran):
    # Logika simpan keuangan ke keuangan.json
    data = db_manager.load_json("keuangan.json")
    transaksi = {
        "timestamp": datetime.now().isoformat(),
        "deskripsi": deskripsi,
        "kategori": kategori,
        "diterima": float(diterima or 0),
        "pengeluaran": float(pengeluaran or 0),
        "sumber": sumber,
        "lampiran": lampiran
    }
    data.append(transaksi)
    db_manager.save_json("keuangan.json", data)
    return "Berhasil", (float(diterima or 0) - float(pengeluaran or 0))

def simpan_kegiatan(nama, detail, sumber, diterima, pengeluaran, lampiran):
    # Logika simpan kegiatan ke kegiatan.json
    data = db_manager.load_json("kegiatan.json")
    kegiatan = {
        "timestamp": datetime.now().isoformat(),
        "nama_aktivitas": nama,
        "detail": detail,
        "sumber": sumber,
        "diterima": float(diterima or 0),
        "pengeluaran": float(pengeluaran or 0),
        "lampiran": lampiran
    }
    data.append(kegiatan)
    db_manager.save_json("kegiatan.json", data)
    return "Berhasil", (float(diterima or 0) - float(pengeluaran or 0))

def get_data_keuangan(periode):
    return db_manager.load_json("keuangan.json")

def get_data_kegiatan(periode):
    return db_manager.load_json("kegiatan.json")

def hitung_saldo():
    keu = db_manager.load_json("keuangan.json")
    keg = db_manager.load_json("kegiatan.json")
    total = {"APBN DIPA": 0, "Patungan Pegawai": 0}
    for item in keu + keg:
        sumber = item.get('sumber')
        if sumber in total:
            total[sumber] += (item.get('diterima', 0) - item.get('pengeluaran', 0))
    return total