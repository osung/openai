import openai
import os
from dotenv import load_dotenv

load_dotenv()
os.environ['CURL_CA_BUNDLE'] = 'C:\work\kisti_cert.crt'
openai.api_key = os.getenv("OPENAI_API_KEY")

ret_file = openai.File.create(
    file = open("C:\work\\finetuning\\ft_gene_therapy_en_sample.jsonl", "rb"), 
    #file = open("C:\work\\finetuning\\ft_micro_led_display_en_sample.jsonl", "rb"),
    purpose = 'fine-tune'
)

print(ret_file)

ret_model = openai.FineTuningJob.create(training_file=ret_file.id, model="davinci-002")

print(ret_model)
