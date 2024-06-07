from datetime import datetime
import json
import requests
import secrets_manager
import hmac
import base64
from hashlib import sha256


sm = secrets_manager.SecretsManager()
secret_coinbase = sm.get_secret('hdx-coinbase-hc5-viewonly')

ACCESS_KEY = secret_coinbase['api_key']
SIGNING_KEY = secret_coinbase['secret_key']
PASSPHRASE = secret_coinbase['passphrase']
PORTFOLIO_ID = secret_coinbase['portfolio_id']

class CoinbaseApi:
    
    def __init__(self):
        self.api = requests.Session()
        self.api.headers.update({'Accept': 'application/json'})
        self.api.headers.update({'X-CB-ACCESS-KEY': ACCESS_KEY})
        self.api.headers.update({'X-CB-ACCESS-PASSPHRASE': PASSPHRASE})
        self.base_url = 'https://api.prime.coinbase.com'
        
    def generate_signature(self, timestamp: str, method: str, path: str, params: dict):
        body = json.dumps(params) if (params != {} and method != 'GET') else ""
        s = f'{timestamp}{method}{path}{body}'
        print(s)
        dig = hmac.new(SIGNING_KEY.encode(), msg=s.encode(), digestmod=sha256).digest()
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