#!/usr/bin/env python3
# lru_cache.py
from collections import OrderedDict
import random
import time


class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


def range_sum_no_cache(array, left, right):
    return sum(array[left:right + 1])


def update_no_cache(array, index, value):
    array[index] = value


def range_sum_with_cache(array, left, right, cache):
    key = (left, right)
    result = cache.get(key)
    if result == -1:
        result = sum(array[left:right + 1])
        cache.put(key, result)
    return result


def update_with_cache(array, index, value, cache):
    array[index] = value
    # Удаляем из кеша все диапазоны, которые включают изменённый индекс
    for key in list(cache.cache.keys()):
        if key[0] <= index <= key[1]:
            del cache.cache[key]


def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [
        (random.randint(0, n // 2), random.randint(n // 2, n - 1))
        for _ in range(hot_pool)
    ]
    queries = []
    for _ in range(q):
        if random.random() < p_update:
            queries.append(("Update", random.randint(0, n - 1), random.randint(1, 100)))
        else:
            if random.random() < p_hot:
                left, right = random.choice(hot)
            else:
                left = random.randint(0, n - 1)
                right = random.randint(0, n - 1)
            queries.append(("Range", left, right))
    return queries


def run_no_cache(array, queries):
    arr = array.copy()
    start = time.time()
    for q in queries:
        if q[0] == "Range":
            range_sum_no_cache(arr, q[1], q[2])
        else:
            update_no_cache(arr, q[1], q[2])
    return time.time() - start


def run_with_cache(array, queries):
    arr = array.copy()
    cache = LRUCache(1000)
    start = time.time()
    for q in queries:
        if q[0] == "Range":
            range_sum_with_cache(arr, q[1], q[2], cache)
        else:
            update_with_cache(arr, q[1], q[2], cache)
    return time.time() - start


if __name__ == "__main__":
    N, Q = 100_000, 50_000
    array = [random.randint(1, 100) for _ in range(N)]
    queries = make_queries(N, Q)

    time_no_cache = run_no_cache(array, queries)
    time_with_cache = run_with_cache(array, queries)

    print(f"Без кешу : {time_no_cache:.2f} с")
    print(f"LRU-кеш  : {time_with_cache:.2f} с  (прискорення ×{time_no_cache / time_with_cache:.2f})")
