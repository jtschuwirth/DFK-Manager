from functions.data import init_heroes_table, get_accounts, network
from functions.provider import get_account, get_provider
from functions.getAccountHeroes import getAccountHeroes
from functions.send_heros import sendHero

w3 = get_provider(network)



def transferHeroesToMain(main_account):
    heroes_table = init_heroes_table()
    accounts = get_accounts(main_account)
    c=1
    for address in accounts:
        print(f"Sending heroes from {address} ({c}/{len(accounts)}) to {main_account}")
        c+=1
        account = get_account(address, w3)
        nonce = w3.eth.get_transaction_count(account.address)
        heroes = getAccountHeroes(account.address, network)
        for hero in heroes:
            if hero["currentQuest"] != "mining" and hero["xp"]!=0 and hero["xp"]%1000==0:
                heroes_table.put_item(Item={
                    "heroId": str(hero["id"]),
                    "address": str(account.address),
                })
                try:
                    sendHero(main_account, account, hero["id"], nonce, w3)
                    print(f"Sent hero: {hero['id']}")
                    nonce+=1
                except:
                    continue
                