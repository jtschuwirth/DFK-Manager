from functions.data import init_raffles_table
from functions.ticket_cost import ticketCost


def checkRaffleData():
    raffles_table = init_raffles_table()
    raffles = raffles_table.scan()
    raffle_rewards = {}
    t = ticketCost(0.5)
    print(f"Ticket cost: {t}")
    for raffle in raffles['Items']:
        print(raffle)
        jewel_per_ticket = float(raffle['rewards_price'])*float(raffle['winners'])/float(raffle['tickets'])

        tickets = float(raffle['tickets'])
        price = float(raffle["rewards_price"])

        optimal_tickets = - tickets + ((price*tickets)/t)**(1/2)
        max_tickets = 380
        if optimal_tickets > max_tickets: optimal_tickets = max_tickets
        if (optimal_tickets < 0): continue
        print(f"jewel per ticket: {jewel_per_ticket}")
        print(f"optimal tickets: {optimal_tickets}")
        win_chance = optimal_tickets/(tickets+optimal_tickets)
        expected_profit_per_ticket = (price * win_chance)/tickets - t
        if str(raffle['rewards'])+str(raffle['rewards_amount']) not in raffle_rewards:
            raffle_rewards[str(raffle['rewards'])+str(raffle['rewards_amount'])] = {"cumulative": 0, "count": 0, "optimal_tickets": 0}
        raffle_rewards[str(raffle['rewards'])+str(raffle['rewards_amount'])]["cumulative"] += expected_profit_per_ticket
        raffle_rewards[str(raffle['rewards'])+str(raffle['rewards_amount'])]["optimal_tickets"] += optimal_tickets
        raffle_rewards[str(raffle['rewards'])+str(raffle['rewards_amount'])]["count"] += 1
        print("")
        print(f"win chance: {win_chance*100}")
        print(f"expected return: {price * win_chance}")
        print(f"expected return per ticket: {expected_profit_per_ticket}")
        print("")
        print("")
    
    #Sort raffle rewards by cumulative jewel per ticket / count

    raffle_rewards = {k: v for k, v in sorted(raffle_rewards.items(), key=lambda item: item[1]["cumulative"]/item[1]["count"], reverse=True)}
    print("")
    print("")
    for reward in raffle_rewards:
        profit_per_ticket = raffle_rewards[reward]["cumulative"]/raffle_rewards[reward]["count"]
        optimal_tickets = round(raffle_rewards[reward]["optimal_tickets"]/raffle_rewards[reward]["count"])
        expected_return = profit_per_ticket * optimal_tickets
        print(f"{reward}, profit per ticket: {profit_per_ticket}, optimal tickets: {optimal_tickets} expected return: {expected_return}, data entries: {raffle_rewards[reward]['count']}")

if __name__ == "__main__":
    checkRaffleData()