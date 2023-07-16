from functions.data import init_tracking_table
from functions.getItemPriceJewel import getCrystalPriceJewel
from functions.provider import get_provider
import time
from datetime import datetime
import matplotlib.pyplot as plt

w3 = get_provider("dfk")

def buyer_avg_expending():
    crystal_value = getCrystalPriceJewel(w3)
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
    plt.bar(buy_per_day.keys(), buy_per_day.values(), color='g')
    plt.show()
    plt.bar(buy_per_hour.keys(), buy_per_hour.values(), color='b')
    plt.show()
    avg_expenditure = total_expenditure/len(buys)
    avg_daily_expenditure = total_expenditure/(timeframe/86400)
    print(f"Average heros bought per day: {str(len(buys)/(timeframe/86400))}")
    print(f"Average expenditure per day: {str(avg_daily_expenditure)} crystal / {str(avg_daily_expenditure*crystal_value)} jewel" )
    print(f"Average hero cost: {str(avg_expenditure)} crystal / {str(avg_expenditure*crystal_value)} jewel")
    print(f"total heros bought: {str(len(buys))}")
    print(f"Total expenditure: {str(total_expenditure)} crystal / {str(total_expenditure*crystal_value)} jewel")
    print(f"last hero bought {datetime.fromtimestamp(int(buys[0]['time_']))} for {buys[0]['price']} crystal / {float(buys[0]['price'])*crystal_value} jewel")

    
buyer_avg_expending()