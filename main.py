import yfinance as yf
import sqlite3
import pandas as pd
import os
import matplotlib.pyplot as plt

def get_stock_data(ticker):
    """
    Obtiene datos de un ticker. Revisa la base de datos SQLite primero,
    si no los encuentra, los descarga de Yahoo Finance y los guarda.
    """
    db_path = os.path.join(os.getcwd(), 'stocks.db')
    conn = sqlite3.connect(db_path)

    # 1. Revisar si el ticker existe en la base de datos
    query = f"SELECT * FROM '{ticker}'"
    try:
        df = pd.read_sql_query(query, conn, index_col='Date')
    except pd.io.sql.DatabaseError:
        df = pd.DataFrame()

    if not df.empty:
        print(f"✅ Datos del ticker '{ticker}' encontrados en la base de datos.")
        conn.close()
        # Convertir el índice a formato de fecha si es necesario
        df.index = pd.to_datetime(df.index)
        return df
    else:
        print(f"❌ Datos de '{ticker}' no encontrados en la base de datos. Descargando...")

        # 2. Descargar datos de Yahoo Finance
        try:
            df = yf.download(ticker, period="1y")
            if df.empty:
                print(f"❌ No se pudieron descargar datos para el ticker '{ticker}'. Por favor, verifica el ticker.")
                conn.close()
                return None

            # 3. Guardar en SQLite
            df.to_sql(ticker, conn, if_exists='replace')
            print(f"✅ Datos de '{ticker}' guardados en la base de datos.")
            conn.close()
            return df
        except Exception as e:
            print(f"❌ Error al descargar datos: {e}")
            conn.close()
            return None

def plot_stock_data(df, ticker):
    """
    Genera y muestra un gráfico de los precios de cierre.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Close'], color='dodgerblue', linewidth=2)
    plt.title(f'Precios Históricos de {ticker} (Cierre)', fontsize=16)
    plt.xlabel('Fecha', fontsize=12)
    plt.ylabel('Precio de Cierre (USD)', fontsize=12)
    plt.grid(True)
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.show()

if __name__ == "__main__":
    ticker_input = input("Ingresa un ticker (ej. AAPL, MSFT): ").upper()

    data = get_stock_data(ticker_input)

    if data is not None:
        print("\n--- Vista previa de los datos ---")
        print(data[['Close', 'Volume']].tail())

        plot_stock_data(data, ticker_input)