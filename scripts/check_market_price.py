from functions.getMarketHeros import getMarketHeros


total_cost = 0
heros = getMarketHeros(18)
for hero in heros:
    total_cost+=hero["price"]/10**18
avg_cost = total_cost/len(heros)
print(f"total cost: {total_cost} Crystal")
print(f"avg cost: {avg_cost}")
print(f"heros: {len(heros)}")


     