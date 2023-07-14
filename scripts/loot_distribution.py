from functions.data import get_accounts, network, manager_account, init_account_table
from functions.provider import get_account, get_provider
from functions.utils import checkAllowance, addAllowance
import json

w3 = get_provider(network)

itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)
decimalsJson = open("items_data/decimals.json")
decimals_data = json.load(decimalsJson)

ERC20Json = open("abi/ERC20.json")
ERC20ABI = json.load(ERC20Json)



sellables = [
    #"DFKGold",
    #"Shvas Rune",
    #"Moksha Rune",
    #"Gaias Tears",
    "Yellow Pet Egg",
]

def sendItem(account, itemContract, amount, to, nonce):
    tx = itemContract.functions.transfer(
        to,
        amount,
    ).build_transaction({
        "from": account.address,
        "nonce": nonce,
    })
    tx["gas"] = int(w3.eth.estimate_gas(tx))
    tx["maxFeePerGas"] = w3.toWei(50, 'gwei')
    tx["maxPriorityFeePerGas"] = w3.toWei(2, "gwei")
    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    hash = w3.toHex(hash)


def getItemAmount(account, item):
    contract = w3.eth.contract(address= items[item], abi=ERC20ABI)
    return int(contract.functions.balanceOf(account.address).call())

def sellRewards():
    accounts = get_accounts(manager_account)
    c=1
    for user in accounts:
        account = get_account(user, w3)
        account_table= init_account_table()
        payout_account = account_table.query(
            KeyConditionExpression="address_ = :address_",
            ExpressionAttributeValues={
                ":address_": account.address,
            })["Items"][0]["pay_to"]
        nonce = w3.eth.get_transaction_count(account.address)
        print("")
        print(f"{user} ({c}/{len(accounts)})")
        c+=1
        for item in sellables:
            itemContract = w3.eth.contract(address=items[item], abi=ERC20ABI)
            decimals = 0
            amount = getItemAmount(account, item)
            if item in decimals_data:
                decimals = decimals_data[item]
            print(f"{item}: {amount/10**decimals}")
            if checkAllowance(account, item, items[item], ERC20ABI, w3):
                try:
                    addAllowance(account, item, items[item], nonce, ERC20ABI, w3)
                    nonce+=1
                    print(f"Added allowance to {item}")
                except Exception as error:
                    print(f"Error adding allowance to {item}")
                    print(error)

            if amount != 0:
                try:
                    sendItem(account, itemContract, amount, payout_account, nonce)
                    nonce+=1
                    print(f"Sent {item} to {payout_account}")
                except Exception as error:
                    print(f"Error sending {item}")
                    print(error)
            else:
                pass

sellRewards()
