import pandas as pd
import os


# Make a list of the crypto symbols available in the ./data folder stripping the .csv extension and the "_OHLC" from the file names
crypto_names = list(filter(lambda f: f.endswith('.csv'), os.listdir("./data")))
crypto_names = [name.replace("_OHLC.csv", "") for name in crypto_names]


#make UI selector for crypto
crypto_dict = [{"label": name, "value": name} for name in crypto_names]