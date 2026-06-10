import requests, json, sys

url = "http://127.0.0.1:8000/api/predict"
img_path = "test_image.jpg"

with open(img_path,"rb") as f:
    files = {"image": f}
    try:
        r = requests.post(url, files=files, timeout=30)
    except Exception as e:
        print('ERROR', e)
        sys.exit(1)

print('STATUS', r.status_code)
try:
    print(r.text)
except Exception as e:
    print('ERROR printing response', e)
    print(r.content)
