import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import accounting

class AppEmenPro(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Akuntansi Emen Pro v4.0")
        self.geometry("800x650")
        self.grid_columnconfigure(0, weight=1)
        
        self.tabview = ctk.CTkTabview(self, width=700, height=550)
        self.tabview.grid(row=0, column=0, pady=20, padx=20)
        
        tab_keu = self.tabview.add("Keuangan")
        tab_keg = self.tabview.add("Kegiatan")
        tab_dash = self.tabview.add("Dashboard")

        # --- TAB KEUANGAN ---
        self.desc_k = ctk.CTkEntry(tab_keu, placeholder_text="Deskripsi Transaksi")
        self.desc_k.pack(pady=5, fill="x")
        self.kat_k = ctk.CTkOptionMenu(tab_keu, values=["Pengadaan Barang", "Maintenance Jasa"])
        self.kat_k.pack(pady=5, fill="x")
        self.sumber_k = ctk.CTkOptionMenu(tab_keu, values=["APBN DIPA", "Patungan Pegawai"])
        self.sumber_k.pack(pady=5, fill="x")
        self.d_entry = ctk.CTkEntry(tab_keu, placeholder_text="Uang Diterima")
        self.d_entry.pack(pady=5, fill="x")
        self.p_entry = ctk.CTkEntry(tab_keu, placeholder_text="Pengeluaran")
        self.p_entry.pack(pady=5, fill="x")
        self.path_k = ctk.CTkEntry(tab_keu, placeholder_text="Lampiran Bukti")
        self.path_k.pack(pady=5, fill="x")
        ctk.CTkButton(tab_keu, text="Pilih Bukti", command=lambda: self.browse(self.path_k)).pack(pady=5)
        ctk.CTkButton(tab_keu, text="Simpan & Cek Selisih", fg_color="green", command=self.save_keuangan).pack(pady=10)

        # --- TAB KEGIATAN ---
        self.nama_act = ctk.CTkEntry(tab_keg, placeholder_text="Nama Aktivitas")
        self.nama_act.pack(pady=5, fill="x")
        self.detail_act = ctk.CTkEntry(tab_keg, placeholder_text="Detail Kegiatan")
        self.detail_act.pack(pady=5, fill="x")
        self.sumber_a = ctk.CTkOptionMenu(tab_keg, values=["APBN DIPA", "Patungan Pegawai"])
        self.sumber_a.pack(pady=5, fill="x")
        self.d_a = ctk.CTkEntry(tab_keg, placeholder_text="Dana Diterima")
        self.d_a.pack(pady=5, fill="x")
        self.p_a = ctk.CTkEntry(tab_keg, placeholder_text="Dana Dikeluarkan")
        self.p_a.pack(pady=5, fill="x")
        self.path_a = ctk.CTkEntry(tab_keg, placeholder_text="Path Bukti")
        self.path_a.pack(pady=5, fill="x")
        ctk.CTkButton(tab_keg, text="Pilih Bukti", command=lambda: self.browse(self.path_a)).pack(pady=5)
        ctk.CTkButton(tab_keg, text="Simpan & Cek Selisih", fg_color="blue", command=self.save_kegiatan).pack(pady=10)

        # --- TAB DASHBOARD ---
        self.periode_menu = ctk.CTkOptionMenu(tab_dash, values=["Harian", "Mingguan", "Bulanan", "Tahunan"], command=self.tampilkan_buku_besar)
        self.periode_menu.pack(pady=10)
        
        self.label_apbn = ctk.CTkLabel(tab_dash, text="APBN DIPA: Rp 0", font=("Arial", 14, "bold"))
        self.label_apbn.pack()
        
        # Label Judul Dinamis
        self.label_judul_keu = ctk.CTkLabel(tab_dash, text="Jurnal Keuangan", font=("Arial", 12, "italic"))
        self.label_judul_keu.pack()

        self.dash_tab = ctk.CTkTabview(tab_dash)
        self.dash_tab.pack(fill="both", expand=True)
        
        self.tabel_keu = self.buat_tabel(self.dash_tab.add("Buku Keuangan"))
        self.tabel_keg = self.buat_tabel(self.dash_tab.add("Buku Kegiatan"))
        
        self.update_dashboard()
        
        # --- TABEL BUKU BESAR (Profesional) ---
        # Membuat style agar terlihat modern
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        
        columns = ("tgl", "desc", "masuk", "keluar")
        self.tabel = ttk.Treeview(tab_dash, columns=columns, show="headings", height=8)
        
        self.tabel.heading("tgl", text="Tanggal")
        self.tabel.heading("desc", text="Deskripsi")
        self.tabel.heading("masuk", text="Masuk")
        self.tabel.heading("keluar", text="Keluar")
        
        # Mengatur lebar kolom
        self.tabel.column("tgl", width=80)
        self.tabel.column("desc", width=200)
        self.tabel.column("masuk", width=100)
        self.tabel.column("keluar", width=100)
        
        self.tabel.pack(pady=10, padx=10, fill="both", expand=True)

    def browse(self, entry):
        path = filedialog.askopenfilename()
        if path:
            entry.delete(0, 'end')
            entry.insert(0, path)

    def save_keuangan(self):
        status, selisih = accounting.simpan_transaksi(self.desc_k.get(), self.kat_k.get(), self.d_entry.get(), self.p_entry.get(), self.sumber_k.get(), self.path_k.get())
        messagebox.showinfo("Hasil Inspektorat", f"Status: {status}\nSelisih: Rp {selisih:,.2f}")
        self.update_dashboard()

    def save_kegiatan(self):
        status, selisih = accounting.simpan_kegiatan(self.nama_act.get(), self.detail_act.get(), self.sumber_a.get(), self.d_a.get(), self.p_a.get(), self.path_a.get())
        messagebox.showinfo("Hasil Inspektorat", f"Status: {status}\nSelisih: Rp {selisih:,.2f}")
        self.update_dashboard()

    def update_dashboard(self):
        saldo = accounting.hitung_saldo()
        self.label_apbn.configure(text=f"APBN DIPA: Rp {saldo['APBN DIPA']:,}")
        self.label_patungan.configure(text=f"Patungan Pegawai: Rp {saldo['Patungan Pegawai']:,}")
        self.after(5000, self.update_dashboard)

    def buat_tabel(self, parent):
        cols = ("tgl", "desc", "sumber", "masuk", "keluar")
        tabel = ttk.Treeview(parent, columns=cols, show="headings", height=8)
        for col in cols: tabel.heading(col, text=col.capitalize())
        tabel.column("tgl", width=80); tabel.column("desc", width=150)
        tabel.pack(fill="both", expand=True)
        return tabel

    def tampilkan_buku_besar(self, periode):
        # Update teks judul dinamis
        self.label_judul_keu.configure(text=f"Jurnal {periode} Keuangan & Kegiatan")
        
        # Bersihkan tabel
        for t in [self.tabel_keu, self.tabel_keg]:
            for i in t.get_children(): t.delete(i)
        
        # Isi data (Pastikan accounting.py sudah punya fungsi ini)
        for entry in accounting.get_data_keuangan(periode):
            self.tabel_keu.insert("", "end", values=(entry['timestamp'][:10], entry['deskripsi'], entry['sumber'], entry['diterima'], entry['pengeluaran']))
        for entry in accounting.get_data_kegiatan(periode):
            self.tabel_keg.insert("", "end", values=(entry['timestamp'][:10], entry['nama_aktivitas'], entry['sumber'], entry['diterima'], entry['pengeluaran']))

    def update_dashboard(self):
        saldo = accounting.hitung_saldo()
        self.label_apbn.configure(text=f"APBN DIPA: Rp {saldo['APBN DIPA']:,} | Patungan: Rp {saldo['Patungan Pegawai']:,}")
        self.after(5000, self.update_dashboard)

app = AppEmenPro()
app.mainloop()