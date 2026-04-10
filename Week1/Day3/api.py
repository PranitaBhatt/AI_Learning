import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_user(user_id):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"  #url as api
    response = requests.get(url, verify=False)  #with help of requests with we fetching data usinf get function

    if response.status_code == 200:  #if the status code iss 200(reuqeust successful)
        return response.json()       #it will return response.json
    return None
