import requests, sys, json, datetime

client_id = sys.argv[1]
client_secret = sys.argv[2]

#need to not include this in anything shared
headers = {"client_id": client_id, "client_secret": client_secret}

url_stem = "https://prod-tw-opendata-app.uk-e1.cloudhub.io/data/STE/v1"
#date filter
more_recent_than = "2020-12-31"
locations_file_headers = f"LocationName|PermitNumber|LocationGridRef|X|Y|LATITUDE|LONGITUDE|ReceivingWaterCourse|AlertStatus|AlertPast48Hours|MostRecentDischargeAlertStart|MostRecentDischargeAlertStop\n"
locations_file = open(f"data/locations_with_current_status.csv","w")
locations_archive_file = open(f"data/archive/locations_with_current_status_{datetime.datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S')}.csv","w")
locations_file.write(locations_file_headers)
locations_archive_file.write(locations_file_headers)

alerts_file_headers = f"LocationName|PermitNumber|LocationGridRef|X|Y|LATITUDE|LONGITUDE|ReceivingWaterCourse|AlertType|DateTime\n"
alerts_file = open(f"data/alerts_history.csv","w")
alerts_archive_file = open(f"data/archive/alerts_history_{datetime.datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S')}.csv","w")
alerts_file.write(alerts_file_headers)
alerts_archive_file.write(alerts_file_headers)

discharge_current_status_url = f"{url_stem}/DischargeCurrentStatus"

discharge_current_status_response = requests.get(url=discharge_current_status_url,headers=headers)
discharge_current_status_json_data = json.loads(discharge_current_status_response.text)

for item in discharge_current_status_json_data['items']:
    #get the latitude and longitude
    lat_lon_url = f"https://webapps.bgs.ac.uk/data/webservices/CoordConvert_LL_BNG.cfc?method=BNGtoLatLng&easting={item['X']}&northing={item['Y']}"
    lat_lon_response = requests.get(url=lat_lon_url)
    lat_lon_json_data = json.loads(lat_lon_response.text)
        #write out to the locations file
    output = f"{item['LocationName']}|{item['PermitNumber']}|{item['LocationGridRef']}|{item['X']}|{item['Y']}|{lat_lon_json_data['LATITUDE']}|{lat_lon_json_data['LONGITUDE']}|{item['ReceivingWaterCourse']}|{item['AlertStatus']}|{item['AlertPast48Hours']}|{item['MostRecentDischargeAlertStart']}|{item['MostRecentDischargeAlertStop']}\n"
    locations_file.write(output)
    locations_archive_file.write(output)
    #get the alerts
    discharge_alerts_url = f"{url_stem}/DischargeAlerts?limit=1000&col_1=LocationName&operand_1=eq&value_1={item['LocationName']}"
    discharge_alerts_response = requests.get(url=discharge_alerts_url,headers=headers)
    discharge_alerts_json_data = json.loads(discharge_alerts_response.text)
    if 'items' in discharge_alerts_json_data:
        for alert_item in discharge_alerts_json_data['items']:
            output = f"{item['LocationName']}|{item['PermitNumber']}|{item['LocationGridRef']}|{item['X']}|{item['Y']}|{lat_lon_json_data['LATITUDE']}|{lat_lon_json_data['LONGITUDE']}|{item['ReceivingWaterCourse']}|{alert_item['AlertType']}|{alert_item['DateTime']}\n"
            alerts_file.write(output)
            alerts_archive_file.write(output)