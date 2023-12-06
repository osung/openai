import os
from dotenv import load_dotenv

import openai

from langchain.prompts import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus

import pandas as pd
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

    # Retriever 정의 및 반환
    return db


def print_paged(json_data, lines_per_page=50):
    lines = json_data.split('\n')
    for i in range(0, len(lines), lines_per_page):
        
        print('\n'.join(lines[i:i+lines_per_page]))
        input('Press Enter to continue...')


# JSON 데이터의 노드들을 tree 형태로 구조화하여 출력하는 함수
def print_json_tree(node, indent=0, max_depth=2):
    if indent > max_depth:
        return
    
    if isinstance(node, dict):
        for key, value in node.items():
            print("  " * indent + f"{key}:")
            print_json_tree(value, indent + 1, max_depth)
    elif isinstance(node, list):
        for item in node:
            print("  " * indent + "-")
            print_json_tree(item, indent + 1, max_depth)
    else:
        print("  " * indent + str(node))


# 노드의 데이터 가져오기
def get_node_data(node, path):
    for key in path:
        if isinstance(node, dict) and key in node:
            node = node[key]
        else:
            return None
    return node

load_dotenv()
os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'
openai_api_key = os.getenv("OPENAI_API_KEY")
kmaps_service_key = os.getenv("KMAPS_API_KEY")

# set up a PDF list 
pdf_path_list = ['C:\work\pdf\제조용+협동로봇.pdf', 'C:\work\pdf\협동로봇시장.pdf', 'C:\work\pdf\Collaborative_Robot_Market.pdf', 'C:\work\pdf\협동로봇_기술동향.pdf']
market = '협동로봇'

# set up the kmaps server
kmaps_url = "http://112.155.255.158:9090/productApi/getMrktData.do"


# query templates

market = '협동로봇'

template = """ 이번 보고서의 주제는 {market} 입니다. 
{market} 시장의 규모와 업체현황을 한글 2000자가 되도록 작성해주세요. 
국내외 시장규모는 시장규모와 성장률을 국내시장과 세계시장으로 구분하여 각각 구체적인 수치를 이용해서 작성해주세요. 가능한 많은 연도의 시장규모를 알려주고 향후 몇 %의 성장률을 보여 미래 시점에 얼마의 시장규모를 형성할지 작성해주세요. 연도별 시장규모와 성장률을 표로 정리해주세요. 
업체현황은 ”협동로봇”을 연구개발 혹은 판매하고 있는 국내 5개 이상의 기업들의 현황을 정리해서 작성해주세요. 각 기업들의 점유율을 포함해서 그 기업들이 언제 무엇을 어떻게 했는지 구체적으로 작성해주세요.
화폐 단위는 백만달러를 사용하고, 개조식으로 작성하지 말고 서술식으로 작성해주세요. 존대말을 사용하지 말고 ~이다. 로 끝내주세요.
"""

# PDF 문서 로드
db = load_db(pdf_path_list, 5)
print("DB loading 완료")

# retreive query to the kmaps 
queryParams = '?' + urlencode({quote_plus('serviceKey') : kmaps_service_key,
                               quote_plus('query') : "협동로봇",
                               quote_plus('year') : "2021" })

response = urlopen(kmaps_url + queryParams)
json_api = response.read().decode("utf-8")

json_file = json.loads(json_api)

print(json_file)

node1 = get_node_data(json_file, ["companymarketshare"])
node2 = get_node_data(json_file, ["marketstructure"])
node3 = get_node_data(json_file, ["productsales"]) #productinfo_by_com"])

pretty_node1 = json.dumps(node1, ensure_ascii=False, indent=4)
pretty_node2 = json.dumps(node2, ensure_ascii=False, indent=4)
pretty_node3 = json.dumps(node3, ensure_ascii=False, indent=4)

print(pretty_node1, pretty_node2, pretty_node3)

# ChatGPT LLM 준비
llm = ChatOpenAI(#model_name='gpt-4',
                 model="ft:gpt-3.5-turbo-0613:kisti::8DiKRa6P",  
                 openai_api_key = openai_api_key,
                 temperature=0,
                 max_tokens=3000,
                )

# 시장 분석 시작
prompt = PromptTemplate(input_variables=["market"], template=template)
question = prompt.format(market=market)

docs = db.similarity_search(question, 3)
merged_doc = ""

for doc in docs:
    merged_doc += doc.page_content

merged_doc += pretty_node1 + pretty_node2 + pretty_node3 #json_api

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

# OpenAI API 응답에서 답변을 추출합니다.
answer = response['choices'][0]['message']['content']

print(answer)