import openai
import os
from dotenv import load_dotenv

load_dotenv()
os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'
openai.api_key = os.getenv("OPENAI_API_KEY")

openai.File.create(
    file = open("C:\work\\finetuning\\ft_gene_therapy_en_refine.jsonl", "rb"), 
    #file = open("C:\work\\finetuning\\ft_micro_led_display_en_refine.jsonl", "rb"), 
    purpose = 'fine-tune'
)
