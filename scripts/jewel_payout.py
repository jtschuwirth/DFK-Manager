from functions.data import get_accounts, network, gas_buffer, chainId, init_account_table, manager_account, init_payouts_table
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
    for user in get_accounts(manager_account):
        account = get_account(user, w3)
        account_table = init_account_table()
        payouts_table = init_payouts_table()
        payout_account = account_table.query(
            KeyConditionExpression="address_ = :address_",
            ExpressionAttributeValues={
                ":address_": account.address,
            })["Items"][0]["pay_to"]
        nonce = w3.eth.get_transaction_count(account.address)
        print("")
        print(user)
        balance = getJewelBalance(account, w3)
        to_send = balance - gas_buffer*10**18
        if to_send > 0:
            sendJewel(account, payout_account, to_send, nonce)
            try:
                last_payout_time = payouts_table.get_item(Key={"address_": account.address})["Item"]["time_delta"]
            except:
                last_payout_time = 0
            try:
                payouts_table.delete_item(Key={"address_": account.address})
            except:
                pass
            payouts_table.put_item(Item={
                "address_": account.address,
                "amount_": str(to_send/10**18),
                "time_delta": str(int(time.time()) - int(last_payout_time)),
            })
            total_sent += to_send/10**18
            print(f"{to_send/10**18} Jewel payed to main account")
        else:
            print("No jewel to pay")
    print("")
    print("total payout")
    print(total_sent)


payout()