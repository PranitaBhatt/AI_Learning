import requests

API_KEY = 'your_api_key_here'
url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=%7BAPI_KEY%7D"
response = requests.get(url)
print(response.status_code)