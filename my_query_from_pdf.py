import os
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

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
    return db.as_retriever(search_type="similarity", search_kwargs={"k": k})

load_dotenv()
os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'
openai_api_key = os.getenv("OPENAI_API_KEY")

pdf_path_list = ['C:\work\pdf\Camera_Modules_Market.pdf'] 
market = '휴대폰용 카메라 모듈'

# PDF 문서 로드
retriever = load_db(pdf_path_list, 3)
print("DB loading 완료")

# ChatGPT LLM 준비
llm = ChatOpenAI(model_name='gpt-4', #gpt-4', #3.5-turbo', 
                 openai_api_key = openai_api_key,
                 temperature=0,
                 #max_tokens=1000,
                )
            
# 시장 분석 시작
question = "휴대폰용 카메라 모듈 시장에 대한 세계 각국의 주요 정책 및 규제 동향을 알려줘"

chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
)

print(chain.run(question))
