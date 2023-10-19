import os
from dotenv import load_dotenv

from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus

import pandas as pd
#from pandas.io.json import json_normalize
import json

load_dotenv()
os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'
openai_api_key = os.getenv("OPENAI_API_KEY")
kmaps_service_key = os.getenv("KMAPS_API_KEY")

url = "http://112.155.255.158:9090/productApi/getMrktData.do"

queryParams = '?' + urlencode({quote_plus('serviceKey') : kmaps_service_key,
                               quote_plus('query') : "의자",
                               quote_plus('year') : "2019" })

response = urlopen(url + queryParams)
json_api = response.read().decode("utf-8")

#print(json_api)

json_file = json.loads(json_api)
print(json_file)
