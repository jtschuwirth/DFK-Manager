from cryptography.fernet import Fernet
import os
import boto3
from dotenv import load_dotenv
load_dotenv()

f = Fernet(os.environ.get('key').encode())
def init_account_table():
    my_session = boto3.session.Session(
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_KEY"),
            region_name = "us-east-1",
        )

    return my_session.resource('dynamodb').Table("dfk-autoplayer-accounts")
account_table = init_account_table()

def get_accounts():
    accounts = []
    scan_response = account_table.scan(
            FilterExpression="enabled_manager = :enabled",
            ExpressionAttributeValues={
                ":enabled": True 
            })
    for item in scan_response["Items"]:
        accounts.append(item["address_"])
    return accounts



network = "dfk"
chainId= 53935
gas_buffer = 20
