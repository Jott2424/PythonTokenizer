import requests
from requests.auth import HTTPBasicAuth

API_URL = "http://localhost:5000"
AUTH = HTTPBasicAuth("admin", "changeme")

resp = requests.post(
    f"{API_URL}/encrypt",
    json={"data": "this is a really big string", "key": "encryption"},
    auth=AUTH
)
print("Single encrypted:", resp.json())

batch = ["value13", "value2", "value3"]
resp = requests.post(
    f"{API_URL}/batch_encrypt",
    json={"data": batch, "key": "encryption"},
    auth=AUTH
)
print("Batch encrypted:", resp.json())