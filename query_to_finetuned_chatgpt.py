import os
from dotenv import load_dotenv
import openai
from langchain.prompts import PromptTemplate

load_dotenv()
os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'
openai_api_key = os.getenv("OPENAI_API_KEY")

#market = 'micro oled display'
market = 'gene therapy'

overview_template = """{market}의 정의, 원리, 종류, 타 기술과의 특징 비교 등을 한글 2000자 분량으로 작성해줘.
개조식으로 작성하지 말고 서술식으로 작성해줘. 존대말을 사용하지 말고 ~이다. 로 끝내줘."""

trend_template = """{market}에 대한 기술동향을 한글로 2000 글자가 되도록 작성해줘. 
기술동향에는 {market}의 원리, 세부종류, 핵심적인 요소기술, 최근 연구동향 등을 구체적으로 설명해줘. 
최근 연구동향은 국내외에서 누가 언제 어떤 기술을 개발했는지 3개 이상 나열해줘.
개조식으로 작성하지 말고 서술식으로 작성해줘."""

characteristic_template = """{market} 산업과 시장에 대한 시장특징을 한글로 2000 글자가 되도록 작성해줘.
시장특징에는 {market} 산업이 어떤 특징을 가지고 있는 산업인지 정리해줘.
여러 가지 특징이 있다면 각각의 특징을 리스트업 해줘.
개조식으로 작성하지 말고 서술식으로 작성해줘."""

size_template = """국내외 {market} 시장규모를 한글 2000 글자가 되도록 작성해줘.
국내외 시장규모는 {market} 시장규모와 성장률을 국내시장과 세계시장으로 구분하여 각각 구체적인 수치를 이용해서 작성해줘.
가능한 많은 연도의 시장규모를 알려주고 향후 몇 %의 성장률을 보여 미래 시점에 얼마의 시장규모를 형성할지 작성해줘.
연도별 시장규모와 성장률을 표로 정리해줘. 우리나라의 시장규모는 원화로 작성해줘."""

company_template = """{market} 시장의 업체현황을 한글 2000 글자가 되도록 작성해줘.
업체현황은 {market}을 연구개발 혹은 판매하고 있는 적어도 5개 이상의 기업들의 현황을 정리해서 작성해줘.
각 기업들의 점유율을 포함해서 그 기업들이 언제 무엇을 어떻게 했는지 구체적으로 작성해줘. 
개조식으로 작성하지 말고 서술식으로 작성해줘."""

factor_template = """{market} 시장의 촉진 및 저해요인을 한글 2000 글자가 되도록 작성해줘. 
정치, 경제, 사회, 기술적인 관점에서 어떤 요인들이 {market} 산업과 시장의 성장을 촉진할 것인지 혹은 저해할 것인지 정리해줘.
촉진요인을 먼저 5가지 이상 정리하고 그 후에 이어서 저해요인을 5가지 이상 정리해줘.
개조식으로 작성하지 말고 서술식으로 작성해줘."""

contents = {"개요": overview_template, 
            "기술동향": trend_template,
            "시장특징": characteristic_template,
            "시장규모": size_template,
            "업체현황": company_template,
            "시장요인": factor_template}

#question = "What is the expected size of the Neurological Diseases Gene Therapy market in 2027?" 
system_message = "You are a helpful assistant."

max_tokens = 2000

# 시장 분석 시작
for name, template in contents.items() :
    prompt = PromptTemplate(input_variables=["market"], template=template)
    question = prompt.format(market=market)

    messages = [
        {"role": "system", "content": system_message}, 
        {"role": "user", "content": question}
    ]

    response = openai.ChatCompletion.create(
        #model="gpt-4", 
        #model = "gpt-3.5-turbo",
        model = "ft:gpt-3.5-turbo-0613:kisti::8D5TXpRs", # gene therapy
        #model = "ft:gpt-3.5-turbo-0613:kisti::8D5RUDNn",  # micro led display
        messages=messages,
        temperature=0.0,  # 창의성을 조절하는 옵션
        max_tokens=max_tokens,  # 답변의 최대 토큰 수 설정
    )

    answer = response['choices'][0]['message']['content']

    print(f"\n=========================== {name} ===========================")
    print(answer)

