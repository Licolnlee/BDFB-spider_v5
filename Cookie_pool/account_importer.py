from .account_saver import RedisClient

class CookieGenator(object):
    def __init__(self,website):
        self.website = website
        self.accounts = RedisClient('accounts', website)
        self.cookies = RedisClient('cookies', website)
        self.init_browser()

    def init_browser(self):

    def __del__(self):
        self.close()