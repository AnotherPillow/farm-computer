from src.config import (
    IRIDIUM_EMOJI,
    GOLD_EMOJI,
    SILVER_EMOJI,
    HEALTH_EMOJI,
    ENERGY_EMOJI,
    COIN_EMOJI,
    IRIDIUM_ENERGY_EMOJI,
    GOLD_ENERGY_EMOJI,
    SILVER_ENERGY_EMOJI,
    IRIDIUM_HEALTH_EMOJI,
    GOLD_HEALTH_EMOJI,
    SILVER_HEALTH_EMOJI,
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

def qualityHealthEnergy(back_path, foreimages):
    imgs = foreimages[0].find_all('img')

    if not len(imgs) > 0:
        return None

    fore_path = imgs[0]['src']

    # print(f'fore_path: {fore_path}')
    # print(f'back_path: {back_path}')

    if fore_path.endswith('Silver_Quality_Icon.png'):
        if back_path.endswith('Health.png'):
            return SILVER_HEALTH_EMOJI
        elif back_path.endswith('Energy.png'):
            return SILVER_ENERGY_EMOJI
    elif fore_path.endswith('Gold_Quality_Icon.png'):
        if back_path.endswith('Health.png'):
            return GOLD_HEALTH_EMOJI
        elif back_path.endswith('Energy.png'):
            return GOLD_ENERGY_EMOJI
    elif fore_path.endswith('Iridium_Quality_Icon.png'):
        if back_path.endswith('Health.png'):
            return IRIDIUM_HEALTH_EMOJI
        elif back_path.endswith('Energy.png'):
            return IRIDIUM_ENERGY_EMOJI

    return None

def identify(str, pagename=None, foreimages=None, backimage=None):
    if q := getQualityFromPath(str):
        return q
    elif (q := qualityHealthEnergy(str, foreimages)) and len(foreimages)>0:
        return q
    elif h := getHealthEnergyFromPath(str):
        return h
    elif (g := checkIfShouldBeGoldCoin(foreimages)) and len(foreimages)>0 and pagename:
        return g

    return None