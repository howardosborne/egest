import datetime, time, sys
current_location = ""
current_alert_type = ""
current_timestamp = 0

header = """<div id="location_alerts" style="height: 100%; width: 100%;"></div>

<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

<script type="text/javascript">
  google.charts.load("current", {packages:["timeline"]});
  google.charts.setOnLoadCallback(drawChart);
  function drawChart() {
    var container = document.getElementById('location_alerts');
    var chart = new google.visualization.Timeline(container);
    var dataTable = new google.visualization.DataTable();
    dataTable.addColumn({ type: 'string', id: 'Location' });
    dataTable.addColumn({ type: 'string', id: 'Event' });
    dataTable.addColumn({ type: 'string', id: 'style', role: 'style' });
    dataTable.addColumn({ type: 'string', role: 'tooltip' });
    dataTable.addColumn({ type: 'date', id: 'Start' });
    dataTable.addColumn({ type: 'date', id: 'End' });
    dataTable.addRows(["""

footer = """]);
    chart.draw(dataTable, options);
  }
</script>"""
body = []

def process_timestamp(ts):
    month = str(int(ts[5:7]) - 1).zfill(2)
    return f'new Date({ts[0:4]},{month},{ts[8:10]},{ts[11:13]},{ts[14:16]},{ts[17:19]})'
                                                                                                                                      
#open alert history file in reverse
lines = list(open(sys.argv[1]))
#ignore header
for line in reversed(lines[1:]):
    #read the location, state and time
    location_name, license_ref, grid_ref,X,Y,LATITUDE,LONGITUDE,ReceivingWaterCourse,alert_type,timestamp = line.strip().split("|")
    #if location field is not the same as current location then set the current location, alert status and time and read new line
    if location_name != current_location:
        if current_alert_type == 'Start':
            now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
            #must be still discharging...
            body.append(f'["{current_location}", "", "#603913", "discharging {current_timestamp} to {now}", {process_timestamp(current_timestamp)}, {process_timestamp(now)}]')
        elif current_alert_type == 'Offline start':
            now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
            #must be still offline...
            body.append(f'["{current_location}", "", "#cbb69d", "offline {current_timestamp} to {now}", {process_timestamp(current_timestamp)}, {process_timestamp(now)}]')
        current_location = location_name
        current_license_ref = license_ref
        current_grid_ref = grid_ref
        current_X = X
        current_Y = Y
        current_LATITUDE = LATITUDE
        current_LONGITUDE = LONGITUDE
        current_ReceivingWaterCourse = ReceivingWaterCourse
        current_alert_type = alert_type
        current_timestamp = timestamp
    else:
        if alert_type == 'Start':
            if current_alert_type in ['Stop', 'Offline stop']:
                current_alert_type = alert_type
                current_timestamp = timestamp 
            else:
                print(f"unexpected state change: {line}")
        elif alert_type == 'Offline start':
            if current_alert_type in ['Stop', 'Offline stop']:
                current_alert_type = alert_type
                current_timestamp = timestamp
            else:
                print(f"unexpected state change: {line}")
        elif alert_type == 'Stop':
            if current_alert_type == 'Start':
                body.append(f'["{current_location}", "", "#603913", "discharging {current_timestamp} to {timestamp}", {process_timestamp(current_timestamp)}, {process_timestamp(timestamp)}]')
                current_alert_type = alert_type
                current_timestamp = timestamp 
            else:
                print(f"unexpected state change: {line}")
                current_alert_type = alert_type
                current_timestamp = timestamp
        elif alert_type == 'Offline stop':
            if current_alert_type == 'Offline start':
                body.append(f'["{current_location}", "", "#cbb69d", "offline {current_timestamp} to {timestamp}", {process_timestamp(current_timestamp)}, {process_timestamp(timestamp)}]')
                current_alert_type = alert_type
                current_timestamp = timestamp 
            else:
                print(f"unexpected state change: {line}")
                current_alert_type = alert_type
                current_timestamp = timestamp
print(header)

print(",\n".join(reversed(body)))
print(footer)