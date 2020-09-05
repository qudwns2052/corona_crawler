from selenium import webdriver
from bs4 import BeautifulSoup 
import csv
import os
import sys
import re
import argparse

<<<<<<< HEAD

# args 받는 방법 변경 -> flag 사용하는 것으로 
keyword = sys.argv[1] # 코로나
start_date = sys.argv[2] # 20200101
end_date = sys.argv[3] # 20200131
=======
parser = argparse.ArgumentParser()

parser.add_argument('--keyword', required=True, help = "검색할 키워드")
parser.add_argument('--start', required=True, help = "시작할 날짜")
parser.add_argument('--end', required=True, help = "끝나는 날짜")

args = parser.parse_args()


keyword = args.keyword
start_date = args.start
end_date = args.end
>>>>>>> origin/master

options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome('./chromedriver', chrome_options=options) 

url = "https://search.naver.com/search.naver?where=news&query={0}&sort=2&nso=so:da,"\
            "p:from{1}to{2},a:all&field=1".format(keyword, start_date, end_date)

infos = []

driver.get(url) 
driver.implicitly_wait(10) 


cnt = 1
before_date = ""
while True :
    html = driver.page_source 
    bs = BeautifulSoup(html,"html.parser")
    infos += bs.find("ul", class_="type01").find_all("li")

    next_page = bs.find("div", class_ = "paging").find_all("a")[-1]
    if((next_page.text != "다음페이지") and (cnt != 400)) :
        break

    cnt+=1

    if(cnt <= 400) :
        driver.get("https://search.naver.com/search.naver" + next_page["href"])
        driver.implicitly_wait(10)
    else :
        temp = infos[-1].find("dl").find("dd").text
        # try :
        pattern = r'\d+.\d+.\d+.' 
        r = re.compile(pattern)
        temp_date = r.search(temp).group(0).replace(".","")
        
        if(temp_date == before_date) :
            if(int(end_date) == int(temp_date)) :
                break
            else :
                temp_date = str(int(temp_date) + 1)

        before_date = temp_date

        url = "https://search.naver.com/search.naver?where=news&query={0}&sort=2&nso=so:da,"\
            "p:from{1}to{2},a:all&field=1".format(keyword, temp_date, end_date)
        driver.get(url)
        driver.implicitly_wait(10)
        cnt = 1

print("Finish make infos")



temp = []
for i in infos :
    if (i not in temp) :
        temp.append(i)

infos = temp

result = []

print("Start get info")

for info in infos :

    link = info.find("dl").find("a")["href"]
    title = info.find("dl").find("a")["title"]
    temp = info.find("dl").find("dd").text

    try :
        pattern = r'\d+.\d+.\d+.' 
        r = re.compile(pattern)
        date = r.search(temp).group(0) 
    except AttributeError:
        pattern = r'\w* (\d\w*)' 
        r = re.compile(pattern)
        date = r.search(temp).group(1)
        
    where = temp.split()[0]
    result.append([date, title, where, link])



if not(os.path.isdir(keyword)):
    os.makedirs(os.path.join(keyword))


f = open("{0}/naver_{1}_{2}.csv".format(keyword, start_date, end_date),"w",newline="") 
wr = csv.writer(f) 
wr.writerow(["date","title","where","link"]) 

print("Start writerow")

for i in result : 
    wr.writerow(i)


f.close() 
driver.quit()

print("Finish")
