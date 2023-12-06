import os

#file = open('C:\work\finetuning\231020_ftdata_gene therapy_26to145p.txt')

# 파일을 읽기 모드로 열기 ('euc-kr' 인코딩으로 읽기)
with open('C:\work\\finetuning\\231020_ftdata_gene therapy_26to145p.txt', 'r', encoding='euc-kr') as file:
    lines = file.readlines()

print(lines)


with open('C:\work\\finetuning\\micro_led_display.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

print(lines)


# 각 라인을 utf-8로 인코딩하고 출력
#utf8_encoded_lines = [line.decode('euc-kr').encode('utf-8') for line in lines]

# utf-8로 인코딩된 라인을 출력 (바이트 형태로 출력됨)
#for utf8_line in utf8_encoded_lines:
#    print(utf8_line)
