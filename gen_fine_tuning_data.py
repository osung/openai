import openai
import os
from dotenv import load_dotenv

load_dotenv()

#os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'

openai.api_key = os.getenv("OPENAI_API_KEY")

question = "generate five pairs of question and answers from following text and give me answers as following structure :{\"prompt\": question, \"completion\": answer}: "

kr_context = """협동 로봇의 분류
1. 협동 운용 방식에 따른 분류
 1.1. 안전 정격 감시 정지(Safety-Rated Monitored Stop): 작업영역에 사람이 없을 경우에만 일반 산업용 로봇(Non-Collaborative Robot)처럼 작동
 1.2. 핸드 가이딩((Hand Guiding): 사람이 수작업 장치(Handoperated Device)를 사용하여 로봇을 이용
 1.3. 속도 및 위치 감시(Speed&Separation Monitoring): 로봇과 사람 사이의 거리를 모니터링하며, 안전거리를 확보하며 작업
 1.4. 동력 및 힘 제한(Power&Force Limiting): 일정 값의 동력(Power) 또는 힘(Force)이 감지되면 로봇이 즉각 작동을 멈춤으로써 사람의 상해를 방지
2. 활용 산업에 따른 분류
 2.1. 일반제조용: 자동차, 전자 등 제조업 기반 산업에 활용되며, 용접･도장･핸들링 공정 등 표준화된 반복 작업 공정 및 식료품･화장품 등 비표준화･비정형 공정의 자동화 영역을 포함
 2.2. 전문제조용: 반도체 공정 등 별도의 설계 기술이 요구되는 특수제조업에 적용
 2.3. 의료산업용: 의료기기로 분류되며 제품 설계 착수부터 멸균･안전･의료분야 요구사항을 만족시키도록 제작
 
 """

en_context = '''Commercializing quantum cryptography is a challenge due to the lack of customer awareness, as knowledge is one of the key drivers for economic growth. 
For the commercialization of high-technology innovations, the enterprise commercialization team must identify, obtain, combine, and manage the required technological knowledge. 
Moreover, innovation could be successful if the innovation team can adhere to the employees’ learning paths and create and maintain a good network. 
As quantum cryptography is a new concept, various challenges are also surfacing, such as failure to obtain sufficient and relevant market information, 
failure to use the information properly, insufficient knowledge about the market, and the inability to locate local and international sales and distributions centers. 
Therefore, proper customer awareness of quantum cryptography solutions is needed to implement the deployment of quantum cryptography solutions successfully. 
These are some of the major challenging factors that are affecting the market growth.'''

messages = [
    {"role": "system", "content": "You are an industrial market expert. You have to give specialied and detailed answers.Always anaswer in Korean."},
    {"role": "user", "content": question + en_context }
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.0,  # 창의성을 조절하는 옵션
    max_tokens=2000,  # 답변의 최대 토큰 수 설정
)

# API 응답에서 답변을 추출합니다.
answer = response['choices'][0]['message']['content']

# 답변을 출력합니다.
print(answer)
