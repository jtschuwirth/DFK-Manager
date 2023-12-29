import json
from functions.provider import get_provider, get_account

w3 = get_provider("dfk")

FactoryAddress = "0x794C07912474351b3134E6D6B3B7b3b4A07cbAAa"
FactoryJson = open("abi/UniswapFactory.json")
FactoryABI = json.load(FactoryJson)

itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)

def getPairAddress(token1, token2):
    FactoryContract = w3.eth.contract(address=FactoryAddress, abi=FactoryABI)
    pairAddress = FactoryContract.functions.getPair(
        items[token1],
        items[token2]
    ).call()
    return pairAddress

for item in items:
    if item == "Jewel":
        continue
    print(item, "Jewel", getPairAddress(item, "Jewel"))