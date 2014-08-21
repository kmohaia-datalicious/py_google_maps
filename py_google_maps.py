import sys

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

	def __init__(self, lat, lon, radius):
		self.stroke_color = '#FF0000'
		self.stroke_opacity = 0.8
		self.stroke_weight = 2
		self.fill_color = 'green' #'#FF0000'
		self.fill_opacity = 0.35
		self.map = 'map'
		self.center_lat = lat
		self.center_lon = lon
		self.radius = radius

	@property
	def js(self):
		params = {
		'STROKE_COLOR': self.stroke_color,
		'STROKE_OPACITY': str(self.stroke_opacity),
		'STROKE_WEIGHT': str(self.stroke_weight),
		'FILL_COLOR': self.fill_color,
		'FILL_OPACITY': str(self.fill_opacity),
		'MAP': self.map,
		'CENTER_LAT': str(self.center_lat),
		'CENTER_LON': str(self.center_lon),
		'RADIUS': str(self.radius)
		}
		return JS_CIRCLE %params

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

	def __init__(self, lat, lon, title='', draggable=False, animation=None, icon=None):
		self.title = title
		self.lat = lat
		self.lon = lon
		if icon is None:
			self._icon = Icon()
		else:
			self._icon = Icon(icon)

	@property
	def icon(self):
		return self._icon.path

	@property
	def js(self):
		params = {
		'MARKER_LAT': self.lat,
		'MARKER_LON': self.lon,
		'MARKER_TITLE': self.title,
		'ICON_IMAGE': self.icon
		}
		return JS_MARKER %params


class Map(object):

	def __init__(self, id="map-canvas", width=100, height=100, lat=-34.397, lon=150.644, zoom=12, points=None):
		self.id = id
		self.width = width
		self.height = height
		self.center_lat = lat
		self.center_lon = lon
		self.zoom = zoom
		self._points = points
		self._js = None

	#@property
	#def center_lat(self):
	#	return self._center[0]

	#@property
	#def center_lon(self):
	#	return self._center[1]

	@property
	def js(self):
		params = {
			'CENTER_LAT': str(self.center_lat),
			'CENTER_LON': str(self.center_lon),
			'ZOOM': str(self.zoom),
			'MAP_ID': str(self.id)
			}

		return JS_MAP %params

	@property
	def points(self):
		if self._points is None:
			self._points = []
		return self._points

	def add_point(self, point):
		self.points.append(point)


class GoogleMaps(object):

	def __init__(self, key=None, center_lat=0, center_lon=0, zoom=10, markers=[], circles=[]):
		self.key = key
		self._map = None
		self.init_map(lat=center_lat, lon=center_lon, zoom=zoom)
		self._markers = markers 				#list of marker objects
		self._circles = circles					#list of circle objects

	@property
	def map(self):
		if self._map is None:
			self._map = Map()
		return self._map

	@property
	def markers(self):
		return self._markers

	@property
	def circles(self):
		return self._circles

	def init_map(self, lat, lon, zoom):
		m = Map(lat=lat, lon=lon, zoom=zoom)
		self._map = m

	def add_marker(self, title, lat, lon, icon=None):
		m = Marker(lat=lat, lon=lon, title=title, icon=icon)
		self._markers.append(m)

	def add_circle(self, lat, lon, radius):
		c = Circle(lat=lat, lon=lon,radius=radius)
		self._circles.append(c)

	@property
	def _js_includes(self):
		params = {
		'API_KEY': self.key
		}
		return JS_INCLUDES %params

	@property
	def _js_markers(self):
		markers = []
		for m in self.markers:
			markers.append(m.js)
		return '\n'.join(markers)

	@property
	def _js_circles(self):
		circles = []
		if not self.circles:return ''
		for c in self.circles:
			circles.append(c.js)
		return '\n'.join(circles)

	@property
	def _js_main(self):

		params = {
			'JS_MAP': self.map.js,
			'JS_MARKER': self._js_markers,
			'JS_CIRCLE': self._js_circles
			}

		return JS_MAIN %params

	@property
	def html(self):
		params = {
		'CSS': CSS,
		'JS_INCLUDES': self._js_includes,
		'JS_MAIN': self._js_main,
		'MAP_ID': str(self.map.id)
		}

		return HTML_TEMPLATE %params

	def create_static_html(self, outfile='test.html'):
		with open(outfile, 'w') as of:
			of.write(self.html)

if __name__=='__main__':
	# API_KEY can be obtained from the google https://developers.google.com/maps/documentation/javascript/tutorial
	gm = GoogleMaps(key=API_KEY, center_lat=-34.397, center_lon=150.644, zoom=12)
	gm.add_marker(lat=-34.392,lon=150.624, title='marker1', icon='light_blue_dot')
	gm.add_marker(lat=-34.389,lon=150.614, title='marker2', icon='green_dot')
	gm.add_marker(lat=-34.392,lon=150.634, title='marker3', icon='red_dot')
	gm.add_marker(lat=-34.389,lon=150.654, title='marker4', icon='yellow_pushpin')
	gm.add_circle(lat=-34.397, lon=150.644, radius=150)
	gm.add_circle(lat=-34.327, lon=150.604, radius=1500)
	gm.add_circle(lat=-34.392,lon=150.624, radius=1000)
	gm.create_static_html(outfile='test.html')
