# egest
format friendly data dumps about rivers and sewers

## directories
/scripts
this is where the scripts are that go and get the data and make it usable

### scripts
get_discharge_alerts_by_location.py
works with the Thames API to get discharge sites, current status and history
produces two files (actually four files because it creates a timestamped version)
- locations_with_current_status.csv
- alerts_history.csv
functional but could do with a tidy up

calculate_summary_information.py
produces a file with calculations on the length of time that each location was in a particular state 

get_lat_lon.py
gets the latitude and longitude for a given northing and easting - this makes it usable with things like google maps
needs a tidy up

make_visual.py
creates a timeline 
/data
were the useful output is stored
/data/archive
archive of previous executions