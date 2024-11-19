import tkinter as tk
from tkinter import ttk, messagebox

class AbsensiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Kehadiran Pegawai Kafe IF")
        self.geometry("500x400")
        self.configure(bg='#f0f0f0')
        self.create_main_menu()

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

if __name__ == "__main__":
    app = AbsensiApp()
    app.mainloop()
