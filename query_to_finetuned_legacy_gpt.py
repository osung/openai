import os
from dotenv import load_dotenv
import openai

load_dotenv()
os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'
openai_api_key = os.getenv("OPENAI_API_KEY")

question = "What is the global micro LED display market a part of?"
system_message = "You are an industrial market expert in Korea. You have to give specialied and detailed answers. Always answer in Korean." # but write in English for technical terms and proper names."

max_tokens = 2000

messages = [
    {"role": "system", "content": system_message}, 
    {"role": "user", "content": question}
]

'''
res = openai.FineTuningJob.retrieve('ftjob-ILMimho0dFBxXr9AgPYYQV1c')
print(res) '''

response = openai.Completion.create(
    #engine = "davinci-002",
    #engine = "ft:davinci-002:kisti::8ChB1Nh5", 
    engine = "ft:davinci-002:kisti::8ChJ1oxz",
    prompt = question,
    temperature=0.0,  # 창의성을 조절하는 옵션
    max_tokens=max_tokens,  # 답변의 최대 토큰 수 설정
)

# API 응답에서 답변을 추출합니다.
answer = response['choices'][0].text.strip()

# 답변을 출력합니다.
print(answer)
