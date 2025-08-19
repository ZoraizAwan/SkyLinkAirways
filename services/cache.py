from functools import lru_cache

# Decorator alias to make it easy to spot cached functions
cached = lru_cache(maxsize=256)

# Registry of clearers
_CACHE_CLEARERS = []

def register_cache_clearer(fn):
    _CACHE_CLEARERS.append(fn)
    return fn

def clear_all_caches():
    for c in _CACHE_CLEARERS:
        c()
