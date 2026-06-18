import urllib.request
import urllib.error

req = urllib.request.Request('https://ims-backend-z1in.onrender.com/api/v1/articles/', method='GET')
try:
    res = urllib.request.urlopen(req)
    print(res.read())
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.read())
