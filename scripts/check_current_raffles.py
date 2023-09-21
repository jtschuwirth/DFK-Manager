from functions.provider import get_provider
import json
from functions.getItemPriceJewel import getItemPriceJewelByAddress
from functions.data import init_raffles_table
from functions.ticket_cost import ticketCost

raffleMasterAddress = "0xd8D7CE8921490b75EC489bd076AD0f27DC765675"
raffleMasterJson = open("abi/RaffleMaster.json")
raffleMasterABI = json.load(raffleMasterJson)


w3 = get_provider("dfk")

contract = w3.eth.contract(address= raffleMasterAddress, abi=raffleMasterABI)
def checkCurrentRaffles():
    raffles = contract.functions.getCurrentRaffleData().call()
    raffles_table = init_raffles_table()
    t = ticketCost(0.5)
    print(f"Ticket cost: {t}")
    print("Current raffles:")
    for index in range(len(raffles[0])):
        if raffles[0][index][0] == 0: continue
        prize_price = 0
        duration = raffles[1][index][4]
        for prize_index in range(len(raffles[1][index][1])):
            prize_price += getItemPriceJewelByAddress(raffles[1][index][1][prize_index], w3) * raffles[1][index][2][prize_index]
        print(f"id {raffles[0][index][0]}, tickets: {raffles[0][index][3]}, winners {len(raffles[0][index][6])}, rewards {raffles[1][index][1]} x {raffles[1][index][2]} x {raffles[1][index][3]}, reward price: {prize_price}, duration: {duration}")
        scan_response=  raffles_table.scan(
                FilterExpression="rewards = :rewards AND rewards_amount = :amount",
                ExpressionAttributeValues={
                    ":rewards": str(raffles[1][index][1]),
                    ":amount": str(raffles[1][index][2])
                })
        if len(scan_response["Items"]) == 0: 
            print("raffle data not found")
            print("")
            continue
        
        cumulative = 0
        count = 0
        cumulative_optimal_tickets = 0
        for raffle in scan_response["Items"]:
            jewel_per_ticket = float(raffle['rewards_price'])*float(raffle['winners'])/float(raffle['tickets'])

            tickets = float(raffle['tickets'])
            price = float(raffle["rewards_price"])

            optimal_tickets = - tickets + ((price*tickets)/t)**(1/2)
            if duration == 1200:
                max_tickets = 380
                if optimal_tickets > max_tickets: optimal_tickets = max_tickets
            if (optimal_tickets < 0): continue
            win_chance = optimal_tickets/(tickets+optimal_tickets)
            expected_profit_per_ticket = (price * win_chance)/tickets - t
            cumulative += expected_profit_per_ticket
            cumulative_optimal_tickets += optimal_tickets
            count += 1
        if count == 0: 
            print("raffle data not found")
            print("")
            continue
        profit_per_ticket = cumulative/count
        optimal_tickets = round(cumulative_optimal_tickets/count)
        expected_return = profit_per_ticket * optimal_tickets
        print(f"Optimal tokens to bid: {optimal_tickets}")
        print(f"Profit per ticket: {profit_per_ticket}")
        print("")
        

if __name__ == "__main__":
    checkCurrentRaffles()