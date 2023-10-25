import os
from dotenv import load_dotenv

import openai

load_dotenv()
os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'
openai_api_key = os.getenv("OPENAI_API_KEY")

market = "협동로봇"
#q_list = [f"{market}의 정의를 작성해줘.", f"{market}의 특징을 작성해줘.", f"{market}의 종류를 작성해줘.", f"{market}과 다른 유사 기술을 비교해줘.", 
#          f"{market}의 원리를 작성해줘.", f"{market}의 세부종류를 작성해줘.", f"{market}의 구성요소를 작성해줘.", f"{market}의 핵심 요소기술을 작성해줘.", f"{market}의 최근 연구동향을 작성해줘.", 
q_list = [f"2023년 전후로 몇년간의 {market} 시장의 국내 시장규모를 전망해줘. CAGR도 함께 작성해줘.", f"2023년 전후로 몇년간의 {market} 시장의 국내 시장규모를 전망해줘. CAGR도 함께 작성해줘.", 
          f"{market} 시장을 여러 분류 체계로 분류하고 각 분류별 특징을 설명해줘. 최소 5개 이상으로 분류해줘."]
            
print(q_list)

# 시장 분석 시작
for question in q_list :

    messages = [
        {"role": "system", "content": "You are an industrial market expert. You have to give specialied and detailed answers. Always anaswer in Korean."},
        {"role": "user", "content": question + "문장 사이에 '\n'를 1개 이상 넣지 말아줘. 존대말을 사용하지 말고 ~이다.로 끝내줘."}
    ]

    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0613:kisti::8DBFHaXp",  
        messages=messages,
        temperature=0.0,  # 창의성을 조절하는 옵션
        #max_tokens=2000,  # 답변의 최대 토큰 수 설정
    )

    # API 응답에서 답변을 추출합니다.
    answer = response['choices'][0]['message']['content']

    print('\n' + question + ': ')
    print(answer)
