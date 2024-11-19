import tkinter as tk
from tkinter import ttk, messagebox

class AbsensiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Kehadiran Pegawai Kafe IF")
        self.geometry("500x400")
        self.configure(bg='#f0f0f0')
        self.create_main_menu()

    def show_pegawai_login(self):
        # Bersihkan semua widget
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("350x250")
        self.configure(bg='#3d2b1f')

        tk.Label(self, text="Login Pegawai", font=("Arial", 16, "bold"), bg='#f0f0f0', fg='#333').pack(pady=(20, 0))

        tk.Label(self, text="Nomor Telepon:", bg='#f0f0f0', fg='#333').pack(pady=(10, 5))
        nomor_telepon_entry = tk.Entry(self)
        nomor_telepon_entry.pack()

        ttk.Button(self, text="Login", command=self.menu_pegawai).pack(pady=10)
        ttk.Button(self, text="Back", command=self.create_main_menu).pack(pady=10)

    def menu_pegawai(self):
        # Bersihkan semua widget
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("500x400")
        
        main_frame = tk.Frame(self, bg='#3d2b1f')
        main_frame.pack(expand=True, fill='both')
        
        tk.Label(main_frame, text="Select To Continue", font=("Arial", 18, "bold"), bg='#f0f0f0', fg='#333').pack(pady=(20, 0))

        ttk.Button(main_frame, text="Absensi", command=self.tampilan_absensi).pack(pady=10)
        ttk.Button(main_frame, text="Gaji", command=self.tampilan_gaji).pack(pady=10)
        ttk.Button(self, text="Back", command=self.show_pegawai_login).pack(pady=10)

    def tampilan_absensi(self):
        # Bersihkan semua widget
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("400x300")
        self.configure(bg="#3d2b1f")

        # Judul
        tk.Label(self, text="Absensi", font=("Helvetica", 24, "bold"), bg="#3d2b1f", fg="white").pack(pady=10)

        # Pilihan masuk/keluar
        tk.Label(self, text="Apakah ini waktu masuk atau keluar? (masuk/keluar):", 
                 font=("Helvetica", 10), bg="#3d2b1f", fg="white").pack(pady=5)
        
        combo_option = ttk.Combobox(self, values=["Masuk", "Keluar"], font=("Helvetica", 10))
        combo_option.pack()

        # Input nomor telepon
        tk.Label(self, text="Masukkan nomor telepon untuk check-in/check-out:", 
                 font=("Helvetica", 10), bg="#3d2b1f", fg="white").pack(pady=5)
        
        entry_phone = tk.Entry(self, font=("Helvetica", 10))
        entry_phone.pack()

        # Tombol submit dan back
        button_frame = tk.Frame(self, bg="#3d2b1f")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="BACK", font=("Helvetica", 10), bg="gray", fg="black", width=10, command=self.menu_pegawai).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="SUBMIT", font=("Helvetica", 10), bg="#d5aa66", fg="black", width=10, command=lambda: messagebox.showinfo("Absensi", "Data berhasil di-submit!")).grid(row=0, column=1, padx=10)

    def tampilan_gaji(self):
        # Bersihkan semua widget
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("400x300")
        self.configure(bg="#3d2b1f")

        # Judul
        tk.Label(self, text="Gaji Mingguan", font=("Helvetica", 24, "bold"), bg="#3d2b1f", fg="white").pack(pady=10)

        # Kotak informasi
        info_frame = tk.Frame(self, bg="#d5aa66", width=300, height=150)
        info_frame.pack(pady=10)
        info_frame.pack_propagate(False)

        tk.Label(info_frame, text="Total Jam Kerja: 0 jam", font=("Helvetica", 12), bg="#d5aa66", fg="black").pack(pady=5)
        tk.Label(info_frame, text="Total Gaji : Rp 0", font=("Helvetica", 12), bg="#d5aa66", fg="black").pack(pady=5)

        # Tombol back
        tk.Button(self, text="BACK", font=("Helvetica", 10), bg="gray", fg="black", width=10, command=self.menu_pegawai).pack(pady=20)

if __name__ == "__main__":
    app = AbsensiApp()
    app.mainloop()