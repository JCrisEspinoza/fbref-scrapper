import requests


class Requests:

    def __init__(self):
        self._memory = {}

    def get(self, url, *args, **kwargs):
        if url in self._memory:
            return self._memory[url]
        self._memory[url] = requests.get(url, *args, **kwargs)
        return self._memory[url]
