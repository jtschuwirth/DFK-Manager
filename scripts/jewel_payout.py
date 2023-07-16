from functions.data import get_accounts, network, chainId, init_account_table, init_settings_table, manager_account
from functions.provider import get_account, get_provider
from functions.utils import getJewelBalance
import json
import time

itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)

w3 = get_provider(network)

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
    accounts = get_accounts(manager_account)
    c=1
    for user in accounts:
        account = get_account(user, w3)
        account_table = init_account_table()
        settings_table = init_settings_table()
        gas_buffer = int(settings_table.get_item(Key={"key_": "seller_settings"})["Item"]["min_buffer"])
        payout_account = account_table.query(
            KeyConditionExpression="address_ = :address_",
            ExpressionAttributeValues={
                ":address_": account.address,
            })["Items"][0]["pay_to"]
        nonce = w3.eth.get_transaction_count(account.address)
        print("")
        print(f"account: {user} ({c}/{len(accounts)})")
        c+=1
        balance = getJewelBalance(account, w3)
        to_send = balance - gas_buffer*10**18
        if to_send > 0:
            sendJewel(account, payout_account, to_send, nonce)
            total_sent += to_send/10**18
            print(f"{to_send/10**18} Jewel payed to main account")
        else:
            print("No jewel to pay")
    print("")
    print(f"total payout {total_sent} Jewel")


payout()