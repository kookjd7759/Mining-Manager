import requests

def send_message(WEBHOOK, text):     
    data = {
        "content" : text,
    }
    requests.post(WEBHOOK, json=data)

