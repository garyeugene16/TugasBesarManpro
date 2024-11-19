import tkinter as tk
from tkinter import ttk, messagebox

class AbsensiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Kehadiran Pegawai Kafe IF")
        self.geometry("500x400")
        self.configure(bg='#f0f0f0')
        self.create_main_menu()

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
