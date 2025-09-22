import sqlite3
import os

def contar_registros_en_tablas():
    """
    Se conecta a la base de datos stocks.db, muestra las tablas y cuenta los registros en cada una.
    """
    db_path = os.path.join(os.getcwd(), 'stocks.db')

    if not os.path.exists(db_path):
        print(f"❌ Error: El archivo de la base de datos '{db_path}' no existe.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener la lista de todas las tablas en la base de datos
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if not tables:
        print("❌ La base de datos no contiene ninguna tabla.")
        conn.close()
        return

    print("✅ Cantidad de registros por tabla en la base de datos:")
    for table_name in tables:
        table_name = table_name[0]
        # Contar los registros en cada tabla
        cursor.execute(f"SELECT COUNT(*) FROM '{table_name}';")
        count = cursor.fetchone()[0]
        print(f"Tabla '{table_name}': {count} registros")

    conn.close()

if __name__ == "__main__":
    contar_registros_en_tablas()