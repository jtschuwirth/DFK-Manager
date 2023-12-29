from functions.data import get_accounts, network, chainId, init_account_table, init_settings_table, manager_account
from functions.getAccountHeroes import getAccountHeroes
from functions.send_heros import sendHero
from functions.provider import get_account, get_provider
import time

w3 = get_provider(network)
warehouse = "0x867df63D1eEAEF93984250f78B4bd83C70652dcE"
main_address = "0xa691623968855b91A066661b0552a7D3764c9a64"


def swapHero(heroId, targetAddress):
    wh_account = get_account(warehouse, w3)
    wh_nonce = w3.eth.get_transaction_count(wh_account.address)

    target_account= get_account(targetAddress, w3)
    target_nonce = w3.eth.get_transaction_count(target_account.address)

    sendHero(main_address, target_account, heroId, target_nonce, w3)
    
    wh_heroes = getAccountHeroes(wh_account.address, "dfk")
    sendHero(target_account.address, wh_account, wh_heroes[0]["id"], wh_nonce, w3)



swapHero(
    "1000000123309", 
    "0x17765249F934ceC90E6BC2C9AF8376Ece0bA19Ef"
    )


