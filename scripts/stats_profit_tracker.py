from functions.getItemPriceJewel import getCrystalPriceJewel
from functions.classes.RPCProvider import get_rpc_provider
from functions.classes.TablesManager import TablesManager
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

RPCProvider = get_rpc_provider("dfk", [], logger)
tablesManager = TablesManager(False)

def getTotalAccounts():
    accounts = tablesManager.accounts.scan(
        FilterExpression="pay_to = :pay_to",
            ExpressionAttributeValues={
                ":pay_to": "0xa691623968855b91A066661b0552a7D3764c9a64"
            }
    )["Items"]
    return len(accounts)


def getAccountIncome():
    track_results = tablesManager.autoplayer_tracker.scan()["Items"]
    track_results.sort(key=lambda x: x["time_"], reverse=True)
    real_avg_profit = sum(float(track_results[i]['daily_real_avg_profit']) for i in range(7)) / 7
    return float(real_avg_profit)

def getDailyHeroData():
    crystal_value = getCrystalPriceJewel(RPCProvider.w3) 
    buys = tablesManager.buyer_tracker.scan()["Items"]
    buys.sort(key=lambda x: int(x["time_"]), reverse=True)
    timeframe =  24*60*60*7
    buys = list(filter(lambda x: int(x["time_"]) > int(time.time())-timeframe, buys))
    total_expenditure = 0
    total_buys = 0
    for buy in buys:
        total_expenditure += float(buy["price"])
        total_buys += 1

    avg_daily_expenditure = total_expenditure/(timeframe/86400)
    avg_daily_buys = total_buys/(timeframe/86400)
    return {"avg_daily_expenditure_jewel": avg_daily_expenditure*crystal_value, "avg_daily_buys": avg_daily_buys, "avg_daily_expenditure": avg_daily_expenditure}




total_accounts = getTotalAccounts()
account_income = getAccountIncome()
income = total_accounts*account_income

hero_data = getDailyHeroData()
expense = hero_data["avg_daily_expenditure_jewel"]
expense_crystal = hero_data["avg_daily_expenditure"]
buys = hero_data["avg_daily_buys"]
hero_avg_cost = expense/buys
hero_avg_cost_crystal = expense_crystal/buys
account_cost = hero_avg_cost*18


print(f"Total accounts: {total_accounts}")
print(f"Account daily income: {account_income} jewel")
print(f"Daily income: {income} jewel")
print("")
print(f"Daily hero buys: {buys}")
print("")
print(f"avg hero cost: {hero_avg_cost} jewel")
print(f"avg hero cost: {hero_avg_cost_crystal} crystal")
print("")
print(f"Daily expense: {expense} jewel")
print(f"Daily expense: {expense_crystal} crystal")
print("")
print(f"Daily profit: {income-expense} jewel")


accounts_for_break_even = (expense-income)/getAccountIncome()
days_for_break_even = accounts_for_break_even*18/buys
if days_for_break_even < 0: days_for_break_even = 0
if accounts_for_break_even < 0: accounts_for_break_even = 0

jewel_for_break_even = (expense-income)*days_for_break_even
if jewel_for_break_even <= 0: jewel_for_break_even = 0
print("")
print(f"Accounts needed for break even: {accounts_for_break_even}")
print(f"Days for break even: {days_for_break_even}")
print(f"Jewel needed for break even: {jewel_for_break_even}")

print("")
print(f"Account jewel recovery time: {account_cost/account_income} days")
print(f"Account yearly returns: {round((account_income*365/account_cost)*100)}%")
