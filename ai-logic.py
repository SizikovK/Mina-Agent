from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("BASE_URL")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

response = client.chat.completions.create(
    model="deepseek-chat", #определение модели
    messages=[
        {"role": "system", "content": "You are a helpful assistant"}, #описание роли самой нейронки
        {"role": "user", "content": "Hello"}, #сообщение от юзера
    ],
    stream=False #если True - делит ответ на куски для постепенного отображения
)

print(response.choices[0].message.content)