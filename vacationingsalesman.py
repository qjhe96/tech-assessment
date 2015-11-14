import sys, getopt, json
from geopy import Nominatim
from geopy.distance import great_circle
from urllib2 import Request, urlopen, URLError

API_KEY = 'AIzaSyBcL1cDvmIbM8Mnu_ty-iiodlxf6q0-7IQ'
API_QUERY = 'https://maps.googleapis.com/maps/api/distancematrix/json?'


# Create an API query to Google Maps API
def get_api_query(units, travel_mode, city1, city2):
	origin_lat, origin_long = city1
	destination_lat, destination_long = city2
	query_units = ''
	if units == 'kilometers':
		query_units = 'metric'
	elif units == 'miles':
		query_units = 'imperial'
	api_query = API_QUERY + 'origins=' + str(origin_lat) + ',' + str(origin_long) + '&destinations=' + str(destination_lat) + ',' + str(destination_long) \
			+ '&mode=' + travel_mode + '&units=' + query_units + '&key=' + API_KEY
	return api_query

# Call the Query on the API
def query_api(query):
	request = Request(query)
	try:
		response = urlopen(request)
		return response.read()
	except URLError, e:
		print("Invalid Query!", e)

# Load the JSON into a dictionary
def parse_JSON(json_obj):
	return json.loads(json_obj)

# Find distances given unit, and list of cities, and travel mode
def find_distances(units, cities_list, travel_mode):

	distances_list = []
	geolocator = Nominatim()
	for i in range(len(cities_list)):
		if i == len(cities_list)-1:
			return distances_list
		else:
			distance = 0
			city1 = cities_list[i]
			city2 = cities_list[i+1]
			geocode1 = geolocator.geocode(city1, timeout=5)
			geocode2 = geolocator.geocode(city2, timeout=5)
			city1_lat = geocode1.latitude
			city1_long = geocode1.longitude
			city2_lat = geocode2.latitude
			city2_long = geocode2.longitude
			coord1 = (city1_lat, city1_long)
			coord2 = (city2_lat, city2_long)
			# Crow's Flying
			if travel_mode == 'default':
				distance = find_direct_distance(units, coord1, coord2)

			# A mode was specified, so we must call Google Maps API
			else:
				distance = find_distance_by_mode(units, travel_mode, coord1, coord2)
			distances_list.append(distance)
	return distances_list

# Find the direct distance between two coordinates
def find_direct_distance(units, coord1, coord2):
	if units == 'kilometers':
		return great_circle(coord1, coord2).kilometers
	elif units == 'miles':
		return great_circle(coord1, coord2).miles

# Find distance by querying the API
def find_distance_by_mode(units, travel_mode, coord1, coord2):
	api_query = get_api_query(units, travel_mode, coord1, coord2)
	response = query_api(api_query)
	parsed_response = parse_JSON(response)
	if parsed_response['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS':
		return 0
	else:
		distance = parsed_response['rows'][0]['elements'][0]['distance']['text'].split()[0]
	return distance


if __name__ == '__main__':

	sys.argv = sys.argv[1:]
	units = 'miles'
	travel_mode = 'default'
	try:
		opts, args = getopt.getopt(sys.argv, "hu:m:", ["units=", "mode="])
	except getopt.GetoptError:
		print('usage: vacationingsalesman.py -u <kilometers or miles>')
		sys.exit()

	for opt, arg in opts:
		if opt == '-h':
			print('usage: vacationingsalesman.py -u <kilometers or miles> -m <mode: driving, transit, walking, biking>')
			sys.exit()
		elif opt in ('-u', 'units='):
			units = arg
		elif opt in ('-m', 'mode='):
			travel_mode = arg

	cities_list = []
	for line in sys.stdin:
		line = line.replace('\n', '')
		cities_list.append(line)

	distances = find_distances(units, cities_list, travel_mode)
	print("Success! Your itinerary is: ")
	for i in range(len(distances)):
		if distances[i] == 0:
			print('Not feasible to travel from ' + cities_list[i] + ' -> ' + cities_list[i+1] + ' by ' + travel_mode)
		print(cities_list[i] + ' -> ' + cities_list[i+1] + ': ' + str(distances[i]) + ' ' + units)

	sys.exit()
