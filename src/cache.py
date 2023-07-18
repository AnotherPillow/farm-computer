from .wiki import parse

class Cache:

    cache = {}

    def __init__(self) -> None:
        pass

    def get(self, query: str) -> dict:
        # em = parse(query, False)

        if query in self.cache:
            return self.cache[query].build()
        
        self.cache[query] = parse(query, False)
        return self.cache[query].build()
