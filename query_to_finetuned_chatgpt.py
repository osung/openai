import os
from dotenv import load_dotenv
import openai

load_dotenv()
os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'
openai_api_key = os.getenv("OPENAI_API_KEY")

question = "What is the expected size of the Neurological Diseases Gene Therapy market in 2027?" 
#question = "What are the factors that may negatively impact the growth of the electronic equipment and devices market?"
system_message = "You are a helpful assistant."

max_tokens = 2000

messages = [
    {"role": "system", "content": system_message}, 
    {"role": "user", "content": question}
]

response = openai.ChatCompletion.create(
    model="gpt-4", 
    #model = "gpt-3.5-turbo",
    #model = "ft:gpt-3.5-turbo-0613:kisti::8D3OcpAk", # gene therapy
    #model = "ft:gpt-3.5-turbo-0613:kisti::8D3NyH2S",  # micro led display
    messages=messages,
    temperature=0.0,  # 창의성을 조절하는 옵션
    max_tokens=max_tokens,  # 답변의 최대 토큰 수 설정
)

# API 응답에서 답변을 추출합니다.
print("Q: " + question)

answer = response['choices'][0]['message']['content']

# 답변을 출력합니다.
print("A: " + answer)

