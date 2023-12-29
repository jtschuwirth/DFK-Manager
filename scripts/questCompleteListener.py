from functions.provider import get_provider
from functions.data import init_account_table, init_tracking_table
import time
from datetime import datetime
import json

#event QuestCompleted(uint256 indexed questId, address indexed player, uint256 indexed heroId, tuple(uint256 id, uint256 questInstanceId, uint8 level, uint256[] heroes, address player, uint256 startBlock, uint256 startAtTime, uint256 completeAtTime, uint8 attempts, uint8 status, uint8 questType) quest);

QuestCoreAddress = "0x530fff22987E137e7C8D2aDcC4c15eb45b4FA752"
QuestCoreJson = open("abi/QuestCoreV3.json")
QuestCoreABI = json.load(QuestCoreJson)

w3 = get_provider("dfk")
QuestCoreContract = w3.eth.contract(address=QuestCoreAddress, abi=QuestCoreABI)

start = time.time()

def listener(start, timeout):
    quest_finished = 0
    heroes_used = 0
    event_filter = QuestCoreContract.events.QuestCompleted.createFilter(fromBlock="latest")
    print("Starting Listener ...")
    #while time.time() - start < timeout:
    while True:
        new_entries = event_filter.get_new_entries()
        for entry in new_entries:
            if (entry["args"]["quest"][1] != "3"): continue
            quest_finished += 1
            heroes_used += len(entry["args"]['quest'][3])
            print(f"Mining Quest Completed by {entry['args']['player']}, with {heroes_used} heroes")
            print(f"Elapsed time: {time.time() - start}")
            print(f"Quests finished so far: {quest_finished}")
            print(f"Heroes used so far: {heroes_used}")
            print("")



listener(start, 60*10)