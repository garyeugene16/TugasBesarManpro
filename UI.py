import tkinter as tk
from tkinter import ttk, messagebox

class AbsensiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Kehadiran Pegawai Kafe IF")
        self.geometry("500x400")
        self.configure(bg='#f0f0f0')
        self.create_main_menu()
    
    def create_main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("500x400")
        
        main_frame = tk.Frame(self, bg='#3d2b1f')
        main_frame.pack(expand=True, fill='both')
        
        tk.Label(main_frame, text="Sistem Manajemen", font=("Arial", 18, "bold"), bg='#3d2b1f', fg='white').pack(pady=(20, 0))
        tk.Label(main_frame, text="Kehadiran Pegawai Kafe IF", font=("Arial", 14), bg='#3d2b1f', fg='white').pack(pady=(0, 20))

        ttk.Button(main_frame, text="Pemilik", command=self.show_pemilik_login).pack(pady=10)
        ttk.Button(main_frame, text="Pegawai", command=self.show_pegawai_login).pack(pady=10)

    def show_pemilik_login(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("350x300")
        self.configure(bg='#3d2b1f')

        tk.Label(self, text="Login Pemilik", font=("Arial", 16, "bold"), bg='#f0f0f0', fg='#333').pack(pady=(20, 0))

        tk.Label(self, text="Username:", bg='#f0f0f0', fg='#333').pack(pady=(10, 5))
        username_entry = tk.Entry(self)
        username_entry.pack()

        tk.Label(self, text="Password:", bg='#f0f0f0', fg='#333').pack(pady=(10, 5))
        password_entry = tk.Entry(self, show="*")
        password_entry.pack()

        ttk.Button(self, text="Login", command=lambda: self.show_pemilik_menu()).pack(pady=10)
        ttk.Button(self, text="Back", command=self.create_main_menu).pack(pady=10)

    def show_pemilik_menu(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("350x300")
        self.configure(bg='#3d2b1f')

        tk.Label(self, text="Menu Pemilik", font=("Arial", 16, "bold"), bg='#f0f0f0', fg='#333').pack(pady=(20, 0))

        ttk.Button(self, text="Registrasi Pegawai Baru", command=self.pegawai_baru).pack(pady=10)
        ttk.Button(self, text="Laporan Absensi", command=lambda: self.show_laporan("Laporan Absensi")).pack(pady=10)
        ttk.Button(self, text="Laporan Gaji", command=lambda: self.show_laporan("Laporan Gaji")).pack(pady=10)

        ttk.Button(self, text="Back", command=self.create_main_menu).pack(pady=10)

    # Tambahan Baru
    def pegawai_baru(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("500x600")
        self.configure(bg='#3d2b1f')

        tk.Label(self, text="Registrasi Pegawai Baru", font=("Arial", 16, "bold"), bg='#f0f0f0', fg='#333').pack(pady=(20, 0))

        # Nama
        tk.Label(self, text="Nama:", bg='#f0f0f0', fg='#333').pack(pady=(10, 5))
        nama_entry = tk.Entry(self)
        nama_entry.pack()

        # Nomor Telepon
        tk.Label(self, text="Nomor Telepon:", bg='#f0f0f0', fg='#333').pack(pady=(10, 5))
        telepon_entry = tk.Entry(self)
        telepon_entry.pack()

        # Email
        tk.Label(self, text="Email:", bg='#f0f0f0', fg='#333').pack(pady=(10, 5))
        email_entry = tk.Entry(self)
        email_entry.pack()

        # Alamat
        tk.Label(self, text="Alamat:", bg='#f0f0f0', fg='#333').pack(pady=(10, 5))
        alamat_entry = tk.Entry(self)
        alamat_entry.pack()

        # Dropdown Kecamatan
        tk.Label(self, text="Kecamatan:", bg='#f0f0f0', fg='#333').pack(pady=(10, 5))
        kecamatan_var = tk.StringVar()
        kecamatan_dropdown = ttk.Combobox(self, textvariable=kecamatan_var, state="readonly")
        kecamatan_dropdown['values'] = ["Kecamatan A", "Kecamatan B", "Kecamatan C"]  # Contoh opsi
        kecamatan_dropdown.pack()

        # Dropdown Kelurahan
        tk.Label(self, text="Kelurahan:", bg='#f0f0f0', fg='#333').pack(pady=(10, 5))
        kelurahan_var = tk.StringVar()
        kelurahan_dropdown = ttk.Combobox(self, textvariable=kelurahan_var, state="readonly")
        kelurahan_dropdown['values'] = ["Kelurahan X", "Kelurahan Y", "Kelurahan Z"]  # Contoh opsi
        kelurahan_dropdown.pack()

        # Dropdown Jabatan
        tk.Label(self, text="Jabatan:", bg='#f0f0f0', fg='#333').pack(pady=(10, 5))
        jabatan_var = tk.StringVar()
        jabatan_dropdown = ttk.Combobox(self, textvariable=jabatan_var, state="readonly")
        jabatan_dropdown['values'] = ["Manager", "Koki", "Bartender", "Pelayan", "Kasir"]  # Contoh opsi
        jabatan_dropdown.pack()

        # Tombol Submit
        ttk.Button(self, text="Submit", command=lambda: messagebox.showinfo("Registrasi", "Data berhasil di-submit!")).pack(pady=10)

        # Tombol Back
        ttk.Button(self, text="Back", command=self.show_pemilik_menu).pack(pady=10)

    def show_laporan(self, title):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("500x400")
        self.configure(bg='#3d2b1f')

        # Background styling (sesuai tema kopi)
        bg_frame = tk.Frame(self, bg="#3e2c21")  # Warna latar belakang cokelat
        bg_frame.pack(expand=True, fill="both")

        # Judul Laporan
        tk.Label(bg_frame, text=title, font=("Brush Script MT", 28, "bold"), bg="#3e2c21", fg="#d8b982").pack(pady=(20, 10))

        # Input Tanggal Mulai
        tk.Label(bg_frame, text="Masukkan tanggal mulai (YYYY-MM-DD)", font=("Arial", 12, "bold"), bg="#3e2c21", fg="#fff").pack(pady=(10, 5))
        tanggal_mulai_entry = tk.Entry(bg_frame, font=("Arial", 12), bg="#f9f9f9", fg="#333", justify="center")
        tanggal_mulai_entry.pack(pady=5, padx=20, fill="x")

        # Input Tanggal Akhir
        tk.Label(bg_frame, text="Masukkan tanggal akhir (YYYY-MM-DD)", font=("Arial", 12, "bold"), bg="#3e2c21", fg="#fff").pack(pady=(10, 5))
        tanggal_akhir_entry = tk.Entry(bg_frame, font=("Arial", 12), bg="#f9f9f9", fg="#333", justify="center")
        tanggal_akhir_entry.pack(pady=5, padx=20, fill="x")

        # Tombol Navigasi
        button_frame = tk.Frame(bg_frame, bg="#3e2c21")
        button_frame.pack(pady=(20, 0))

        ttk.Button(button_frame, text="BACK", command=self.show_pemilik_menu).pack(side="left", padx=20)
        ttk.Button(button_frame, text="SUBMIT", command=lambda: messagebox.showinfo("Laporan", "Berikut Datanya: ")).pack(side="right", padx=20)
        
if __name__ == "__main__":
    app = AbsensiApp()
    app.mainloop()
