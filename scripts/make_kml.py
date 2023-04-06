import sys, html, datetime

header = """<Style id="brown-sewer-normal">
      <IconStyle><color>ff485579</color><scale>1</scale><Icon><href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href></Icon></IconStyle>
      <LabelStyle><scale>0</scale></LabelStyle>
    </Style>
    <Style id="brown-sewer-highlight">
      <IconStyle><color>ff485579</color><scale>1</scale><Icon><href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href></Icon></IconStyle>
      <LabelStyle><scale>1</scale></LabelStyle>
    </Style>
    <StyleMap id="brown-sewer">
      <Pair><key>normal</key><styleUrl>#brown-sewer-normal</styleUrl></Pair>
      <Pair><key>highlight</key><styleUrl>#brown-sewer-highlight</styleUrl></Pair>
    </StyleMap>
    <Style id="amber-sewer-normal">
      <IconStyle><color>ff00b4f4</color><scale>1</scale><Icon><href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href></Icon></IconStyle>
      <LabelStyle><scale>0</scale></LabelStyle>
    </Style>
    <Style id="amber-sewer-highlight">
      <IconStyle><color>ff00b4f4</color><scale>1</scale><Icon><href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href></Icon></IconStyle>
      <LabelStyle><scale>1</scale></LabelStyle>
    </Style>
    <StyleMap id="amber-sewer">
      <Pair><key>normal</key><styleUrl>#amber-sewer-normal</styleUrl></Pair>
      <Pair><key>highlight</key><styleUrl>#amber-sewer-highlight</styleUrl></Pair>
    </StyleMap>
    <Style id="green-sewer-normal">
      <IconStyle><color>7CFC00</color><scale>1</scale><Icon><href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href></Icon></IconStyle>
      <LabelStyle><scale>0</scale></LabelStyle>
    </Style>
    <Style id="green-sewer-highlight">
      <IconStyle><color>7CFC00</color><scale>1</scale><Icon><href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href></Icon></IconStyle>
      <LabelStyle><scale>1</scale></LabelStyle>
    </Style>
    <StyleMap id="green-sewer">
      <Pair><key>normal</key><styleUrl>#green-sewer-normal</styleUrl></Pair>
      <Pair><key>highlight</key><styleUrl>#green-sewer-highlight</styleUrl></Pair>
    </StyleMap>
  """

footer = """  </Document>
</kml>"""

def make_placemark(name, description, longitude, latitude, style_url="#brown-sewer"):
    return f"<Placemark><name>{name}</name><description>{description}</description><styleUrl>{style_url}</styleUrl><Point><coordinates>{longitude},{latitude},0</coordinates></Point></Placemark>"

def process_timestamp(ts):
    month = str(int(ts[5:7]) - 1).zfill(2)
    return f'new Date({ts[0:4]},{month},{ts[8:10]},{ts[11:13]},{ts[14:16]},{ts[17:19]})'
                                                                                                                                      
#open alert history file in reverse
lines = list(open(sys.argv[1])) 

discharging_file = open(f"data/thames_discharging_{datetime.datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S')}.kml","w")
not_discharging_file = open(f"data/thames_not_discharging_{datetime.datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S')}.kml","w")
recently_discharging_file = open(f"data/thames_recently_discharging_{datetime.datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S')}.kml","w")

discharging_file.write(f'<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>discharging sewer outlets</name>{header}')
not_discharging_file.write(f'<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>not discharging sewer outlets</name>{header}')
recently_discharging_file.write(f'<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>recently discharging sewer outlets</name>{header}')

#ignore header
for line in reversed(lines[1:]):
    #read the location, state and time
    LocationName, PermitNumber, LocationGridRef, X, Y, LATITUDE, LONGITUDE, ReceivingWaterCourse, AlertStatus, AlertPast48Hours, MostRecentDischargeAlertStart, MostRecentDischargeAlertStop = line.strip().split("|")
    if AlertStatus == "Discharging":
      discharging_file.write(f'<Placemark><name>{html.escape(LocationName)}</name><description><p><b>{html.escape(AlertStatus)}</b></p><p>Discharging Started:{html.escape(MostRecentDischargeAlertStart)}</p></description><styleUrl>#brown-sewer</styleUrl><Point><coordinates>{LONGITUDE},{LATITUDE},0</coordinates></Point></Placemark>\n')
    elif AlertPast48Hours == "True":      
      recently_discharging_file.write(f'<Placemark><name>{html.escape(LocationName)}</name><description><p>{html.escape(AlertStatus)}</p><p>Recently Discharged:</p><p>Start: {html.escape(MostRecentDischargeAlertStart)} Stop: {html.escape(MostRecentDischargeAlertStop)}</p></description><styleUrl>#amber-sewer</styleUrl><Point><coordinates>{LONGITUDE},{LATITUDE},0</coordinates></Point></Placemark>\n')
    else:
      not_discharging_file.write(f'<Placemark><name>{html.escape(LocationName)}</name><description><p>{html.escape(AlertStatus)}</p></description><styleUrl>#green-sewer</styleUrl><Point><coordinates>{LONGITUDE},{LATITUDE},0</coordinates></Point></Placemark>\n')

discharging_file.write(footer)
not_discharging_file.write(footer)
recently_discharging_file.write(footer)