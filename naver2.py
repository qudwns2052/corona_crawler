from bs4 import BeautifulSoup
import requests
import re
import csv
import sys
from konlpy.tag import Okt, Hannanum, Kkma, Komoran
from collections import Counter
import argparse

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
# hannanum = Hannanum()
# komoran = Komoran()

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
        # noun = hannanum.nouns(text)
        # noun = komoran.morphs(text)
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

result2 = []
for key in result:
    wr.writerow([key,result[key]])

f.close()
print("Finish")


# url = 'https://www1.president.go.kr/articles/7940'
# html = requests.get(url)
# soup = BeautifulSoup(html.text, 'html.parser')
# text = soup.get_text(' ', strip=True)

# okt = Okt()
# noun = okt.nouns(text)
# count = Counter(noun)

# noun_list = count.most_common(10)
# for v in noun_list :
#     print(v)

# text = re.sub('[0-9]+', '', text)
# text = re.sub('[A-Za-z]+', '', text)
# text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ·!』\\‘’|\(\)\[\]\<\>`\'…》}{;\n\t\r]', '', text)

# print(okt.morphs(text))

