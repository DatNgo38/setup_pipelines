import json
import requests as rq

f = open('piplines.json')

token = rq.post('http://localhost:8080/unidata-backend/api/core/authentication/login', json= {
    "userName": "admin",
    "password": "123456",
    "locale"  : "en"
}).json()["content"]["token"]
print(token)

url = 'http://localhost:8080/unidata-backend/api/core/system/pipeline'
headers = { 'Accept': 'application/json',
            'Authorization': token,
            'Content-Type': 'application/json'}
data = json.load(f)

numSuccess = 0
numError = 0
for i in data['pipelines']:
    response = rq.post(url, headers, json.dumps(i))
    if response.status_code == '500' and response.status_code == '401':
        numError = numError + 1
        print(i)
    else:
        numSuccess = numSuccess + 1

print(numSuccess)
print(numError)
f.close()