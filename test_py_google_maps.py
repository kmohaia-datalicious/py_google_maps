#!/usr/bin/env python

import unittest

from py_google_maps import Map,PyGoogleMaps

API_KEY = 'AIzaSyDvx1iHz6ZDmvR5DpXHx9TrIvw4_hfg8-s'

class TestMap(unittest.TestCase):

	def setUp(self):
		self.map = Map()

	def test_center_lat(self):
		self.assertEquals( -34.397, self.map.center_lat)

	def test_center_lon(self):
		self.assertEquals( 150.644, self.map.center_lon)


class TestPyGoogleMaps(unittest.TestCase):

	def setUp(self):
		mymap = Map()
		self.google_maps = PyGoogleMaps(key=API_KEY, _map=mymap)

	def test_js_includes(self):
		expected = '\n<src="https://maps.googleapis.com/maps/api/js?key=%s">\n' %API_KEY
		self.assertEquals(expected, self.google_maps._js_includes())

	def test_js_main(self):
		expected = ''
		self.assertEquals(expected, self.google_maps._js_main())

	def test_html(self):
		expected = ''
		self.assertEquals(expected, self.google_maps.html())
if __name__=='__main__':
	unittest.main()
