import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import tkinter as tk  # PENTING: Perlu untuk Menu
import accounting
import pandas as pd

class AppEmenPro(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Akuntansi Emen Pro v4.0")
        self.geometry("900x700")
        self.grid_columnconfigure(0, weight=1)
        # Mengatur agar baris ke-0 melar (weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.tabview = ctk.CTkTabview(self, width=850, height=600)
        # Gunakan sticky="nsew" agar widget menempel ke semua sisi saat di-maximize
        self.tabview.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")
        
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
        self.periode_menu = ctk.CTkOptionMenu(tab_dash, values=["Semua", "Harian", "Mingguan", "Bulanan", "Tahunan"], command=self.tampilkan_buku_besar)
        self.periode_menu.pack(pady=10)
        
        self.label_apbn = ctk.CTkLabel(tab_dash, text="APBN DIPA: Rp 0 | Patungan: Rp 0", font=("Arial", 14, "bold"))
        self.label_apbn.pack()
        self.label_patungan = ctk.CTkLabel(tab_dash, text="Patungan: Rp 0", font=("Arial", 14, "bold"))
        self.label_patungan.pack()
        self.label_judul_keu = ctk.CTkLabel(tab_dash, text="Jurnal Keuangan", font=("Arial", 12, "italic"))
        self.label_judul_keu.pack()

        # Tabview di Dashboard
        self.dash_tab = ctk.CTkTabview(tab_dash, command=lambda: self.tampilkan_buku_besar(self.periode_menu.get()))
        self.dash_tab.pack(fill="both", expand=True, pady=10)
        
        self.frame_keu = self.dash_tab.add("Buku Besar Keuangan")
        self.frame_keg = self.dash_tab.add("Buku Besar Kegiatan")
        
        self.tabel_keu = self.buat_tabel(self.frame_keu)
        self.tabel_keg = self.buat_tabel(self.frame_keg)
        
        # Binding Klik Kanan
        self.tabel_keu.bind("<Button-3>", self.tampilkan_menu)
        self.tabel_keg.bind("<Button-3>", self.tampilkan_menu)
        
        # Tombol Export
        ctk.CTkButton(tab_dash, text="Export ke Excel", fg_color="gray", command=self.export_to_excel).pack(pady=5)

        self.update_dashboard()

    # --- FUNGSI ---
    def tampilkan_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Hapus Transaksi", command=self.hapus_transaksi)
        menu.post(event.x_root, event.y_root)

    def browse(self, entry):
        path = filedialog.askopenfilename()
        if path:
            entry.delete(0, 'end')
            entry.insert(0, path)

    def save_keuangan(self):
        status, selisih, lebih, kurang = accounting.simpan_transaksi(self.desc_k.get(), self.kat_k.get(), self.d_entry.get(), self.p_entry.get(), self.sumber_k.get(), self.path_k.get())
        messagebox.showinfo("Hasil", f"Status: {status}\nSelisih: {selisih:,.2f}")
        self.update_dashboard()

    def save_kegiatan(self):
        status, selisih, lebih, kurang = accounting.simpan_kegiatan(self.nama_act.get(), self.detail_act.get(), self.sumber_a.get(), self.d_a.get(), self.p_a.get(), self.path_a.get())
        messagebox.showinfo("Hasil", f"Status: {status}\nSelisih: {selisih:,.2f}")
        self.update_dashboard()

    def buat_tabel(self, parent):
        cols = ("tgl", "desc", "sumber", "masuk", "keluar", "lebih", "kurang", "lampiran")
        tabel = ttk.Treeview(parent, columns=cols, show="headings", height=8)
        for col in cols: 
            tabel.heading(col, text=col.capitalize())
            tabel.column(col, width=80)
        tabel.pack(fill="both", expand=True)
        # Warna
        tabel.tag_configure("positif", foreground="green")
        tabel.tag_configure("negatif", foreground="red")
        return tabel

    def tampilkan_buku_besar(self, periode):
        tab_aktif = self.dash_tab.get()
        self.label_judul_keu.configure(text=f"Jurnal {periode} - {tab_aktif}")
        for t in [self.tabel_keu, self.tabel_keg]:
            for i in t.get_children(): t.delete(i)
        
        # Isi Tabel
        for entry in accounting.get_data_keuangan(periode):
            selisih = float(entry.get('diterima', 0)) - float(entry.get('pengeluaran', 0))
            tag = "positif" if selisih >= 0 else "negatif"
            self.tabel_keu.insert("", "end", values=(entry['timestamp'][:10], entry['deskripsi'], entry['sumber'], entry['diterima'], entry['pengeluaran'], entry.get('kelebihan', 0), entry.get('kekurangan', 0), entry['lampiran']), tags=(tag,))
        
        for entry in accounting.get_data_kegiatan(periode):
            selisih = float(entry.get('diterima', 0)) - float(entry.get('pengeluaran', 0))
            tag = "positif" if selisih >= 0 else "negatif"
            self.tabel_keg.insert("", "end", values=(entry['timestamp'][:10], entry['nama_aktivitas'], entry['sumber'], entry['diterima'], entry['pengeluaran'], entry.get('kelebihan', 0), entry.get('kekurangan', 0), entry['lampiran']), tags=(tag,))

    def update_dashboard(self):
        saldo = accounting.hitung_saldo()
        self.label_apbn.configure(text=f"APBN DIPA: Rp {saldo['APBN DIPA']:,}")
        self.label_patungan.configure(text=f"Patungan Pegawai: Rp {saldo['Patungan Pegawai']:,}")
        self.after(5000, self.update_dashboard)

    def hapus_transaksi(self):
        # Tambahkan logika hapus permanen dari JSON di sini nanti
        messagebox.showinfo("Info", "Fitur hapus permanen akan segera tersedia.")

    def export_to_excel(self):
        data = []
        tabel = self.tabel_keu if "Keuangan" in self.dash_tab.get() else self.tabel_keg
        for child in tabel.get_children(): data.append(tabel.item(child)["values"])
        df = pd.DataFrame(data, columns=["Tgl", "Desc", "Sumber", "Masuk", "Keluar", "Lebih", "Kurang", "Lampiran"])
        path = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if path: df.to_excel(path, index=False)

if __name__ == "__main__":
    app = AppEmenPro()
    app.mainloop()