import yfinance as yf
import sqlite3
import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime

def get_stock_data(ticker, start_date_str, end_date_str):
    """
    Obtiene los datos de un ticker, los actualiza si ya existen en la base de datos
    o los descarga por primera vez si no existen.
    """
    db_path = os.path.join(os.getcwd(), 'stocks.db')
    conn = sqlite3.connect(db_path)
    
    # Convertir fechas de string a objetos datetime para validación
    try:
        start_date = pd.to_datetime(start_date_str).date()
        end_date = pd.to_datetime(end_date_str).date()
        if start_date > end_date:
            print("❌ La fecha de inicio no puede ser posterior a la fecha de fin.")
            return pd.DataFrame()
    except ValueError:
        print("❌ Formato de fecha inválido. Usa AAAA-MM-DD.")
        return pd.DataFrame()

    # Verificar si la tabla existe en la base de datos
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (ticker,))
    table_exists = cursor.fetchone() is not None
    
    df_data = pd.DataFrame()
    
    if table_exists:
        print(f"✅ Datos del ticker '{ticker}' encontrados en la base de datos.")
        try:
            # Leer los datos existentes y manejar errores de columna
            df_existing = pd.read_sql_query(f"SELECT * FROM '{ticker}'", conn)
            
            # Asegurar que el DataFrame tiene la estructura correcta
            if not df_existing.empty and 'Date' in df_existing.columns and 'Close' in df_existing.columns:
                df_existing['Date'] = pd.to_datetime(df_existing['Date'])
                df_existing.set_index('Date', inplace=True)
                df_existing.columns = [col.capitalize() for col in df_existing.columns]
                
                # Obtener la última fecha de la base de datos
                last_date = df_existing.index.max().date()
                
                # Descargar solo datos nuevos si la fecha de fin es posterior
                if end_date > last_date:
                    print(f"Descargando datos nuevos para '{ticker}' desde {last_date + datetime.timedelta(days=1)}...")
                    df_new = yf.download(ticker, start=str(last_date + datetime.timedelta(days=1)), end=end_date_str)
                    
                    if not df_new.empty:
                        df_combined = pd.concat([df_existing, df_new])
                        df_combined.reset_index(inplace=True)
                        df_combined.to_sql(ticker, conn, if_exists='replace', index=False)
                        print(f"✅ Base de datos de '{ticker}' actualizada con {len(df_new)} nuevos registros.")
                        df_data = df_combined
                    else:
                        print(f"ℹ️ No hay datos nuevos para actualizar para '{ticker}'.")
                        df_data = df_existing.reset_index()
                else:
                    df_data = df_existing.reset_index()

            else:
                # Si la tabla está corrupta, se borra y se descarga de nuevo
                print(f"⚠️ La tabla de '{ticker}' está corrupta. Borrando tabla y descargando de nuevo...")
                cursor.execute(f"DROP TABLE '{ticker}'")
                conn.commit()
                raise ValueError("Tabla corrupta, se requiere nueva descarga.")
                
        except (pd.io.sql.DatabaseError, ValueError) as e:
            # Descargar datos si la tabla no se puede leer o está corrupta
            print(f"❌ Error al leer la tabla '{ticker}': {e}. Descargando desde {start_date} a {end_date}...")
            df_data = yf.download(ticker, start=start_date_str, end=end_date_str)
            if not df_data.empty:
                df_data.reset_index(inplace=True)
                df_data.to_sql(ticker, conn, if_exists='replace', index=False)
                print(f"✅ Datos de '{ticker}' guardados en la base de datos.")
            else:
                print(f"❌ No se pudieron descargar datos para el ticker '{ticker}'.")
                return pd.DataFrame()
    
    else:
        print(f"❌ Datos de '{ticker}' no encontrados en la base de datos. Descargando desde {start_date} a {end_date}...")
        try:
            df_data = yf.download(ticker, start=start_date_str, end=end_date_str)
            if not df_data.empty:
                df_data.reset_index(inplace=True)
                df_data.to_sql(ticker, conn, if_exists='replace', index=False)
                print(f"✅ Datos de '{ticker}' guardados en la base de datos.")
            else:
                print(f"❌ No se pudieron descargar datos para el ticker '{ticker}'.")
                return pd.DataFrame()
        except Exception as e:
            print(f"❌ Error al descargar datos: {e}")
            return pd.DataFrame()
    
    conn.close()
    
    # Volver a procesar el DataFrame para la visualización
    if not df_data.empty and 'Date' in df_data.columns:
        df_data['Date'] = pd.to_datetime(df_data['Date'])
        df_data.set_index('Date', inplace=True)
        # La línea problemática ya no es necesaria aquí.
        
        # Filtrar por el rango de fechas ingresado por el usuario
        df_data = df_data.loc[start_date_str:end_date_str]
    else:
        return pd.DataFrame()
    
    return df_data

def plot_multiple_tickers_combined(data_frames):
    """
    Genera y muestra un gráfico de los precios de cierre para múltiples tickers en una sola figura.
    """
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(14, 8))
    
    found_data = False
    for ticker, df in data_frames.items():
        if 'Close' in df.columns and not df['Close'].dropna().empty:
            plt.plot(df.index, df['Close'], label=f'{ticker} Cierre', linewidth=2)
            found_data = True
        else:
            print(f"⚠️ El DataFrame de '{ticker}' no contiene datos válidos en la columna 'Close'. Saltando gráfico.")

    if found_data:
        plt.title('Evolución de Precios de Cierre (Combinado)', fontsize=18)
        plt.xlabel('Fecha', fontsize=14)
        plt.ylabel('Precio de Cierre (USD)', fontsize=14)
        plt.legend(fontsize=12)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        print("No hay datos válidos para generar el gráfico combinado.")

def plot_multiple_tickers_separate(data_frames):
    """
    Genera y muestra un gráfico para cada ticker en una ventana separada.
    """
    plt.style.use('seaborn-v0_8-whitegrid')
    
    for ticker, df in data_frames.items():
        if 'Close' in df.columns and not df['Close'].dropna().empty:
            plt.figure(figsize=(14, 8))
            plt.plot(df.index, df['Close'], color='dodgerblue', linewidth=2)
            plt.title(f'Evolución del Precio de Cierre de {ticker}', fontsize=18)
            plt.xlabel('Fecha', fontsize=14)
            plt.ylabel('Precio de Cierre (USD)', fontsize=14)
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        else:
            print(f"⚠️ El DataFrame de '{ticker}' no contiene datos válidos en la columna 'Close'. Saltando gráfico.")

if __name__ == "__main__":
    ticker_input = input("Ingresa uno o más tickers separados por comas (ej. AAPL,MSFT,GOOG): ").upper()
    tickers = [ticker.strip() for ticker in ticker_input.split(',')]
    
    # Solicitar las fechas de inicio y fin
    start_date = input("Ingresa la fecha de inicio (formato AAAA-MM-DD): ")
    end_date = input("Ingresa la fecha de fin (formato AAAA-MM-DD): ")
    
    all_data = {}
    for ticker in tickers:
        data = get_stock_data(ticker, start_date, end_date)
        if not data.empty:
            all_data[ticker] = data
    
    if all_data:
        print("\nOpciones de visualización:")
        print("1. Gráfico combinado (todos los tickers en uno)")
        print("2. Gráficos separados (una ventana por ticker)")
        
        choice = input("Elige una opción (1 o 2): ")
        
        if choice == '1':
            plot_multiple_tickers_combined(all_data)
        elif choice == '2':
            plot_multiple_tickers_separate(all_data)
        else:
            print("❌ Opción no válida. Por favor, elige 1 o 2.")
    else:
        print("No se encontraron datos válidos para graficar.")