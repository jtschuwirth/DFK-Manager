from functions.get_market_heros import getMarketHeros
from functions.data import network
from functions.provider import get_account, get_provider
from functions.hero_number import heroNumber
from functions.utils import checkAllowance
import json

w3 = get_provider(network)

itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)

ERC20Json = open("abi/ERC20.json")
ERC20ABI = json.load(ERC20Json)

HeroSaleAddress = "0xc390fAA4C7f66E4D62E59C231D5beD32Ff77BEf0"
HeroSaleJson = open("abi/HeroSale.json")
HeroSaleABI = json.load(HeroSaleJson)
HeroSaleContract = w3.eth.contract(address=HeroSaleAddress, abi=HeroSaleABI)

user = "0x88a90E420277d11ca8d671237365bBceDFA01353"

def addAllowance(account, nonce):
    contract = w3.eth.contract(address= items["Crystal"], abi=ERC20ABI)
    tx = contract.functions.approve(HeroSaleAddress, 115792089237316195423570985008687907853269984665640564039457584007913129639935).build_transaction({
        "from": account.address,
        "nonce": nonce
    })
    gas = int(w3.eth.estimate_gas(tx)*1.4)
    tx["gas"] = gas
    tx["maxFeePerGas"] = w3.toWei(250, 'gwei')
    tx["maxPriorityFeePerGas"] = w3.toWei(2, "gwei")
    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    hash = w3.toHex(hash)
    
def buyHero(account, hero, nonce):
    tx = HeroSaleContract.functions.bid(hero["id"], hero["price"]).build_transaction({
        "from": account.address,
        "nonce": nonce
    })
    gas = int(w3.eth.estimate_gas(tx)*2)
    tx["gas"] = gas
    tx["maxFeePerGas"] = w3.toWei(250, 'gwei')
    tx["maxPriorityFeePerGas"] = w3.toWei(2, "gwei")
    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    hash = w3.toHex(hash)

def buyHeros():
    account = get_account(user, w3)
    c = heroNumber(account)
    heros = getMarketHeros()
    nonce = w3.eth.get_transaction_count(account.address)
    if checkAllowance(account, "Crystal", HeroSaleAddress, ERC20ABI):
        addAllowance(account, nonce)
        print("Added allowance")
        return
    for hero in heros:
        if c==18: 
            print("Already has 18 heros")
            break
        try:
            buyHero(account, hero, nonce)
            print(f"Bought hero: {hero['id']}")
            nonce+=1
            c+=1
        except Exception as error:
            print(f"Error buying hero: {hero['id']}")
            print(error)
            print("")

buyHeros()