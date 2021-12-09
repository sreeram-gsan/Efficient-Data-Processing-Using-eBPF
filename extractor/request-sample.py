import requests

url = 'http://localhost:5023/api/v1/extract'
myobj = {'filter': 'two', 'source' : '/app/data.txt'}
x = requests.post(url, json = myobj)
print(x.text)