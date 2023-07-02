from functions.data import get_accounts, network
from functions.provider import get_account, get_provider
from functions.utils import heroNumber
from functions.utils import getJewelBalance
import json

ERC721Json = open("abi/ERC721.json")
ERC721ABI = json.load(ERC721Json)
itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)

w3 = get_provider(network)

def checkHeros():
    ready_accounts = []
    missing = []
    zero = []
    for user in get_accounts():
        account = get_account(user, w3)
        hero_number = heroNumber(account, w3)
        if hero_number == 18:
            ready_accounts.append(account.address)
        elif hero_number == 0:
            zero.append(account.address)
        else:
            missing.append(account.address)
    print(f"Missing Heros: {missing}")
    print("")
    print(f"No Heros: {zero}")

def checkBalance():
    zero = []
    missing = []
    for user in get_accounts():
        account = get_account(user, w3)
        balance = getJewelBalance(account, w3)
        if balance == 0:
            zero.append(account.address)
        elif 5 > balance/10**18:
            missing.append(account.address)
    print(f"Missing Jewel: {missing}")
    print("")
    print(f"No Jewel: {zero}")



checkHeros()
print("")
print("-----------------------------------------")
print("")
checkBalance()

