import random
import redis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None


class RedisClient(object):
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host = host, port = port, password = password, decode_responses = True)
        self.type = type
        self.website = website

    def name(self):
        return "{type}:{website}".format(type = self.type, website = self.website)

    def set(self, username, userpassword):
        return self.db.hset(self.name( ), username, userpassword)

    def get(self,username):
        return self.db.hget(self.name(), username)

    def delete(self,username):
        return self.db.hdel(self.name(),username)

    def count(self):
        return self.db.hlen(self.name())

    def random(self):
        return random.choice(self.db.hvals(self.name()))

    def usernames(self):
        return self.db.hkeys(self.name())

    def all(self):
        return self.db.hgetall(self.name())

    def scan(self):
        return self.db.hkeys(self.name())

    def random_key(self):
        return random.choice(self.db.hkeys(self.name()))

    def get_alval(self):
        return self.db.hvals(self.name())
