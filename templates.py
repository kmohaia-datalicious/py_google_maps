__all__= ['CSS', 'JS_INCLUDES', 'JS_MAIN', 'JS_MAP', 'JS_MARKER', 'JS_CIRCLE', 'JS_INFO_WINDOW', 'HTML_TEMPLATE']

CSS = """
html { height: 100% }
body { height: 100%; margin: 0; padding: 0 }
#map-canvas { height: 100% }
"""

JS_INFO_WINDOW = """

"""

JS_INCLUDES = """
"https://maps.googleapis.com/maps/api/js?key=%(API_KEY)s"
"""

JS_MAIN = """
function initialize() {

	%(JS_MAP)s

	%(JS_CIRCLE)s

	%(JS_MARKER)s
      }
      google.maps.event.addDomListener(window, 'load', initialize);
"""


JS_MAP = """

var mapOptions = {
          center: new google.maps.LatLng(%(CENTER_LAT)s, %(CENTER_LON)s),
          zoom: %(ZOOM)s
        };

        var map = new google.maps.Map(document.getElementById("%(MAP_ID)s"),
            mapOptions);

"""

JS_MARKER = """
var marker = new google.maps.Marker({
	position: new google.maps.LatLng(%(MARKER_LAT)s, %(MARKER_LON)s),
      	map: map,
      	title: '%(MARKER_TITLE)s',
	icon: '%(ICON_IMAGE)s'
});
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <style type="text/css">
    	%(CSS)s
    </style>

    <script type="text/javascript" src=%(JS_INCLUDES)s>
    </script>

    <script type="text/javascript">
	%(JS_MAIN)s
    </script>

  </head>
  <body>
    <div id="%(MAP_ID)s"/>
  </body>
</html>
"""

JS_CIRCLE = """
var circleOptions = {
      strokeColor: '%(STROKE_COLOR)s',
      strokeOpacity: %(STROKE_OPACITY)s,
      strokeWeight: %(STROKE_WEIGHT)s,
      fillColor: '%(FILL_COLOR)s',
      fillOpacity: %(FILL_OPACITY)s,
      map: %(MAP)s,
      center: new google.maps.LatLng(%(CENTER_LAT)s, %(CENTER_LON)s),
      radius: %(RADIUS)s
    };
    circle = new google.maps.Circle(circleOptions);
"""
