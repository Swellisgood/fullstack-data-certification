# Importing libraries 
from binance.client import Client
import configparser
import pandas as pd

# Loading keys from config file
config = configparser.ConfigParser()
config.read_file(open(r'C:\Users\swell\OneDrive\Bureau\Data_Science_Fullstack\projet-final\data\secret.cfg'))
actual_api_key = config.get('BINANCE', 'ACTUAL_API_KEY')
actual_secret_key = config.get('BINANCE', 'ACTUAL_SECRET_KEY')

client = Client(actual_api_key, actual_secret_key)

top20_list = ['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE', 'MATIC', 'SOL', 'AVAX', 'XLM', 'DOT', 'UNI', 'LINK', 'BCH', 'LTC', 'GRT', 'ETC', 'FIL', 'AAVE', 'ALGO', 'EOS']

for coin in top20_list:
    earliest_timestamp = client._get_earliest_valid_timestamp(f'{coin}USDT', '1d')  # Here "ETHUSDT" is a trading pair and "1d" is time interval
    candle = client.get_historical_klines(f"{coin}USDT", "1d", earliest_timestamp, limit=1000)
    print(f"Data for coin : {coin}, has been found and downloaded !")
    coin_df = pd.DataFrame(candle, columns=['Date', 'open', 'high', 'low', 'close', 'volume', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])
    coin_df.Date = pd.to_datetime(coin_df.Date, unit='ms')
    coin_df['MACD'] = coin_df['close'].ewm(span=12, adjust=False, min_periods=12).mean() - coin_df['close'].ewm(span=26, adjust=False, min_periods=26).mean()
    coin_df['MACD_Signal'] = coin_df['MACD'].ewm(span=9, adjust=False, min_periods=9).mean()
    coin_df.closeTime = pd.to_datetime(coin_df.closeTime, unit='ms')
    coin_df.set_index('Date', inplace=True)
    coin_df.to_csv(f'./{coin}_OHLC.csv')

print("All Data was scraped ! It has been saved in .csv format !")