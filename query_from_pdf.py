import PyPDF2
import openai
import os
from dotenv import load_dotenv

load_dotenv()
os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'
openai.api_key = os.getenv("OPENAI_API_KEY")

question = "다음 문서를 읽고 유럽의 오픈소스 정책에 대해서 상세히 알려줘."
system_message = "You are an industrial market expert in Korea. You have to give specialied and detailed answers. Always answer in Korean." # but write in English for technical terms and proper names."

max_tokens = 2000

# PDF 파일 열기
pdf_file_path = 'C:\work\pdf\opensource.pdf'
pdf_file = open(pdf_file_path, 'rb')

# PDF 파일을 텍스트로 변환
pdf_reader = PyPDF2.PdfReader(pdf_file)
text_list = []

# 페이지 번호는 0부터 시작!!!
for page_num in range(25,28):
    page = pdf_reader.pages[page_num]
    text_list.append(page.extract_text())

#print(pdf_text)
pdf_text = " ".join(text_list)

messages = [
    {"role": "system", "content": system_message}, 
    {"role": "user", "content": question + pdf_text}
]

response = openai.ChatCompletion.create(
    model="gpt-4", #3.5-turbo",
    messages=messages,
    temperature=0.0,  # 창의성을 조절하는 옵션
    max_tokens=max_tokens,  # 답변의 최대 토큰 수 설정
)

# API 응답에서 답변을 추출합니다.
answer = response['choices'][0]['message']['content']

# 답변을 출력합니다.
print(answer)
