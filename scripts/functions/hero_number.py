from functions.data import network
from functions.provider import get_provider
import json

ERC721Json = open("abi/ERC721.json")
ERC721ABI = json.load(ERC721Json)
itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)

w3 = get_provider(network)

def heroNumber(account):
    contract = w3.eth.contract(address= items["Heroes"], abi=ERC721ABI)
    return int(contract.functions.balanceOf(account.address).call())