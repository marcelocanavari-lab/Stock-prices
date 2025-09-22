import sqlite3
import pandas as pd
import os

def read_db(ticker):
    """
    Lee los datos de un ticker específico de la base de datos stocks.db.
    """
    db_path = os.path.join(os.getcwd(), 'stocks.db')
    
    # Verificar si el archivo de la base de datos existe
    if not os.path.exists(db_path):
        print(f"❌ El archivo '{db_path}' no existe.")
        return None
    
    conn = sqlite3.connect(db_path)
    
    # Verificar si la tabla existe en la base de datos
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (ticker,))
    if cursor.fetchone() is None:
        print(f"❌ La tabla para el ticker '{ticker}' no existe en la base de datos.")
        conn.close()
        return None
    
    # Leer la tabla completa en un DataFrame de pandas
    try:
        df = pd.read_sql_query(f"SELECT * FROM '{ticker}'", conn, index_col='Date')
        print(f"✅ Datos del ticker '{ticker}' leídos correctamente.")
        return df
    except Exception as e:
        print(f"❌ Error al leer la tabla: {e}")
        return None
    finally:
        conn.close()

if __name__ == "__main__":
    ticker_to_read = input("Ingresa el ticker que deseas leer (ej. AAPL, MSFT): ").upper()
    
    data_from_db = read_db(ticker_to_read)
    
    if data_from_db is not None:
        print("\n--- Datos del DataFrame ---")
        print(data_from_db.head()) # Muestra las primeras 5 filas
        print("\n--- Resumen de los datos ---")
        print(data_from_db.info())