import openai
import os
from dotenv import load_dotenv

load_dotenv()

#os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'

openai.api_key = os.getenv("OPENAI_API_KEY")

question = "generate five pairs of question and answers from following text and give me answers as following structure :{\"prompt\": question, \"completion\": answer}: "

kr_context = """양자 암호화 상업화는 고객 인식 부족으로 어려움이 있으며, 지식은 경제 성장의 주요 동력 중 하나입니다. 
고기술 혁신을 상업화하기 위해서는 기업 상업화 팀이 필요한 기술 지식을 식별, 확보, 결합 및 관리해야 합니다. 
또한 혁신이 성공하려면 혁신 팀이 직원의 학습 경로를 준수하고 강력한 네트워크를 생성 및 유지할 수 있어야 합니다. 
양자 암호화가 새로운 개념이기 때문에 충분하고 관련성 있는 시장 정보를 얻지 못하거나 정보를 올바르게 활용하지 못하는 등 다양한 어려움이 나타나고 있으며, 
시장에 대한 지식 부족 및 지역 및 국제 판매 및 유통 센터를 찾지 못하는 등의 문제가 있습니다. 
따라서 양자 암호화 솔루션에 대한 적절한 고객 인식이 양자 암호화 솔루션의 배포를 성공적으로 구현하기 위해 필요합니다. 
이러한 것들은 시장 성장에 영향을 미치는 주요 어려운 요소 중 일부입니다."""

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
