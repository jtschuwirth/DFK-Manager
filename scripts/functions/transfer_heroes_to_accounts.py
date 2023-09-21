from functions.data import init_heroes_table, get_accounts, network
from functions.provider import get_account, get_provider
from functions.getAccountHeroes import getAccountHeroes
from functions.send_heros import sendHero

w3 = get_provider(network)



def transferHeroesToAccounts(main_account):
    heroes_table = init_heroes_table()
    account = get_account(main_account, w3)
    nonce = w3.eth.get_transaction_count(account.address)
    print(f"Sending heroes from {main_account}")
    heroes = heroes_table.scan()["Items"]
    heroes_main_account = getAccountHeroes(account.address, network)
    heroes_in_main = []
    for hero in heroes_main_account:
        heroes_in_main.append(hero["id"])
    for hero in heroes:
        if hero["heroId"] in heroes_in_main:
            try:
                sendHero(hero["address"], account, hero["heroId"], nonce, w3)
                print(f"Sent hero: {hero['heroId']} to {hero['address']}")
                nonce+=1
            except Exception as e:
                print(f"failed to send hero {hero['heroId']}", e)
                continue
