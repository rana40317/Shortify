import string

class shortenurl:
    def __init__(self):
        self.long_to_short = {}
        self.short_to_long = {}
        self.counter = 0
        self.base62 = string.ascii_letters + string.digits

    def _to_base62(self, num):
        if num == 0:
            return self.base62[0]
        result = []
        base = len(self.base62)
        while num > 0:
            result.append(self.base62[num % base])
            num //= base
        return ''.join(reversed(result))

    def encode(self, long_url):
        if long_url in self.long_to_short:
            return self.long_to_short[long_url]
        self.counter += 1
        short_key = self._to_base62(self.counter)
        self.short_to_long[short_key] = long_url
        self.long_to_short[long_url] = short_key
        return short_key

    def decode(self, key):
        return self.short_to_long.get(key)