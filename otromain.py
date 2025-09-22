import yfinance as yf
import sqlite3
import pandas as pd
import os
import matplotlib.pyplot as plt

def get_stock_data(ticker):
    """
    Obtiene datos de un ticker, revisa la base de datos SQLite, si no existen, los descarga.
    """
    db_path = os.path.join(os.getcwd(), 'stocks.db')
    conn = sqlite3.connect(db_path)
    df = pd.DataFrame()
    
    try:
        # Intenta leer desde la base de datos
        df = pd.read_sql_query(f"SELECT * FROM '{ticker}'", conn)
        
        if not df.empty:
            print(f"✅ Datos del ticker '{ticker}' encontrados en la base de datos.")
            # Convertir el índice a formato de fecha
            df.columns = [col.capitalize() for col in df.columns]
            df.set_index('Date', inplace=True)
            df.index = pd.to_datetime(df.index)
        else:
            print(f"❌ Datos de '{ticker}' no encontrados en la base de datos. Descargando...")
            df = yf.download(ticker, period="1y")
            if not df.empty:
                df.to_sql(ticker, conn, if_exists='replace')
                print(f"✅ Datos de '{ticker}' guardados en la base de datos.")
            else:
                print(f"❌ No se pudieron descargar datos para el ticker '{ticker}'.")

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.close()
        return pd.DataFrame()

    finally:
        conn.close()
        return df

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
    
    if not data.empty:
        print("\n--- Vista previa de los datos ---")
        print(data[['Close', 'Volume']].tail())
        
        plot_stock_data(data, ticker_input)
    else:
        print("❌ No se pudieron obtener datos para graficar.")