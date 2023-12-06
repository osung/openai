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


def load_single_db(file):

    # 문서 로드
    loader = PyPDFLoader(file)
    document = loader.load()

    # 조각으로 자르기
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=150)
    doc = text_splitter.split_documents(document)

    # 임베딩 정의
    embeddings = OpenAIEmbeddings()

    # 데이터로 in-memory 벡터 DB 만들기
    db = DocArrayInMemorySearch.from_documents(doc, embeddings)

    return db

def load_db(files):

    docs = []

    for file in files :
        # 문서 로드
        loader = PyPDFLoader(file)
        documents = loader.load()

        # 조각으로 자르기
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=150)
        docs += text_splitter.split_documents(documents)

    # 임베딩 정의
    embeddings = OpenAIEmbeddings()

    # 데이터로 in-memory 벡터 DB 만들기
    db = DocArrayInMemorySearch.from_documents(docs, embeddings)

    return db


def load_db_as_retreiver(files, k=5):

    db = load_db(files)

    # Retriever 정의 및 반환
    return db.as_retriever(search_type="similarity", search_kwargs={"k": k})

load_dotenv()
os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'
openai_api_key = os.getenv("OPENAI_API_KEY")

pdf_name = {'개요': 'C:\work\pdf\협동로봇_기술동향.pdf', 
            '기술동향': 'C:\work\pdf\협동로봇_기술동향.pdf',
            '시장특징': 'C:\work\pdf\협동로봇_기술동향.pdf',
            '국내 시장규모': 'C:\work\pdf\협동로봇시장_KISTI_국내시장규모.pdf',
            '세계 시장규모': 'C:\work\pdf\협동로봇시장_KISTI_세계시장규모.pdf',
            '국내 업체현황': 'C:\work\pdf\협동로봇시장_KISTI_업체현황.pdf',
            '해외 업체현황': 'C:\work\pdf\협동로봇시장_KISTI_업체현황.pdf',
            '시장요인': 'C:\work\pdf\협동로봇시장_KISTI_시장요인.pdf'
            }

market = '협동로봇'

overview_template = """{market}의 정의, 원리, 종류, 타 기술과의 특징 비교 등을 한글 2000자 분량으로 작성해줘.
"""

trend_template = """{market}에 대한 기술동향을 한글로 2000 글자가 되도록 작성해줘. 
기술동향에는 {market}의 원리, 세부종류, 핵심적인 요소기술, 최근 연구동향 등을 구체적으로 설명해줘. 
최근 연구동향은 국내외에서 누가 언제 어떤 기술을 개발했는지 3개 이상 나열해줘."""

characteristic_template = """{market} 산업과 시장에 대한 시장특징을 한글로 2000 글자가 되도록 작성해줘.
시장특징에는 {market} 산업이 어떤 특징을 가지고 있는 산업인지 정리해줘.
여러 가지 특징이 있다면 각각의 특징을 리스트업 해줘."""

size_template = """{market} 시장의 국내외 시장규모를 한글 2000 글자가 되도록 작성해줘.
국내외 시장규모는 {market} 시장규모와 성장률을 국내시장과 세계시장으로 구분하여 각각 구체적인 수치를 이용해서 표로 정리해줘.
가능한 많은 연도의 시장규모를 보여주고, 연간 성장률 및 미래 시점에 얼마의 시장규모를 형성할지 작성해줘.
국내 시장규모의 단위는 억 원을, 세계 시장규모의 단위는 백만 달러로 작성해줘."""

ko_size_template = """{market} 시장의 국내 시장규모를 한글 2000 글자가 되도록 작성해줘.
국내 시장규모는 {market} 시장규모와 성장률을 구체적인 수치를 이용해서 표로 정리해줘.
가능한 많은 연도의 시장규모를 보여주고, 연간 성장률 및 미래 시점에 얼마의 시장규모를 형성할지 작성해줘.
국내 시장규모의 단위는 억 원으로 작성해줘."""

wo_size_template = """{market} 시장의 세계 시장규모를 한글 2000 글자가 되도록 작성해줘.
세계 시장규모는 {market} 시장규모와 성장률을 구체적인 수치를 이용해서 표로 정리해줘.
가능한 많은 연도의 시장규모를 보여주고, 연간 성장률 및 미래 시점에 얼마의 시장규모를 형성할지 작성해줘.
세계 시장규모의 단위는 백만 달러로 작성해줘."""

ko_company_template = """{market} 시장의 국내 업체 현황을 한글 2000 글자가 되도록 작성해줘.
국내 업체 현황은 {market}을 연구개발 혹은 판매하고 있는 적어도 5개 이상의 국내 기업들의 현황을 정리해서 작성해줘.
각 기업들의 점유율을 포함해서 그 기업들이 언제 무엇을 어떻게 했는지 구체적으로 작성해줘. """

wo_company_template = """{market} 시장의 해외 업체 현황을 한글 2000 글자가 되도록 작성해줘.
해외 업체 현황은 {market}을 연구개발 혹은 판매하고 있는 적어도 5개 이상의 해외 기업들의 현황을 정리해서 작성해줘.
각 기업들의 점유율을 포함해서 그 기업들이 언제 무엇을 어떻게 했는지 구체적으로 작성해줘. """

factor_template = """{market} 시장의 촉진 및 저해요인을 한글 2000 글자가 되도록 작성해줘. 
어떤 요인들이 {market} 산업과 시장의 성장을 촉진할 것인지 혹은 저해할 것인지 정리해줘.
촉진요인을 먼저 5가지 이상 정리하고 그 후에 이어서 저해요인을 5가지 이상 정리해줘."""

system_message = "당신은 한국의 시장조사 전문가이다. 질문에 대해 항상 전문적인 관점에서 자세하게 대답해야 한다. 존대말을 사용하지 말고 ~ 이다. 로 끝내고, 개조식으로 작성하지 말고 서술식으로 작성해야 한다."

contents = {"개요": overview_template, 
            "기술동향": trend_template,
            "시장특징": characteristic_template,
            "국내 시장규모": ko_size_template,
            "세계 시장규모": wo_size_template,
            "국내 업체현황": ko_company_template,
            "해외 업체현황": wo_company_template,
            "시장요인": factor_template
            } 

# ChatGPT LLM 준비
llm = ChatOpenAI(model_name='gpt-3.5-turbo', 
                 openai_api_key = openai_api_key,
                 temperature=0,
                )
            
# 시장 분석 시작
for name, template in contents.items() :
    prompt = PromptTemplate(input_variables=["market"], template=template)
    question = prompt.format(market=market)

    db = load_single_db(pdf_name[name])
    docs = db.similarity_search(question, 2)
    merged_doc = ""

    for doc in docs :
        merged_doc += doc.page_content
    
    messages = [
    SystemMessage(
        content = system_message
    ),
    HumanMessage(
        content = question + merged_doc
    ), ]

    print(f"\n=========================== {name} ===========================\n")
    print(llm(messages).content)

