import os
from dotenv import load_dotenv

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

def load_db(file, k=10):
    # 문서 로드
    loader = PyPDFLoader(file)
    documents = loader.load()

    # 조각으로 자르기
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)

    # 임베딩 정의
    embeddings = OpenAIEmbeddings()

    # 데이터로 in-memory 벡터 DB 만들기
    db = DocArrayInMemorySearch.from_documents(docs, embeddings)

    return db


load_dotenv()
os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'
openai_api_key = os.getenv("OPENAI_API_KEY")

pdf_file_path = 'C:\work\pdf\Blockchain_Market_M&M.pdf'
market_name = 'blockchain'

#question ='blockchain 시장을 여러 segment로 분류하고 각 segment별 시장 규모를 알려줘.'
#question ='blockchain 기술을 분류하고 각 분류 기법을 장단점을 포함해서 설명해줘.'
#question = 'blockchain 시장의 주요 참여기업들에 대해 상세히 설명해줘'
#question = 'blockchain 시장의 value chain에 대해 분석해줘'
#question = 'blockchain 시장의 촉진 및 저해요인을 한글 1000 글자가 되도록 작성해줘. 정치, 경제, 사회, 기술적인 관점에서 어떤 요인들이 "blockchain" 산업과 시장의 성장을 촉진할 것인지 혹은 저해할 것인지 정리해줘. 촉진요인을 먼저 5가지 이상 정리하고 그 후에 이어서 저해요인을 5가지 이상 정리해줘.'
#question = 'blockchain 시장의 특허 분석을 한글 1000글자 이상으로 상세하게 해줘'
#question = 'Show me the BLOCKCHAIN MARKET IN GOVERNMENT BY REGION from 2018 to 2021 year by year as well as CAGR'
#question = "Show me the amount of blockchain investment from 2018 to 2020 year by year."
#question = "Show me the month-wise blockchain investment in 2022."
question = "Show me the number of patents by top 10 owners."
#question = "Show me the top TOP JURISDICTION WISE - DOCUMENT COUNT"
#question = "Show me the number of patents published over last 10 years year by year."
system_message = "You are an industrial market expert in Korea. You have to give specialied and detailed answers. Always answer in Korean but write in English for the technical terms and the proper names."

# PDF 문서 로드
db = load_db(pdf_file_path)
print("DB loading 완료")

docs = db.similarity_search(question, 10)
merged_doc = ""

for doc in docs:
    #print("========================================")
    #print(doc.page_content)
    # print(doc.metadata)
    
    merged_doc += doc.page_content

#print("========================================")

messages = [
    SystemMessage(
        content = system_message
    ),
    HumanMessage(
        content = question + merged_doc
    ),
]

print(messages)

llm = ChatOpenAI(model_name='gpt-4', #3.5-turbo', 
                 openai_api_key = openai_api_key,
                 temperature=0,
                )

print(llm(messages).content)
