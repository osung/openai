import os
from dotenv import load_dotenv
import openai
from langchain.prompts import PromptTemplate

load_dotenv()
os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'
openai_api_key = os.getenv("OPENAI_API_KEY")

#market = 'micro oled display'
market = '협동로봇'

template = """ 이번 보고서의 주제는 {market} 입니다. 
{market} 시장의 규모와 업체현황을 한글 2000자가 되도록 작성해주세요. 
국내외 시장규모는 시장규모와 성장률을 국내시장과 세계시장으로 구분하여 각각 구체적인 수치를 이용해서 작성해주세요. 가능한 많은 연도의 시장규모를 알려주고 향후 몇 %의 성장률을 보여 미래 시점에 얼마의 시장규모를 형성할지 작성해주세요. 연도별 시장규모와 성장률을 표로 정리해주세요. 
업체현황은 ”협동로봇”을 연구개발 혹은 판매하고 있는 국내 5개 이상의 기업들의 현황을 정리해서 작성해주세요. 각 기업들의 점유율을 포함해서 그 기업들이 언제 무엇을 어떻게 했는지 구체적으로 작성해주세요.
화폐 단위는 백만달러를 사용하고, 개조식으로 작성하지 말고 서술식으로 작성해주세요. 존대말을 사용하지 말고 ~이다. 로 끝내주세요.
"""

#question = "What is the expected size of the Neurological Diseases Gene Therapy market in 2027?" 
system_message = "당신의 역할은 특정 주제에 대한 기술시장 분석보고서를 작성하는 것입니다. 앞으로 제시하는 주제와 보고서 구성에 맞게, 보고서를 작성해야 합니다."

max_tokens = 2000

# 시장 분석 시작
prompt = PromptTemplate(input_variables=["market"], template=template)
question = prompt.format(market=market)

messages = [
        {"role": "system", "content": system_message}, 
        {"role": "user", "content": question}
    ]

response = openai.ChatCompletion.create(
        #model="gpt-4", 
        #model = "gpt-3.5-turbo",
        #model = "ft:gpt-3.5-turbo-0613:kisti::8D5TXpRs", # gene therapy
        #model = "ft:gpt-3.5-turbo-0613:kisti::8D5RUDNn",  # micro led display
        model="ft:gpt-3.5-turbo-0613:kisti::8DiKRa6P",  # 협동로봇
        messages=messages,
        temperature=0.0,  # 창의성을 조절하는 옵션
        max_tokens=max_tokens,  # 답변의 최대 토큰 수 설정
    )

answer = response['choices'][0]['message']['content']

#print(f"\n=========================== {name} ===========================")
print(answer)

