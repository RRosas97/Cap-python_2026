import sqlite3 as sql


def create_DB():
    connection = sql.connect("singers.db")
    connection.commit()
    connection.close()


def create_table():
    connection = sql.connect("singers.db")
    cursor = connection.cursor()
    cursor.execute(
        """CREATE TABLE singers(
            name text,
            followers integer,
            discs integer
            )"""
    )
    connection.commit()
    connection.close()


def insert_row(nombre, followers, discs):
    connection = sql.connect("singers.db")
    cursor = connection.cursor()
    instruccion = f"INSERT INTO singers VALUES('{nombre}', {followers}, {discs})"
    cursor.execute(instruccion)
    connection.commit()
    connection.close()


def read_rows():
    connection = sql.connect("singers.db")
    cursor = connection.cursor()
    instruccion = "SELECT * FROM singers"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    connection.commit()
    connection.close()
    print(datos)


def insert_rows(singerList):
    connection = sql.connect("singers.db")
    cursor = connection.cursor()
    instruccion = "INSERT INTO singers VALUES(?, ?, ?)"
    cursor.executemany(instruccion, singerList)
    connection.commit()
    connection.close()


def get_items_ordered(field, order=""):
    connection = sql.connect("singers.db")
    cursor = connection.cursor()
    instruccion = f"SELECT * FROM singers ORDER BY {field} {order}"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    connection.commit()
    connection.close()
    print(datos)


def search():
    connection = sql.connect("singers.db")
    cursor = connection.cursor()
    instruccion = "SELECT * FROM singers WHERE name like 'mi%'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    connection.commit()
    connection.close()
    print(datos)


def edit_row():
    connection = sql.connect("singers.db")
    cursor = connection.cursor()
    instruccion = "UPDATE singers SET name = 'Dua Lipa' WHERE name = 'DuaLipa'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    connection.commit()
    connection.close()
    print(datos)


def delete_row():
    connection = sql.connect("singers.db")
    cursor = connection.cursor()
    instruccion = "DELETE FROM singers WHERE name = 'Sia'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    connection.commit()
    connection.close()
    print(datos)


if __name__ == "__main__":
    # createDB()
    # createTable()
    # insertRow("Bruno Mars", 10000000, 5)
    # insertRow("DuaLipa", 100000000, 3)
    # insertRow("Kaia Lana", 50000, 4)
    # readRows()
    singers = [
        ("Michael Jackson", 100000000, 6),
        ("Sabino", 900000, 4),
        ("Sia", 9999999, 3),
    ]
    # insertRows(singers)
    # get_items_ordered("discs")
    # search()
    # edit_row()
    delete_row()
    pass
