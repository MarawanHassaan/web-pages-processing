import requests
import csv
import time
from bs4 import BeautifulSoup

f = open("apartments.tsv", "wt", encoding='utf-8', newline='')
tsv_writer = csv.writer(f, delimiter='\t')
#write header
tsv_writer.writerow(["title", "desc", "location", "price", "t", "link"])

url = "https://www.kijiji.it/case/affitto/roma-annunci-roma/"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

last_page = int(soup.find("a", {"class": "last-page"}).getText(strip=True))
#strip removes and strips the unneeded spaces in the html line, the last page has field a with class last-page

#total number of apartments
total_num = 0
#number of apartments except ads
num_apt = 0

#list of top announcments
top_ann = []

for i in range(last_page):
    print("Parsing page ", i)
    if (i>0):
        r = requests.get(url, params = {"p": i+1}) #The following pages are in format of url/?p=i+1
        soup = BeautifulSoup(r.text, "html.parser")

    #ul is a container of all the apts, each apartment is is a li element    
    apartments = soup.find("ul", {"id": "search-result"}).findAll("li")

    #apt is a <li> element
    for apt in apartments:
        
        #if it's not an apartment, skip it
        #ex: <li class="dfp-banner-slot" id="KWM_SA"></li>
        if not (apt.find("div", {"class": "item-content"})):
            continue

        #check if top announcement
        if (apt.find("span", {"class": "top"})):
            data_id = apt.attrs["data-id"]
            
            #if it's in top_ann then we already have it
            if (data_id in top_ann):
                continue
            
            #else we add it
            top_ann.append(data_id)

        #at this point we know apt is a new apartment and the total number is basically all the apartments whether it is an ad or top one or a normal one
        total_num += 1

        #if it's an ad, skip it
        #"flag flag-YELLOW" is a class for ads
        if(apt.find("span", {"class": "flag flag-YELLOW"})):
            continue

        #at this point we know apt is a new apartment and it's not an ad
        num_apt += 1
        
        title = apt.find("h3", {"class": "title"}).getText(strip=True)
        desc = apt.find("p", {"class": "description"}).getText(strip=True).replace("\n","")
        location = apt.find("p", {"class": "locale"}).getText(strip=True)
        t = apt.find("p", {"class": "timestamp"}).getText(strip=True)
        price = apt.find("h4", {"class": "price"}).getText(strip=True).replace(" ", "").replace("€", "").replace(".", "")

        #This means there is no price and contact the owner
        if (price != "Contattal'utente"):
            price = int(price)
            
        link = apt["data-href"]
        
        tsv_writer.writerow([title, desc, location, price, t, link])

    time.sleep(1)
    
f.close()

print("Total number of apartments including ads: ", total_num)
print("Number of apartments without ads: ", num_apt)
print("Number of top announcements: ", len(top_ann))

