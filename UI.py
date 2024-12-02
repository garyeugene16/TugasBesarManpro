import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime, timedelta
from tkcalendar import DateEntry
from PIL import Image, ImageTk

connectionString = ('DRIVER={ODBC Driver 17 for SQL Server};'
                    'Server=LEGION-YOO\\SQLEXPRESS;'
                    'Database=TestingManpro;'
                    'Trusted_Connection=yes;'
                    'TrustServerCertificate=yes;')

BACKGROUND_COLOR = "#f0f8ff"  # Alice Blue

def setup_database():
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()
    
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Kecamatan' AND xtype='U')
    CREATE TABLE Kecamatan(
        idKecamatan int IDENTITY(1,1) PRIMARY KEY,
        namaKecamatan varchar(100) NOT NULL
    )""")
    
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Kelurahan' AND xtype='U')
    CREATE TABLE Kelurahan(
        idKelurahan int IDENTITY(1,1) PRIMARY KEY,
        namaKelurahan varchar(100) NOT NULL,
        idKecamatan int FOREIGN KEY REFERENCES Kecamatan(idKecamatan)
    )""")
    
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Pemilik' AND xtype='U')
    CREATE TABLE Pemilik(
        username varchar(50) NOT NULL PRIMARY KEY,
        email varchar(50) NOT NULL,
        password varchar(50) NOT NULL
    )""")
    
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Jabatan' AND xtype='U')
    CREATE TABLE Jabatan(
        idJabatan int PRIMARY KEY,
        namaJabatan varchar(100) NOT NULL,
        satuanGaji int NOT NULL
    )""")
    
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Pegawai' AND xtype='U')
    CREATE TABLE Pegawai(
        idPegawai int IDENTITY(1,1) NOT NULL PRIMARY KEY,
        nama varchar(255) NOT NULL,
        NomorTelepon varchar(15) NOT NULL,
        email varchar(255) NOT NULL,
        Alamat varchar(100) NOT NULL,
        idKelurahan int NOT NULL FOREIGN KEY REFERENCES Kelurahan(idKelurahan),
        idJabatan int NOT NULL FOREIGN KEY REFERENCES Jabatan(idJabatan)
    )""")
    
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Absensi' AND xtype='U')
    CREATE TABLE Absensi (
        idAbsensi int IDENTITY(1,1) PRIMARY KEY,
        idPegawai int NOT NULL,
        waktuMasuk TIME,
        waktuKeluar TIME,
        tanggalAbsensi DATE DEFAULT CAST(GETDATE() AS DATE),
        Durasi TIME,
        WeeklyHours INT DEFAULT 0,
        FOREIGN KEY (idPegawai) REFERENCES Pegawai(idPegawai)
    )""")
    
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM Pemilik WHERE username='Owner')
    INSERT INTO Pemilik (username, email, password) VALUES
    ('Owner', 'Owner@mail.com', '12345')
    """)
    
    jabatan_data = [
        (1, 'Manajer', 200000),
        (2, 'Koki', 150000),
        (3, 'Bartender', 120000),
        (4, 'Pelayan', 100000),
        (5, 'Kasir', 100000)
    ]
    cursor.executemany("""
    IF NOT EXISTS (SELECT * FROM Jabatan WHERE idJabatan=?)
    INSERT INTO Jabatan (idJabatan, namaJabatan, satuanGaji) VALUES (?, ?, ?)
    """, [(j[0], j[0], j[1], j[2]) for j in jabatan_data])
    
    kecamatan_data = [
        'Andir', 'Astana Anyar', 'Antapani', 'Arcamanik', 'Babakan Ciparay',
        'Bandung Kidul', 'Bandung Kulon', 'Batununggal', 'Bojongloa Kaler', 'Bojongloa Kidul'
    ]
    for kecamatan in kecamatan_data:
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Kecamatan WHERE namaKecamatan=?)
        INSERT INTO Kecamatan (namaKecamatan) VALUES (?)
        """, (kecamatan, kecamatan))
    
    kelurahan_data = [
        ('Ciroyom', 1), ('Kebon Jeruk', 1), ('Maleber', 1), ('Dungus Cariang', 1), ('Campaka', 1),
        ('Karang Anyar', 2), ('Nyengseret', 2), ('Panjunan', 2), ('Cibadak', 2), ('Karasak', 2),
        ('Antapani Kidul', 3), ('Antapani Tengah', 3), ('Antapani Wetan', 3), ('Antapani Kulon', 3),
        ('Cisaranten Kulon', 4), ('Cisaranten Bina Harapan', 4), ('Cisaranten Endah', 4),
        ('Sukamiskin', 4), ('Sindang Jaya', 4), ('Babakan Ciparay', 5), ('Sukahaji', 5),
        ('Margahayu Utara', 5), ('Babakan', 5), ('Warung Muncang', 5), ('Mengger', 6),
        ('Wates', 6), ('Batununggal', 6), ('Kujangsari', 6), ('Kebon Gedang', 6),
        ('Cijerah', 7), ('Gempol Sari', 7), ('Caringin', 7), ('Warung Muncang', 7),
        ('Cigondewah Rahayu', 7), ('Kebon Gedang', 8), ('Kacapiring', 8), ('Binong', 8),
        ('Gumuruh', 8), ('Cibangkong', 8), ('Jamika', 9), ('Sukahaji', 9), ('Cibuntu', 9),
        ('Cibaduyut', 9), ('Kebon Lega', 9), ('Kebon Lega', 10), ('Mekarwangi', 10),
        ('Situsaeur', 10), ('Cibaduyut Kidul', 10), ('Cibaduyut', 10)
    ]
    cursor.executemany("""
    IF NOT EXISTS (SELECT * FROM Kelurahan WHERE namaKelurahan=? AND idKecamatan=?)
    INSERT INTO Kelurahan (namaKelurahan, idKecamatan) VALUES (?, ?)
    """, kelurahan_data)
    
    conn.commit()
    conn.close()

def fetch_pegawai():
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()

    cursor.execute("SELECT idPegawai, nama FROM Pegawai")
    pegawai_data = cursor.fetchall()
    conn.close()

    return {row[0]: row[1] for row in pegawai_data}  # Mengembalikan dictionary idPegawai -> nama

def fetch_kecamatan_kelurahan():
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()
    
    cursor.execute("SELECT idKecamatan, namaKecamatan FROM kecamatan")
    kecamatan_data = cursor.fetchall()
    
    cursor.execute("SELECT idKelurahan, namaKelurahan, idKecamatan FROM kelurahan")
    kelurahan_data = cursor.fetchall()
    
    conn.close()
    
    kecamatan_dict = {row[0]: row[1] for row in kecamatan_data}
    kelurahan_dict = {row[0]: (row[1], row[2]) for row in kelurahan_data}
    
    return kecamatan_dict, kelurahan_dict

def fetch_jabatan():
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()
    
    cursor.execute("SELECT idJabatan, namaJabatan FROM jabatan")
    jabatan_data = cursor.fetchall()
    
    conn.close()
    
    jabatan_dict = {row[0]: row[1] for row in jabatan_data}
    
    return jabatan_dict

def fetch_weekly_hours_and_gaji(id_pegawai):
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()

    # Tentukan rentang Senin hingga hari terakhir data yang tersedia dalam minggu tersebut
    today = datetime.now()
    start_of_week = (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')  # Senin
    current_date = today.strftime('%Y-%m-%d')  # Hari akses

    query = """
    SELECT 
        CONVERT(VARCHAR, a.tanggalAbsensi, 23) AS Tanggal,
        SUM(DATEDIFF(HOUR, a.waktuMasuk, a.waktuKeluar)) AS JamKerja
    FROM 
        Absensi a
    WHERE
        a.idPegawai = ? AND
        a.tanggalAbsensi BETWEEN ? AND ?
    GROUP BY
        a.tanggalAbsensi
    ORDER BY
        a.tanggalAbsensi
    """
    cursor.execute(query, (id_pegawai, start_of_week, current_date))
    results = cursor.fetchall()
    conn.close()

    # Format hasil sebagai rincian per hari
    rincian = []
    total_jam = 0
    # Modifikasi saat memproses rincian absensi
    for row in results:
        tanggal, jam_kerja = row
        hari = datetime.strptime(tanggal, "%Y-%m-%d").strftime("%A")
        rincian.append((f"{tanggal} ({hari})", jam_kerja))
        total_jam += jam_kerja

    return rincian, total_jam


def format_tanggal_with_hari(tanggal):
    """
    Format tanggal dalam bentuk "Hari, DD Month YYYY"
    """
    hari = tanggal.strftime("%A")  # Nama hari
    hari_indonesia = {
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jumat",
        "Saturday": "Sabtu",
        "Sunday": "Minggu"
    }
    hari = hari_indonesia.get(hari, hari)  # Ubah ke bahasa Indonesia
    formatted_date = tanggal.strftime(f"{hari}, %d %B %Y")  # Contoh: Selasa, 25 November 2024
    return formatted_date

def check_payment_status(start_date, end_date):
    """
    Cek status pembayaran berdasarkan apakah tanggal sudah melewati Minggu terakhir.
    """
    today = datetime.now().date()  # Gunakan tanggal hari ini
    end_of_week = end_date + timedelta(days=(6 - end_date.weekday()))  # Hitung hari Minggu minggu tersebut

    if today > end_of_week:
        return "Sudah Dilunasi"
    else:
        return "Belum Dilunasi"

def group_by_week(start_date, end_date):
    """
    Mengelompokkan tanggal ke dalam minggu-minggu yang sesuai.
    """
    weeks = []
    current_start = start_date
    while current_start <= end_date:
        current_end = min(current_start + timedelta(days=6), end_date)
        weeks.append((current_start, current_end))
        current_start = current_end + timedelta(days=1)
    return weeks

def round_to_monday(date):
    """
    Membulatkan tanggal ke hari Senin terdekat.
    """
    return date - timedelta(days=date.weekday())

class AbsensiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("☕Sistem Manajemen Kehadiran Pegawai Kafe IF☕")
        self.geometry("1024x768")
        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.geometry("1024x768")

        # Muat gambar sebagai latar belakang
        bg_image = Image.open("ass.png")  # Ganti dengan path ke gambar Anda
        bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)  # Sesuaikan ukuran gambar dengan jendela

        # Tambahkan opacity pada gambar (0-255)
        opacity = 200  # Semakin rendah nilai, semakin transparan
        bg_image = bg_image.convert("RGBA")  # Ubah gambar ke format RGBA
        alpha = bg_image.split()[3]  # Ambil channel alpha
        alpha = alpha.point(lambda p: opacity)  # Sesuaikan nilai alpha
        bg_image.putalpha(alpha)

        # Konversi ke ImageTk untuk Tkinter
        bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self, image=bg_photo, borderwidth=0)
        bg_label.image = bg_photo  # Mencegah garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame untuk elemen
        # main_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        # main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Pusatkan di layar


        # # Gunakan label langsung tanpa frame tambahan
        tk.Label(self, text="☕ Sistem Manajemen Kehadiran Pegawai Kafe Bahagia ☕", font=("Helvetica", 18, "bold"), bg="#AB886D", fg="#493628").pack(pady=(20, 250))
        # tk.Label(self, text="Kehadiran Pegawai Kafe IF", font=("Helvetica", 14)).pack(pady=(0, 250))

        style = ttk.Style()
        style.configure(
            "Custom.TButton",  # Nama gaya
            font=("Helvetica", 12),  # Font
            padding=10, 
            background="#AB886D",  # Warna latar belakang
            foreground="#493628"   # Warna teks
        )
        style.map(
            "Custom.TButton",
            background=[("active", "#ff8533")]  # Warna saat tombol aktif
        )

        ttk.Button(self, text="Pemilik", style="Custom.TButton", command=self.show_pemilik_login).pack(pady=10)
        ttk.Button(self, text="Pegawai", style="Custom.TButton", command=self.show_pegawai_login).pack(pady=10)


        # tk.Label(self, text="Jayden Raphael - 6182201034", font=("Helvetica", 10)).pack(pady=2)
        # tk.Label(self, text="Rio Sugiarno - 6182201043", font=("Helvetica", 10)).pack(pady=2)
        # tk.Label(self, text="Gary Eugene - 6182201046", font=("Helvetica", 10)).pack(pady=2)
        # tk.Label(self, text="Hepi Rahmat Stevanus Daeli - 6182201052", font=("Helvetica", 10)).pack(pady=2)

    def show_pemilik_login(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("1024x768")

        # Muat gambar sebagai latar belakang
        bg_image = Image.open("ass.png")  # Ganti dengan path ke gambar Anda
        bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)  # Sesuaikan ukuran gambar dengan jendela

        # Tambahkan opacity pada gambar (0-255)
        opacity = 200  # Semakin rendah nilai, semakin transparan
        bg_image = bg_image.convert("RGBA")  # Ubah gambar ke format RGBA
        alpha = bg_image.split()[3]  # Ambil channel alpha
        alpha = alpha.point(lambda p: opacity)  # Sesuaikan nilai alpha
        bg_image.putalpha(alpha)

        # Konversi ke ImageTk untuk Tkinter
        bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self, image=bg_photo, borderwidth=0)
        bg_label.image = bg_photo  # Mencegah garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(
            self, 
            text="Login to Continue", 
            font=("Helvetica", 24, "bold"), 
            bg="#AB886D", 
            fg="#493628"
        ).pack(pady=(20, 50))

        # Field Username
        tk.Label(self, text="Username:", font=("Helvetica", 16, "bold"), bg="#AB886D", fg="black").pack(pady=(10, 5))
        username_entry = tk.Entry(self, font=("Helvetica", 14), width=30)
        username_entry.pack(pady=(5, 15))

        # Field Email
        tk.Label(self, text="Email:", font=("Helvetica", 16, "bold"), bg="#AB886D", fg="black").pack(pady=(10, 5))
        email_entry = tk.Entry(self, font=("Helvetica", 14), width=30)
        email_entry.pack(pady=(5, 15))

        # Field Password
        tk.Label(self, text="Password:", font=("Helvetica", 16, "bold"), bg="#AB886D", fg="black").pack(pady=(10, 5))
        password_entry = tk.Entry(self, font=("Helvetica", 14), width=30, show='*')
        password_entry.pack(pady=(5, 15))

        def submit_login():
            username = username_entry.get()
            email = email_entry.get()
            password = password_entry.get()

            try:
                conn = pyodbc.connect(connectionString)
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM Pemilik WHERE username=? AND email=? AND password=?", (username, email, password))
                row = cursor.fetchone()
                if row:
                    self.show_pemilik_menu()
                else:
                    if not cursor.execute("SELECT * FROM Pemilik WHERE username=?", (username,)).fetchone():
                        messagebox.showerror("Error", "Incorrect username.")
                    elif not cursor.execute("SELECT * FROM Pemilik WHERE username=? AND email=?", (username, email)).fetchone():
                        messagebox.showerror("Error", "Incorrect email.")
                    else:
                        messagebox.showerror("Error", "Incorrect password.")
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Gaya tombol
        style = ttk.Style()
        style.configure(
            "Custom.TButton",
            font=("Helvetica", 14),
            padding=10,
            background="#AB886D",
            foreground="#493628"
        )
        style.map(
            "Custom.TButton",
            background=[("active", "#ff8533")]
        )

        # Tombol Login
        ttk.Button(self, text="Login", style="Custom.TButton", command=submit_login).pack(pady=20, ipadx=10, ipady=5)
        
        # Tombol Back
        ttk.Button(self, text="Back", style="Custom.TButton", command=self.create_main_menu).pack(pady=20, ipadx=10, ipady=5)

    def show_pemilik_menu(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("1024x768")
        
        # Muat gambar sebagai latar belakang
        bg_image = Image.open("ass.png")  # Ganti dengan path ke gambar Anda
        bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)  # Sesuaikan ukuran gambar dengan jendela


        # Tambahkan opacity pada gambar (0-255)
        opacity = 200  # Semakin rendah nilai, semakin transparan
        bg_image = bg_image.convert("RGBA")  # Ubah gambar ke format RGBA
        alpha = bg_image.split()[3]  # Ambil channel alpha
        alpha = alpha.point(lambda p: opacity)  # Sesuaikan nilai alpha
        bg_image.putalpha(alpha)

        # Konversi ke ImageTk untuk Tkinter
        bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self, image=bg_photo, borderwidth=0)
        bg_label.image = bg_photo  # Mencegah garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(
            self, 
            text="Select to Continue", 
            font=("Helvetica", 24, "bold"), 
            bg="#AB886D", 
            fg="#493628"
        ).pack(pady=(20, 50))
        

        # Gaya tombol
        style = ttk.Style()
        style.configure(
            "Custom.TButton",
            font=("Helvetica", 14),
            padding=10,
            background="#AB886D",
            foreground="#493628"
        )
        style.map(
            "Custom.TButton",
            background=[("active", "#ff8533")]
        )

        ttk.Button(self, text="Registrasi Pegawai Baru", style="Custom.TButton", command=self.pegawai_baru).pack(pady=10)
        ttk.Button(self, text="Laporan Absensi",style="Custom.TButton", command=self.laporan_kehadiran).pack(pady=10)
        ttk.Button(self, text="Laporan Gaji",style="Custom.TButton", command=self.laporan_gaji).pack(pady=10)
        ttk.Button(self, text="Back",style="Custom.TButton", command=self.create_main_menu).pack(pady=10)

    def show_pegawai_login(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("1024x768")

        # Muat gambar sebagai latar belakang
        bg_image = Image.open("ass.png")  # Ganti dengan path ke gambar Anda
        bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)  # Sesuaikan ukuran gambar dengan jendela


        # Tambahkan opacity pada gambar (0-255)
        opacity = 200  # Semakin rendah nilai, semakin transparan
        bg_image = bg_image.convert("RGBA")  # Ubah gambar ke format RGBA
        alpha = bg_image.split()[3]  # Ambil channel alpha
        alpha = alpha.point(lambda p: opacity)  # Sesuaikan nilai alpha
        bg_image.putalpha(alpha)

        # Konversi ke ImageTk untuk Tkinter
        bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self, image=bg_photo, borderwidth=0)
        bg_label.image = bg_photo  # Mencegah garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(
            self, 
            text="Login Pegawai", 
            font=("Helvetica", 24, "bold"), 
            bg="#AB886D", 
            fg="#493628"
        ).pack(pady=(20, 50))

        tk.Label(self, text="Nomor Telepon:", bg="#AB886D", fg="black", font=("Helvetica", 15)).pack(pady=(10, 5))
        nomor_telepon_entry = tk.Entry(self, font=("Helvetica", 14), width=30)
        nomor_telepon_entry.pack(pady=(5, 15))

        def submit_login():
            nomor_telepon = nomor_telepon_entry.get()

            try:
                conn = pyodbc.connect(connectionString)
                cursor = conn.cursor()
                
                cursor.execute("SELECT idPegawai FROM Pegawai WHERE NomorTelepon=?", (nomor_telepon,))
                row = cursor.fetchone()
                if row:
                    self.id_pegawai = row[0]
                    self.show_pegawai_menu()
                else:
                    messagebox.showerror("Error", "Nomor telepon tidak ditemukan.")
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            
            style = ttk.Style()
            style.configure(
                "Custom.TButton",
                font=("Helvetica", 15),
                padding=3,
                background="#AB886D",
                foreground="black"
            )
            style.map(
                "Custom.TButton",
                background=[("active", "#ff8533")]
            )

        ttk.Button(self, text="Login", style="Custom.TButton", command=submit_login).pack(pady=10)
        ttk.Button(self, text="Back", style="Custom.TButton", command=self.create_main_menu).pack(pady=10)

    def show_pegawai_menu(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("1024x768")
        
        # Muat gambar sebagai latar belakang
        bg_image = Image.open("ass.png")  # Ganti dengan path ke gambar Anda
        bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)  # Sesuaikan ukuran gambar dengan jendela

        # Tambahkan opacity pada gambar (0-255)
        opacity = 200  # Semakin rendah nilai, semakin transparan
        bg_image = bg_image.convert("RGBA")  # Ubah gambar ke format RGBA
        alpha = bg_image.split()[3]  # Ambil channel alpha
        alpha = alpha.point(lambda p: opacity)  # Sesuaikan nilai alpha
        bg_image.putalpha(alpha)

        # Konversi ke ImageTk untuk Tkinter
        bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self, image=bg_photo, borderwidth=0)
        bg_label.image = bg_photo  # Mencegah garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Judul layar
        tk.Label(self, text="Select to Continue", font=("Helvetica", 18, "bold"), bg="#AB886D", fg="#493628").pack(pady=(20, 250))

        # Setup Style untuk tombol
        style = ttk.Style()
        style.configure(
            "Custom.TButton",
            font=("Helvetica", 10),
            padding=3,
            background="#AB886D",
            foreground="black"
        )
        style.map(
            "Custom.TButton",
            background=[("active", "#ff8533")]
        )

        # Tombol-tombol navigasi
        ttk.Button(self, text="Absensi", style="Custom.TButton", command=self.absensi).pack(pady=10)
        ttk.Button(self, text="Gaji", style="Custom.TButton", command=self.gaji).pack(pady=10)
        ttk.Button(self, text="Back", style="Custom.TButton", command=self.create_main_menu).pack(pady=10)


    def pegawai_baru(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("500x600")
        self.configure(bg=BACKGROUND_COLOR)

        tk.Label(self, text="Registrasi Pegawai Baru", font=("Arial", 16, "bold"), bg=BACKGROUND_COLOR, fg='#333').pack(pady=(20, 0))
        tk.Label(self, text="Nama:", bg=BACKGROUND_COLOR).pack(pady=(10, 5))
        nama_entry = tk.Entry(self)
        nama_entry.pack()

        tk.Label(self, text="Nomor Telepon:", bg=BACKGROUND_COLOR).pack(pady=(10, 5))
        nomor_telepon_entry = tk.Entry(self)
        nomor_telepon_entry.pack()

        tk.Label(self, text="Email:", bg=BACKGROUND_COLOR).pack(pady=(10, 5))
        email_entry = tk.Entry(self)
        email_entry.pack()

        tk.Label(self, text="Alamat:", bg=BACKGROUND_COLOR).pack(pady=(10, 5))
        alamat_entry = tk.Entry(self)
        alamat_entry.pack()

        tk.Label(self, text="Kecamatan:", bg=BACKGROUND_COLOR).pack(pady=(10, 5))
        kecamatan_var = tk.StringVar()
        kecamatan_dropdown = ttk.Combobox(self, textvariable=kecamatan_var, values=list(kecamatan_dict.values()))
        kecamatan_dropdown.pack()

        tk.Label(self, text="Kelurahan:", bg=BACKGROUND_COLOR).pack(pady=(10, 5))
        kelurahan_var = tk.StringVar()
        kelurahan_dropdown = ttk.Combobox(self, textvariable=kelurahan_var)
        kelurahan_dropdown.pack()

        def update_kelurahan(*args):
            selected_kecamatan = kecamatan_var.get()
            selected_kecamatan_id = [k for k, v in kecamatan_dict.items() if v == selected_kecamatan][0]
            kelurahan_list = [v[0] for k, v in kelurahan_dict.items() if v[1] == selected_kecamatan_id]
            kelurahan_dropdown['values'] = kelurahan_list
        
        kecamatan_var.trace_add('write', update_kelurahan)

        tk.Label(self, text="Nama Jabatan:", bg=BACKGROUND_COLOR).pack(pady=(10, 5))
        jabatan_var = tk.StringVar()
        jabatan_dropdown = ttk.Combobox(self, textvariable=jabatan_var, values=list(jabatan_dict.values()))
        jabatan_dropdown.pack()

        def submit_pegawai():
            nama = nama_entry.get()
            nomor_telepon = nomor_telepon_entry.get()
            email = email_entry.get()
            alamat = alamat_entry.get()
            kecamatan = kecamatan_var.get()
            kelurahan = kelurahan_var.get()
            nama_jabatan = jabatan_var.get()
            
            try:
                conn = pyodbc.connect(connectionString)
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM Pegawai WHERE NomorTelepon = ?", (nomor_telepon,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror("Error", "Nomor Telepon sudah terdaftar.")
                    return

                selected_kelurahan_id = [k for k, v in kelurahan_dict.items() if v[0] == kelurahan][0]
                id_jabatan = [k for k, v in jabatan_dict.items() if v == nama_jabatan][0]
                
                SQL_QUERY_Pegawai = """
                    INSERT INTO pegawai (
                        nama,
                        NomorTelepon,
                        email,
                        Alamat,
                        idKelurahan,
                        idJabatan
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                cursor.execute(SQL_QUERY_Pegawai, (nama, nomor_telepon, email, alamat, selected_kelurahan_id, id_jabatan))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Pegawai baru berhasil ditambahkan.")
                self.show_pemilik_menu()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(self, text="Submit", command=submit_pegawai).pack(pady=10)
        ttk.Button(self, text="Back", command=self.show_pemilik_menu).pack(pady=10)

    def absensi(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("400x275")
        self.configure(bg=BACKGROUND_COLOR)

        tk.Label(self, text="Absensi", font=("Arial", 16, "bold"), bg=BACKGROUND_COLOR, fg='#333').pack(pady=(20, 0)) 

        tk.Label(self, text="Apakah ini waktu masuk atau keluar? (masuk/keluar):", bg=BACKGROUND_COLOR).pack(pady=(10, 5))
        action_var = tk.StringVar()
        action_dropdown = ttk.Combobox(self, textvariable=action_var, values=["masuk", "keluar"])
        action_dropdown.pack()

        tk.Label(self, text="Masukkan nomor telepon untuk check-in/check-out:", bg=BACKGROUND_COLOR).pack(pady=(10, 5))
        nomor_telepon_entry = tk.Entry(self)
        nomor_telepon_entry.pack()

        def submit_absensi():
                action = action_var.get().strip().lower()
                nomor_telepon = nomor_telepon_entry.get()

                try:
                    conn = pyodbc.connect(connectionString)
                    cursor = conn.cursor()

                    cursor.execute("SELECT idPegawai FROM pegawai WHERE NomorTelepon = ?", (nomor_telepon,))
                    row = cursor.fetchone()
                    if row:
                        id_pegawai = row[0]
                    else:
                        raise ValueError("Pegawai dengan nomor telepon tersebut tidak ditemukan.")

                    current_time = datetime.now().strftime('%H:%M:%S')
                    current_date = datetime.now().strftime('%Y-%m-%d')

                    if action == "masuk":
                        SQL_QUERY_Absensi = """
                            INSERT INTO Absensi (
                                idPegawai,
                                waktuMasuk,
                                tanggalAbsensi
                            )
                            VALUES (?, ?, ?)
                        """
                        cursor.execute(SQL_QUERY_Absensi, (id_pegawai, current_time, current_date))
                    elif action == "keluar":
                        cursor.execute("""
                            SELECT waktuMasuk
                            FROM Absensi
                            WHERE idPegawai = ? AND tanggalAbsensi = ? AND waktuKeluar IS NULL
                        """, (id_pegawai, current_date))
                        row = cursor.fetchone()

                        if row:
                            waktu_masuk = row[0]
                            waktu_keluar = datetime.strptime(current_time, '%H:%M:%S')
                            waktu_masuk = waktu_masuk.strftime('%H:%M:%S') 
                            waktu_masuk = datetime.strptime(waktu_masuk, '%H:%M:%S')

                            durasi = waktu_keluar - waktu_masuk
                            durasi_str = str(durasi)
                            weekly_hours = durasi.total_seconds() // 3600

                            SQL_QUERY_Absensi = """
                                UPDATE Absensi
                                SET waktuKeluar = ?, Durasi = ?
                                WHERE idPegawai = ? AND tanggalAbsensi = ? AND waktuKeluar IS NULL
                            """
                            cursor.execute(SQL_QUERY_Absensi, (current_time, durasi_str, id_pegawai, current_date))
                        else:
                            raise ValueError("Tidak ditemukan waktu masuk untuk pegawai ini hari ini.")
                    else:
                        raise ValueError("Tindakan tidak valid. Masukkan 'masuk' atau 'keluar'.")

                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Absensi berhasil diperbarui.")
                    self.show_pegawai_menu()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        ttk.Button(self, text="Submit", command=submit_absensi).pack(pady=10)
        ttk.Button(self, text="Back", command=self.show_pegawai_menu).pack(pady=10)

    
    
    def gaji(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("400x300")
        
        tk.Label(self, text="Gaji Mingguan", font=("Arial", 14)).pack(pady=(20, 0))

        try:
            rincian, total_jam = fetch_weekly_hours_and_gaji(self.id_pegawai)

            # Tampilkan rincian jam kerja per hari
            tk.Label(self, text="Rincian Jam Kerja:").pack(pady=(10, 5))
            for tanggal, jam_kerja in rincian:
                tk.Label(self, text=f"{tanggal}: {jam_kerja} jam").pack()

            # Hitung total gaji
            jabatan_dict = fetch_jabatan()
            conn = pyodbc.connect(connectionString)
            cursor = conn.cursor()
            cursor.execute("SELECT j.satuanGaji FROM pegawai p JOIN jabatan j ON p.idJabatan = j.idJabatan WHERE p.idPegawai = ?", (self.id_pegawai,))
            satuan_gaji = cursor.fetchone()[0]
            conn.close()
            
            total_gaji = total_jam * satuan_gaji
            tk.Label(self, text=f"Total Jam Kerja: {total_jam} jam").pack(pady=(10, 5))
            tk.Label(self, text=f"Total Gaji: Rp {total_gaji}").pack(pady=(10, 5))
        except Exception as e:
            messagebox.showerror("Error", str(e))

        tk.Button(self, text="Back", command=self.show_pegawai_menu).pack(pady=10)

    def laporan_gaji(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("400x400")
        self.configure(bg=BACKGROUND_COLOR)

        tk.Label(self, text="Laporan Gaji", font=("Arial", 16, "bold"), bg=BACKGROUND_COLOR, fg='#333').pack(pady=(20, 0))    

        # Dropdown untuk memilih Pegawai
        tk.Label(self, text="Pilih Pegawai:", bg=BACKGROUND_COLOR).pack(pady=(10, 5))
        pegawai_dict = fetch_pegawai()
        pegawai_var = tk.StringVar()
        pegawai_dropdown = ttk.Combobox(self, textvariable=pegawai_var, values=list(pegawai_dict.values()))
        pegawai_dropdown.pack()

        tk.Label(self, text="Pilih tanggal mulai:", bg=BACKGROUND_COLOR).pack(pady=(10, 5))
        start_date_entry = DateEntry(self, width=15, background='darkblue', foreground='white', date_pattern='yyyy-MM-dd')
        start_date_entry.pack()

        tk.Label(self, text="Pilih tanggal akhir:", bg=BACKGROUND_COLOR).pack(pady=(10, 5))
        end_date_entry = DateEntry(self, width=15, background='darkblue', foreground='white', date_pattern='yyyy-MM-dd')
        end_date_entry.pack()

        def submit_laporan_gaji():
            selected_pegawai = pegawai_var.get()
            start_date = start_date_entry.get_date()
            end_date = end_date_entry.get_date()

            # Cari idPegawai berdasarkan nama
            id_pegawai = None
            for key, value in pegawai_dict.items():
                if value == selected_pegawai:
                    id_pegawai = key
                    break

            if id_pegawai is None:
                messagebox.showerror("Error", "Pilih Pegawai yang valid!")
                return

            try:
                conn = pyodbc.connect(connectionString)
                cursor = conn.cursor()
                
                query = """
                SELECT 
                    p.nama AS Nama_Pegawai,
                    j.namaJabatan AS Nama_Jabatan,
                    j.satuanGaji AS SatuanGaji,
                    SUM(DATEDIFF(HOUR, a.waktuMasuk, a.waktuKeluar)) AS TotalJamKerja,
                    SUM(DATEDIFF(HOUR, a.waktuMasuk, a.waktuKeluar) * j.satuanGaji) AS Laporan_Gaji
                FROM 
                    pegawai p
                JOIN 
                    Absensi a ON p.idPegawai = a.idPegawai
                JOIN 
                    jabatan j ON p.idJabatan = j.idJabatan
                WHERE
                    a.tanggalAbsensi BETWEEN ? AND ? AND a.idPegawai = ?
                GROUP BY 
                    p.nama, j.namaJabatan, j.satuanGaji
                """
                cursor.execute(query, (start_date, end_date, id_pegawai))
                columns = [column[0] for column in cursor.description]
                results = cursor.fetchall()
                
                result_window = tk.Toplevel(self)
                result_window.title("Laporan Gaji")
                
                tree = ttk.Treeview(result_window, columns=columns, show='headings')
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, minwidth=0, width=120)
                tree.pack(fill=tk.BOTH, expand=True)
                
                for row in results:
                    tree.insert('', tk.END, values=row)
                
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(self, text="Submit", command=submit_laporan_gaji).pack(pady=10)
        ttk.Button(self, text="Back", command=self.show_pemilik_menu).pack(pady=10)

        
    def laporan_kehadiran(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("400x400")
        self.configure(bg=BACKGROUND_COLOR)

        tk.Label(self, text="Laporan Absensi", font=("Arial", 16, "bold"), bg=BACKGROUND_COLOR, fg='#333').pack(pady=(20, 0))   

        # Dropdown untuk memilih Pegawai
        tk.Label(self, text="Pilih Pegawai:", bg=BACKGROUND_COLOR).pack(pady=(10, 5))
        pegawai_dict = fetch_pegawai()
        pegawai_var = tk.StringVar()
        pegawai_dropdown = ttk.Combobox(self, textvariable=pegawai_var, values=list(pegawai_dict.values()))
        pegawai_dropdown.pack()

        tk.Label(self, text="Pilih tanggal mulai:", bg=BACKGROUND_COLOR).pack(pady=(10, 5))
        start_date_entry = DateEntry(self, width=15, background='darkblue', foreground='white', date_pattern='yyyy-MM-dd')
        start_date_entry.pack()

        tk.Label(self, text="Pilih tanggal akhir:", bg=BACKGROUND_COLOR).pack(pady=(10, 5))
        end_date_entry = DateEntry(self, width=15, background='darkblue', foreground='white', date_pattern='yyyy-MM-dd')
        end_date_entry.pack()

        def submit_laporan_kehadiran():
            selected_pegawai = pegawai_var.get()
            start_date = start_date_entry.get_date()
            end_date = end_date_entry.get_date()

            # Cari idPegawai berdasarkan nama
            id_pegawai = None
            for key, value in pegawai_dict.items():
                if value == selected_pegawai:
                    id_pegawai = key
                    break

            if id_pegawai is None:
                messagebox.showerror("Error", "Pilih Pegawai yang valid!")
                return

            try:
                conn = pyodbc.connect(connectionString)
                cursor = conn.cursor()
                
                query = """
                SELECT 
                    p.nama AS Nama_Pegawai,
                    CONVERT(VARCHAR, a.tanggalAbsensi, 23) AS Tanggal,
                    CONVERT(VARCHAR, a.waktuMasuk, 8) AS Waktu_Masuk,
                    CONVERT(VARCHAR, a.waktuKeluar, 8) AS Waktu_Keluar,
                    DATEDIFF(HOUR, a.waktuMasuk, a.waktuKeluar) AS TotalJamKerja
                FROM 
                    pegawai p
                JOIN 
                    Absensi a ON p.idPegawai = a.idPegawai
                WHERE
                    a.tanggalAbsensi BETWEEN ? AND ? AND a.idPegawai = ?
                ORDER BY
                    a.tanggalAbsensi
                """
                cursor.execute(query, (start_date, end_date, id_pegawai))
                columns = [column[0] for column in cursor.description]
                results = cursor.fetchall()
                
                result_window = tk.Toplevel(self)
                result_window.title("Laporan Kehadiran")
                
                tree = ttk.Treeview(result_window, columns=columns, show='headings')
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, minwidth=0, width=120)
                tree.pack(fill=tk.BOTH, expand=True)
                
                for row in results:
                    tree.insert('', tk.END, values=row)
                
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(self, text="Submit", command=submit_laporan_kehadiran).pack(pady=10)
        ttk.Button(self, text="Back", command=self.show_pemilik_menu).pack(pady=10)

if __name__ == "__main__":
    kecamatan_dict, kelurahan_dict = fetch_kecamatan_kelurahan()
    jabatan_dict = fetch_jabatan()
    app = AbsensiApp()
    app.mainloop()