from bs4 import BeautifulSoup
import requests
import re
import csv
import sys
from konlpy.tag import Okt, Hannanum, Kkma, Komoran, Mecab
from collections import Counter
import argparse


url = 'https://www1.president.go.kr/articles/7940'
html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')
text = soup.get_text(' ', strip=True)
print(text)


text = re.sub('[0-9]+', '', text)
text = re.sub('[A-Za-z]+', '', text)
text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ·!』\\‘’|\(\)\[\]\<\>`\'…》}{;\n\t\r_]', '', text)
print(text)

okt = Okt()
# Hannanum, Kkma, Komoran, Mecab, Okt
# 한나눔 = KAIST
# Kkma = 서울대
# Komoran Shineware
# Mecab 일본어용 형태소 분석기를 한국어에 사용할 수 있도록 수정
# Okt = 오픈 소스 / 과거에는 트위터 형태소 분석기


# nouns = 명사 반환
noun = okt.nouns(text)
print(noun)

# # morphs = 형태소 반환
# noun = okt.morphs(text)
# print(noun)

# # phrases = 어절 반환
# noun = okt.phrases(text)
# print(noun)

# pos = 품사 반환
# noun = okt.pos(text)
# print(noun)


temp = []
for i in noun :
    if(len(i) >= 2) :
        temp.append(i)
print(temp)
noun = temp

count = Counter(noun)
print(count)

print(count.most_common(10))

sys.exit(1)


parser = argparse.ArgumentParser()

parser.add_argument('--keyword', required=True, help = "검색할 키워드")
parser.add_argument('--start', required=True, help = "시작할 날짜")
parser.add_argument('--end', required=True, help = "끝나는 날짜")
parser.add_argument('--frequency', required=True, help = "찾고 싶은 단어")

args = parser.parse_args()

keyword = args.keyword
start_date = args.start
end_date = args.end
frequency = args.frequency


f = open("{0}/naver_{1}_{2}.csv".format(keyword, start_date, end_date),"r") 

rdr = csv.reader(f) 
# print(rdr)
rdr = list(rdr)[1:]

okt = Okt()

result = {}

text = ""
for i, line in enumerate(rdr) :
    date = line[0]
    url = line[-1]
    try :
        html = requests.get(url)
        if not html.ok:
            print("Error")
            continue
        soup = BeautifulSoup(html.text, 'html.parser')
        text = soup.get_text(' ', strip=True)
        text = re.sub('[0-9]+', '', text)
        text = re.sub('[A-Za-z]+', '', text)
        text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ·!』\\‘’|\(\)\[\]\<\>`\'…》}{;\n\t\r]', '', text)
        noun = okt.nouns(text)
        count = Counter(noun)
        if count[frequency] != 0 :        
            if date in result:
                result[date] += count[frequency]
            else:
                result[date] = count[frequency]
        
    except :
        pass

    print(i+1)

f.close()

print(result)

f = open("{0}/naver_{1}_{2}_{3}.csv".format(keyword, start_date, end_date, frequency),"w",newline="") 
wr = csv.writer(f) 
wr.writerow(["date", "count"]) 

print("Start writerow")

for key in result:
    wr.writerow([key,result[key]])

f.close()
print("Finish")


