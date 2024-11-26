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

# Data yang akan dimasukkan
data = [
    (1, 'Manajer', 200000),
    (2, 'Koki', 150000),
    (3, 'Bartender', 120000),
    (4, 'Pelayan', 100000),
    (5, 'Kasir', 100000)
]
cursor = conn.cursor()
for jabatan in data:
    cursor.execute("INSERT INTO Jabatan (idJabatan, namaJabatan, satuanGaji) VALUES (?, ?, ?)", jabatan[0], jabatan[1], jabatan[2])
conn.commit()

conn.close()