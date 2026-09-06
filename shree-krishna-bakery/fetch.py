import requests

url = "https://shreekrishnabakery.com/menu.php"
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
with open("menu_full.html", "w") as f:
    f.write(response.text)
