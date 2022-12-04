import requests
import time
from time import sleep
import random

url = "http://localhost:9696/predict"

client = {"reports": 0, "share": 0.245, "expenditure": 3.438, "owner": "yes"}
response = requests.post(url, json=client).json()

print(response)

while True:
    sleep(0.01)
    val = random.random()*10.
    client = {"reports": 0, "share": 0.245, "expenditure": val, "owner": "yes"}
    response = requests.post(url, json=client).json()
    print(response)
