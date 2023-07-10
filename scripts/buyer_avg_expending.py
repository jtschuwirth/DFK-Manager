from functions.data import init_tracking_table
from functions.getItemPriceJewel import getCrystalPriceJewel
from functions.provider import get_provider

w3 = get_provider("dfk")

def buyer_avg_expending():
    crystal_value = getCrystalPriceJewel(w3)
    tracking_table = init_tracking_table()
    buys = tracking_table.scan()["Items"]
    buys.sort(key=lambda x: int(x["time_"]))
    timeframe = int(buys[-1]["time_"])-int(buys[0]["time_"])
    total_expenditure = 0
    for buy in buys:
        total_expenditure += float(buy["price"])
    avg_expenditure = total_expenditure/len(buys)
    avg_daily_expenditure = avg_expenditure/(timeframe/86400)
    print(f"Average expenditure per day: {str(avg_daily_expenditure)} crystal / {str(avg_daily_expenditure*crystal_value)} jewel" )
    print(f"Average hero cost: {str(avg_expenditure)} crystal / {str(avg_expenditure*crystal_value)} jewel")
    print(f"Total expenditure: {str(total_expenditure)} crystal / {str(total_expenditure*crystal_value)} jewel")
    print(f"total heros bought: {str(len(buys))}")

    
buyer_avg_expending()