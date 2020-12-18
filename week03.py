import time
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)
db=client.dbMusic_Chart
#실시간 시간
RRealTime = time.strftime('%Y%m%d%H', time.localtime(time.time()))
RealTime = time.strftime('%Y%m%d', time.localtime(time.time()))
hour = time.localtime(time.time()).tm_hour
RRT = str(RRealTime)
RT = str(RealTime)
H = str(hour)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
class MusicChart:
    def GenieChart(url):
        U = str(url)
        data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd='+RT+'&hh='+H+'&rtm=Y&pg='+U, headers = headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        Genies = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
        for Genie in Genies:
            title = Genie.select_one('td.info > a.title.ellipsis').text.strip()
            rank = Genie.select_one('td.number').text[0:5].strip()
            artist = Genie.select_one('td.info > a.artist.ellipsis').text.strip()
            print(rank, title +' - '+ artist)
            doc={
                'rank': rank,
                'title': title,
                'artist': artist
            }
            db.Genies.insert_one(doc)
    def MelonChart(url):
        rank_num = 1
        data = requests.get('https://www.melon.com/chart/index.htm?dayTime='+RRT, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        Melons = soup.select('#frm > div > table > tbody > tr')
        for Melon in Melons:
            title = Melon.select_one('td:nth-child(4) > div > div > div.ellipsis.rank01 > span > a').text
            rank = rank_num
            artist = Melon.select_one('td:nth-child(4) > div > div > div.ellipsis.rank02').text.strip()
            print(rank, title + ' - ' + artist)
            rank_num += 1
            doc = {
                'rank': rank,
                'title': title,
                'artist': artist
            }
            db.Melons.insert_one(doc)
    def BugsChart(url):
        data = requests.get('https://music.bugs.co.kr/chart/track/realtime/total?chartdate='+RT+'&charthour='+H,headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        Bugs = soup.select('#CHARTrealtime > table > tbody > tr')
        for bug in Bugs:
            title = bug.select_one('th > p > a').text
            rank = bug.select_one('td > div > strong').text
            artist = bug.select_one('td > p > a').text
            print(rank, title + ' - ' + artist)
            doc = {
                'rank': rank,
                'title': title,
                'artist': artist
            }
            db.Bugs.insert_one(doc)

    def List200(num):
        for i in range(1, num + 1):
            MusicChart.GenieChart(i)

M = MusicChart()
#지니차트 실시간
MusicChart.List200(4)
#멜론차트 24hit 차트
M.MelonChart()
#벅스차트 실시간
M.BugsChart()