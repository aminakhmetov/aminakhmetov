import requests

url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

# submit the image of a cup found in the internet
data = {'url': 'https://upload.wikimedia.org/wikipedia/commons/d/da/Cup_and_Saucer_LACMA_47.35.6a-b_%281_of_3%29.jpg'}

result = requests.post(url, json=data).json()
print(result)
