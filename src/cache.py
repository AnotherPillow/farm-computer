from .wiki import parse
from .MultiLangLogger.python import Logger
from datetime import datetime

from .config import (
    CLEAR_CACHE_HOURS
)


class Cache:
    logger: Logger
    cache = {}

    def __init__(self, logger):
        self.logger = logger
        pass

    def get(self, query: str) -> dict:
        # em = parse(query, False)

        if query in self.cache:
            self.logger.info(f'Found cache for {query}')
            hours_since_cache = (datetime.now() - self.cache[query]['time']).total_seconds() / 3600
            
            self.logger.info(f'Hours since cache: {hours_since_cache} (mins: {hours_since_cache * 60})')
            if hours_since_cache > CLEAR_CACHE_HOURS:
                self.logger.info(f'Clearing cache for {query}')
                del self.cache[query]
                return self.get(query)
            
            return self.cache[query]['embed'].build()
        
        self.cache[query] = {
            'embed': parse(query, False),
            'time': datetime.now()
        }
        self.logger.info(f'Cached {query}')
        return self.cache[query]['embed'].build()
