import requests

# print(requests.__version__)
url = "https://raw.githubusercontent.com/n33lp/cmput404/master/test1.py"
res = requests.get(url)
print(res.text)