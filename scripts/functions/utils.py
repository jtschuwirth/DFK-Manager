import json
from functions.data import chainId 

itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)

decimalsJson = open("items_data/decimals.json")
decimals_data = json.load(decimalsJson)

ERC20Json = open("abi/ERC20.json")
ERC20ABI = json.load(ERC20Json)

ERC721Json = open("abi/ERC721.json")
ERC721ABI = json.load(ERC721Json)

def getJewelBalance(account, w3):
    return int(w3.eth.get_balance(account.address))

def getCrystalBalance(account, w3):
    contract = w3.eth.contract(address= items["Crystal"], abi=ERC20ABI)
    return int(contract.functions.balanceOf(account.address).call())

def checkAllowance(account, item, abi, w3):
    contract = w3.eth.contract(address= items[item], abi=abi)
    if int(contract.functions.allowance(account.address, items[item]).call()) == 0:
        return True
    else: 
        return False

def addAllowance(account, item, nonce, abi, w3):
    contract = w3.eth.contract(address= items[item], abi=abi)
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
    w3.eth.wait_for_transaction_receipt(hash)

def heroNumber(account, w3):
    contract = w3.eth.contract(address= items["Heroes"], abi=ERC721ABI)
    return int(contract.functions.balanceOf(account.address).call())

def fillGas(account, manager, amount, nonce, w3):
    tx = {
        "from": manager.address,
        "to": account.address,
        "value": amount,
        "nonce": nonce,
        "chainId": chainId
    }
    gas = w3.eth.estimate_gas(tx)
    tx["gas"] = gas
    tx["gasPrice"] = w3.toWei(50, 'gwei')
    signed_tx = w3.eth.account.sign_transaction(tx, manager.key)
    hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    hash = w3.toHex(hash)
    w3.eth.wait_for_transaction_receipt(hash)

def sendCrystal(account, manager, amount, nonce, w3):
    itemContract = w3.eth.contract(address=items["Crystal"], abi=ERC20ABI)
    tx = itemContract.functions.transfer(
        account.address,
        amount,
    ).build_transaction({
        "from": manager.address,
        "nonce": nonce,
    })
    tx["gas"] = int(w3.eth.estimate_gas(tx))
    tx["maxFeePerGas"] = w3.toWei(50, 'gwei')
    tx["maxPriorityFeePerGas"] = w3.toWei(2, "gwei")
    signed_tx = w3.eth.account.sign_transaction(tx, manager.key)
    hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    hash = w3.toHex(hash)
    w3.eth.wait_for_transaction_receipt(hash)
