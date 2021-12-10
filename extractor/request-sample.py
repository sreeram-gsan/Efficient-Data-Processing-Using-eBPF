import requests

url = 'http://192.168.49.2:30228/api/v1/extract'
myobj = {'filter': 'two', 'source' : '/app/data.txt'}
x = requests.post(url, json = myobj)
print(x.text)