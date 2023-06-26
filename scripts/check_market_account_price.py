from functions.get_market_heros import getMarketHeros


total_cost = 0
heros = getMarketHeros()
for hero in heros:
    total_cost+=hero["price"]/10**18
avg_cost = total_cost/len(heros)
print(f"total cost: {total_cost}")
print(f"avg cost: {avg_cost}")


     