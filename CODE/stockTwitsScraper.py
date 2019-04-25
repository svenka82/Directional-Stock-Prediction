import requests
import urllib.request
import time, json, os, traceback
from json import JSONDecodeError
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import sleep
from collections import deque

class StockTwitsAPIScraper:
    def __init__(self, symbol, date, maxId, queue):
        self.symbol = symbol
        self.stockTwitsDomain = "https://api.stocktwits.com/api/2/streams/symbol/{}.json?".format(symbol)
        self.dateStr = date.strftime("%Y%m%d")
        self.targetDate = date
        self.tweets = []
        self.reqeustQueue = queue
        self.maxId = maxId

    def setLimits(self, size, duration):
        self.size = size
        self.duration = duration
        self.requestInterval = duration // size + 1 if duration % size else duration // size

    # write tweets we get and the ID of the last tweet in case system break down
    def writeJson(self):
        if self.tweets:
            fileName = "stockTwitsJson/{}/{}.json".format(self.symbol, self.tweets[0]["id"])
            with open(fileName, "w") as f:
                json.dump(self.tweets, f)
            self.maxId = self.tweets[-1]["id"]
            print(datetime.now(), self.maxId, len(self.tweets), self.tweets[-1]["time"])
            lastRequest = {}
            with open("lastRequestStockTwits.json", "r") as f:
                lastRequest = json.load(f)
            with open("lastRequestStockTwits.json", "w") as f:                
                lastRequest[self.symbol]["date"] = self.dateStr
                lastRequest[self.symbol]["maxId"] = self.maxId
                json.dump(lastRequest, f)
    
    def getCurrentUrl(self):
        return self.stockTwitsDomain + "max={}".format(self.maxId)

    # request manager
    # can't exceed 200 requests within an hour
    def requestManager(self):
        if len(self.reqeustQueue) == self.size:
            now = datetime.now()
            firstRequest = self.reqeustQueue.popleft()
            if now < firstRequest + timedelta(seconds=self.duration):
                timeDiff = firstRequest - now
                waitTime = timeDiff.total_seconds() + 1 + self.duration                
                print("Reach request limit, wait for {} seconds.".format(waitTime))
                sleep(waitTime)

    def getMessages(self, url):
        self.requestManager()

        response = requests.get(url)
        self.reqeustQueue.append(datetime.now())
        try:
            data = json.loads(response.text)
        except JSONDecodeError:
            if "Gateway" in response.text:
                print("A small Gateway issue, just wait for 1 minute.")
                sleep(60)
                return True
            print(len(self.reqeustQueue))
            print(self.reqeustQueue[0], datetime.now())
            print(url)
            print(response.text)
            print(traceback.format_exc())
            raise Exception("Something worong with the response.")
        if data and data["response"]["status"] == 200:
            data["cursor"]["max"]
            for m in data["messages"]:
                record = {}            
                createdAt = datetime.strptime(m["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                if createdAt < self.targetDate:
                    return False
                record["id"] = m["id"]
                record["text"] = m["body"]
                record["time"] = createdAt.timestamp()
                record["sentiment"] = m["entities"]["sentiment"]["basic"] if m["entities"]["sentiment"] else ""
                self.tweets.append(record)
            self.maxId = self.tweets[-1]["id"]
        else:
            print(response.text)
        sleep(self.requestInterval)
        return True

    def getFiveRequestsAndWriteToFile(self):
        for _ in range(5):
            if not self.getMessages(self.getCurrentUrl()):
                break
        if self.tweets:
            self.writeJson()        
        print("Scrap {} tweets starting from {}.".format(len(self.tweets), self.maxId))
        self.tweets.clear()
        return True

    def scrapTweets(self):        
        try:
            doScrap = True
            while doScrap:
                doScrap = self.getFiveRequestsAndWriteToFile()
        except Exception:
            print(traceback.format_exc())

startDate = input("Enter the earliest date you want to scrap (mmddyyyy):")
symbol = input("Enter the stock symbol: ").upper()
startDate = datetime.strptime(startDate, "%m%d%Y")

with open("lastRequestStockTwits.json", "r") as f:
    data = json.load(f)
    if data[symbol]["maxId"] < maxId:
        maxId = data[symbol]["maxId"]

queue = deque()
scraper = StockTwitsAPIScraper(symbol.upper(), startDate, maxId, queue)    
scraper.setLimits(200, 3600)
scraper.scrapTweets()