from functions.data import get_accounts, network, chainId, init_account_table, init_settings_table, manager_account
from functions.provider import get_account, get_provider
from functions.utils import getJewelBalance
import json
import time

itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)

w3 = get_provider(network)

def getGasPrice(w3):
    gasPrice = w3.eth.gas_price/10**9
    return gasPrice
    

print(getGasPrice(w3))