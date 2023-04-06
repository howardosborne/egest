import requests, sys, json
#example
#easting = 523040
#northing = 178150
easting = sys.argv[1]
northing = sys.argv[2]

url = f'https://webapps.bgs.ac.uk/data/webservices/CoordConvert_LL_BNG.cfc?method=BNGtoLatLng&easting={easting}&northing={northing}'

response = requests.get(url=url)
json_data = json.loads(response.text)
#print(f"{json_data}")
print(f"{json_data['LATITUDE']}, {json_data['LONGITUDE']}")