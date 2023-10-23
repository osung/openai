import os

def refine_data(filename, outfilename) :
    with open(filename, 'r') as file:
        selected_lines = [
            line.rstrip().rstrip(',') + '\n' if line.rstrip().endswith(',') else line 
            for line in file if line.strip().startswith('{"prompt":')
        ]
        
    # 선택된 줄만 다시 파일에 쓰기
    with open(outfilename, 'w') as file:
        file.writelines(selected_lines)

    # 확인을 위해 선택된 줄 출력
    for line in selected_lines:
        print(line.strip())

    print(len(selected_lines))


refine_data('C:\work\\finetuning\\ft_gene_therapy_en.txt', 'C:\work\\finetuning\\ft_gene_therapy_en_refine.jsonl')

refine_data('C:\work\\finetuning\\ft_micro_led_display_en.txt', 'C:\work\\finetuning\\ft_micro_led_display_en_refine.jsonl')
