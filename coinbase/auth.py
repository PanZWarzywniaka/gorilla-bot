import time
import hashlib
import hmac
import base64
from requests.auth import AuthBase


class CoinbaseWalletAuth(AuthBase):
    def __init__(self, api_key, secret_key, pass_phrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.pass_phrase = pass_phrase

    def decode(self, string: str):
        return base64.b64decode(string)

    def encode(self, string: str):
        return base64.b64encode(string)

    def __call__(self, request):
        timestamp = str(int(time.time()))

        message = timestamp + request.method.upper() + \
            request.path_url + (request.body or '')

        signature = hmac.new(self.decode(self.secret_key), message.encode(),
                             hashlib.sha256).digest()

        signature = self.encode(signature)

        request.headers.update({
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.pass_phrase,
        })
        return request
