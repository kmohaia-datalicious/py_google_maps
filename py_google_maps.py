import sys
import json
from templates import *
from icons import *


# steps for creating a simple map
# 1. declare the application as HTML5 <!DOCTYPE html> declaration
# 2. include the Maps API JavaScript using a script tag
# 3. create a div element named "map-canvas" to hold the Map
# 4. create a JavaScript object literal to hold a number of map properties
# 5. create a JavaScript 'map' object, passing it the div element and the map properties
# 6. use an event listener to load the map after the page has loaded.



class InfoWindow(object):

	def __init__(self, content, lat, lon, pixel_offset=None, max_width=None):
		self.content = content
		self.lat = lat
		self.lon = lon
		self.pixel_offset = pixel_offset
		self.max_width = max_width


	@property
	def js(self):
		params = {}


		return JS_INFO %params

class Circle(object):

	def __init__(self, **kwargs):
		try:
			self.stroke_color = kwargs['stroke_color']
		except KeyError:
			self.stroke_color = '#FF0000'

		try:
			self.stroke_opacity = kwargs['stroke_opacity']
		except KeyError:
			self.stroke_opacity = 0.8


		try:
			self.stroke_weight = kwargs['stroke_weight']
		except KeyError:
			self.stroke_weight = 2

		try:
			self.fill_color = kwargs['fill_color']
		except KeyError:
			self.fill_color = 'green' #'#FF0000'

		try:
			self.fill_opacity = kwargs['fill_opacity']

		except KeyError:
			self.fill_opacity = 0.35

		self.latitude = kwargs['latitude']
		self.longitude = kwargs['longitude']
		self.radius = kwargs['radius']


	@property
	def center(self):
		return {'latitude': self.latitude, 'longitude': self.longitude}

	@property
	def stroke(self):
		return {'color': self.stroke_color,
			'weight': self.stroke_weight,
			'opacity': self.stroke_opacity}

	@property
	def fill(self):
		return { 'color': self.fill_color, 'opacity': self.fill_opacity }


	@property
	def data(self):
		return {
		'center': self.center, 'radius': self.radius, 'stroke': self.stroke, 'fill': self.fill
		}


	@property
	def json(self):
		return json.dumps(self.data)


class Icon(object):

	def __init__(self, name='blue_dot'):
		self.icons = icons_dict
		self.name = name

	@property
	def path(self):
		return self.icons[self.name]

	@property
	def icon_names(self):
		return self.icons.keys()

	@property
	def icon_paths(self):
		return self.icons.values()

class Marker(object):

	def __init__(self, latitude, longitude, title='', icon=None):
		self.title = title
		self.latitude = latitude
		self.longitude = longitude
		if icon is None:
			self._icon = Icon()
		else:
			self._icon = Icon(icon)

	@property
	def icon(self):
		return self._icon.path

	@property
	def data(self):
		return  {
		'coords': {'latitude': self.latitude, 'longitude': self.longitude},
		'title': self.title,
		'icon': self.icon
		}


	@property
	def json(self):
		return json.dumps(self.data)


class GoogleMaps(object):
	_model = {
	'center': {},
	'zoom': 12,
	'options': {},
	'markers': [],
	'circles': []
	}

	def __init__(self, **kwargs):
		self._key = kwargs['key']
		self._markers = [] 				#list of marker objects
		self._circles = []					#list of circle objects
		self._longitude = kwargs['longitude']
		self._latitude = kwargs['latitude']
		self._zoom = kwargs['zoom']
		# google maps options
		# https://developers.google.com/maps/documentation/javascript/reference#MapOptions
		try:
			self._options = kwargs['options']
		except KeyError:
			self._options = {}

	@property
	def center(self):
		return {'latitude': self._latitude, 'longitude': self._longitude}

	@property
	def zoom(self):
		return self._zoom

	@property
	def options(self):
		return self._options

	@options.setter
	def options(self, opts):
		self._options = opts


	@property
	def key(self):
		return self._key

	@property
	def model(self):
		self._model['center'] = self.center
		self._model['zoom'] = self.zoom
		self._model['options'] = self.options
		self._model['markers'] = self.markers
		self._model['circles'] = self.circles
		return self._model

	@property
	def markers(self):
		return self._markers

	@property
	def circles(self):
		return self._circles


	def add_marker(self, title, latitude, longitude, icon=None):
		m = Marker(latitude=latitude, longitude=longitude, title=title, icon=icon)
		self.markers.append(m.data)

	def add_circle(self, latitude, longitude, radius):
		c = Circle(latitude=latitude, longitude=longitude,radius=radius)
		self.circles.append(c.data)

	@property
	def _js_includes(self):
		params = {
		'API_KEY': self.key
		}
		return JS_INCLUDES %params


	@property
	def html(self):
		return HTML_TEMPLATE %{
		'CSS': CSS,
		'JS_INCLUDES': self._js_includes,
		'MODEL': json.dumps(self.model)
		}


	def create_static_html(self, outfile='test.html'):
		with open(outfile, 'w') as of:
			of.write(self.html)

if __name__=='__main__':
	# API_KEY can be obtained from the google https://developers.google.com/maps/documentation/javascript/tutorial
	API_KEY = sys.argv[1]
	gm = GoogleMaps(key=API_KEY, latitude=-34.397, longitude=150.644, zoom=12, options={'scrollwheel': False})
	gm.add_marker(latitude=-34.392, longitude=150.624, title='marker1', icon='light_blue_dot')
	gm.add_marker(latitude=-34.389, longitude=150.614, title='marker2', icon='green_dot')
	gm.add_marker(latitude=-34.392, longitude=150.634, title='marker3', icon='red_dot')
	gm.add_marker(latitude=-34.389, longitude=150.654, title='marker4', icon='yellow_pushpin')
	gm.add_circle(latitude=-34.397, longitude=150.644, radius=150)
	gm.add_circle(latitude=-34.327, longitude=150.604, radius=1500)
	gm.add_circle(latitude=-34.392,longitude=150.624, radius=1000)
	gm.create_static_html(outfile='test.html')
