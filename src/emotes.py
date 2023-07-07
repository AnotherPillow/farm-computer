from src.config import (
    IRIDIUM_EMOJI,
    GOLD_EMOJI,
    SILVER_EMOJI,
    HEALTH_EMOJI,
    ENERGY_EMOJI,
    COIN_EMOJI,
)

def getQualityFromPath(path):
    if path.endswith('Iridium_Quality.png'):
        return IRIDIUM_EMOJI
    elif path.endswith('Gold_Quality.png'):
        return GOLD_EMOJI
    elif path.endswith('Silver_Quality.png'):
        return SILVER_EMOJI

    return None

def getHealthEnergyFromPath(path):
    if path.endswith('Health.png'):
        return HEALTH_EMOJI
    elif path.endswith('Energy.png'):
        return ENERGY_EMOJI

    return None

def checkIfShouldBeGoldCoin(foreimages, path=None):
    if not path:
        path = foreimages[0].find_all('img')[0]['src']

    if path.endswith('Gold_Quality_Icon.png'):
        return COIN_EMOJI

    return None

def identify(str, pagename=None, foreimages=None, backimage=None):
    if q := getQualityFromPath(str):
        return q
    elif h := getHealthEnergyFromPath(str):
        return h
    elif (g := checkIfShouldBeGoldCoin(foreimages)) and len(foreimages)>0 and pagename:
        return g
