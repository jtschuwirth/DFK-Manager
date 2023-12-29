from functions.getAccountHeroes import getAccountHeroesByClass
from functions.data import get_accounts, network
from functions.provider import get_account, get_provider

w3 = get_provider(network)

def checkCombatHeroes(start_index = 0):
    main_address = "0xa691623968855b91A066661b0552a7D3764c9a64"
    accounts = get_accounts(main_address)
    c=1
    for address in accounts:
        if c<start_index:
            c+=1
            continue

        print(f"Checking {address} ({c}/{len(accounts)})")
        c+=1

        account = get_account(address, w3)
        heroes = getAccountHeroesByClass(account.address, network, [0,1,3,4])

        for hero in heroes:
            if hero['level'] > 8:
                print(f"{hero['id']}: lvl: {hero['level']}, mainClass: {hero['mainClass']}")

checkCombatHeroes()