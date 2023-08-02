from functions.getItemPriceJewel import getItemPriceJewel, getCrystalPriceJewel
from functions.provider import get_provider
from functions.data import network, init_payouts_table, init_account_table, init_tracking_table
from datetime import datetime
import time

w3 = get_provider(network)

#General
miners_per_account = 18
heros_per_quest = 6
daily_avg_gas_cost = 0.6

#Mining
miner_avg_cost = 40 #Crystal
avg_gold = 65 #per quest
tear_drop_rate = 0.1125 #per try
shvas_drop_rate = 0.015 #per try
moksha_drop_rate = 0.00045 #per try
egg_drop_rate = 0.0004 #per quest
quest_per_day = 1.84615
loot_slots = 5
jewel_value = 0.140039

def printStats():
    print("Prices")	
    crystal_value = getCrystalPriceJewel(w3) 
    tear_value = getItemPriceJewel("Gaias Tears", w3)
    gold_value = getItemPriceJewel("DFKGold", w3)
    shvas_value = getItemPriceJewel("Shvas Rune", w3)
    moksha_value = getItemPriceJewel("Moksha Rune", w3)
    egg_value = getItemPriceJewel("Yellow Pet Egg", w3)

    tracking_table = init_tracking_table()
    buys = tracking_table.scan()["Items"]
    buys.sort(key=lambda x: int(x["time_"]), reverse=True)
    timeframe = int(time.time())-int(buys[-1]["time_"])
    total_expenditure = 0
    buy_per_day = {}
    buy_per_hour = {}
    for buy in buys:
        total_expenditure += float(buy["price"])
        datetime.fromtimestamp(int(buy["time_"]))
        if datetime.fromtimestamp(int(buy["time_"])).strftime("%Y-%m-%d") in buy_per_day:
            buy_per_day[datetime.fromtimestamp(int(buy["time_"])).strftime("%Y-%m-%d")] += 1
        else:
            buy_per_day[datetime.fromtimestamp(int(buy["time_"])).strftime("%Y-%m-%d")] = 1
        if datetime.fromtimestamp(int(buy["time_"])).strftime("%H") in buy_per_hour:
            buy_per_hour[datetime.fromtimestamp(int(buy["time_"])).strftime("%H")] += 1
        else:
            buy_per_hour[datetime.fromtimestamp(int(buy["time_"])).strftime("%H")] = 1
    avg_daily_expenditure = total_expenditure/(timeframe/86400)
    print(f"Average heros bought per day: {str(len(buys)/(timeframe/86400))}")
    avg_expenditure = total_expenditure/len(buys)
    print(f"Average hero cost: {str(avg_expenditure*crystal_value)} jewel")

    accounts_table = init_account_table()
    payouts_table = init_payouts_table()
    payouts_list = payouts_table.scan()["Items"]
    accounts_list = accounts_table.scan(
        FilterExpression="pay_to = :pay_to",
            ExpressionAttributeValues={
                ":pay_to": "0xa691623968855b91A066661b0552a7D3764c9a64"
            }
    )["Items"]
    total_earnings = 0 
    total_time_delta = 0
    no_stats = 0
    for payout in payouts_list:
        if int(payout["time_delta"]) == 0:
            no_stats += 1
            continue
        total_earnings += float(payout["amount_"])
        total_time_delta += int(payout["time_delta"])
    avg_earnings = total_earnings/(len(payouts_list)-no_stats)
    avg_time_delta = total_time_delta/(len(payouts_list)-no_stats)
    avg_daily_earnings = avg_earnings/avg_time_delta*24*60*60
    print(f"total accounts: {len(accounts_list)}")
    print(f"total payments: {len(payouts_list)-no_stats}")
    print(f"Avg real daily earnings per account: {avg_daily_earnings}")
    print(f"Total payout in last round: {total_earnings} Jewel ({round(avg_time_delta/(24*60*60), 2)} days)")
    print(f"total payout per day: {total_earnings/avg_time_delta*24*60*60} Jewel")
    print("")
    accounts = len(accounts_list)
        

    print(f"jewel: {jewel_value} USD")
    print(f"tear: {tear_value} jewel")
    print(f"gold: {gold_value} jewel")
    print(f"shvas: {shvas_value} jewel")
    print(f"moksha: {moksha_value} jewel")
    print(f"egg: {egg_value} jewel")
    print(f"crystal: {crystal_value} jewel")

    print("")
    print("Individual Raw Income")
    daily_gold = quest_per_day*avg_gold
    daily_gold_value = daily_gold*gold_value

    daily_tears = quest_per_day*loot_slots*tear_drop_rate
    daily_tears_value = daily_tears*tear_value

    daily_shvas = quest_per_day*loot_slots*shvas_drop_rate
    daily_shvas_value = daily_shvas*shvas_value

    daily_moksha = quest_per_day*loot_slots*moksha_drop_rate
    daily_moksha_value = daily_moksha*moksha_value

    daily_egg = quest_per_day*egg_drop_rate
    daily_egg_value = daily_egg*egg_value

    daily_income = daily_gold_value + daily_tears_value + daily_moksha_value + daily_shvas_value + daily_egg_value
    print(f"1d: {daily_income} Jewel = {daily_gold} GOLD / {daily_tears} Tears / {daily_shvas} Shvas / {daily_moksha} Moksha / {daily_egg} Yellow Egg")
    print(f"7d: {daily_income*7} Jewel = {daily_gold*7} GOLD / {daily_tears*7} Tears / {daily_shvas*7} Shvas / {daily_moksha*7} Moksha / {daily_egg*7} Yellow Egg")
    print(f"30d: {daily_income*30} Jewel = {daily_gold*30} GOLD / {daily_tears*30} Tears / {daily_shvas*30} Shvas / {daily_moksha*30} Moksha / {daily_egg*30} Yellow Egg")

    print("")
    print("Rewards value ratio")
    print(f"gold: {round(daily_gold_value/daily_income, 4)*100}%")
    print(f"tears: {round(daily_tears_value/daily_income, 4)*100}%")
    print(f"Shvas: {round(daily_shvas_value/daily_income, 4)*100}%")
    print(f"Moksha: {round(daily_moksha_value/daily_income, 4)*100}%")
    print(f"Yellow Egg: {round(daily_egg_value/daily_income, 4)*100}%")

    print("")
    print("Account Raw Income")
    account_daily_income = daily_income*miners_per_account
    account_daily_gold = daily_gold*miners_per_account
    account_daily_tears = daily_tears*miners_per_account
    account_daily_shvas = daily_shvas*miners_per_account
    account_daily_moksha = daily_moksha*miners_per_account
    account_daily_egg = daily_egg*miners_per_account


    print(f"1d: {account_daily_income} Jewel = {account_daily_gold} GOLD / {account_daily_tears} Tears / {account_daily_shvas} Shvas / {account_daily_moksha} Moksha / {account_daily_egg} Yellow Egg")
    print(f"7d: {account_daily_income*7} Jewel = {account_daily_gold*7} GOLD / {account_daily_tears*7} Tears / {account_daily_shvas*7} Shvas / {account_daily_moksha*7} Moksha / {account_daily_egg*7} Yellow Egg")
    print(f"30d: {account_daily_income*30} Jewel = {account_daily_gold*30} GOLD / {account_daily_tears*30} Tears / {account_daily_shvas*30} Shvas / {account_daily_moksha*30} Moksha / {account_daily_egg*30} Yellow Egg")

    print("")
    print("Account Gas Cost")
    account_daily_gas_cost = daily_avg_gas_cost
    print(f"1d: {account_daily_gas_cost} Jewel")
    print(f"7d: {account_daily_gas_cost*7} Jewel")
    print(f"30d: {account_daily_gas_cost*30} Jewel")

    print("")
    print("Account Earnings")
    account_daily_earnings = account_daily_income - daily_avg_gas_cost
    print(f"1d: {account_daily_earnings} Jewel")
    print(f"3d: {account_daily_earnings*3} Jewel")
    print(f"7d: {account_daily_earnings*7} Jewel")
    print(f"30d: {account_daily_earnings*30} Jewel")

    print("")
    print("Total Earnings")
    total_daily_earnings = account_daily_earnings*accounts
    print(f"1d: {total_daily_earnings} Jewel")
    print(f"3d: {total_daily_earnings*3} Jewel")
    print(f"7d: {total_daily_earnings*7} Jewel")
    print(f"30d: {total_daily_earnings*30} Jewel")

    print("")
    print("Total USD earnings")
    print(f"1d: {total_daily_earnings*jewel_value} USD")
    print(f"7d: {total_daily_earnings*7*jewel_value} USD")
    print(f"30d: {total_daily_earnings*30*jewel_value} USD")

    #Account Creation Price
    print("")
    print("Account Creation Price")
    print("Account cost")
    account_cost_jewel = avg_expenditure*crystal_value*miners_per_account + 5
    account_cost_usd = account_cost_jewel*jewel_value
    print(f"{account_cost_jewel} Jewel")
    print(f"{account_cost_usd} USD")

    print("")
    print("Inversion reimburse time")
    print(f"{account_cost_jewel/account_daily_earnings} days")

    print("")
    print("Amount invested")
    print(f"{account_cost_jewel*accounts} Jewel")
    print(f"{account_cost_jewel*accounts*jewel_value} USD")

    #Stats
    print("")
    print("Stats")
    initial_inversion = account_cost_jewel
    yearly_earnings = account_daily_earnings*365
    print("Yearly Returns")
    print(f"{round(yearly_earnings/initial_inversion*100)}%")

    print("")
    current_avg_daily_earnings = account_daily_earnings*len(accounts_list)
    print(f"Current Accounts: {len(accounts_list)}")
    print(f"Current Avg Daily Earnings: {str(current_avg_daily_earnings)} Jewel")
    print(f"Average expenditure per day: {str(avg_daily_expenditure*crystal_value)} jewel" )
    print(f"Avg delta: {str(current_avg_daily_earnings - avg_daily_expenditure*crystal_value)} jewel" )

printStats()