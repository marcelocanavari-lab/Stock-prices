import sqlite3
import pandas as pd
import os

def mostrar_todos_los_registros(ticker):
    """
    Se conecta a la base de datos stocks.db y muestra todos los registros de una tabla específica.
    """
    db_path = os.path.join(os.getcwd(), 'stocks.db')

    if not os.path.exists(db_path):
        print(f"❌ Error: El archivo de la base de datos '{db_path}' no existe.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Verificar si la tabla existe en la base de datos
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (ticker,))
    if cursor.fetchone() is None:
        print(f"❌ Error: La tabla para el ticker '{ticker}' no existe en la base de datos.")
        conn.close()
        return

    # Leer todos los registros de la tabla en un DataFrame de pandas
    try:
        df = pd.read_sql_query(f"SELECT * FROM '{ticker}'", conn)
        conn.close()
    except Exception as e:
        print(f"❌ Error al leer la tabla: {e}")
        conn.close()
        return

    # Asegurar que el DataFrame no esté vacío
    if df.empty:
        print(f"❌ La tabla '{ticker}' no contiene datos.")
        return

    print(f"✅ Todos los registros para el ticker '{ticker}':\n")
    # Imprimir todos los registros
    print(df.to_string())

if __name__ == "__main__":
    ticker_input = input("Ingresa el ticker que deseas ver (ej. AAPL): ").upper()
    mostrar_todos_los_registros(ticker_input)