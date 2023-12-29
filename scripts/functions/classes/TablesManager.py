import os
import boto3

class TablesManager:
    def __init__(self, prod) -> None:
        session = boto3.session.Session(
            region_name = "us-east-1",
        )
       
        self.accounts = session.resource('dynamodb').Table("dfk-autoplayer-accounts")
        self.autoplayer = session.resource('dynamodb').Table("dfk-autoplayer")
        self.profit_tracker = session.resource('dynamodb').Table("dfk-profit-tracker")
        self.buyer_tracker = session.resource('dynamodb').Table("dfk-buyer-tracking")
        self.autoplayer_tracker = session.resource('dynamodb').Table("dfk-autoplayer-tracking")
        self.managers = session.resource('dynamodb').Table("dfk-autoplayer-managers")
        self.trades = session.resource('dynamodb').Table("dfk-trading-trades")
        self.active_orders = session.resource('dynamodb').Table("dfk-trading-active-orders")
        


    

