import requests
import json


def send_post_request(url, data):
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()


url = "http://hikos.cn/kmind/api/act"
data = {
    "actCode": "CustomerAct2d216",
    "action": "start",
    "accessKey": "27602e326d6a4d478969a4a53b9b73d9",
    "accessSecretKey": "V6Z7VAw9pg/vd4f3T8HxxEuIhry7BuUbx6xHZTZOYuKj6JpIrmNz6bcxML9XfufHgn48d85Ux2k4yUQ8kTMWcJf24SvmsoCK",
    "apiRequest": {
        "input": "阿里巴巴"}
}

response = send_post_request(url, data)
print(response)
