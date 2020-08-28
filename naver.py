from selenium import webdriver
from bs4 import BeautifulSoup 
import csv
import os
import sys

keyword = sys.argv[1]
start_date = sys.argv[2]
end_date = sys.argv[3]


driver = webdriver.Chrome() 

url = "https://search.naver.com/search.naver?where=news&query={0}&sort=2&nso=so:da,"\
            "p:from{1}to{2},a:all&field=1".format(keyword, start_date, end_date)
infos = []

driver.get(url) 
driver.implicitly_wait(10) 

while True :
    html = driver.page_source 
    bs = BeautifulSoup(html,"html.parser")
    infos += bs.find("ul", class_="type01").find_all("li")

    next_page = bs.find("div", class_ = "paging").find_all("a")[-1]
    if(next_page.text != "다음페이지") :
        break

    driver.get("https://search.naver.com/search.naver" + next_page["href"])
    driver.implicitly_wait(10)



result = []

for info in infos :

    link = info.find("dl").find("a")["href"]
    title = info.find("dl").find("a")["title"]
    temp = info.find("dl").find("dd").text.split()
    where = temp[0]
    date = temp[1]  
    result.append([date, title, where, link])



if not(os.path.isdir(keyword)):
    os.makedirs(os.path.join(keyword))


f = open("{0}/naver_{1}_{2}.csv".format(keyword, start_date, end_date),"w",newline="") 
wr = csv.writer(f) 
wr.writerow(["date","title","where","link"]) 

for i in result : 
    wr.writerow(i) 


# f.close() 
driver.quit()