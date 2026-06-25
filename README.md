# Sistem Akuntansi Emen Pro v4.0
Sistem Akuntansi Emen Pro adalah aplikasi desktop berbasis Python yang dirancang untuk membantu pencatatan keuangan dan kegiatan secara sistematis, transparan, dan akuntabel.

## 🚀 Fitur Utama
- Dashboard Interaktif: Pantau saldo APBN DIPA dan Patungan Pegawai secara real-time.
- Dual Tracking: Buku Besar Keuangan dan Buku Besar Kegiatan terpisah untuk akurasi data.
- Filter Periode: Analisis data harian, mingguan, bulanan, hingga tahunan.
- Export Laporan: Ekspor data langsung ke file Excel (.xlsx).
- Version Control: Terintegrasi dengan GitHub untuk keamanan data kode.
- Manajemen Lampiran: Kelola bukti transaksi dengan mudah.

## 🛠️ Persiapan Lingkungan
Pastikan Anda sudah menginstal Python (versi 3.10 atau lebih baru) di komputer Anda.

### 1. Clone Repositori:
Buka terminal/CMD dan jalankan perintah:

```Bash
git clone https://github.com/duhemen/jurnal.git
cd jurnal
```
### 2. Instalasi Library:
Aplikasi ini membutuhkan customtkinter, pandas, dan openpyxl. Jalankan perintah berikut:

```Bash
pip install customtkinter pandas openpyxl
```
## 🏃 Cara Menjalankan Aplikasi
### 1. Pastikan Anda berada di direktori C:\jurnal.
### 2. Jalankan aplikasi dengan perintah:

~~~Bash
python app_gui.py
~~~
## 📝 Panduan Pengaplikasian
### 1. Input Data:
- Pilih tab Keuangan atau Kegiatan.
- Isi formulir yang tersedia.
- Klik "Simpan & Cek Selisih" untuk menyimpan transaksi. Sistem akan otomatis menghitung selisih (lebih/kurang) dana.
### 2. Dashboard & Laporan:
- Buka tab Dashboard.
- Pilih periode pada dropdown (Harian, Mingguan, dll) untuk memfilter data.
- Gunakan sub-tab untuk berpindah antara "Buku Besar Keuangan" dan "Buku Besar Kegiatan".
### 3. Ekspor Data:
- Klik tombol "Export ke Excel" pada tab Dashboard untuk menyimpan laporan ke komputer Anda.
### 4. Manajemen Transaksi:
- Klik kanan pada baris tabel di Dashboard untuk opsi menghapus transaksi yang salah input.
## 🛡️ Keamanan
Aplikasi ini menyimpan data secara lokal dalam format .json. Pastikan untuk melakukan backup folder ini secara berkala ke penyimpanan awan (cloud).
