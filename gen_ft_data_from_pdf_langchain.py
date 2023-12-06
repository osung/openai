import os
from dotenv import load_dotenv

import openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.document_loaders import PyPDFLoader

import json

def load_db(files, k=10):

    docs = []

    for file in files :
        # 문서 로드
        loader = PyPDFLoader(file)
        document = loader.load()

        # 조각으로 자르기
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        docs += text_splitter.split_documents(document)

    # 임베딩 정의
    embeddings = OpenAIEmbeddings()

    # 데이터로 in-memory 벡터 DB 만들기
    db = DocArrayInMemorySearch.from_documents(docs, embeddings)
   
    return db #.as_retriever(search_type="similarity", search_kwargs={"k": k})  # Retriever 정의 및 반환

load_dotenv()
os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'
openai_api_key = os.getenv("OPENAI_API_KEY")

#pdf_path_list = ['C:\work\pdf\제조용+협동로봇.pdf', 'C:\work\pdf\Collaborative_Robot_Market.pdf', 'C:\work\pdf\협동로봇_기술동향.pdf']
pdf_path_list = ['C:\work\pdf\협동로봇시장_KISTI.pdf'] #, 'C:\work\pdf\협동로봇_기술동향.pdf', 'C:\work\pdf\제조용+협동로봇.pdf']

market = '협동로봇'

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
#market = 'micro_led_display'
#market = 'Gene_Therapy_Market'
#pdf_path_list = [f"C:\work\\finetuning\{market}.pdf"]

#market = 'micro led display'
#market = 'gene therapy'

# PDF 문서 로드
#db = load_db(pdf_path_list, 3)
print("DB loading 완료")

market = "협동로봇"
q_list = [#f"{market}의 정의를 작성해줘.", f"{market}의 특징을 5개 이상 작성해줘.", 
        #   f"{market}을 협동 운용 방식과 활용 산업에 따라 분류하고 각 분류 별 특징을 작성해줘.", #f"{market}과 다른 유사 기술을 비교해줘.", 
        #   f"{market}의 원리를  5개 이상으로 작성해줘.", f"{market}의 세부종류를 5개 이상 작성해줘.", f"{market}의 구성요소를 5개 이상 작성해줘.", 
        #   f"{market}의 핵심 요소기술을 5개 이상 작성해줘.", f"{market}의 최근 국내 연구동향을 5개 이상 작성해줘.",
        #   f"{market}의 최근 해외 연구동향을 작성해줘. 미국과 유럽, 중국과 일본의 연구동향을 포함해줘.", f"{market} 산업의 특징을 5개 이상 작성해줘.", 
        #  f"최근 및 향후 몇년간의 {market} 시장의 국내 시장규모를 작성해서 연도별로 정리해줘. CAGR도 함께 작성해줘.",
        #  f"최근 및 향후 몇년간의 {market} 시장의 해외 시장규모를 작성해서 연도별로 정리해줘. CAGR도 함께 작성해줘.",
          f"{market} 시장의 국내 업체 현황을 두산로보틱스, 한화기계, 레인보우틱스, 뉴로메카, 민트로봇을 포함해서 5개 이상 작성해줘. 각 기업들의 현황을 언제 무엇을 어떻게 했는지 구체적으로 작성하고, 점유율과 매출액을 포함해줘.",
        #  f"{market} 시장의 해외 업체 현황을  Universal Robots, FANUC, ABB, Techman Robot, KUKA을 포함해서 작성해줘. 각 기업들의 현황을 언제 무엇을 어떻게 했는지 구체적으로 작성하고, 점유율과 매출액을 포함해줘.",
        #  f"{market} 시장을 여러 분류 체계로 분류하고 각 분류별 특징을 설명해줘. 최소 5개 이상으로 분류해줘.",
        #  f"{market} 시장의 촉진요인을 정치, 경제, 사회, 기술적 관점으로 각각 3개 이상씩 정리해줘.",
        #  f"{market} 시장의 저해요인을 정치, 경제, 사회, 기술적 관점으로 각각 3개 이상씩 정리해줘.",
        ]

print(q_list)

#outfile = open('C:\work\\finetuning\\ft_col_robot_chat_new10.jsonl', 'w', encoding='utf-8')

# 시장 분석 시작
for question in q_list :

    # DB에서 유사한 내용 찾기
    docs = db.similarity_search(question, 3)
    merged_doc = ""

    for doc in docs:
         merged_doc += doc.page_content

    messages = [
        {"role": "system", "content": "You are an industrial market expert. You have to give specialied and detailed answers. Always anaswer in Korean."},
        {"role": "user", "content": question + "다음을 참고해서 작성하고, 존대말을 사용하지 말고 ~이다.로 끝내줘. 개조식으로 작성하지 말고 서술식으로 해줘." + merged_doc } #kr_context }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4", #3.5-turbo",
        messages=messages,
        temperature=0.0,  # 창의성을 조절하는 옵션
        #max_tokens=2000,  # 답변의 최대 토큰 수 설정
    )

    # API 응답에서 답변을 추출합니다.
    answer = response['choices'][0]['message']['content']
    print('\n'+question+'\n')
    print('->' + answer)

    # 답변을 출력합니다.
    new_obj = {
                "messages": [
                    {"role": "system", "content": messages[0]['content']},
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": answer}
                ]
            }

    #print(new_obj)

    # 변환된 객체를 출력 파일에 쓰기
    #outfile.write(json.dumps(new_obj, ensure_ascii=False) + '\n')
