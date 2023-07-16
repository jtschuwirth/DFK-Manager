from functions.data import init_profit_tracking_table
from datetime import datetime

def lastTrackingResults():
    tracking_table = init_profit_tracking_table()
    track_results = tracking_table.scan()["Items"]
    track_results.sort(key=lambda x: x["time_"], reverse=True)
    print(f"last tracking results:")
    print(f"time {datetime.fromtimestamp(int(track_results[0]['time_']))}")
    print(f"daily avg earnings {track_results[0]['daily_avg_earnings']} jewel")
    print(f"daily avg gas cost {track_results[0]['daily_avg_gas_cost']} jewel")
    print(f"daily expected avg profit {track_results[0]['daily_expected_avg_profit']} jewel")
    print(f"daily real avg profit {track_results[0]['daily_real_avg_profit']} jewel")


lastTrackingResults()
