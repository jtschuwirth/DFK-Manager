from functions.provider import get_account, get_provider
from functions.utils import sendJewel

main_acc="0xa691623968855b91A066661b0552a7D3764c9a64"

accounts = ["0xdB7784bC37131381B6f54657638D257713F96CFB"]
w3 = get_provider("dfk")

def test_account_nonce(account):
    pending_nonce = w3.eth.get_transaction_count(account.address, "pending")
    nonce = w3.eth.get_transaction_count(account.address)
    print(nonce, pending_nonce)



for address in accounts:
    account = get_account(address, w3)
    nonce = w3.eth.get_transaction_count(account.address)
    test_account_nonce(account)
    sendJewel(account, main_acc, 10**16, w3, nonce) 
