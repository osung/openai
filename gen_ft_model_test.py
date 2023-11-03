import os
from dotenv import load_dotenv

import openai

load_dotenv()
os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'
openai_api_key = os.getenv("OPENAI_API_KEY")

market = "협동로봇"
q_list = [f"{market}의 정의를 작성해줘.", f"{market}의 특징을 작성해줘.", f"{market}를 여러 분류체계로 분류하고 각 분류별 특징을 작성해줘.", 
          f"{market}과 다른 유사 기술을 비교해줘.", f"{market}의 원리를 작성해줘."
          f"{market}의 세부종류를 작성해줘. 가능하면 표로 정리해줘.", f"{market}의 구성요소를 작성해줘. 가능하면 표로 정리해줘.", 
          f"{market}의 핵심 요소기술을 작성해줘.", f"{market}의 최근 연구동향을 작성해줘.", 
          f"{market} 시장의 연차별 국내 시장규모와 CAGR을 작성하고 표로 정리해줘.", 
          f"{market} 시장의 연차별 해외 시장규모와 CAGR을 작성하고 표로 정리해줘.", 
          #f"{market} 시장을 여러 분류 체계로 분류하고 각 분류별 특징을 설명해줘. 최소 5개 이상으로 분류해줘.", 
          f"{market} 산업의 특징을 작성해줘.", 
          f"{market} 시장의 국내 업체 현황을 점유율과 매출액을 포함해서 작성해줘.",
          f"{market} 시장의 해외 업체 현황을 점유율과 매출액을 포함해서 작성해줘.",
          f"{market} 시장의 국내외 업체 현황을 점유율과 매출액을 포함해서 작성해줘.",
          f"{market} 시장의 촉진요인과 저해요인을 정치, 경제, 사회, 기술적 관점으로 각각 작성해줘."

          ]
            
# q_list = [f"{market}의 정의를 작성해줘.", f"{market}의 특징을 5개 이상 작성해줘.", 
#           f"{market}을 협동 운용 방식과 활용 산업에 따라 분류하고 각 분류 별 특징을 작성해줘.", #f"{market}과 다른 유사 기술을 비교해줘.", 
#           f"{market}의 원리를  5개 이상으로 작성해줘.", f"{market}의 세부종류를 5개 이상 작성해줘.", f"{market}의 구성요소를 5개 이상 작성해줘.", 
#           f"{market}의 핵심 요소기술을 5개 이상 작성해줘.", f"{market}의 최근 국내 연구동향을 5개 이상 작성해줘.",
#           f"{market}의 최근 해외 연구동향을 작성해줘. 미국과 유럽, 중국과 일본의 연구동향을 포함해줘.", f"{market} 산업의 특징을 5개 이상 작성해줘.", 
#           f"최근 및 향후 몇년간의 {market} 시장의 국내 시장규모를 작성해서 연도별로 정리해줘. CAGR도 함께 작성해줘.",
#           f"최근 및 향후 몇년간의 {market} 시장의 해외 시장규모를 작성해서 연도별로 정리해줘. CAGR도 함께 작성해줘.",
#           f"{market} 시장의 국내 업체 현황을 두산로보틱스, 한화기계, 레인보우틱스, 뉴로메카, 민트로봇을 포함해서 5개 이상 작성해줘. 각 기업들의 현황을 언제 무엇을 어떻게 했는지 구체적으로 작성하고, 점유율과 매출액을 포함해줘.",
#           f"{market} 시장의 해외 업체 현황을  Universal Robots, FANUC, ABB, Techman Robot, KUKA을 포함해서 작성해줘. 각 기업들의 현황을 언제 무엇을 어떻게 했는지 구체적으로 작성하고, 점유율과 매출액을 포함해줘.",
#           f"{market} 시장을 여러 분류 체계로 분류하고 각 분류별 특징을 설명해줘. 최소 5개 이상으로 분류해줘.",
#           f"{market} 시장의 촉진요인을 정치, 경제, 사회, 기술적 관점으로 각각 3개 이상씩 정리해줘.",
#           f"{market} 시장의 저해요인을 정치, 경제, 사회, 기술적 관점으로 각각 3개 이상씩 정리해줘.",
#         ]

print(q_list)

# 시장 분석 시작
for question in q_list :

    messages = [
        {"role": "system", "content": "You are an industrial market expert. You have to give specialied and detailed answers. Always anaswer in Korean."},
        {"role": "user", "content": question + "개조식으로 작성하지 말고 서술형으로 작성해줘. 존대말을 사용하지 말고 ~이다.로 끝내줘."}
    ]

    response = openai.ChatCompletion.create(
        #model="ft:gpt-3.5-turbo-0613:kisti::8DSE7USP",  
        model="ft:gpt-3.5-turbo-0613:kisti::8DiKRa6P",  
        messages=messages,
        temperature=0.0,  # 창의성을 조절하는 옵션
        #max_tokens=2000,  # 답변의 최대 토큰 수 설정
    )

    # API 응답에서 답변을 추출합니다.
    answer = response['choices'][0]['message']['content']

    print('\n' + question + ': ')
    print(answer)
