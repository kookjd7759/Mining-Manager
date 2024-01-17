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