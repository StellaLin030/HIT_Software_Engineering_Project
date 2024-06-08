import requests  
  
response = requests.post(  
    'http://localhost:5000/api/dashscope',  
    json={'question': '你知道哈尔滨工业大学吗！'}  
)  
  
print(response.json())