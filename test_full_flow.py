import urllib.request
import urllib.parse
import json
import urllib.error

# 1. Login
data = urllib.parse.urlencode({'username': 'admin@company.com', 'password': 'admin123'}).encode('ascii')
req = urllib.request.Request('https://ims-backend-z1in.onrender.com/api/v1/auth/login', data=data)
try:
    res = urllib.request.urlopen(req)
    token_data = json.loads(res.read())
    token = token_data['access_token']
    print("Logged in successfully!")
except urllib.error.HTTPError as e:
    print("Login failed:", e.code, e.read())
    exit(1)

# 2. Post Article
article_data = json.dumps({
    "title": "Test Title",
    "content": "This is a test content that is definitely long enough to pass validation in the backend schema.",
    "category": "Software"
}).encode('utf-8')

req2 = urllib.request.Request(
    'https://ims-backend-z1in.onrender.com/api/v1/articles/', 
    data=article_data, 
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
)

try:
    res2 = urllib.request.urlopen(req2)
    print("Post successful!", res2.read())
except urllib.error.HTTPError as e:
    print("Post failed:", e.code)
    print(e.read())
