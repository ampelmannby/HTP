
import json
import requests

webhook_url = 'https://www.ampelmann.by:5000'

data = { 'name': 'KBZ',
         'age': 41}

r = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'applocation/json'})

