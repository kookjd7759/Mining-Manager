import requests
import json

WEBSITE_LIST = ['https://kaspa-pool.org/api/user/workers/?wallet=kaspa:qp29mc9qzdpyq6kjwnvw450vewylk8szej3mju8lwt40h995xm7pxx7pwq08z']

def connection_test(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.status_code
        else:
            return response.status_code
    except requests.exceptions.RequestException as e:
        return -1

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

