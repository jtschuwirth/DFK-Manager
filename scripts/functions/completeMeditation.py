import json

meditationCircleAddress = "0xD507b6b299d9FC835a0Df92f718920D13fA49B47"
meditationCircleJson = open("abi/MeditationCircle.json")
meditationCircleABI = json.load(meditationCircleJson)


def completeMeditation(heroId, account, nonce,  w3):
    meditationCircleContract = w3.eth.contract(address=meditationCircleAddress, abi=meditationCircleABI)
    tx = meditationCircleContract.functions.completeMeditation(int(heroId)).build_transaction({
        "from": account.address,
        "nonce": nonce
    })
    gas = int(w3.eth.estimate_gas(tx)*1.1)
    tx["gas"] = gas
    tx["maxFeePerGas"] = w3.toWei(50, 'gwei')
    tx["maxPriorityFeePerGas"] = w3.toWei(2, "gwei")
    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    hash = w3.toHex(hash)
    w3.eth.wait_for_transaction_receipt(hash)

def completeAllMeditations(heroesIds, account, nonce,  w3):
    meditationCircleContract = w3.eth.contract(address=meditationCircleAddress, abi=meditationCircleABI)
    tx = meditationCircleContract.functions.completeMeditations(heroesIds).build_transaction({
        "from": account.address,
        "nonce": nonce
    })
    gas = int(w3.eth.estimate_gas(tx)*1.1)
    tx["gas"] = gas
    tx["maxFeePerGas"] = w3.toWei(50, 'gwei')
    tx["maxPriorityFeePerGas"] = w3.toWei(2, "gwei")
    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    hash = w3.toHex(hash)
    w3.eth.wait_for_transaction_receipt(hash)