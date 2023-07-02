from functions.data import get_accounts, network
from functions.provider import get_account, get_provider
from functions.utils import checkAllowance
import json
import time

w3 = get_provider(network)

itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)
decimalsJson = open("items_data/decimals.json")
decimals_data = json.load(decimalsJson)

RouterAddress = "0x3C351E1afdd1b1BC44e931E12D4E05D6125eaeCa"
RouterJson = open("abi/UniswapV2Router02.json")
RouterABI = json.load(RouterJson)
RouterContract = w3.eth.contract(address=RouterAddress, abi=RouterABI)

ERC20Json = open("abi/ERC20.json")
ERC20ABI = json.load(ERC20Json)

sellables = [
    "DFKGold",
    "Shvas Rune",
    "Moksha Rune",
    "Gaias Tears",
    "Yellow Pet Egg",
]

def sellItem(account, item, amount, nonce):
    tx = RouterContract.functions.swapExactTokensForETH(
        amount,
        0,
        [items[item], items["Crystal"], items["Jewel"]],
        account.address,
        int(time.time()+60)
        
    ).build_transaction({
        "from": account.address,
        "nonce": nonce
    })
    tx["gas"] = int(w3.eth.estimate_gas(tx))
    tx["maxFeePerGas"] = w3.toWei(50, 'gwei')
    tx["maxPriorityFeePerGas"] = w3.toWei(3, "gwei")
    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    hash = w3.toHex(hash)


def getItemAmount(account, item):
    contract = w3.eth.contract(address= items[item], abi=ERC20ABI)
    return int(contract.functions.balanceOf(account.address).call())

def addAllowance(account, item, nonce):
    contract = w3.eth.contract(address= items[item], abi=ERC20ABI)
    tx = contract.functions.approve(RouterAddress, 115792089237316195423570985008687907853269984665640564039457584007913129639935).build_transaction({
        "from": account.address,
        "nonce": nonce
    })
    gas = int(w3.eth.estimate_gas(tx))
    tx["gas"] = gas
    tx["maxFeePerGas"] = w3.toWei(50, 'gwei')
    tx["maxPriorityFeePerGas"] = w3.toWei(2, "gwei")
    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    hash = w3.toHex(hash)
    w3.eth.wait_for_transaction_receipt(hash)

def sellRewards():
    for user in get_accounts():
        account = get_account(user, w3)
        nonce = w3.eth.get_transaction_count(account.address)
        print("")
        print(user)
        for item in sellables:
            decimals = 0
            amount = getItemAmount(account, item)
            if item in decimals_data:
                decimals = decimals_data[item]
            print(f"{item}: {amount/10**decimals}")
            if checkAllowance(account, item, RouterAddress, ERC20ABI, w3):
                try:
                    addAllowance(account, item, nonce)
                    nonce+=1
                    print(f"Added allowance to {item}")
                except Exception as error:
                    print(f"Error adding allowance to {item}")
                    print(error)

            if amount != 0:
                try:
                    sellItem(account, item, amount, nonce)
                    nonce+=1
                    print(f"Sold {item}")
                except Exception as error:
                    print(f"Error selling {item}")
                    print(error)
            else:
                pass
        

sellRewards()
