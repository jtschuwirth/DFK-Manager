from functions.data import get_accounts, network, account_table
from functions.provider import get_account, get_provider
from functions.utils import checkAllowance
import json

w3 = get_provider(network)

itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)
decimalsJson = open("items_data/decimals.json")
decimals_data = json.load(decimalsJson)

ERC20Json = open("abi/ERC20.json")
ERC20ABI = json.load(ERC20Json)



sellables = [
    "DFKGold",
    "Shvas Rune",
    "Moksha Rune",
    "Gaias Tears",
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

def addAllowance(account, item, nonce):
    contract = w3.eth.contract(address= items[item], abi=ERC20ABI)
    tx = contract.functions.approve(items[item], 115792089237316195423570985008687907853269984665640564039457584007913129639935).build_transaction({
        "from": account.address,
        "nonce": nonce,
    })
    tx["gas"] = int(w3.eth.estimate_gas(tx))
    tx["maxFeePerGas"] = w3.toWei(50, 'gwei')
    tx["maxPriorityFeePerGas"] = w3.toWei(2, "gwei")
    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    hash = w3.toHex(hash)

def sellRewards():
    for user in get_accounts():
        account = get_account(user, w3)
        payout_account = account_table.query(
            KeyConditionExpression="address_ = :address_",
            ExpressionAttributeValues={
                ":address_": account.address,
            })["Items"][0]["pay_to"]
        nonce = w3.eth.get_transaction_count(account.address)
        print("")
        print(user)
        for item in sellables:
            itemContract = w3.eth.contract(address=items[item], abi=ERC20ABI)
            decimals = 0
            amount = getItemAmount(account, item)
            if item in decimals_data:
                decimals = decimals_data[item]
            print(f"{item}: {amount/10**decimals}")
            if checkAllowance(account, item, items[item], ERC20ABI):
                try:
                    addAllowance(account, item, nonce)
                    nonce+=1
                    print(f"Added allowance to {item}")
                except Exception as error:
                    print(f"Error adding allowance to {item}")
                    print(error)

            elif amount != 0:
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
