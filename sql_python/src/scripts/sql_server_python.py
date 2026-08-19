import pandas as pd
import pyodbc
from sqlalchemy import create_engine  # noqa: F401
from tabulate import tabulate

# Conexión con sqlalchemy - create_engine
server = "Hijo_del_Trueno"
db_name = "Users"
username = "sa"
password = "abcd123"

query = "SELECT * FROM users;"

# engine = create_engine(f"mssql+pyodbc://{username}:{password}@{server}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server")
# conn = engine.connect()


# results = pd.read_sql(query, conn)
# results.head()
# print(results)

# Conexión con pyodbc


conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={db_name};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=yes;"  # noqa: E501
try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    rows = [tuple(row) for row in cursor.fetchall()]

    dataframe_sql = pd.DataFrame(rows, columns=columns)
    table = tabulate(rows, headers=columns, tablefmt="grid")
    print(dataframe_sql)
    conn.close()

except pyodbc.Error as e:
    print(f"Hubo un error al realizar la conexión: {e}")
