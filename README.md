# Install

pip install -r requirements.txt

# Configure

Copy and paste .env.example to .env
input your openai api key,port......

# Run
python3 api.py

---
## 测试 API

### 接口：`/api/data`

- **请求方法**：GET

该接口用于获取测试数据。

#### 请求参数

无

#### 响应示例

```json
{
    "message": "Hello, API!",
    "data": [1, 2, 3, 4, 5]
}
```

- `message`：包含一个消息字符串，显示为 "Hello, API!"。
- `data`：包含一个整数列表，其中包含了数字 1 到 5。

---
## Chat API

此API允许您与OpenAI的GPT-3.5 Turbo模型进行对话。您可以向API发送一个包含问题的请求，并获取对应的回答。

### 请求

- **URL**: `/chat`
- **方法**: GET
- **请求体** (JSON格式):

```json
{
  "question": "用日语说你好"
}
```

### 响应

- **状态码**: 200 OK
- **响应体** (JSON格式):

```json
{
  "message": {
    "content": "こんにちは (Konnichiwa)。",
    "role": "assistant"
  }
}
```
---