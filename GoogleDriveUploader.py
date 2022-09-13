import json
import requests
headers = {"Authorization": "Bearer ###youraccesstoken###"}
para = {
    "name": "Meet My Son Krishiv Naik @Krishiv Naik Vlogs.3gpp",
    "parents": ["1JSFwH6zicMLR3uEQC6JPu0In04EpO_Y9"]
}
files = {
    'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
    'file': ('application/3gpp',open("./dl.zip", "rb"))
}
r = requests.post(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    headers=headers,
    files=files
)
print(r.text)