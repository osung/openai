import json
import sys

#market = "micro_led_display"
market = "gene_therapy"

infilename = f"C:\work\\finetuning\\ft_{market}_en_refine.jsonl"
outfilename = f"C:\work\\finetuning\\ft_{market}_en_chat_all.jsonl"

# 입력 파일을 읽기
with open(infilename, 'r', encoding='utf-8') as infile:
    # 출력 파일을 쓰기
    with open(outfilename, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # 각 줄의 JSON 객체를 파싱
            obj = json.loads(line)
            print(obj)
            # 새 형식으로 변환
            new_obj = {
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": obj['prompt']},
                    {"role": "assistant", "content": obj['completion']}
                ]
            }
            # 변환된 객체를 출력 파일에 쓰기
            outfile.write(json.dumps(new_obj) + '\n')
            