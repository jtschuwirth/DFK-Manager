from functions.provider import get_provider
import json
from functions.getItemPriceJewel import getItemPriceJewelByAddress
from functions.data import init_raffles_table

raffleMasterAddress = "0xd8D7CE8921490b75EC489bd076AD0f27DC765675"
raffleMasterJson = open("abi/RaffleMaster.json")
raffleMasterABI = json.load(raffleMasterJson)


w3 = get_provider("dfk")

contract = w3.eth.contract(address= raffleMasterAddress, abi=raffleMasterABI)
raffles = contract.functions.getPreviousRaffleData().call()
raffles_table = init_raffles_table()

for index in range(len(raffles[0])):
    if raffles[0][index][0] == 0: continue
    prize_price = 0
    for prize_index in range(len(raffles[1][index][1])):
        prize_price += getItemPriceJewelByAddress(raffles[1][index][1][prize_index], w3) * raffles[1][index][2][prize_index]
        try:
            raffles_table.put_item(Item={
                        'raffleId': str(raffles[0][index][0]),
                        'tickets': str(raffles[0][index][3]),
                        'closed_timestamp': str(raffles[0][index][4]),
                        'rewards': str(raffles[1][index][1]),
                        'rewards_amount': str(raffles[1][index][2]),
                        'winners': str(raffles[1][index][3]),
                        "rewards_price": str(prize_price),
                    })
        except Exception as e:
            print(e)