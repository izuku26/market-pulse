import yfinance as yf
import pandas as pd
import os
import time

def run_etl():
    print("Démarrage de l'ETL pour les données financières...")

    tickers = [
        "^GSPC", "^FCHI", "^N225",   # Indices
        "GC=F", "W=F",       # Matières premières
        "BTC-USD", "ETH-USD",        # Cryptos
        "EURUSD=X", "AAPL", "NVDA", "TSLA" # Tech & Forex
    ]

    os.makedirs('data', exist_ok=True)
    data_frames = {}

    for ticker in tickers:
        try:
            print(f"Récupération de {ticker}...", end=" ", flush=True)
            
            t_obj = yf.Ticker(ticker)
            data = t_obj.history(start="2012-01-01", interval="1d")
            
            if not data.empty:
                
                data_frames[ticker] = data['Close']
                print("ok")
            else:
                print("Aucune donnée trouvée")
            
            time.sleep(0.5) 
            
        except Exception as e:
            print(f"Erreur: {e}")

    print("Fusion des colonnes")
    
    final_df = pd.DataFrame(data_frames)
    
    # Transformation 
    print("Nettoyage")
    final_df = final_df.ffill()
    final_df.index = pd.to_datetime(final_df.index).date 
    final_df.index = pd.to_datetime(final_df.index)

    # Chargement
    output_path = "data/market_data.parquet"
    final_df.to_parquet(output_path, engine='pyarrow')

    print(f"Données sauvegardées : {final_df.index.min().date()} au {final_df.index.max().date()}")
    print(f"Terminé ! Actifs Récupérés : {len(final_df.columns)}/{len(tickers)}")

if __name__ == "__main__":
    run_etl()