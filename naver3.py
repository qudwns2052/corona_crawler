from bs4 import BeautifulSoup
import requests
import re
import csv
import sys
import os
from konlpy.tag import Okt, Hannanum, Kkma, Komoran
from collections import Counter
import argparse
import operator
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import rc

parser = argparse.ArgumentParser()

parser.add_argument('--keyword', required=True, help = "검색할 키워드")
parser.add_argument('--start', required=True, help = "시작할 날짜")
parser.add_argument('--end', required=True, help = "끝나는 날짜")

args = parser.parse_args()

keyword = args.keyword
start_date = args.start
end_date = args.end

def get_csv_data() :
    f = open("{0}/naver_{1}_{2}.csv".format(keyword, start_date, end_date),"r", encoding='utf-8') 
    rdr = csv.reader(f) 
    rdr = list(rdr)[1:]
    f.close()
    return rdr

def save_cloud(li, collect_date) :
    collect_date = collect_date[:-1]
    count = Counter(li)
    wc = WordCloud(font_path='/Library/Fonts/NanumSquareB.ttf', background_color='white', width=800, height=600)
    cloud = wc.generate_from_frequencies(dict(count))
    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(cloud)

    if not(os.path.isdir("{0}_wordcloud".format(keyword))):
        os.makedirs(os.path.join("{0}_wordcloud".format(keyword)))

    plt.savefig('{0}_wordcloud/{1}.jpg'.format(keyword, collect_date))
    plt.close()
    
    f = open("{0}_wordcloud/{1}.csv".format(keyword, collect_date),"w",newline="", encoding='utf-8') 
    wr = csv.writer(f) 
    wr.writerow(["word", "count"]) 

    count = sorted(count.items(), key=operator.itemgetter(1), reverse=True)
    for i in count : 
        wr.writerow(list(i))
    f.close()




if __name__ == "__main__":
    data = get_csv_data()
    okt = Okt()
    result = {}
    li = []
    temp_date = data[0][0]

    for i, line in enumerate(data) :
        date = line[0]
        text = line[1]
        text = re.sub('[0-9]+', '', text)
        text = re.sub('[A-Za-z]+', '', text)
        text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ·!』\\‘’|\(\)\[\]\<\>`\'…》}{;\n\t\r]', '', text)
        noun = okt.nouns(text)
        if(len(noun) == 0) :
            continue

        if(temp_date != date) :
            save_cloud(li, temp_date)
            li = []
            print("Save {0}".format(temp_date))
            temp_date = date

        for j in noun :
                if(len(j) > 1) :
                    li.append(j)    
    
    save_cloud(li, temp_date)
    print("Save {0}".format(temp_date))

