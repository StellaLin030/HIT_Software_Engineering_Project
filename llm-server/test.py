import requests

# url = "https://api.openai.com/v1/chat/completions"
url = "https://apikeyplus.com/v1/chat/completions"

headers = {
  'Content-Type': 'application/json',
  # 填写 OpenKEY 生成的令牌/KEY，注意前面的 Bearer 要保留，并且和 KEY 中间有一个空格。
  'Authorization': 'sk-EpjUlDRPazWZA88tEbFbBd5650E54e97A79743A018145b08'
}

data = {
  "model": "gpt-3.5-turbo",
  "messages": [{"role": "user", "content": "你好呀"}]
}

response = requests.post(url, headers=headers, json=data)

print("Status Code", response.status_code)
print("JSON Response ", response.json())

if response.status_code == 200:
    # 处理响应数据
    json_response = response.json()  # 将 JSON 响应解析为 Python 字典或列表
    content = json_response['choices'][0]['message']['content']  # 获取 content 内容
    print(content)
else:
    print(f"Request failed with status code: {response.status_code}")

