"""
Connects to a SQL database using pyodbc
"""
import pyodbc
server = 'localhost,1433'
database = 'ManajemenProyek'
username = 'sa'
password = 'Doraemon16!'

# Connection string
connectionstring = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;'
conn = pyodbc.connect(connectionstring)

print("--Pengisian data pegawai--")

# #Menerima input data - data diri pegawai
nama = str(input("Masukkan nama: "))
NomorTelepon = str(input("Masukkan nomor telepon: "))
email = str(input("Masukkan email: "))
Alamat = str(input("Masukkan alamat lengkap: "))
namaKelurahan = str(input("Masukkan nama kelurahan: "))
namaKecamatan = str(input("Masukkan nama kecamatan: "))
namaJabatan = str(input("Masukkan nama jabatan: "))

# Check or insert kecamatan
cursor = conn.cursor()
cursor.execute("SELECT idKecamatan FROM kecamatan WHERE namaKecamatan = ?", (namaKecamatan))
row = cursor.fetchone()
if row:
    idKecamatan = row[0]
else:
    cursor.execute("INSERT INTO kecamatan (namaKecamatan) OUTPUT INSERTED.idKecamatan VALUES (?)", (namaKecamatan))
    idKecamatan = cursor.fetchone()[0]
    conn.commit()

# Check or insert kelurahan
cursor.execute("SELECT idKelurahan FROM kelurahan WHERE namaKelurahan = ? AND idKecamatan = ?", (namaKelurahan, idKecamatan))
row = cursor.fetchone()
if row:
    idKelurahan = row[0]
else:
    cursor.execute("INSERT INTO kelurahan (namaKelurahan, idKecamatan) OUTPUT INSERTED.idKelurahan VALUES (?, ?)", (namaKelurahan, idKecamatan))
    idKelurahan = cursor.fetchone()[0]
    conn.commit()

# Get idJabatan from namaJabatan
cursor.execute("SELECT idJabatan FROM jabatan WHERE namaJabatan = ?", (namaJabatan,))
row = cursor.fetchone()
if row:
    idJabatan = row[0]
else:
    raise ValueError("Jabatan yang dipilih tidak valid.")

# Insert into pegawai table
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
cursor.execute(SQL_QUERY_Pegawai, (nama, NomorTelepon, email, Alamat, idKelurahan, idJabatan))
conn.commit()

conn.close()