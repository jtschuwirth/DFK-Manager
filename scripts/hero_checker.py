from functions.data import get_accounts, network
from functions.provider import get_account, get_provider
from functions.hero_number import heroNumber
import json

ERC721Json = open("abi/ERC721.json")
ERC721ABI = json.load(ERC721Json)
itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)

w3 = get_provider(network)

def checkHeros():
    ready_accounts = []
    missing_heroes = []
    no_heroes = []
    for user in get_accounts():
        account = get_account(user, w3)
        hero_number = heroNumber(account)
        if hero_number == 18:
            ready_accounts.append(account.address)
        elif hero_number == 0:
            no_heroes.append(account.address)
        else:
            missing_heroes.append(account.address)
    print(f"Missing: {missing_heroes}")
    print("")
    print(f"None: {no_heroes}")

checkHeros()

