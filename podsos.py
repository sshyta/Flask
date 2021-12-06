import requests
import json
import sys

params = {
    'dev_eui': '393935347B386F14',
    'fport': '2',
    'start_date': '2019-4-26',
    'end_date': '2021-11-26',
    'empty': 'false',
    'utc': 'false',
    'limit': '1000',
    'offset': '0',
    'page': '5',
    'dir': 'up',
}


response_API = requests.get("https://server.air-bit.eu/api/data/", params=params)
print(response_API.status_code)
data = response_API.text
parse_json = json.loads(data)
active_case = parse_json['0']['data']['1']['data']
print("data cases in 0", active_case)

# import requests
# import json
# response_API = requests.get('https://api.covid19india.org/state_district_wise.json')
# #print(response_API.status_code)
# data = response_API.text
# parse_json = json.loads(data)
# active_case = parse_json['Andaman and Nicobar Islands']['districtData']['South Andaman']['active']
# print("Active cases in South Andaman:", active_case)
