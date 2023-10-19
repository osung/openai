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

    # Retriever 정의 및 반환
    return db.as_retriever(search_type="similarity", search_kwargs={"k": k})



load_dotenv()
os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'
openai_api_key = os.getenv("OPENAI_API_KEY")

pdf_file_path = 'C:\work\pdf\Blockchain_Market_M&M.pdf'
market = 'blockchain'

trend_template = """{market}에 대한 기술동향을 한글로 2000 글자가 되도록 작성해줘. 
기술동향에는 {market}의 원리, 세부종류, 핵심적인 요소기술, 최근 연구동향 등을 구체적으로 설명해줘. 
최근 연구동향은 국내외에서 누가 언제 어떤 기술을 개발했는지 3개 이상 나열해줘."""

characteristic_template = """{market} 산업과 시장에 대한 시장특징을 한글로 500 글자가 되도록 작성해줘.
시장특징에는 {market} 산업이 어떤 특징을 가지고 있는 산업인지 정리해줘.
여러 가지 특징이 있다면 각각의 특징을 리스트업 해줘. """

size_template = """국내외 {market} 시장규모를 한글 500 글자가 되도록 작성해줘.
국내외 시장규모는 {market} 시장규모와 성장률을 국내시장과 세계시장으로 구분하여 각각 구체적인 수치를 이용해서 작성해줘.
가능한 많은 연도의 시장규모를 알려주고 향후 몇 %의 성장률을 보여 미래 시점에 얼마의 시장규모를 형성할지 작성해줘."""

company_template = """{market} 시장의 업체현황을 한글 1000 글자가 되도록 작성해줘.
업체현황은 {market}을 연구개발 혹은 판매하고 있는 5개 이상의 기업들의 현황을 정리해서 작성해줘.
그 기업들이 언제 무엇을 어떻게 했는지 구체적으로 작성해줘. 
"""

factor_template = """{market} 시장의 촉진 및 저해요인을 한글 1000 글자가 되도록 작성해줘. 
정치, 경제, 사회, 기술적인 관점에서 어떤 요인들이 {market} 산업과 시장의 성장을 촉진할 것인지 혹은 저해할 것인지 정리해줘.
촉진요인을 먼저 5가지 이상 정리하고 그 후에 이어서 저해요인을 5가지 이상 정리해줘."""

prompt = PromptTemplate(input_variables=["market"], template=company_template)
question = prompt.format(market=market)
print(question)

system_message = "You are an industrial market expert in Korea. You have to give specialied and detailed answers. Always answer in Korean but write in English for the technical terms and the proper names."

# PDF 문서 로드
retriever = load_db(pdf_file_path)
print("DB loading 완료")

llm = ChatOpenAI(model_name='gpt-4', #3.5-turbo', 
                 openai_api_key = openai_api_key,
                 temperature=0,
                )

chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
)

print(chain.run(question))
