import json

itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)

ERC20Json = open("abi/ERC20.json")
ERC20ABI = json.load(ERC20Json)

def getJewelBalance(account, w3):
    return int(w3.eth.get_balance(account.address))

def checkAllowance(account, item, address, abi, w3):
    contract = w3.eth.contract(address= items[item], abi=abi)
    if int(contract.functions.allowance(account.address, address).call()) == 0:
        return True
    else: 
        return False