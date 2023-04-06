import datetime, time, sys
current_location = ""
current_alert_type = ""
current_timestamp = 0

file_headers = f"LocationName|PermitNumber|LocationGridRef|X|Y|LATITUDE|LONGITUDE|ReceivingWaterCourse|event|start|end|duration(hh:mm:ss)|duration in seconds\n"
alerts_file = open(f"../data/processed_alerts_history.csv","w")
alerts_archive_file = open(f"../data/archive/processed_alerts_history_{datetime.datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S')}.csv","w")
alerts_file.write(file_headers)
alerts_archive_file.write(file_headers)

#open alert history file in reverse
lines = list(open(sys.argv[1]))
#ignore header
for line in reversed(lines[1:]):
    #read the location, state and time
    location_name, license_ref, grid_ref,X,Y,LATITUDE,LONGITUDE,ReceivingWaterCourse,alert_type,timestamp = line.strip().split("|")
    #if location field is not the same as current location then set the current location, alert status and time and read new line
    if location_name != current_location:
        if current_alert_type == 'Start':
            event = "discharge"
            now = datetime.datetime.strptime(datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00'),'%Y-%m-%dT%H:%M:%S')
            ts = datetime.datetime.strptime(current_timestamp,'%Y-%m-%dT%H:%M:%S')
            duration = now - ts
            hours = duration.seconds//3600 + (duration.days*24)
            minutes = (duration.seconds%3600)//60
            seconds = (duration.seconds%3600)%60
            #have a column with total time in seconds
            total_seconds = duration.seconds + duration.days*86400
            #must be still discharging...
            output = f"{current_location}|{current_license_ref}|{current_grid_ref}|{current_X}|{current_Y}|{current_LATITUDE}|{current_LONGITUDE}|{current_ReceivingWaterCourse}|{event}|{ts}|{now}|{hours}:{minutes}:{seconds}|{total_seconds}\n"
            alerts_file.write(output)
            alerts_archive_file.write(output)
        elif current_alert_type == 'Offline start':
            event = "offline"
            now = datetime.datetime.strptime(datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00'),'%Y-%m-%dT%H:%M:%S')
            ts = datetime.datetime.strptime(current_timestamp,'%Y-%m-%dT%H:%M:%S')
            duration = now - ts
            hours = duration.seconds//3600 + (duration.days*24)
            minutes = (duration.seconds%3600)//60
            seconds = (duration.seconds%3600)%60
            #have a column with total time in seconds
            total_seconds = duration.seconds + duration.days*86400
            #must be still offline...
            output = f"{current_location}|{current_license_ref}|{current_grid_ref}|{current_X}|{current_Y}|{current_LATITUDE}|{current_LONGITUDE}|{current_ReceivingWaterCourse}|{event}|{ts}|{now}|{hours}:{minutes}:{seconds}|{total_seconds}\n"
            alerts_file.write(output)
            alerts_archive_file.write(output)
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
                event = "discharge"
                ts = datetime.datetime.strptime(timestamp,'%Y-%m-%dT%H:%M:%S')
                current_ts = datetime.datetime.strptime(current_timestamp,'%Y-%m-%dT%H:%M:%S')
                duration = ts - current_ts
                hours = duration.seconds//3600 + (duration.days*24)
                minutes = (duration.seconds%3600)//60
                seconds = (duration.seconds%3600)%60
                #have a column with total time in seconds
                total_seconds = duration.seconds + duration.days*86400
                output = f"{location_name}|{license_ref}|{grid_ref}|{X}|{Y}|{LATITUDE}|{LONGITUDE}|{ReceivingWaterCourse}|{event}|{current_timestamp}|{timestamp}|{hours}:{minutes}:{seconds}|{total_seconds}\n"
                alerts_file.write(output)
                alerts_archive_file.write(output)
                current_alert_type = alert_type
                current_timestamp = timestamp 
            else:
                print(f"unexpected state change: {line}")
                current_alert_type = alert_type
                current_timestamp = timestamp
        elif alert_type == 'Offline stop':
            if current_alert_type == 'Offline start':
                event = "offline"
                duration = datetime.datetime.strptime(timestamp,'%Y-%m-%dT%H:%M:%S') - datetime.datetime.strptime(current_timestamp,'%Y-%m-%dT%H:%M:%S')
                hours = duration.seconds//3600 + (duration.days*24)
                minutes = (duration.seconds%3600)//60
                seconds = (duration.seconds%3600)%60
                #have a column with total time in seconds
                total_seconds = duration.seconds + duration.days*86400
                output = f"{location_name}|{license_ref}|{grid_ref}|{X}|{Y}|{LATITUDE}|{LONGITUDE}|{ReceivingWaterCourse}|{event}|{current_timestamp}|{timestamp}|{hours}:{minutes}:{seconds}|{total_seconds}\n"
                alerts_file.write(output)
                alerts_archive_file.write(output)
                current_alert_type = alert_type
                current_timestamp = timestamp 
            else:
                print(f"unexpected state change: {line}")
                current_alert_type = alert_type
                current_timestamp = timestamp