import os

def refine_data(filename, outfilename, encoding='euc-kr') :
    with open(filename, 'r', encoding=encoding) as file:
        selected_lines = [line for line in file if line.strip().startswith('{"prompt":')]

    # 선택된 줄만 다시 파일에 쓰기
    with open(outfilename, 'w', encoding='utf-8') as file:
        file.writelines(selected_lines)

    # 확인을 위해 선택된 줄 출력
    for line in selected_lines:
        print(line.strip())

    print(len(selected_lines))


refine_data('C:\work\\finetuning\\ft_gene therapy.txt', 'C:\work\\finetuning\\ft_gene_therapy_refine.jsonl')

refine_data('C:\work\\finetuning\\ft_micro_led_display.txt', 'C:\work\\finetuning\\ft_micro_led_display_refine.jsonl', encoding='utf-8')
