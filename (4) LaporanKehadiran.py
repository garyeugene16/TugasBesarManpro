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

# Ask user for the date range
start_date = input("Masukkan tanggal mulai (YYYY-MM-DD): ")
end_date = input("Masukkan tanggal akhir (YYYY-MM-DD): ")

# SQL query to generate the Laporan Absensi report
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
    a.tanggalAbsensi BETWEEN ? AND ?
ORDER BY
    p.nama, a.tanggalAbsensi
"""

cursor.execute(query, (start_date, end_date))
columns = [column[0] for column in cursor.description]
results = cursor.fetchall()

# Display the results in a tabular format
column_widths = [20, 12, 12, 12, 15]
header_format = "{:<20} {:<12} {:<12} {:<12} {:<15}"
row_format = "{:<20} {:<12} {:<12} {:<12} {:<20}"

# Print header
print(header_format.format(*columns))
print("-" * sum(column_widths))

# Print rows
for row in results:
    print(row_format.format(*row))
conn.close()