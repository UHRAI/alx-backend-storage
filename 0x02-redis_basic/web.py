#!/usr/bin/env python3
""" web module """

import requests
import redis
from typing import Callable
from functools import wraps

r = redis.Redis()

def count_url(method: Callable) -> Callable:
    """ Decorator that counts how many times each URL was accessed """
    @wraps(method)
    def wrapper(url):
        """ Wrapper function """
        r.incr(f"count:{url}")
        page = r.get(url)
        if not page:
            page = method(url)
            r.setex(url, 10, page)
        return page
    return wrapper

@count_url
def get_page(url: str) -> str:
    """ Function that obtains the HTML content of a particular URL and returns it """[^2^][2]
    req = requests.get(url)
    return req.text

