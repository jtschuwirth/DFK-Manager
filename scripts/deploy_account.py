from functions.data import network, init_settings_table
from functions.create_eth_address import createETHAddress
from functions.save_encryption import saveEncryption
from functions.utils import getJewelBalance
from functions.provider import get_account, get_provider
from functions.utils import fillGas, sendCrystal, heroNumber, getCrystalBalance
from functions.getMarketHeros import getMarketHeros
from functions.buy_account_heros import buyHeros
from functions.send_heros import sendHeros
import time

from functions.getItemPriceJewel import getCrystalPriceJewel
from functions.utils import buyCrystal

w3 = get_provider(network)

manager_address = "0xa691623968855b91A066661b0552a7D3764c9a64"
setup_address = "0xa691623968855b91A066661b0552a7D3764c9a64"
warehouse_address = "0x867df63D1eEAEF93984250f78B4bd83C70652dcE"


def deployAccount(manager_address, setup_address, warehouse_address):
    jewel_loss = 0
    crystal_loss = 0
    settings_table = init_settings_table()
    last_account_address = settings_table.get_item(Key={"key_": "deployer_settings"})["Item"]["last_account"]
    last_account = get_account(last_account_address, w3)
    last_acc_jewel_balance = getJewelBalance(last_account, w3)
    last_acc_hero_number = heroNumber(last_account, w3)
    if 18 <= last_acc_hero_number and last_acc_jewel_balance != 0:
        print("Last account has 18 heros and jewel balance")
        print("creating new account")
        new_account = createETHAddress()
        saveEncryption(new_account["address"], new_account["private_key"], manager_address)
        account = get_account(new_account["address"], w3)
        account_nonce = w3.eth.get_transaction_count(account.address)
        print(f"New account created: {new_account['address']}")
        settings_table.update_item(
                Key={"key_": "deployer_settings"},
                UpdateExpression="SET last_account = :account",
                ExpressionAttributeValues={":account": new_account["address"]}
        )
    else:
        account = last_account
        account_nonce = w3.eth.get_transaction_count(account.address)
    setup = get_account(setup_address, w3)
    setup_nonce = w3.eth.get_transaction_count(setup.address)
    warehouse = get_account(warehouse_address, w3)
    warehouse_nonce = w3.eth.get_transaction_count(warehouse.address)

    hero_number = heroNumber(account, w3)
    jewel_balance = getJewelBalance(account, w3)
    print(f"Account has {hero_number} heros")
    print(f"Account has {jewel_balance} jewel")

    if 18 <= hero_number and jewel_balance != 0:
        print("Account is already deployed")
        print (f"Account setup cost, jewel {jewel_loss}, crystal {crystal_loss}")
        return
    if jewel_balance == 0:
        fill_gas_bool = input("Account has no jewel, fill gas? (y/n)")
        if fill_gas_bool == "y":
            print("Adding Gas")
            gas_fill_amount = 10
            fillGas(account, setup, gas_fill_amount*10**18, setup_nonce, w3)
            jewel_loss += gas_fill_amount
            setup_nonce+=1
            print(f"Filled gas to account {account.address}")
    

    warehouse_heros = heroNumber(warehouse, w3)
    while 0 < warehouse_heros and 18 > hero_number:
        warehouse_bool = input(f"Get heros from warehouse ({warehouse_heros})? (y/n)")
        if warehouse_bool == "y":
            amount = min(18-hero_number, warehouse_heros)
            print("Getting heros from warehouse")
            sendHeros(account, warehouse, amount, warehouse_nonce, w3)
            print("Waiting for transactions to go through")
            time.sleep(1)
            warehouse_heros = heroNumber(warehouse, w3)
            hero_number = heroNumber(account, w3)
            print(f"Account has {hero_number} heros")
            if 0 < warehouse_heros and 18 > hero_number:
                continue
        else:
            print("Continue without warehouse heros")
            break
        
        hero_number = heroNumber(account, w3)
        print(f"Account has {hero_number} heros")
        jewel_balance = getJewelBalance(account, w3)
        print(f"Account has {jewel_balance} jewel")
        if 18 <= hero_number:
            print("Account already has 18 heros")
            print (f"Account setup cost, jewel {jewel_loss}, crystal {crystal_loss}")
            return
        break
    
    print("Getting Market Data")
    heros = getMarketHeros(18-hero_number)
    crystal_value = getCrystalPriceJewel(w3) 
    total_cost = 0
    for hero in heros:
        total_cost+=hero["price"]
    avg_cost = total_cost/10**18/len(heros)
    print(f"Missing heros {18-hero_number}")
    print(f"heros cost: {total_cost/10**18} crystal / {(total_cost/10**18)*crystal_value} jewel")
    print(f"avg cost: {avg_cost} crystal / {avg_cost*crystal_value} jewel")
    buy_bool = input("Continue buying heros? (y/n)")
    if buy_bool == "y":
        jewel_balance = getJewelBalance(account, w3)
        if (jewel_balance == 0):
            print("Adding Gas")
            gas_fill_amount = 10
            fillGas(account, setup, gas_fill_amount*10**18, setup_nonce, w3)
            jewel_loss += gas_fill_amount
            print(f"Filled gas to account {account.address}")
            setup_nonce+=1
        else:
            print(f"Account {account.address} already has gas")
        
        crystal_balance = getCrystalBalance(account, w3)
        if crystal_balance < total_cost:
            needed_crystal = total_cost-crystal_balance
            print(f"Buying {(total_cost-crystal_balance)/10**18} crystal")
            buyCrystal(setup, needed_crystal, int(needed_crystal*crystal_value*1.05), setup_nonce, w3)
            setup_nonce+=1
            print(f"Sending {needed_crystal/10**18} crystal")
            sendCrystal(account, setup, needed_crystal, setup_nonce, w3)
            setup_nonce+=1
            print(f"Sent {needed_crystal/10**18} crystal to account {account.address}")
            crystal_loss += needed_crystal/10**18

        print("Preparing to buy heros")
        buyHeros(account, account_nonce, w3)
    else:
        print("Continue without buying heros")
    print("Done")
    print(f"Account setup cost, jewel {jewel_loss}, crystal {crystal_loss}")
    





deployAccount(manager_address, setup_address, warehouse_address)