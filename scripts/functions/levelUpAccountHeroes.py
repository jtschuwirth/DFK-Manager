from functions.data import network
from functions.provider import get_account, get_provider
from functions.getAccountHeroes import getAccountHeroes
from functions.startMeditation import startMeditation, startAllMeditations
from functions.completeMeditation import completeMeditation, completeAllMeditations
from functions.utils import checkAllowance, addAllowance, getMaxExp
import time
import json

meditationCircleAddress = "0xD507b6b299d9FC835a0Df92f718920D13fA49B47"
ERC20Json = open("abi/ERC20.json")
ERC20ABI = json.load(ERC20Json)

itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)

meditationSelectionJson = open("items_data/meditation_selection.json")
meditationSelection = json.load(meditationSelectionJson)

w3 = get_provider(network)

def startMeditations(account, heroes):
    account = get_account(account, w3)
    nonce = w3.eth.get_transaction_count(account.address)
    added_allowance = False
    if checkAllowance(account, "Shvas Rune", "0xD507b6b299d9FC835a0Df92f718920D13fA49B47", ERC20ABI, w3):
        try:
            addAllowance(account, "Shvas Rune", "0xD507b6b299d9FC835a0Df92f718920D13fA49B47", nonce, ERC20ABI, w3)
            nonce+=1
            print(f"Added allowance to Shvas Rune")
            added_allowance = True
        except Exception as error:
            print(f"Error adding allowance to Shvas Rune")
            print(error)
    if checkAllowance(account, "Crystal", "0xD507b6b299d9FC835a0Df92f718920D13fA49B47", ERC20ABI, w3):
        try:
            addAllowance(account, "Crystal", "0xD507b6b299d9FC835a0Df92f718920D13fA49B47", nonce, ERC20ABI, w3)
            nonce+=1
            print(f"Added allowance to Crystal")
            added_allowance = True
        except Exception as error:
            print(f"Error adding allowance to Crystal")
            print(error)
    if added_allowance:
        time.sleep(20)

    meditations = []
    for hero in heroes:
        max_exp = getMaxExp(hero["level"])
        if max_exp == 0: continue
        if hero["xp"]==max_exp and hero["currentQuest"]=="0x0000000000000000000000000000000000000000":
            meditations.append(
                (int(hero["id"]), 
                meditationSelection[str(hero["mainClass"])]["main"], 
                meditationSelection[str(hero["mainClass"])]["secondary"],
                meditationSelection[str(hero["mainClass"])]["tertiary"],
                "0x0000000000000000000000000000000000000000",
                False))
            print(f"adding hero {hero['id']} to start meditation")
    try:            
        startAllMeditations(meditations, account, nonce, w3)
        print(f"Started meditations")
        nonce+=1
    except Exception as error: 
        print(f"Error starting meditations: {error}")

            
def completeMeditations(account, heroes): 
    account = get_account(account, w3)
    nonce = w3.eth.get_transaction_count(account.address)    
    heroes_to_level = [] 
    for hero in heroes:
        max_exp = getMaxExp(hero["level"])
        if max_exp == 0: continue
        if hero["xp"]==max_exp and hero["currentQuest"]!="0x0000000000000000000000000000000000000003":
            heroes_to_level.append(int(hero["id"]))
            print(f"adding hero {hero['id']} to complete meditation")
    try:            
        completeAllMeditations(heroes_to_level, account, nonce, w3)
        print("Completed meditations")
        nonce+=1
    except Exception as error:
        print(f"Error completing meditations: {error}")