import requests 
import json

Wallet_kaspa = 'qp29mc9qzdpyq6kjwnvw450vewylk8szej3mju8lwt40h995xm7pxx7pwq08z'

KEY_kaspaPool = 'kaspa-pool.org'
KEY_kas2miner = 'kas.2miners.com'
Url_dictionary = {KEY_kaspaPool: [f'https://kaspa-pool.org/api/user/workers/?wallet=kaspa:{Wallet_kaspa}', 'https://kaspa-pool.org/'],
                KEY_kas2miner: [f'https://kas.2miners.com/api/accounts/kaspa:{Wallet_kaspa}', f'https://kas.2miners.com/ko/account/kaspa:{Wallet_kaspa}']
                }

User_url_dictionary = {KEY_kaspaPool: f'https://kaspa-pool.org/#/dashboard/kaspa:{Wallet_kaspa}',
                       KEY_kas2miner: f'https://kas.2miners.com/ko/account/kaspa:{Wallet_kaspa}'}

def connection_test(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.status_code
        else:
            return response.status_code
    except requests.exceptions.RequestException as e:
        return -1

def get_json(url, header):
    print('Loading ...')
    response = requests.get(url, headers=header)
    print('Loading completed')
    data = json.loads(response.text)
    return data

def getList(key):
    url = Url_dictionary[key][0]
    header = {
    'referer': Url_dictionary[key][1]
    }
    data = get_json(url=url, header=header)
    name_hashList = []
    if key == KEY_kaspaPool:
        for worker in data['workers']:
            hash_TH = float(worker['current_hashrate']['hashrate'])
            if worker['current_hashrate']['hashrate_unit'] == 'TH/s':
                hash_TH = round(hash_TH, 2)
            elif worker['current_hashrate']['hashrate_unit'] == 'GH/s':
                hash_TH = round(hash_TH / 1000, 2)
            else:
                hash_TH = 0.0
            name_hashList.append([worker['name'], hash_TH])
    elif key == KEY_kas2miner:
        for name in data['workers']:
            hash_TH = round(float(data['workers'][name]['hr']) / 1000000000000.0, 2)
            name_hashList.append([name, hash_TH])
    
    name_hashList.sort(key=lambda x:x[0]) # 첫번째 값 기준 ('name') 정렬
    return name_hashList


