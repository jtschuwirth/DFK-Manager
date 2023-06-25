from functions.data import get_accounts, network, gas_buffer, payout_account, chainId
from functions.provider import get_account, get_provider
import json

itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)

w3 = get_provider(network)

def getJewelBalance(account):
    return int(w3.eth.get_balance(account.address))

def sendJewel(account, payout_account, amount, nonce):
    tx = {
        "from": account.address,
        "to": payout_account,
        "value": amount,
        "nonce": nonce,
        "chainId": chainId
    }
    gas = w3.eth.estimate_gas(tx)
    tx["gas"] = gas
    tx["gasPrice"] = w3.toWei(50, 'gwei')
    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    hash = w3.toHex(hash)


def payout():
    total_sent = 0
    for user in get_accounts:
        account = get_account(user, w3)
        nonce = w3.eth.get_transaction_count(account.address)
        print("")
        print(user)
        balance = getJewelBalance(account)
        to_send = balance - gas_buffer*10**18
        if to_send > 0:
            sendJewel(account, payout_account, to_send, nonce)
            total_sent += to_send/10**18
            print(f"{to_send/10**18} Jewel payed to main account")
        else:
            print("No jewel to pay")
    print("")
    print("total payout")
    print(total_sent)


payout()