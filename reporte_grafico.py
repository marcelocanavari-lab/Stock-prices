import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_stock_report(ticker):
    """
    Genera un reporte gráfico de los precios de cierre para un ticker.
    Lee los datos desde la base de datos stocks.db.
    """
    db_path = os.path.join(os.getcwd(), 'stocks.db')

    if not os.path.exists(db_path):
        print(f"❌ Error: No se encontró el archivo de la base de datos '{db_path}'.")
        return

    conn = sqlite3.connect(db_path)
    
    # Verificar si la tabla existe en la base de datos
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (ticker,))
    if cursor.fetchone() is None:
        print(f"❌ Error: La tabla para el ticker '{ticker}' no existe en la base de datos.")
        conn.close()
        return

    # Leer los datos de la tabla en un DataFrame
    try:
        df = pd.read_sql_query(f"SELECT * FROM '{ticker}'", conn)
        conn.close()
    except Exception as e:
        print(f"❌ Error al leer la tabla: {e}")
        conn.close()
        return

    if df.empty:
        print(f"❌ La tabla '{ticker}' no contiene datos.")
        return

    # Imprimir los nombres de las columnas antes de la modificación
    print(f"Nombres de las columnas originales: {df.columns.tolist()}")

    # Solución definitiva: Renombrar las columnas de forma explícita
    new_columns = {}
    for col in df.columns:
        if col.lower() == 'close':
            new_columns[col] = 'Close'
        elif col.lower() == 'date':
            new_columns[col] = 'Date'
        else:
            new_columns[col] = col.capitalize()
            
    df = df.rename(columns=new_columns)
    
    # Imprimir los nombres de las columnas después de la modificación
    print(f"Nombres de las columnas después de la modificación: {df.columns.tolist()}")
    
    # Asegurar que el DataFrame tiene las columnas correctas
    if 'Date' not in df.columns or 'Close' not in df.columns:
        print("❌ Error: El DataFrame no contiene las columnas 'Date' o 'Close'.")
        return

    # Preparar los datos para el gráfico
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    # Generar el gráfico
    plt.figure(figsize=(12, 7))
    plt.plot(df.index, df['Close'], color='dodgerblue', linewidth=2)
    plt.title(f'Evolución del Precio de Cierre de {ticker}', fontsize=18)
    plt.xlabel('Fecha', fontsize=14)
    plt.ylabel('Precio de Cierre (USD)', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Personalizar el gráfico
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    ticker_input = input("Ingresa el ticker que deseas graficar (ej. AAPL/MSFT): ").upper()
    generate_stock_report(ticker_input)