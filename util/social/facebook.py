import simplejson
import urllib

class Facebook():
	def __init__(self, facebook_app_id):
		self.facebook_app_id = facebook_app_id

	def init_data_from_cookie(self, cookies):
		if cookies.has_key('fbs_' + self.facebook_app_id):
			cookie = cookies['fbs_' + self.facebook_app_id]
			args = cookie.split('&')
			facebook_values = {}
			for arg in args:
				key_value_pair = arg.split('=')
				facebook_values[key_value_pair[0]] = key_value_pair[1]
				self.access_token = facebook_values['access_token']
				return self.access_token
		else:
			return None

	def get_user(self):
		try:
			file = urllib.urlopen("https://graph.facebook.com/me?access_token=" + self.access_token)
			self.user = simplejson.loads(file.read())
		except e:
			self.error = e
			return None
		finally:
			file.close()
		return self.user
