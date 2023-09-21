from functions.getItemPriceJewel import getItemPriceJewel, getCrystalPriceJewel
from functions.provider import get_provider
from functions.data import network, init_payouts_table, init_account_table, init_tracking_table
from datetime import datetime
import time

w3 = get_provider(network)

gas_factor = 3

heros_per_quest = 6
quest_per_day = 3
fishers_per_account = 18
daily_avg_gas_cost = (0.6/3)*quest_per_day*gas_factor

loot_slots = 6
tear_drop_rate = 0.075
shvas_drop_rate = 0.01
moksha_drop_rate = 0.0003
egg_drop_rate = 0.0001
bloater_drop_rate = 0.23
ironscale_drop_rate = 0.09015
lanterneye_drop_rate=0.09015
speckle_tail_drop_rate=0.06015
three_eyed_eel_drop_rate = 0.01015
king_pincer_drop_rate = 0.01015
shimmerskin_drop_rate = 0.00915

crystal_value = getCrystalPriceJewel(w3) 
tear_value = getItemPriceJewel("Gaias Tears", w3)
gold_value = getItemPriceJewel("DFKGold", w3)
shvas_value = getItemPriceJewel("Shvas Rune", w3)
moksha_value = getItemPriceJewel("Moksha Rune", w3)
egg_value = getItemPriceJewel("Blue Pet Egg", w3)
bloater_value = getItemPriceJewel("Frost Bloater", w3)
ironscale_value = getItemPriceJewel("Ironscale", w3)
lanterneye_value = getItemPriceJewel("Lanterneye", w3)
speckle_tail_value = getItemPriceJewel("Speckle Tail", w3)
three_eyed_eel_value = getItemPriceJewel("Three-Eyed Eel", w3)
king_pincer_value = getItemPriceJewel("King Pincer", w3)
shimmerskin_value = getItemPriceJewel("Shimmerskin", w3)

daily_tears = quest_per_day*loot_slots*tear_drop_rate
daily_tears_value = daily_tears*tear_value

daily_shvas = quest_per_day*loot_slots*shvas_drop_rate
daily_shvas_value = daily_shvas*shvas_value

daily_moksha = quest_per_day*loot_slots*moksha_drop_rate
daily_moksha_value = daily_moksha*moksha_value

daily_egg = quest_per_day*egg_drop_rate
daily_egg_value = daily_egg*egg_value

daily_bloater = quest_per_day*loot_slots*bloater_drop_rate
daily_bloater_value = daily_bloater*bloater_value

daily_ironscale = quest_per_day*loot_slots*ironscale_drop_rate
daily_ironscale_value = daily_ironscale*ironscale_value

daily_lanterneye = quest_per_day*loot_slots*lanterneye_drop_rate
daily_lanterneye_value = daily_lanterneye*lanterneye_value

daily_speckle_tail = quest_per_day*loot_slots*speckle_tail_drop_rate
daily_speckle_tail_value = daily_speckle_tail*speckle_tail_value

daily_three_eyed_eel = quest_per_day*loot_slots*three_eyed_eel_drop_rate
daily_three_eyed_eel_value = daily_three_eyed_eel*three_eyed_eel_value

daily_king_pincer = quest_per_day*loot_slots*king_pincer_drop_rate
daily_king_pincer_value = daily_king_pincer*king_pincer_value

daily_shimmerskin = quest_per_day*loot_slots*shimmerskin_drop_rate
daily_shimmerskin_value = daily_shimmerskin*shimmerskin_value

daily_income = daily_tears_value + daily_moksha_value + daily_shvas_value + daily_egg_value + daily_bloater_value + daily_ironscale_value + daily_lanterneye_value + daily_speckle_tail_value + daily_three_eyed_eel_value + daily_king_pincer_value + daily_shimmerskin_value

print(f"1d: {daily_income} Jewel")
print(f"7d: {daily_income*7} Jewel")
print(f"30d: {daily_income*30} Jewel")

print("")
print("Rewards value ratio")
print(f"fishes: {round((daily_bloater_value+daily_ironscale_value+daily_lanterneye_value+daily_speckle_tail_value+daily_three_eyed_eel_value+daily_king_pincer_value+daily_shimmerskin_value)/daily_income, 4)*100}%")
print(f"tears: {round(daily_tears_value/daily_income, 4)*100}%")
print(f"Shvas: {round(daily_shvas_value/daily_income, 4)*100}%")
print(f"Moksha: {round(daily_moksha_value/daily_income, 4)*100}%")
print(f"Blue Egg: {round(daily_egg_value/daily_income, 4)*100}%")

print("")
print("Account Raw Income")
account_daily_income = daily_income*fishers_per_account


print(f"1d: {account_daily_income} Jewel")
print(f"7d: {account_daily_income*7} Jewel")
print(f"30d: {account_daily_income*30} Jewel")

print("")
print("Account Gas Cost")
account_daily_gas_cost = daily_avg_gas_cost
print(f"1d: {account_daily_gas_cost} Jewel")
print(f"7d: {account_daily_gas_cost*7} Jewel")
print(f"30d: {account_daily_gas_cost*30} Jewel")

print("")
print("Account Earnings")
account_daily_earnings = account_daily_income - daily_avg_gas_cost
print(f"1d: {account_daily_earnings} Jewel")
print(f"3d: {account_daily_earnings*3} Jewel")
print(f"7d: {account_daily_earnings*7} Jewel")
print(f"30d: {account_daily_earnings*30} Jewel")