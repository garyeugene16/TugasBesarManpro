"""
Connects to a SQL database using pyodbc
"""
import pyodbc
from datetime import datetime
server = 'localhost,1433'
database = 'ManajemenProyek'
username = 'sa'
password = 'Doraemon16!'

# Connection string
connectionstring = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;'
conn = pyodbc.connect(connectionstring)
cursor = conn.cursor()

print("--Absensi--")
action = str(input("Apakah ini waktu masuk atau keluar? (masuk/keluar): ")).strip().lower()

NomorTelepon = str(input("Masukkan nomor telepon untuk check-in/check-out: "))

# Retrieve Id_Pegawai using NomorTelepon
cursor.execute("SELECT idPegawai FROM pegawai WHERE NomorTelepon = ?", (NomorTelepon))
row = cursor.fetchone()
if row:
    idPegawai = row[0]
else:
    raise ValueError("Pegawai dengan nomor telepon tersebut tidak ditemukan.")

# Get current time and date
current_time = datetime.now().strftime('%H:%M:%S')
current_date = datetime.now().strftime('%Y-%m-%d')

if action == "masuk":
    # Insert check-in time
    SQL_QUERY_Absensi = """
        INSERT INTO Absensi (
            idPegawai,
            waktuMasuk,
            tanggalAbsensi
        )
        VALUES (?, ?, ?)
    """
    cursor.execute(SQL_QUERY_Absensi, (idPegawai, current_time, current_date))
elif action == "keluar":
    # Update check-out time for the latest entry of the day
    SQL_QUERY_Absensi = """
        UPDATE Absensi
        SET waktuKeluar = ?
        WHERE idPegawai = ? AND tanggalAbsensi = ? AND waktuKeluar IS NULL
    """
    cursor.execute(SQL_QUERY_Absensi, (current_time, idPegawai, current_date))
else:
    raise ValueError("Tindakan tidak valid. Masukkan 'masuk' atau 'keluar'.")

conn.commit()

conn.close()