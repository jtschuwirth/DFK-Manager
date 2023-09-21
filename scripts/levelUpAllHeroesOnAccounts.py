from functions.levelUpAccountHeroes import startMeditations, completeMeditations
from functions.data import get_accounts, network
from functions.provider import get_account, get_provider
from functions.utils import getItemAmount, sendItem, getMaxExp
import json
import time
import math

from functions.getAccountHeroes import getAccountHeroes

itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)

ERC20Json = open("abi/ERC20.json")
ERC20ABI = json.load(ERC20Json)

w3 = get_provider(network)

def neededRunes(heroes):
    runes =0
    for hero in heroes:
        runes += math.floor(hero["level"]/2)+1
        
    return runes


def levelUpAllHeroesOnAccounts(main_address, onlyComplete = False, start_index = 0):
    accounts = get_accounts(main_address)
    main_account = get_account(main_address, w3)
    main_account_nonce = w3.eth.get_transaction_count(main_account.address)
    c=1
    runesContract = w3.eth.contract(address=items["Shvas Rune"], abi=ERC20ABI)
    crystalContract = w3.eth.contract(address=items["Crystal"], abi=ERC20ABI)
    for address in accounts:
        if c<start_index:
            c+=1
            continue

        sent = False
        if sent:
            main_account_nonce = w3.eth.get_transaction_count(main_account.address)
        print(f"Checking {address} ({c}/{len(accounts)})")
        c+=1
        account = get_account(address, w3)
        heroes = getAccountHeroes(account.address, network)
        heroes_to_level = []
        for hero in heroes:
            max_exp = getMaxExp(hero["level"])
            if max_exp == 0: continue
            if hero["xp"]==max_exp and hero["currentQuest"]=="0x0000000000000000000000000000000000000000":
                heroes_to_level.append(hero)
        if len(heroes_to_level)==0:
            print("No heroes ready to start meditation")
        else:
            print(f"Account has {len(heroes_to_level)} heroes ready to start meditation")

        if not onlyComplete and len(heroes_to_level)!=0:
            amount_runes = getItemAmount(account, "Shvas Rune", w3)
            amount_crystal = getItemAmount(account, "Crystal", w3)

            needed_runes = neededRunes(heroes_to_level)
            
            if amount_runes < needed_runes:
                sendItem(main_account, runesContract, needed_runes-amount_runes, account.address, main_account_nonce, w3)
                print(f"Sent {needed_runes-amount_runes} Shvas Runes to " + account.address)
                main_account_nonce+=1
                time.sleep(5)
                sent=True
            if amount_crystal < 5*10**18:
                sendItem(main_account, crystalContract, 5*10**18-amount_crystal, account.address, main_account_nonce, w3)
                print(f"Sent {(5*10**18-amount_crystal)/(10**18)} Crystal to " + account.address)
                main_account_nonce+=1
                time.sleep(5)
                sent=True

        if not onlyComplete and len(heroes_to_level)!=0:
            print(f"Starting meditations on {address}")
            startMeditations(address, heroes_to_level)

            time.sleep(30)
        
            heroes = getAccountHeroes(account.address, network)
        heroes_to_level = []
        for hero in heroes:
            max_exp = getMaxExp(hero["level"])
            if max_exp == 0: continue
            if hero["xp"]==max_exp and hero["currentQuest"]!="0x0000000000000000000000000000000000000003" and hero["currentQuest"]!="0x0000000000000000000000000000000000000000":
                heroes_to_level.append(hero)
        if len(heroes_to_level)==0:
            print("No heroes ready to complete meditation")
            print("")
            continue
        if len(heroes_to_level)!=0:
            print(f"Completing meditations on {address}")
            completeMeditations(address, heroes_to_level)

        print("")

levelUpAllHeroesOnAccounts("0xa691623968855b91A066661b0552a7D3764c9a64")
