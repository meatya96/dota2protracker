import requests

url = "https://api.opendota.com/api/matches/8209707363"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    patch = data.get("patch")  # Доступ к ключу "patch"
    print("Patch:", patch)
else:
    print("Ошибка запроса:", response.status_code)
