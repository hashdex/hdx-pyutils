from datetime import datetime
import json
import requests
import secrets_manager
import hmac
import base64
from hashlib import sha256
import hdxpyutils

class CoinbaseApi:
    
    def __init__(self, secret_name):
        """CoinbaseApi Constructor.

        @param secret: Secret name from AWS - Secret Manager.
        """

        secret_manager = hdxpyutils.SecretsManager()
        self.secret = secret_manager.get_secret(secret_name)

        self.api = requests.Session()
        self.api.headers.update({'Accept': 'application/json'})
        self.api.headers.update({'X-CB-ACCESS-KEY': self.secret['api_key']})
        self.api.headers.update({'X-CB-ACCESS-PASSPHRASE': self.secret['passphrase']})
        self.base_url = 'https://api.prime.coinbase.com'
        
    def generate_signature(self, timestamp: str, method: str, path: str, params: dict):
        body = json.dumps(params) if (params != {} and method != 'GET') else ""
        s = f'{timestamp}{method}{path}{body}'
        dig = hmac.new(self.secret['secret_key'].encode(), msg=s.encode(), digestmod=sha256).digest()
        sig = base64.b64encode(dig)
        return sig
    
    def request(self, method: str, path: str, params: dict = {}):
        method = method.upper()
        timestamp = str(int(datetime.now().timestamp()))
        signature = self.generate_signature(timestamp, method, path, params)
        self.api.headers.update({'X-CB-ACCESS-SIGNATURE': signature})
        self.api.headers.update({'X-CB-ACCESS-TIMESTAMP': timestamp})
        r = None
        if(method == 'GET'):
            r = self.api.get(self.base_url + path, params=params)
        elif(method == 'POST'):
            r = self.api.post(self.base_url + path, data=params)
        else:
            raise Exception('API method not implemented.')
        r.raise_for_status()
        return r.json()