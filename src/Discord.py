import requests

def send_message(WEBHOOK, text):
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