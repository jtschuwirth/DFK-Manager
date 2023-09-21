from functions.data import get_accounts, network, manager_account, init_account_table
from functions.provider import get_account, get_provider
from functions.utils import checkAllowance, addAllowance, getItemAmount, sendItem
import json

w3 = get_provider(network)

itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)
decimalsJson = open("items_data/decimals.json")
decimals_data = json.load(decimalsJson)

ERC20Json = open("abi/ERC20.json")
ERC20ABI = json.load(ERC20Json)



sellables = [
    #"DFKGold",
    #"Shvas Rune",
    #"Moksha Rune",
    #"Gaias Tears",
    "Yellow Pet Egg",
    "Crystal",

    #"Lesser Might Stone",
    #"Lesser Finesse Stone",
    #"Lesser Swiftness Stone",
    #"Lesser Vigor Stone",
    #"Lesser Fortitude Stone",
    #"Lesser Wit Stone",
    #"Lesser Insight Stone",
    #"Lesser Fortune Stone",
    #"Lesser Chaos Stone",

    #"Might Stone",
    #"Finesse Stone",
    #"Swiftness Stone",
    #"Vigor Stone",
    #"Fortitude Stone",
    #"Wit Stone",
    #"Insight Stone",
    #"Fortune Stone",
    #"Chaos Stone",

    #"Greater Might Stone",
    #"Greater Finesse Stone",
    #"Greater Swiftness Stone",
    #"Greater Vigor Stone",
    #"Greater Fortitude Stone",
    #"Greater Wit Stone",
    #"Greater Insight Stone",
    #"Greater Fortune Stone",
    #"Greater Chaos Stone",

    #"Lesser Might Crystal",
    #"Lesser Finesse Crystal",
    #"Lesser Swiftness Crystal",
    #"Lesser Vigor Crystal",
    #"Lesser Fortitude Crystal",
    #"Lesser Wit Crystal",
    #"Lesser Insight Crystal",
    #"Lesser Fortune Crystal",
    #"Lesser Chaos Crystal",

    #"Might Crystal",
    #"Finesse Crystal",
    #"Swiftness Crystal",
    #"Vigor Crystal",
    #"Fortitude Crystal",
    #"Wit Crystal",
    #"Insight Crystal",
    #"Fortune Crystal",
    #"Chaos Crystal",

    #"Greater Might Crystal",
    #"Greater Finesse Crystal",
    #"Greater Swiftness Crystal",
    #"Greater Vigor Crystal",
    #"Greater Fortitude Crystal",
    #"Greater Wit Crystal",
    #"Greater Insight Crystal",
    #"Greater Fortune Crystal",
    #"Greater Chaos Crystal",

]

def sellRewards():
    accounts = get_accounts(manager_account)
    c=1
    for user in accounts:
        account = get_account(user, w3)
        account_table= init_account_table()
        payout_account = account_table.query(
            KeyConditionExpression="address_ = :address_",
            ExpressionAttributeValues={
                ":address_": account.address,
            })["Items"][0]["pay_to"]
        nonce = w3.eth.get_transaction_count(account.address)
        print("")
        print(f"{user} ({c}/{len(accounts)})")
        c+=1
        for item in sellables:
            itemContract = w3.eth.contract(address=items[item], abi=ERC20ABI)
            decimals = 0
            amount = getItemAmount(account, item, w3)
            if item in decimals_data:
                decimals = decimals_data[item]
            print(f"{item}: {amount/10**decimals}")
            if amount != 0:
                if checkAllowance(account, item, items[item], ERC20ABI, w3):
                    try:
                        addAllowance(account, item, items[item], nonce, ERC20ABI, w3)
                        nonce+=1
                        print(f"Added allowance to {item}")
                    except Exception as error:
                        print(f"Error adding allowance to {item}")
                        print(error)
                try:
                    sendItem(account, itemContract, amount, payout_account, nonce, w3)
                    nonce+=1
                    print(f"Sent {item} to {payout_account}")
                except Exception as error:
                    print(f"Error sending {item}")
                    print(error)
            else:
                pass

sellRewards()
