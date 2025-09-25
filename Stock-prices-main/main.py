import yfinance as yf
import sqlite3
import pandas as pd
import os
import matplotlib.pyplot as plt

def get_stock_data(ticker):
    """
    Obtiene datos de un ticker desde la base de datos SQLite o Yahoo Finance.
    Actualiza la base si ya existen datos.
    """
    db_path = os.path.join(os.getcwd(), 'stocks.db')
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (ticker,))
    table_exists = cursor.fetchone() is not None

    if table_exists:
        print(f"✅ Datos del ticker '{ticker}' encontrados en la base de datos.")
        try:
            df_existing = pd.read_sql_query(f"SELECT * FROM '{ticker}'", conn)
            
            # Mostrar columnas para debug
            print("Columnas leídas desde la base:", df_existing.columns.tolist())

            # Aplanar columnas si son tuplas
            if isinstance(df_existing.columns[0], tuple):
                df_existing.columns = [col[0] for col in df_existing.columns]

            # Normalizar nombres de columnas
            col_map = {
                'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close',
                'adj close': 'Adj Close', 'volume': 'Volume', 'date': 'Date', 'index': 'Date'
            }
            df_existing.columns = [col_map.get(col.lower(), col) for col in df_existing.columns]

            # Restaurar índice
            if 'Date' in df_existing.columns:
                df_existing['Date'] = pd.to_datetime(df_existing['Date'])
                df_existing.set_index('Date', inplace=True)

            # Última fecha disponible
            last_date = df_existing.index.max().date()
            print(f"Última fecha en la base: {last_date}")

            # Descargar solo datos nuevos desde el día siguiente
            df_new = yf.download(ticker, start=str(last_date + pd.Timedelta(days=1)))
            if not df_new.empty:
                # Aplanar columnas si es necesario
                if isinstance(df_new.columns[0], tuple):
                    df_new.columns = [col[0] for col in df_new.columns]
                
                # Combinar con datos existentes
                df_combined = pd.concat([df_existing, df_new])
                df_combined.to_sql(ticker, conn, if_exists='replace')
                print(f"✅ Base actualizada con {len(df_new)} nuevos registros.")
                df_existing = df_combined
            else:
                print("ℹ️ No hay datos nuevos para actualizar.")

            conn.close()
            return df_existing

        except Exception as e:
            print(f"❌ Error al leer o actualizar la tabla '{ticker}': {e}")
            conn.close()
            return None

    else:
        print(f"❌ Datos de '{ticker}' no encontrados en la base de datos. Descargando...")
        try:
            df = yf.download(ticker, period="1y")
            if df.empty:
                print(f"❌ No se pudieron descargar datos para el ticker '{ticker}'.")
                conn.close()
                return None

            # Aplanar columnas si son multi-nivel
            if isinstance(df.columns[0], tuple):
                df.columns = [col[0] for col in df.columns]

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
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Close'], color='dodgerblue', linewidth=2)
    plt.title(f'Precios Históricos de {ticker} (Cierre)', fontsize=16)
    plt.xlabel('Fecha', fontsize=12)
    plt.ylabel('Precio de Cierre (USD)', fontsize=12)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    ticker_input = input("Ingresa un ticker (ej. AAPL, MSFT): ").upper()
    
    data = get_stock_data(ticker_input)
    
    if data is not None:
        print("\n--- Vista previa de los datos ---")
        print(data.head())  # Muestra las primeras 5 filas
                
        plot_stock_data(data, ticker_input)
