from xml.dom import minidom
import urllib

class Geocoder(object):
  api_key = None
  latitude = None
  longitude = None
  __xml = None
  def __init__(self, api_key):
    self.api_key = api_key
  def query(self, query):
    request_url = 'http://maps.google.com/maps/geo?q=' + urllib.quote(query) + '&output=xml&oe=utf8&sensor=false&key=' + self.api_key;
    data = urllib.urlopen(request_url).read()
    self.__xml = minidom.parseString(data)
    code = self.__xml.getElementsByTagName('code')[0]
    if code.childNodes[0].nodeValue == '200':
      places = self.__xml.getElementsByTagName('Placemark')
      coordinates = places[0].getElementsByTagName('coordinates')[0]
      coordinate_values = coordinates.childNodes[0].nodeValue.split(',')
      self.longitude = coordinate_values[0]
      self.latitude = coordinate_values[1]
      return len(places)
