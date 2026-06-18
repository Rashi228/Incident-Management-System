import urllib.request
import json
import urllib.error

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODI0ODA2OTQsInN1YiI6ImYyYzVlYmMwLTFiMmMtNGU4OS04ZDgwLTVmMjEyN2ZjNjkxMiIsInJvbGUiOnsicm9sZSI6ImFkbWluIn19.RmcWY-G8U-z4yNFAcdOu60eP_wHYJDJkoVxPn3hhSxY"
data = json.dumps({"title": "Test", "content": "Test content", "category": "Software"}).encode('utf-8')
req = urllib.request.Request('https://ims-backend-z1in.onrender.com/api/v1/articles/', data=data, headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'})
try:
    res = urllib.request.urlopen(req)
    print(res.read())
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.read())
