import pandas as pd
from functions.data import init_account_table

df =  pd.read_csv('raffle_results.csv')
accounts_table = init_account_table()
accounts = accounts_table.scan()["Items"]
for account in accounts:
    address = account["address_"].lower()
    if address in df["address"].values:
        print(f"winner: {account['address_']}, won: {df[df['address'] == address]['item']}")
        

