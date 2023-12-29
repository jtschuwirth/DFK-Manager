import json
from functions.provider import get_provider, get_account

w3 = get_provider("dfk")

RouterAddress = "0x3C351E1afdd1b1BC44e931E12D4E05D6125eaeCa"
RouterJson = open("abi/UniswapV2Router02.json")
RouterABI = json.load(RouterJson)

BazaarAddress = "0x902F2b740bC158e16170d57528405d7f2a793Ca2"
BazaarJson = open("abi/Bazaar.json")
BazaarABI = json.load(BazaarJson)

itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)

decimalsJson = open("items_data/decimals.json")
decimals_data = json.load(decimalsJson)

ERC20Json = open("abi/ERC20.json")
ERC20ABI = json.load(ERC20Json)

bazaarFee = 0.015

def checkLiquidityPrice(item):
    decimals = 0
    if item in decimals_data:
        decimals = decimals_data[item]
    RouterContract = w3.eth.contract(address=RouterAddress, abi=RouterABI)
    amountsIn = RouterContract.functions.getAmountsIn(
        1*(10**decimals),
        [items["Jewel"], items["Crystal"], items[item]]
    ).call()
    jewel_price = amountsIn[0] / 10**18
    return jewel_price

def checkBazaarPrice(item):
    decimals = 0
    if item in decimals_data:
        decimals = decimals_data[item]
    BazaarContract = w3.eth.contract(address=BazaarAddress, abi=BazaarABI)
    bestBuyOrder = BazaarContract.functions.getBestOrder(
        items[item],
        0,
        0
    ).call()

    bestSellOrder = BazaarContract.functions.getBestOrder(
        items[item],
        0,
        1
    ).call()
    return {"bestBuyOrder": bestBuyOrder[6]/(10**18)/(10**12), "bestSellOrder": bestSellOrder[6]/(10**18)/(10**12)}

    

print(checkLiquidityPrice("Gaias Tears"))
print(checkBazaarPrice("Gaias Tears"))