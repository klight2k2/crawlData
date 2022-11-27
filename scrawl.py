import requests;
from bs4 import BeautifulSoup as BS;
import json
from pathlib import Path
def crawlListTruyen():
    urlTruyen="https://truyenqqpro.com/top-ngay/trang-"
    startPage=1
    item=[]
    endPage=264
    for currPage in range(startPage,endPage):
        print("page" +str(currPage))
        urlTruyen="https://truyenqqpro.com/top-ngay/trang-"+str(currPage)+".html"
        content=BS(requests.get(urlTruyen).text, 'html.parser')
        listTruyen=content.find("ul",{"class":"list_grid grid"}).find_all("li")
        for truyen in listTruyen:
            
            # print(truyen.find("div",class_="book_avatar").find("a"))
            title=truyen.find("div",class_="book_avatar").find("a").find("img")["alt"]
            linkTruyen=truyen.find("div",class_="book_avatar").find("a")["href"]
            chapters=getAllChapter(linkTruyen)
            # print(title)
            # print(linkTruyen)
            item.append({"title":title,"linkTruyen":linkTruyen,"chapters":chapters})
            break
    with open('test.json', 'w', encoding="utf-8") as f:
        f.write(json.dumps(item,ensure_ascii=False))
        f.close()

def getAllChapter(linkTruyen):
    titleTruyen=str(linkTruyen).split("/")[-1]
    Path("./"+titleTruyen).mkdir(parents=True, exist_ok=True)
    content=BS(requests.get(linkTruyen).text, 'html.parser')
    chapters=content.find("div",{"class":"works-chapter-list"}).find_all("div",{"class":"works-chapter-item"})
    listInfoChapter=[]
    for chapter in chapters:
        infoChapter={
            "nameChapter":chapter.find("a").text,
            "datePublish":str(chapter.find("div",{"class":"time-chap"}).text).strip(),
            "linkChapter":chapter.find("a")["href"]
        }
        print(infoChapter.get("nameChapter"))
        linkFolder="./"+titleTruyen+"/"+infoChapter.get("nameChapter")
        Path(linkFolder).mkdir(parents=True, exist_ok=True)
        getDetailChapter(infoChapter.get("linkChapter"),linkFolder)
        listInfoChapter.append(infoChapter)
    return listInfoChapter

def getDetailChapter(linkChapter,linkFolder):
    content=BS(requests.get(linkChapter).text, 'html.parser')
    content.find("div",{"id":"page_999"}).decompose()
    chapters=content.find("div",{"class":"chapter_content"}).find_all("div",{"class":"page-chapter"})
    listImageLink=[]
    for index,page in enumerate(chapters):
        page=page.find("img")
        if(page):
            listImageLink.append(page["src"])
            downloadImage(page["src"],linkFolder,index)
       
def downloadImage(linkImage,folder,index):
    fixedName=folder+"/"+str(index)+".jpg"
    headers = {
        'referer': 'Referer: https://truyenqqpro.com'
    }

    r = requests.get(linkImage, headers=headers)

    # print(r.content[:100])  # you can see string `JFIF` or `GIF` in content

    f = open(fixedName, 'wb')
    f.write(r.content)
    f.close()
# crawlListTruyen()
# getAllChapter("https://truyenqqpro.com/truyen-tranh/thanh-nu-gia-mao-cua-nam-13347")
# getDetailChapter("https://truyenqqpro.com/truyen-tranh/tu-truyen-cua-fujiko-fujio-10966-chap-1.html")
# url="https://truyenqqpro.com/truyen-tranh/thanh-guom-diet-quy-2624-chap-205.html"
# image="https://z-cdn.zinmanga.com/manga_e053e4f47a7ccbc51be254596e483d7c/chapter_0//chap_0_12.jpg"
# r=requests.get(image)
# print(scraper.get(image)) 
# print(r.text)
# response = requests.get("https://battwo.com/chapter/2093337")
# print(response.text)

# import requests

# url = 'https://i125.tintruyen.net/2624/fix-205/2.jpg?d=dfgd6546'

# headers = {
#     'referer': 'Referer: https://truyenqqpro.com/truyen-tranh/thanh-guom-diet-quy-2624-chap-205.html'
# }

# r = requests.get(url, headers=headers)

# print(r.content[:100])  # you can see string `JFIF` or `GIF` in content

# f = open('output_2.jpg', 'wb')
# f.write(r.content)
# f.close()