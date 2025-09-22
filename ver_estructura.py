import sqlite3
import pandas as pd
import os

def ver_estructura_db():
    """
    Muestra la estructura de la base de datos stocks.db,
    incluyendo los nombres de las tablas y sus campos.
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

    print("✅ Tablas encontradas en la base de datos:")
    for table_name in tables:
        table_name = table_name[0]
        print(f"\n--- Estructura de la tabla: {table_name} ---")

        # Obtener información sobre las columnas de cada tabla
        cursor.execute(f"PRAGMA table_info('{table_name}');")
        columns_info = cursor.fetchall()

        df_columns = pd.DataFrame(columns_info, columns=['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk'])
        print(df_columns[['name', 'type', 'pk']])

    conn.close()

if __name__ == "__main__":
    ver_estructura_db()