from .wiki import parse
from .MultiLangLogger.python import Logger
from datetime import datetime
import os, json
from .embed import EmbedBuilder

from .config import (
    CLEAR_CACHE_HOURS, 
    CACHE_FILE
)

from .embed import fromDict

class Cache:
    logger: Logger
    cache = {}

    def __init__(self, logger):
        self.logger = logger
        
        if os.path.isfile(CACHE_FILE):
            self.logger.info(f'Loading cache from {CACHE_FILE}')
            file = open(CACHE_FILE, 'r')
            
            _cache = json.load(file)
            for key in _cache:
                self.cache[key] = {
                    'embed': fromDict(_cache[key]['embed']),
                    'time': datetime.strptime(_cache[key]['time'], '%Y-%m-%d %H:%M:%S.%f')
                }
    
    def save(self):
        self.logger.info(f'Saving cache to {CACHE_FILE}')
        file = open(CACHE_FILE, 'w')

        jcache = {}
        for key in self.cache:
            emb = self.cache[key]['embed']
            jcache[key] = {
                'embed': self.cache[key]['embed'].build().to_dict(),
                'str_color': f'#{emb.color.value:0>6X}',
                'time': self.cache[key]['time'].strftime('%Y-%m-%d %H:%M:%S.%f')
            }

        json.dump(jcache, file, indent=4)

    def get(self, query: str) -> dict:
        # em = parse(query, False)
        embed = self.cache[query]['embed'] if query in self.cache else None

        if query in self.cache:
            self.logger.info(f'Found cache for {query}')
            hours_since_cache = (datetime.now() - self.cache[query]['time']).total_seconds() / 3600

            print(embed)
            
            self.logger.info(f'Hours since cache: {hours_since_cache} (mins: {hours_since_cache * 60})')
            if hours_since_cache > CLEAR_CACHE_HOURS:
                self.logger.info(f'Clearing cache for {query}')
                del self.cache[query]
                return self.get(query)
            
            return embed.build()
        
        parsed = parse(query, False)
        self.cache[query] = {
            'embed': parsed,
            'str_color': f'#{parsed.color.value:0>6X}',
            'time': datetime.now()
        }
        
        self.logger.info(f'Cached {query}')
        self.save()

        print(embed)

        # return self.cache[query]['embed']
        if isinstance(embed, EmbedBuilder):
            return embed.build()
        else:
            return embed
