"""
Connects to a SQL database using pyodbc
"""
import pyodbc
from datetime import datetime
SERVER = 'HP-ENVY\\SQLEXPRESS'
DATABASE = 'Demo28May'

# Connection string
connectionstring = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;TrustServerCertificate=yes;'
conn = pyodbc.connect(connectionstring)
# Data yang akan dimasukkan
# Ask user for the date range
start_date = input("Masukkan tanggal mulai (YYYY-MM-DD): ")
end_date = input("Masukkan tanggal akhir (YYYY-MM-DD): ")

# SQL query to calculate TotalJamKerja and Laporan Gaji within the specified date range
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
    a.tanggalAbsensi BETWEEN ? AND ?
GROUP BY 
    p.nama, j.namaJabatan, j.satuanGaji
"""

cursor = conn.cursor()
cursor.execute(query, (start_date, end_date))
columns = [column[0] for column in cursor.description]
results = cursor.fetchall()

# Display the results in a tabular format
print("{:<20} {:<20} {:<15} {:<15} {:<15}".format(*columns))
for row in results:
    print("{:<20} {:<20} {:<15} {:<15} {:<15}".format(row[0], row[1], row[2], row[3], row[4]))


conn.close()