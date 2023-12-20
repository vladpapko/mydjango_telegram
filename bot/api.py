import requests
import json

BASE_URL = 'http://localhost:8000/api/v1'

def create_user(username, name, user_id):
    url = f"{BASE_URL}/bot-users"
    response = requests.get(url=url).text
    data = json.loads(response)
    user_exist = False
    for i in data:
        if i["user_id"] == str(user_id):
            user_exist = True
            break
    if user_exist == False:    
        requests.post(url=url, data={'username':username, "name":name, "user_id":user_id})
        return "Пользователь создан."
    else:
        return "Пользователь существует."
    
def create_feedback(user_id, body):
    url = f"{BASE_URL}/feedbacks"
    if body and user_id :
        post = requests.post(url=url, data = {
            "user_id":user_id,
            "body":body
        })
        return "Отправлено администратору. Спасибо за ваше мнение."
    else:
        return "Акт не закончился."    
    
def update_subscription_status(user_id, subscribed):
    url = f"{BASE_URL}/bot-users/{user_id}/update"
    response = requests.patch(url=url, json={'subscribed': subscribed})
    return response.text


