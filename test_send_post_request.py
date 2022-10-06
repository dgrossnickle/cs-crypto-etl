import requests


# client_key = ''
# headers = {
#     'Gke-Client-Key': client_key,
#     'Content-Type': 'application/json'
# }
url = f'http://127.0.0.1:5001/run_etl'
r = requests.post(url)