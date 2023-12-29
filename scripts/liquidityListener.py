import json
from functions.provider import get_provider, get_account

w3 = get_provider("dfk")

RouterAddress = "0x3C351E1afdd1b1BC44e931E12D4E05D6125eaeCa"
RouterJson = open("abi/UniswapV2Router02.json")
RouterABI = json.load(RouterJson)

PairJson = open("abi/UniswapPair.json")
PairABI = json.load(PairJson)

itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)

decimalsJson = open("items_data/decimals.json")
decimals_data = json.load(decimalsJson)

ERC20Json = open("abi/ERC20.json")
ERC20ABI = json.load(ERC20Json)

pairsJson = open("items_data/pairs.json")
pairs = json.load(pairsJson)

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

def listener():
    crystal_tears_pair_address = pairs["Crystal"]["Gaias Tears"]
    PairContract = w3.eth.contract(address=crystal_tears_pair_address, abi=PairABI)
    event_filter = PairContract.events.Sync.createFilter(fromBlock="latest")
    print("Starting Listener ...")
    #while time.time() - start < timeout:
    print(checkLiquidityPrice("Gaias Tears"))
    while True:
        new_entries = event_filter.get_new_entries()
        if new_entries != []:
            print(checkLiquidityPrice("Gaias Tears"))

listener()
