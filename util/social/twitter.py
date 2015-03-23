from overmortal.util.oauth import oauth
import urllib
import simplejson

class Twitter():
  def __init__(self, api_key, api_secret):
    #Set up private constants
    self.__TWITTER_AUTHORIZATION_URL = 'http://twitter.com/oauth/authorize'
    self.__TWITTER_ACCESS_TOKEN_URL = 'http://twitter.com/oauth/access_token'
    self.__TWITTER_REQUEST_TOKEN_URL = 'http://twitter.com/oauth/request_token'
    self.__TWITTER_CHECK_AUTH_URL = 'https://twitter.com/account/verify_credentials.json'
    self.__TWITTER_FRIENDS_URL = 'https://twitter.com/statuses/friends.json'
    #Set up OAuth consumer
    self.api_key = api_key
    self.api_secret = api_secret
    #Set up private variables for consumer
    self.__consumer = oauth.OAuthConsumer(self.api_key, self.api_secret)
    self.__signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

  def request(self, url, access_token, parameters = None):
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.__consumer, token=access_token, http_url = url, parameters = parameters)
    oauth_request.sign_request(self.__signature_method, self.__consumer, access_token)
    return oauth_request

  def fetch_response(self, oauth_request):
    url = oauth_request.to_url()
    file = urllib.urlopen(url)
    response = file.read()
    return response

  def get_unauthorised_request_token(self):
    oauth_request = self.request(self.__TWITTER_REQUEST_TOKEN_URL, None)
    resp = self.fetch_response(oauth_request)
    token = oauth.OAuthToken.from_string(resp)
    return token

  def get_authorisation_url(self, token):
    oauth_request = self.request(self.__TWITTER_AUTHORIZATION_URL, token)
    return oauth_request.to_url()

  def exchange_request_token_for_access_token(self, request_token):
    oauth_request = self.request(self.__TWITTER_ACCESS_TOKEN_URL, request_token)
    resp = self.fetch_response(oauth_request)
    return oauth.OAuthToken.from_string(resp) 

  def get_user(self, access_token):
    oauth_request = self.request(self.__TWITTER_CHECK_AUTH_URL, access_token)
    json = self.fetch_response(oauth_request)
    if 'screen_name' in json:
        return simplejson.loads(json)
    return None

  def get_friends(self, access_token, page):
    oauth_request = self.request(self.__TWITTER_FRIENDS_URL, access_token, {'page': page})
    json = self.fetch_response(oauth_request)
    return json
