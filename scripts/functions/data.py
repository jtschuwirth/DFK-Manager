from cryptography.fernet import Fernet
import os
import boto3
from dotenv import load_dotenv
load_dotenv()

manager_account = "0xa691623968855b91A066661b0552a7D3764c9a64"

f = Fernet(os.environ.get('key').encode())
def init_account_table():
    my_session = boto3.session.Session(
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_KEY"),
            region_name = "us-east-1",
        )

    return my_session.resource('dynamodb').Table("dfk-autoplayer-accounts")

def init_payouts_table():
    my_session = boto3.session.Session(
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_KEY"),
            region_name = "us-east-1",
        )

    return my_session.resource('dynamodb').Table("dfk-autoplayer-payouts")

def get_accounts(manager_account):
    account_table = init_account_table()
    accounts = []
    scan_response = account_table.scan(
            FilterExpression="enabled_manager = :enabled AND pay_to = :pay_to",
            ExpressionAttributeValues={
                ":enabled": True,
                ":pay_to": manager_account
            })
    for item in scan_response["Items"]:
        accounts.append(item["address_"])
    return accounts

def init_settings_table():
    my_session = boto3.session.Session(
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_KEY"),
            region_name = "us-east-1",
        )

    return my_session.resource('dynamodb').Table("dfk-autoplayer")



network = "dfk"
chainId= 53935
gas_buffer = 10
