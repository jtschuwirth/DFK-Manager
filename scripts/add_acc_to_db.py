from functions.data import init_settings_table
from functions.save_encryption import saveEncryption



settings_table = init_settings_table()

address = ""
private_key = ""
manager_address = settings_table.get_item(Key={"key_": "deployer_settings"})["Item"]["manager_address"]

saveEncryption(address, private_key, manager_address)