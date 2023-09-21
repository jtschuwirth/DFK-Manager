from functions.getItemPriceJewel import getCrystalPriceJewel
from functions.provider import get_provider
from functions.data import network

w3 = get_provider(network)

def ticketCost(win_rate):
    crystal_value = getCrystalPriceJewel(w3) 
    ticket_cost = (10 * crystal_value) / (130*10 * win_rate + 13*10 * (1 - win_rate))
    return ticket_cost
