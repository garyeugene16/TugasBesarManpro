import tkinter as tk
from tkinter import ttk, messagebox

class AbsensiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Kehadiran Pegawai Kafe IF")
        self.geometry("500x400")
        self.configure(bg='#f0f0f0')
        self.create_main_menu()

if __name__ == "__main__":
    app = AbsensiApp()
    app.mainloop()
