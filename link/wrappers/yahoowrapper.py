
from link.common import APIResponse
from link.wrappers import APIRequestWrapper, APIResponseWrapper
from requests.auth import AuthBase
import json
import requests


class YahooAuth(AuthBase):

    def __init__(self, token):
        self.token = token
    
    def __call__(self, req):

        req.url = "https://api-v3.admanagerplus.yahoo.com/v1/report/run?format=csv"

        req.headers['Content-Type'] = 'application/json'
        req.headers['X-Auth-Method'] = 'OAUTH'
        req.headers['X-Auth-Token'] = self.token
        
        return req

class YahooAPIResponse(APIResponseWrapper):
    pass


class YahooAPI(APIRequestWrapper):
    """
    Wrap the console API
    """
    def __init__(self, wrap_name=None, base_url=None, client_encoded=None,
            refresh_token=None, grant_type='refresh_token'):
        self.client_encoded = client_encoded
        self.refresh_token = refresh_token 
        self.grant_type = grant_type
        super(YahooAPI, self).__init__(wrap_name = wrap_name,
                                       base_url = base_url, 
                                       response_wrapper = YahooAPIResponse)

    def authenticate(self):
        self.refresh()
        self._wrapped.auth = YahooAuth(self.access_token)

    def refresh(self):

        body = {'grant_type': self.grant_type,
                'redirect_uri': 'oob', 
                'refresh_token': self.refresh_token
               }

        authorization = 'Basic ' + self.client_encoded
        headers = {'Authorization': authorization,
                   'Content-Type': 'application/x-www-form-urlencoded'
                  }

        token_url = 'https://api.login.yahoo.com/oauth2/get_token'

        self._wrapped = requests.session()

        refresh_response = self.post("/get_token", headers=headers, data=body)

        if not refresh_response.ok:
            import pdb; pdb.set_trace()
            raise Exception("Issue Refreshing")

        resp = json.loads(refresh_response.text)

        if not resp['access_token']:
            import pdb; pdb.set_trace()
            raise Exception("Issue Refreshing")

        self.access_token = resp['access_token']

    
