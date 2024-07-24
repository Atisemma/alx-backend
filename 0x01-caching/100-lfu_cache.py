#!/usr/bin/env python3
""" LFUCache module
"""

from base_caching import BaseCaching
from collections import defaultdict, OrderedDict


class LFUCache(BaseCaching):
    """ LFUCache defines:
      - caching system that inherits from BaseCaching
      - where data are stored in a dictionary with LFU algorithm
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()
        self.frequency = defaultdict(int)
        self.lru = defaultdict(OrderedDict)
        self.min_frequency = 0

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is not None and item is not None:
            if (len(self.cache_data) >= BaseCaching.MAX_ITEMS and
                    key not in self.cache_data):
                lfu_key, _ = self.lru[self.min_frequency].popitem(last=False)
                del self.cache_data[lfu_key]
                del self.frequency[lfu_key]
                if not self.lru[self.min_frequency]:
                    del self.lru[self.min_frequency]
                print(f"DISCARD: {lfu_key}")

            if key in self.cache_data:
                del self.lru[self.frequency[key]][key]
                if not self.lru[self.frequency[key]]:
                    del self.lru[self.frequency[key]]

            self.cache_data[key] = item
            self.frequency[key] += 1
            self.lru[self.frequency[key]][key] = None
            if self.frequency[key] == 1:
                self.min_frequency = 1
            elif key in self.cache_data:
                if self.min_frequency == self.frequency[key] - 1:
                    if not self.lru[self.min_frequency]:
                        self.min_frequency = self.frequency[key]

    def get(self, key):
        """ Get an item by key
        """
        if key is not None and key in self.cache_data:
            del self.lru[self.frequency[key]][key]
            if not self.lru[self.frequency[key]]:
                del self.lru[self.frequency[key]]
            self.frequency[key] += 1
            self.lru[self.frequency[key]][key] = None
            if self.min_frequency == self.frequency[key] - 1:
                if not self.lru[self.min_frequency]:
                    self.min_frequency = self.frequency[key]
            return self.cache_data[key]
        return None
