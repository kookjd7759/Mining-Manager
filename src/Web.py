import requests
import json

def webGet_json(url, header):
    print('Loading ...')
    response = requests.get(url, headers=header)
    print('Loading completed')

    data = json.loads(response.text)
    return data

url = 'https://kaspa-pool.org/api/user/workers/?wallet=kaspa:qp29mc9qzdpyq6kjwnvw450vewylk8szej3mju8lwt40h995xm7pxx7pwq08z'
header = {
    'referer': 'https://kaspa-pool.org/'
}

data = webGet_json(url=url, header=header)
for worker in data['workers']:
    print(worker['name'])