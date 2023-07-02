from functions.data import network
from functions.create_eth_address import createETHAddress
from functions.save_encryption import saveEncryption
from functions.utils import getJewelBalance
from functions.provider import get_account, get_provider
from functions.utils import fillGas, sendCrystal, heroNumber, getCrystalBalance
from functions.get_market_heros import getMarketHeros
from functions.buy_account_heros import buyHeros

w3 = get_provider(network)

manager_address = "0xa691623968855b91A066661b0552a7D3764c9a64"
setup_address = "0xa691623968855b91A066661b0552a7D3764c9a64"
address = ""

def deployAccount(manager_address, setup_address ,address=""):
    jewel_loss = 0
    crystal_loss = 0
    if address == "":
        new_account = createETHAddress()
        saveEncryption(new_account["address"], new_account["private_key"], manager_address)
        account = get_account(new_account["address"], w3)
        account_nonce = w3.eth.get_transaction_count(account.address)
    else:
        account = get_account(address, w3)
        account_nonce = w3.eth.get_transaction_count(account.address)
    setup = get_account(setup_address, w3)
    setup_nonce = w3.eth.get_transaction_count(setup.address)
    jewel_balance = getJewelBalance(account, w3)
    if (jewel_balance == 0):
        gas_fill_amount = 5
        fillGas(account, setup, gas_fill_amount*10**18, setup_nonce, w3)
        jewel_loss += gas_fill_amount
        print(f"Filled gas to account {account.address}")
        setup_nonce+=1
    else:
        print(f"Account {account.address} already has gas")
    hero_number = heroNumber(account, w3)
    if hero_number == 18:
        print("Account is already deployed")
        print (f"Account setup cost, jewel {jewel_loss}, crystal {crystal_loss}")
        return
    print("Getting hero prices")
    heros = getMarketHeros(18-hero_number)
    total_cost = 0
    for hero in heros:
        total_cost+=hero["price"]
    avg_cost = total_cost/10**18/len(heros)
    print(f"Missing heros {18-hero_number}")
    print(f"heros cost: {total_cost/10**18}")
    print(f"avg cost: {avg_cost}")
    buy_bool = input("Continue buying heros? (y/n)")
    if buy_bool == "y":
        crystal_balance = getCrystalBalance(account, w3)
        if crystal_balance < total_cost:
            print(f"Sending {(total_cost-crystal_balance)/10**18} crystal")
            sendCrystal(account, setup, total_cost-crystal_balance, setup_nonce, w3)
            setup_nonce+=1
            print(f"Sent {(total_cost-crystal_balance)/10**18} crystal to account {account.address}")
            crystal_loss += (total_cost-crystal_balance)/10**18

        print("Preparing to buy heros")
        buyHeros(account, account_nonce, 18-hero_number, w3)
    else:
        print("Exiting")
        print (f"account {account.address} left unfinished")
        print(f"Account setup cost, jewel {jewel_loss}")
        return
    print("Done")
    print(f"Account setup cost, jewel {jewel_loss}, crystal {crystal_loss}")
    





deployAccount(manager_address, setup_address, address)