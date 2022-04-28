import json
import requests as rq
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
local_ip_address = s.getsockname()[0]

print(local_ip_address)

f = open('piplines.json')

token = rq.post('http://' + local_ip_address + ':8080/unidata-backend/api/core/authentication/login', json= {
    "userName": "admin",
    "password": "123456",
    "locale"  : "en"
}).json()["content"]["token"]
print(token)

url = 'http://' + local_ip_address + ':8080/unidata-backend/api/core/system/pipeline'
headers = { 'Accept': 'application/json',
            'Authorization': token,
            'Content-Type': 'application/json'}
data = json.load(f)

numSuccess = 0
numError = 0
for i in data['pipelines']:
    i = json.dumps(i)
    response = rq.post(url=url, headers=headers, json=i)
    print(response.status_code)
    if response.status_code == 500:
        numError = numError + 1
    else:
        numSuccess = numSuccess + 1

print(numSuccess)
print(numError)
f.close()