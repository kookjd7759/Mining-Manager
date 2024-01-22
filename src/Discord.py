import requests

import Web

def send_message(WEBHOOK, text):
    print(f'send \n{text}')
    data = {
        "content" : text,
    }
    try:
        requests.post(WEBHOOK, json=data)
    except:
        return -1
    return 1

def connectionTest(WEBHOOK):
    data = {
        "content" : '',
    }
    try:
        requests.post(WEBHOOK, json=data)
    except:
        return -1
    return 1

def add_alert(WEBHOOK, Infosetting, addedWorkerList, url_key, time):
    print('Call add_alert')
    text = ''
    if Infosetting[0] == '1':
        text += '# Worker가 추가되었습니다\n'

    if Infosetting[2] == '1':
        text += f'### 시간 : {time}\n'

    if Infosetting[1] == '1':
        text += f'- 추가된 Worker : {addedWorkerList}\n'
        text += f'- 추가된 Pool : [{url_key}]({Web.User_url_dictionary[url_key]})\n'

    
    send_message(WEBHOOK, text)

def remove_alert(WEBHOOK, Infosetting, removedWorkerList, url_key, time):
    print('Call remove_alert')
    text = ''
    if Infosetting[0] == '1':
        text += '# Worker가 삭제되었습니다\n'

    if Infosetting[2] == '1':
        text += f'### 시간 : {time}\n'

    if Infosetting[1] == '1':
        text += f'- 삭제된 Worker : {removedWorkerList}\n'
        text += f'- 삭제된 Pool : [{url_key}]({Web.User_url_dictionary[url_key]})\n'

    
    send_message(WEBHOOK, text)

def hash_alert(WEBHOOK, Infosetting, hashCheckingList, url_key, time):
    print('Call hash_alert')
    text = ''
    if Infosetting[0] == '1':
        text += '# Hash가 비정상적인 Worker가 발견되었습니다\n'

    if Infosetting[2] == '1':
        text += f'### 시간 : {time}\n'
        
    if Infosetting[1] == '1':
        text += f'- Worker\n'
        for worker in hashCheckingList:
            text += f'  - \'{worker[0]}\'   [{worker[1]}TH/s]\n'
        text += f'- Pool : [{url_key}]({Web.User_url_dictionary[url_key]})\n'

    
    send_message(WEBHOOK, text)