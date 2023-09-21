from functions.data import get_accounts, network, chainId, init_account_table, init_settings_table, manager_account
from functions.getAccountHeroes import getAccountHeroes
from functions.send_heros import sendHero
from functions.provider import get_account, get_provider
import time

w3 = get_provider(network)
breeder ="0x0206aA6c7537b8f08069605503863E18395C3238"
warehouse = "0x867df63D1eEAEF93984250f78B4bd83C70652dcE"

def heroRebalancer():
    accounts = get_accounts(manager_account)
    wh_account = get_account(warehouse, w3)
    wh_nonce = w3.eth.get_transaction_count(wh_account.address)
    c=1
    print("Rebalancing accounts")
    wh_heroes = getAccountHeroes(wh_account.address, "dfk")
    print(f"Warehouse heroes: {len(wh_heroes)}")
    for user in accounts:
        account = get_account(user, w3)
        nonce = w3.eth.get_transaction_count(account.address)
        heroes = getAccountHeroes(user, "dfk")
        print("")
        print(f"account: {user} ({c}/{len(accounts)}) has {len(heroes)} heroes")
        wh_heroes = getAccountHeroes(wh_account.address, "dfk")
        wh_heroes_amount = len(wh_heroes)
        c+=1
        delta_heroes = len(heroes) - 18
        time.sleep(1)
        if delta_heroes == 0:
            continue
        elif delta_heroes > 0:
            print(f"Removing {delta_heroes} heroes")
            #send excedent heroes to warehouse
            for hero in heroes:
                if delta_heroes == 0:
                    print("Account balanced")
                    break
                try:
                    sendHero(wh_account.address, account, hero['id'], nonce, w3)
                    nonce+=1
                    delta_heroes-=1
                    wh_heroes_amount+=1
                except Exception as error:
                    print("Error sending hero")
                    print(error)
                    print("")
        elif delta_heroes < 0:
            print(f"Adding {abs(delta_heroes)} heroes")
            #get missing heroes from warehouse
            for hero in wh_heroes:
                if delta_heroes == 0:
                    print("Account balanced")
                    break
                elif wh_heroes_amount == 0:
                    print("Warehouse empty")
                    break
                try:
                    sendHero(account.address, wh_account, hero['id'], wh_nonce, w3)
                    wh_nonce+=1
                    delta_heroes+=1
                    wh_heroes_amount-=1
                except Exception as error:
                    print("Error sending hero")
                    print(error)
                    print("") 

heroRebalancer()