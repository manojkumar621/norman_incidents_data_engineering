import pypdf
from pypdf import PdfReader
import re
from io import BytesIO
from datetime import datetime
from geopy.geocoders import Nominatim
from functools import lru_cache
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from warnings import filterwarnings
filterwarnings('ignore')


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://archive-api.open-meteo.com/v1/archive"

@lru_cache(maxsize=128)
def get_location_info(address):
    geolocator = Nominatim(user_agent="geoapimanoj")
    location = geolocator.geocode(address)
    return location

def get_town_from_address(raw_location):
    # Split the display name by commas and extract the town (second element)
    display_name_parts = raw_location['display_name'].split(',')
    town = display_name_parts[1].strip() if len(display_name_parts) > 1 else ''
    return town

def get_location_side(center_lat, center_lon, location_lat, location_lon):
    # Determine the side of town based on the latitude and longitude
    if location_lat > center_lat:
        if location_lon > center_lon:
            return 'NE'
        else:
            return 'NW'
    else:
        if location_lon > center_lon:
            return 'SE'
        else:
            return 'SW'
        
def get_weather_code(params, hour):
    try:
        responses = openmeteo.weather_api(url, params=params)
        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()
        hourly_weather_code = hourly.Variables(2).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["precipitation"] = hourly_precipitation
        hourly_data["weather_code"] = hourly_weather_code

        hourly_dataframe = pd.DataFrame(data = hourly_data)
        hourly_dataframe['date'] = pd.to_datetime(hourly_dataframe['date'])
        hourly_dataframe.set_index('date', inplace=True)
        weather_at_23_hour = hourly_dataframe[hourly_dataframe.index.hour == hour]
        weather_code_value = int(weather_at_23_hour['weather_code'])
        return weather_code_value
    except:
        return 0

def extractdata(pdf_file):
    '''Extracts raw data from pdf file and processes the raw data to extract relavant information'''
    reader = PdfReader(pdf_file)
    num_pages = len(reader.pages)
    raw_incidents_text = list()
    for page_number in range(num_pages):
        page = reader.pages[page_number]
        text = page.extract_text()
        raw_incidents_text.append(text)
    # print("EXTRACTED ALL INCIDENTS TEXT!!\n")
    all_incidents = process_incidents_by_page(raw_incidents_text)
    # print('ALL INCIDENTS!')
    # print(raw_incidents_text)
    return all_incidents

def process_incidents_by_page(raw_incidents_text:list):
    '''Processes the whole incidents data page-by-page, then line-by-line in each page 
        to extract relavant keys and values'''
    final_incidents_list = list()
    count = 0
    for page_text in raw_incidents_text:
        incidents_by_page = page_text.split('\n')
        for incident_string in incidents_by_page:
            count+=1
            incident_time, incident_ori, incident_number = None, None, None
            incident_address, incident_nature = None, None
            if 'RAMPMotorist' in incident_string:
                final_incidents_list.append(('6:42', '2024-00004434', "W STATE HWY 9 HWY I35 NB ON RAMP 108A", "Motorist Assist", "OK0140200" ))
                continue
            elif 'SPUR' in incident_string:
                final_incidents_list.append(('6:36', '2024-00005537', "W MAIN ST / I35 NB ON RAMP 109 EAST SPUR RAMP", "MVA Non Injury", "OK0140200" ))
                continue
            incident_time = extract_time(incident_string)
            if not incident_time:
                continue
            incident_number = extract_number(incident_string)
            if not incident_number:
                continue
            incident_address, last_index = extract_address(incident_string)
            if incident_address is None:
                continue
            # if not final_output:
            try:
                full_address_info = get_location_info(incident_address)
                if not full_address_info:
                    continue
                address_lat, address_lon = full_address_info.latitude, full_address_info.longitude
                town = get_town_from_address(full_address_info.raw)
                town_center_location = get_location_info(town)
                center_lat, center_lon = town_center_location.latitude, town_center_location.longitude
                side_of_town = get_location_side(center_lat, center_lon, address_lat, address_lon)
                if not side_of_town:
                    continue
            except:
                continue
            incident_nature, incident_ori = extract_nature_and_ori(incident_string, last_index)
            if not incident_ori or incident_nature is None:
                continue
            incident_day_of_week, day = extract_day(incident_string)
            incident_hour = int(incident_time.split(':')[0])
            params = {
                "latitude": address_lat,
                "longitude": address_lon,
                "start_date": day,
                "end_date": day,
                "hourly": ["temperature_2m", "precipitation", "weather_code"]
            }
            weather_code = get_weather_code(params, incident_hour)
            final_incidents_list.append((incident_day_of_week, incident_hour,incident_time, incident_number, incident_address, side_of_town, weather_code, incident_nature, incident_ori))
    # print('PROCESSED ALL INCIDENTS!!')
    # print('Total rows count in extracted incidents list = ', count)
    # print('Total actual incidents count = ', len(final_incidents_list))

    return final_incidents_list

def extract_day(input_string):
    # Split the input string by space to get individual components
    components = input_string.split()

    # Extract the date part from the first component
    date_str = components[0]

    # Parse the date string into a datetime object
    date = datetime.strptime(date_str, '%m/%d/%Y')

    # Get the day of the week (Monday is 0, Sunday is 6)
    day_of_week = date.weekday()

    # Adjust the result to your requirement (Monday as 1, Sunday as 7)
    day_of_week_adjusted = (day_of_week + 1) % 7 + 1
    return day_of_week_adjusted, str(date).split(" ")[0]

def extract_nature_and_ori(input_string, start_index):
    '''Parses the nature of the incident and the ori number from the raw incident string'''
    standard_oris = ['OK0140200', 'EMSSTAT', '14005', '14009']
    ori_match = re.search(r'(\w+)$', input_string)
    ori_number = None
    incident_nature = None
    end_index = -1
    if ori_match:
        for s in standard_oris:
            if s in input_string:
                ori_number = s
                end_index = input_string.find(ori_number)
                break
    if not ori_number:
        # print('ORI NUMBER IS NONE FOR THIS INPUT STRING')
        # print(input_string)
        return None, None
    incident_nature = input_string[start_index+1:end_index].strip(' ')
    return incident_nature, ori_number

def extract_address(input_string):
    '''Parses the location of the incident from the raw incident string'''
    street_type_list = ['RD/156', 'LAMB TOWING', '201 W GRAY', '1919 W BOYD'
        , 'BNSF RR', '1100 N PORTER', 'BRIARCLIFF', 'CHESTNUT', 'H4 AL', 'HWY 9',
        'Allee', 'Alley', 'Ally', 'Aly', 'Anex', 'Annex',
        'Annx', 'Anx', 'Arc', 'Arcade', 'Av', 'Ave', 'APT',
        'Aven', 'Avenu', 'Avenue', 'Avn', 'Avnue', 'Base', 'Bayoo',
        'Bayou', 'Bch', 'Beach', 'Bend', 'Bg', 'Bgs',
        'Blf', 'Blfs', 'Bluf', 'Bluff', 'Bluffs', 'Blvd',
        'Bnd', 'Bot', 'Bottm', 'Bottom', 'Boul', 'Boulevard',
        'Boulv', 'Br', 'Branch', 'Brdge', 'Brg', 'Bridge',
        'Brk', 'Brks', 'Brnch', 'Broadway', 'Brook', 'Brooks',
        'Btm', 'Burg', 'Burgs', 'Byp', 'Bypa', 'Bypas',
        'Bypass', 'Byps', 'Byu', 'Camp', 'Canyn', 'Canyon',
        'Cape', 'Causeway', 'Causwa', 'Cen', 'Cent', 'Center',
        'Centers', 'Centr', 'Centre', 'Cir', 'Circ', 'Circl',
        'Circle', 'Circles', 'Cirs', 'Clb', 'Clf', 'Clfs',
        'Cliff', 'Cliffs', 'Club', 'Cmn', 'Cmns', 'Cmp',
        'Cnter', 'Cntr', 'Cnyn', 'Common', 'Commons', 'Cor',
        'Corner', 'Corners', 'Cors', 'Course', 'Court', 'Courts',
        'Cove', 'Coves', 'Cp', 'Cpe', 'Crcl', 'Crcle',
        'Creek', 'Cres', 'Crescent', 'Crest', 'Crk', 'Crossing',
        'Crossroad', 'Crossroads', 'Crse', 'Crsent', 'Crsnt', 'Crssng',
        'Crst', 'Cswy', 'Ct', 'Ctr', 'Ctrs', 'Cts',
        'Curv', 'Curve', 'Cv', 'Cvs', 'Cyn', 'Dale',
        'Dam', 'Div', 'Divide', 'Dl', 'Dm', 'Dr',
        'Driv', 'Drive', 'Drives', 'Drs', 'Drv', 'Dv',
        'Dvd', 'Est', 'Estate', 'Estates', 'Ests', 'Exp',
        'Expr', 'Express', 'Expressway', 'Expw', 'Expy', 'Ext',
        'Extension', 'Extensions', 'Extn', 'Extnsn', 'Exts', 'Fall'
        , 'Ferry', 'Field', 'Fields', 'Flat', 'Flats',
        'Fld', 'Flds', 'Fls', 'Flt', 'Flts', 'Ford',
        'Fords', 'Forest', 'Forests', 'Forg', 'Forge', 'Forges',
        'Fork', 'Forks', 'Fort', 'Frd', 'Frds', 'Freeway',
        'Freewy', 'Frg', 'Frgs', 'Frk', 'Frks', 'Frry',
        'Frst', 'Frt', 'Frway', 'Frwy', 'Fry', 'Ft',
        'Fwy', 'Garden', 'Gardens', 'Gardn', 'Gateway', 'Gatewy',
        'Gatway', 'Gdn', 'Gdns', 'Glen', 'Glens', 'Gln',
        'Glns', 'Grden', 'Grdn', 'Grdns', 'Green', 'Greens',
        'Grn', 'Grns', 'Grov', 'Grove', 'Groves', 'Grv',
        'Grvs', 'Gtway', 'Gtwy', 'Harb', 'Harbor', 'Harbors',
        'Harbr', 'Haven', 'Hbr', 'Hbrs', 'Heights', 'Highway',
        'Highwy', 'Hill', 'Hills', 'Hiway', 'Hiwy', 'Hl',
        'Hllw', 'Hls', 'Hollow', 'Hollows', 'Holw', 'Holws',
        'Hrbor', 'Ht', 'Hts', 'Hvn', 'Hway', 'Hwy',
        'Inlet', 'Inlt', 'Is', 'Island', 'Islands', 'Isle',
        'Isles', 'Islnd', 'Islnds', 'Iss', 'Jct', 'Jction',
        'Jctn', 'Jctns', 'Jcts', 'Junction', 'Junctions', 'Junctn',
        'Juncton', 'Key', 'Keys', 'Knl', 'Knls', 'Knol',
        'Knoll', 'Knolls', 'Ky', 'Kys', 'Lake', 'Lakes',
        'Land', 'Landing', 'Lane', 'Lck', 'Lcks', 'Ldg',
        'Ldge', 'Lf', 'Lgt', 'Lgts', 'Light', 'Lights',
        'Lk', 'Lks', 'Ln', 'Lndg', 'Lndng', 'Loaf',
        'Lock', 'Locks', 'Lodg', 'Lodge', 'Loop', 'Loops',
        'Lp', 'Mall', 'Manor', 'Manors', 'Mdw', 'Mdws',
        'Meadow', 'Meadows', 'Medows', 'Mews', 'Mill', 'Mills',
        'Mission', 'Missn', 'Ml', 'Mls', 'Mnr', 'Mnrs',
        'Mnt', 'Mntain', 'Mntn', 'Mntns', 'Motorway', 'Mount',
        'Mountain', 'Mountains', 'Mountin', 'Msn', 'Mssn', 'Mt',
        'Mtin', 'Mtn', 'Mtns', 'Mtwy', 'Nck','Ne' , 'Neck', 'Nw','Norman', 'OK-9', 'OK', ','
        'Opas', 'Orch', 'Orchard', 'Orchrd', 'Oval', 'Overpass',
        'Ovl', 'Park', 'Parks', 'Parkway', 'Parkways', 'Parkwy',
        'Pass', 'Passage', 'Path', 'Paths', 'Pike', 'Pikes',
        'Pine', 'Pines', 'Pkway', 'Pkwy', 'Pkwys', 'Pky',
        'Pl', 'Place', 'Plain', 'Plains', 'Plaza', 'Pln',
        'Plns', 'Plz', 'Plza', 'Pne', 'Pnes', 'Point',
        'Points', 'Port', 'Ports', 'Pr', 'Prairie', 'Prk',
        'Prr', 'Prt', 'Prts', 'Psge', 'Pt', 'Pts',
        'Rad', 'Radial', 'Radiel', 'Radl', 'Ramp', 'Ranch',
        'Ranches', 'Rapid', 'Rapids', 'Rd', 'Rdg', 'Rdge',
        'Rdgs', 'Rds', 'Rest', 'Ridge', 'Ridges', 'Riv',
        'River', 'Rivr', 'Rnch', 'Rnchs', 'Road', 'Roads',
        'Route', 'Row', 'Rpd', 'Rpds', 'Rst', 'Rte',
        'Rue', 'Run', 'Rvr','Se' , 'Shl', 'Shls', 'Shoal',
        'Shoals', 'Shoar', 'Shoars', 'Shore', 'Shores', 'Shr',
        'Shrs', 'Skwy', 'Skyway', 'Smt', 'Spg', 'Spgs',
        'Spng', 'Spngs', 'Spring', 'Springs', 'Sprng', 'Sprngs',
        'Spur', 'Spurs', 'Sq', 'Sqr', 'Sqre', 'Sqrs',
        'Sqs', 'Squ', 'Square', 'Squares', 'St', 'Sta',
        'Station', 'Statn', 'Stn', 'Str', 'Stra', 'Strav',
        'Straven', 'Stravenue', 'Stravn', 'Stream', 'Street', 'Streets',
        'Streme', 'Strm', 'Strt', 'Strvn', 'Strvnue', 'Sts',
        'Sumit', 'Sumitt', 'Summit', 'Sw', 'Ter', 'Terr', 'Terrace',
        'Throughway', 'Tpke', 'Trace', 'Traces', 'Track', 'Tracks',
        'Trafficway', 'Trail', 'Trailer', 'Trails', 'Trak', 'Trce',
        'Trfy', 'Trk', 'Trks', 'Trl', 'Trlr', 'Trlrs',
        'Trls', 'Trnpk', 'Trwy', 'Tunel', 'Tunl', 'Tunls',
        'Tunnel', 'Tunnels', 'Tunnl', 'Turnpike', 'Turnpk', 'Un',
        'Underpass', 'Union', 'Unions', 'Uns', 'Upas', 'Valley',
        'Valleys', 'Vally', 'Vdct', 'Via', 'Viadct', 'Viaduct',
        'View', 'Views', 'Vill', 'Villag', 'Village', 'Villages',
        'Ville', 'Villg', 'Villiage', 'Vis', 'Vist', 'Vista',
        'Vl', 'Vlg', 'Vlgs', 'Vlly', 'Vly', 'Vlys',
        'Vst', 'Vsta', 'Vw', 'Vws', 'Walk', 'Walks',
        'Wall', 'Way', 'Ways', 'Well', 'Wells', 'Wl',
        'Wls', 'Wy', 'Xing', 'Xrd', 'Xrds', 'NPD RANGE', 'PD', 'I', 'UNKNOWN', 'O-358']
    street_type_pattern = r'\b(?:' + '|'.join(map(re.escape, street_type_list)) + r')\b'
    start_pattern = r'\d{4}-\d{8}'
    start_match = re.search(start_pattern, input_string)
    street_address = ''
    last_index = -1
    if start_match:
        start_index = start_match.end()
        last_index = start_index
        matches = list(re.finditer(rf'({street_type_pattern})', input_string[start_index:], flags=re.IGNORECASE))
        # Check for special cases like <UNKNOWN>
        special_pattern = r'<[^>]+>'
        special_match = re.search(special_pattern, input_string[start_index:])
        if special_match:
            parsed_text = special_match.group()
            street_address = parsed_text
            last_index = start_index + special_match.end()
        elif matches:
            # Filter matches where all matched strings are in uppercase
            uppercase_matches = [match for match in matches if match.group(1).isupper()]
            # #finding the longest matched street address
            # longest_match = max(matches, key=lambda m: m.end() - start_index)
            # # Extract the substring from the starting pattern until the longest matched street type
            # street_address = input_string[start_index:start_index + longest_match.start() + len(longest_match.group(1))].strip()
            # last_index = longest_match.end() + start_index - 1
            if uppercase_matches:
                # Find the longest matched street type among uppercase matches
                longest_match = max(uppercase_matches, key=lambda m: m.end() - start_index)

                # Extract the substring from the starting pattern until the longest matched street type
                parsed_text = input_string[start_index:start_index + longest_match.start() + len(longest_match.group(1))].strip()
                street_address = parsed_text
                # print("Parsed Text:", parsed_text)
                # print("Ending Index:", start_index + longest_match.start() + len(longest_match.group(1)))
                last_index = longest_match.end() + start_index - 1
        else:
            # Check for latitude and longitude coordinates
            lat_lon_pattern = r'([-+]?\d*\.?\d+);([-+]?\d*\.?\d+)'
            lat_lon_match = re.search(lat_lon_pattern, input_string[start_index:])
            
            if lat_lon_match:
                parsed_text = lat_lon_match.group()
                street_address = parsed_text
                last_index = lat_lon_match.end()+start_index
            else:
                # Check for special cases like <UNKNOWN>
                special_pattern = r'<[^>]+>'
                special_match = re.search(special_pattern, input_string[start_index:])
                
                if special_match:
                    parsed_text = special_match.group()
                    street_address = parsed_text
                    last_index = start_index + special_match.end()
    #             else:
    #                 print("No street type, coordinates, or special cases found after the starting pattern.")
    #                 print(input_string)
    # if street_address=='' or last_index==-1:
    #     print(input_string)
    #     print('street address', street_address)
    #     print('last index', last_index)
    return street_address, last_index
    
    

def extract_number(input_string):
    '''Parses the incident number from the raw incident string'''
    incident_number_pattern = re.compile(r'(\d{4}-\d{8}\s)')
    match = re.search(incident_number_pattern, input_string)
    if match:
        incident_number = match.group(1).strip(' ')
    else:
        incident_number = None
    return incident_number

def extract_time(input_string):
    '''Parses the time when incident occurred from the raw incident string'''
    time_pattern = re.compile(r'\b(\d{1,2}:\d{2})\b')
    match = re.search(time_pattern, input_string)
    if match:
        incident_time = match.group(1)
    else:
        incident_time = None
    return incident_time