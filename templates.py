__all__= ['CSS', 'SAMPLE_MODEL', 'JS_INCLUDES', 'HTML_TEMPLATE']

CSS = """
.angular-google-map-container { height: 800px; }
"""

SAMPLE_MODEL = """
{
center: {latitude: 40.1451, longitude: -99.6680 },
zoom: 14,
options : {scrollwheel: false},
markers : [
{ coords: {latitude: 40.1451, longitude: -99.6680}, icon: "", title: "Marker1" },
{ coords: {latitude: 40.1452, longitude: -99.6681}, icon: "", title: "Marker2" },
{ coords: {latitude: 40.1453, longitude: -99.6683}, icon: "", title: "Marker3" },
],
circles : [
	{
	center: { latitude: 40.1451, longitude: -99.680 },
	radius: 1000,
	stroke: { color: '#08B21F', weight: 2, opacity: 1 },
	fill: { color: '#08B21F', opacity: 0.5}
	},
	{
	center: { latitude: 40.1449, longitude: -99.670 },
	radius: 1000,
	stroke: { color: '#08B21F', weight: 2, opacity: 1 },
	fill: { color: '#08B21F', opacity: 0.5}
	},
	{
	center: { latitude: 40.1452, longitude: -99.683 },
	radius: 1000,
	stroke: { color: '#08B21F', weight: 2, opacity: 1 },
	fill: { color: '#08B21F', opacity: 0.5}
	}
]
};
"""

JS_INCLUDES = """
<script src="https://maps.googleapis.com/maps/api/js?key=%(API_KEY)s"></script>
<script src='http://cdnjs.cloudflare.com/ajax/libs/lodash.js/2.4.1/lodash.underscore.js'></script>
<script src='https://ajax.googleapis.com/ajax/libs/angularjs/1.2.25/angular.min.js'></script>
<script src='http://cdn.jsdelivr.net/angular.google-maps/1.1.0/angular-google-maps.min.js'></script>
"""



HTML_TEMPLATE = """
<!DOCTYPE html>
<html ng-app="appMaps">
<head>
    <title>Google Maps app</title>
	<meta name="viewport" content="initial-scale=1.0, user-scalable=no"/>
	<style>
	%(CSS)s

	</style>

	%(JS_INCLUDES)s

	<script>

	var model = %(MODEL)s;

	var appMaps = angular.module('appMaps', ['google-maps']);

	appMaps.controller('mainCtrl', function($scope, $log) {
		$scope.map = model;
    	});
	</script>
</head>
<body>
	<div id="map_canvas" ng-controller="mainCtrl">
    		<google-map center="map.center" zoom="map.zoom" draggable="true" options="options">
			<marker  data-ng-repeat="marker in map.markers" coords="marker.coords" icon="marker.icon">
				<window show="show">
					<div>{{marker.title}}</div>
				</window>
			</marker>
			<circle data-ng-repeat="c in map.circles" center="c.center" stroke="c.stroke" fill="c.fill" radius="c.radius"></circle>
		</google-map>
	</div>
</body>
</html>
"""
