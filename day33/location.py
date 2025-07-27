import requests

# STATUS CODES

# 1XX: Hold on
# 2XX: Here you go
# 3XX: Go Away
# 4XX: You screwed up
# 5XX: I screwed up

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

data = response.json()

longitude = data['iss_position']['longitude']
latitude = data['iss_position']['latitude']

iss_position = (longitude, latitude)
print(iss_position)
