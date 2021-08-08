import pyodbc

driver = "SQL Server"
server = "MSSQLSERVER01"
database = "test1"
connect_str = r'Driver=SQL Server;Server=.\MSSQLSERVER01;Database=test1;Trusted_Connection=yes;'
username = "DESKTOP-1F41P9S\linpeng109"
password = "stars2021"
rows = []
with pyodbc.connect(connect_str) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT TOP 3 * FROM test1.dbo.Table_2")
        row = cursor.fetchone()
        while row:
            cols = []
            cols_len=len(row)
            for i in range(cols_len):
                cols.append(row[i])
            rows.append(cols)
            row = cursor.fetchone()
print(rows)
