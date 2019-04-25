import requests
import urllib.request
import time, re, json, os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class Headline:
    def __init__(self, url, time):
        self.url = url
        self.time = time

class NasdaqWebScraer:
    def __init__(self, symbol):
        self.symbol = symbol
        self.domain = "https://www.nasdaq.com/symbol/{}/news-headlines?page=".format(symbol)

    def writeLastRequest(self, page):
        tempData = {}
        with open("lastRequestNasdaq.json", "r") as f:
            tempData = json.load(f)
        tempData[self.symbol]["page"] = max(page, tempData[self.symbol]["page"])
        with open("lastRequestNasdaq.json", "w") as f:
            json.dump(tempData, f)

    def writeData(self, data, date):
        directory = "nasdaqJson/{}".format(self.symbol)
        if not os.path.exists(directory):
            os.makedirs(directory)
        path = "nasdaqJson/{}/{}.json".format(self.symbol, date.strftime("%Y%m%d"))
        if not os.path.isfile(path) and data:
            with open(path, "w") as f:
                json.dump(data, f)

    def scrapNews(self, start, end):
        startDate = datetime.strptime(start, "%m/%d/%Y")
        targetDate = datetime.strptime(end, "%m/%d/%Y")
        page = 1
        with open("lastRequestNasdaq.json", "r") as f:
            data = json.load(f)
            if self.symbol in data:
                page = data[self.symbol]["page"] if data[self.symbol]["page"] else page
        
        while targetDate >= startDate:
            page = self.scrapNewsByDate(targetDate, page)
            targetDate -= timedelta(days=1)
    
    def scrapNewsByDate(self, date, page):
        print("Scrap News on {}......".format(date.strftime("%m%d%Y")))
        urls, page = self.scrapNewsUrl(date, page)        
        self.scrapArticles(urls, date)
        print("Scrap {} News on {}.".format(len(urls), date.strftime("%m%d%Y")))
        self.writeLastRequest(page)
        return page

    def scrapNewsUrl(self, targetDate, page):
        urls, doScrap = [], True
        timeRE = r"[1-2]?[0-9]\/[1-3]?[0-9]\/201[4-9]?\s\d{1,2}:\d{1,2}:\d{1,2}\s(?:AM|PM)"       

        while doScrap:
            domainUrl = self.domain + str(page)
            response = requests.get(domainUrl)

            soup = BeautifulSoup(response.text, "html.parser")
            articleList = soup.find("div", {"class": "news-headlines"})
            headlines = articleList.find_all("div", {"class": None})

            tempHeadlines = []
            for h in headlines[:10]:
                url = h.select_one("span.fontS14px a")['href']        
                timeStr = h.select_one("small").text
                time = re.findall(timeRE, timeStr)[0]
                utcTime = datetime.strptime(time, "%m/%d/%Y %I:%M:%S %p")
                if utcTime.date() == targetDate.date():
                    urls.append(Headline(url, utcTime))
                elif utcTime < targetDate:
                    return urls, page
            urls += tempHeadlines
            page += 1
        return urls, page
        
    def scrapArticles(self, urls, date):
        articles = []
        for headline in urls:
            try:
                articles.append(self.scrapOneArticle(headline))
            except Exception as e:
                pass
        self.writeData(articles, date)
    
    def scrapOneArticle(self, headline):
        response = requests.get(headline.url)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("h1", {"itemprop": "headline"}).text
        articleBodyDiv = soup.find("div", {"id": "articlebody"})
        articleTextDiv = articleBodyDiv.find("div", {"id": "articleText"})
        article = {}
        article["time"] = headline.time.timestamp()
        if articleTextDiv:
            text = re.sub(r"\s+", " ", articleTextDiv.text).strip()
            article["text"] = title + " " + text        
        else:
            textFromP = []
            for child in articleBodyDiv.findChildren(recursive=False):
                if child.name == "p":
                    textFromP.append(child.text)
                elif child.name == "span" and "copyright" in child.attrs["class"]:
                    break
            text = " ".join(textFromP)
            text = re.sub(r"\s+", " ", text).strip()
            article["text"] = title + " " + text 
        return article

startDate = input("Enter the most recent date you want to scrap (mm/dd/yyyy) and the scraper will scrap foward to the past:")
symbol = input("Enter the stock symbol: ")
aaplNewsScraper = NasdaqWebScraer(symbol.lower())
aaplNewsScraper.scrapNews("06/29/2014", startDate)
print("done.")