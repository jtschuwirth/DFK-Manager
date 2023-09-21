from functions.data import get_accounts, network, chainId, init_account_table, init_settings_table, manager_account
from functions.getAccountHeroes import getAccountHeroes
from functions.send_heros import sendHero
from functions.provider import get_account, get_provider
import time

w3 = get_provider(network)
breeder ="0x0206aA6c7537b8f08069605503863E18395C3238"
warehouse = "0x867df63D1eEAEF93984250f78B4bd83C70652dcE"

def heroFinder():
    accounts = get_accounts(manager_account)
    wh_account = get_account(warehouse, w3)
    wh_nonce = w3.eth.get_transaction_count(wh_account.address)
    wh_heroes = getAccountHeroes(wh_account.address, "dfk")
    max_heroes_to_send = len(wh_heroes)
    c=1
    heroes_sent = 0
    for user in accounts:
        print("")
        account = get_account(user, w3)
        nonce = w3.eth.get_transaction_count(account.address)
        heroes = getAccountHeroes(user, "dfk")
        print(f"account: {user} ({c}/{len(accounts)}) has {len(heroes)} heroes")
        time.sleep(1)
        for hero in heroes:
            if (int(hero["generation"]) <= 1 and int(hero['maxSummons']) - int(hero['summons']) >= 3) or (int(hero["generation"]) <= 2 and int(hero['summons']) == 0 and int(hero['maxSummons']) > 0):
                print(f"Sending Hero {hero['id']} is gen {hero['generation']} has {hero['maxSummons']-hero['summons']} summons")
                try:
                    sendHero(breeder, account, hero['id'], nonce, w3)
                    nonce+=1
                    sendHero(account.address, wh_account, wh_heroes[heroes_sent]["id"], wh_nonce, w3)
                    wh_nonce+=1
                    heroes_sent+=1
                    if heroes_sent >= max_heroes_to_send:
                        print("No more heroes to send")
                        return
                    pass
                except Exception as error:
                    print("Error sending hero")
                    print(error)
                    print("")
        
        c+=1

heroFinder()