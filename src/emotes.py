from src.config import (
    IRIDIUM_EMOJI,
    GOLD_EMOJI,
    SILVER_EMOJI
)

def getQualityFromPath(path):
    if path.endswith('Iridium_Quality.png'):
        return IRIDIUM_EMOJI
    elif path.endswith('Gold_Quality.png'):
        return GOLD_EMOJI
    elif path.endswith('Silver_Quality.png'):
        return SILVER_EMOJI
