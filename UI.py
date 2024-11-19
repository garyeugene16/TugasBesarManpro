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

if __name__ == "__main__":
    app = AbsensiApp()
    app.mainloop()
