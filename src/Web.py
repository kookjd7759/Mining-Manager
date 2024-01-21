import requests
import json

Wallet_kaspa = 'qp29mc9qzdpyq6kjwnvw450vewylk8szej3mju8lwt40h995xm7pxx7pwq08z'

KEY_kaspaPool = 'kaspa-pool.org'
KEY_kas2miner = 'kas.2miners.com'
Url_dictionary = {KEY_kaspaPool: [f'https://kaspa-pool.org/api/user/workers/?wallet=kaspa:{Wallet_kaspa}', 'https://kaspa-pool.org/'],
                KEY_kas2miner: [f'https://kas.2miners.com/api/accounts/kaspa:{Wallet_kaspa}', f'https://kas.2miners.com/ko/account/kaspa:{Wallet_kaspa}']
                }


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
            name_hashList.append([worker['name'], round(float(worker['current_hashrate']['hashrate']), 2)])
    elif key == KEY_kas2miner:
        for name in data['workers']:
            name_hashList.append([name, round(float(data['workers'][name]['hr']) / 1000000000000.0, 2)])
    
    name_hashList.sort(key=lambda x:x[0]) # 첫번째 값 기준 ('name') 정렬
    return name_hashList



if __name__ == "__main__":
    for key in Url_dictionary:
        url = Url_dictionary[key][0]
        header = {
        'referer': Url_dictionary[key][1]
        }
        data = get_json(url=url, header=header)
        name_hashList = []
        if key == KEY_kaspaPool:
            for worker in data['workers']:
                name_hashList.append([worker['name'], round(float(worker['current_hashrate']['hashrate']), 2)])
        elif key == KEY_kas2miner:
            for name in data['workers']:
                name_hashList.append([name, round(float(data['workers'][name]['hr']) / 1000000000000.0, 2)])
        
        name_hashList.sort(key=lambda x:x[0]) # 첫번째 값 기준 ('name') 정렬
        print(name_hashList)