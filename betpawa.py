from bs4 import BeautifulSoup
import os
import requests
import urllib
import json

search_link = "https://www.betpawa.co.zm/events/ws/searchAll?searchValue="


# strhtml = requests.get(search_link)

# soup = BeautifulSoup(str(strhtml), "html5lib")
strings = []


def collect(data):

     events = json.loads(data)["events"]
     for event in events:
         name = event["name"]
         e_id= event["eventId"]
         collect_odds(name,e_id)
     txt = ""
     for string in strings:
        txt = txt+string

        with open("./odds.txt","w")as file:
            file.write(txt)

     # print(events)

def collect_odds(name, e_id):
    data = requests.get(search_link +name).json()["Data"]["Events"]["Events"]
    count = 1
    for event in data:
        if str(event["ExId"])==str(e_id):
            markets = event["Markets"]
            for market in markets:
                if market["GroupName"] == "1X2":
                    home_win = market["Prices"][0]["Price"]
                    draw = market["Prices"][1]["Price"]
                    away_win = market["Prices"][2]["Price"]

                    input_= name+"\n"+ "1   " +home_win + "  X  " +draw+ "  2  " +away_win+"\n \n"
                    strings.append(input_)
                    print("done " + str(count))
                    count = count+1


# def showmanship(u, d, t):


# collect("""{"id":336,"name":"emPawa17","paid":false,"status":"Active","prizeTotal":1000000,"fee":1.000,"allowedMin":13,"strategy":"STANDARD","eventsTotal":17,"hasWinners":false,"currencyFormat":"K %s","openTime":"2019-04-18T10:00:00","closeTime":"2019-04-21T10:00:00","freeTicketCount":0,"prizes":[{"id":null,"poolJurisdictionId":null,"templatePrizeId":null,"seed":1000000,"rolledOver":0,"wonPerTicket":null,"wonTickets":null,"mistakes":0},{"id":null,"poolJurisdictionId":null,"templatePrizeId":null,"seed":200000,"rolledOver":0,"wonPerTicket":null,"wonTickets":null,"mistakes":1},{"id":null,"poolJurisdictionId":null,"templatePrizeId":null,"seed":100000,"rolledOver":0,"wonPerTicket":null,"wonTickets":null,"mistakes":2},{"id":null,"poolJurisdictionId":null,"templatePrizeId":null,"seed":25000,"rolledOver":0,"wonPerTicket":null,"wonTickets":null,"mistakes":3},{"id":null,"poolJurisdictionId":null,"templatePrizeId":null,"seed":10000,"rolledOver":0,"wonPerTicket":null,"wonTickets":null,"mistakes":4}],"events":[{"eventId":527478,"poolId":336,"position":1,"scoreHome":null,"scoreAway":null,"cancelled":false,"name":"Levante UD - Espanyol","live":false,"started":false,"groupName":"Spain Primera Division","startDate":"2019-04-21T10:00:00"},{"eventId":527621,"poolId":336,"position":2,"scoreHome":null,"scoreAway":null,"cancelled":false,"name":"Excelsior - Willem II","live":false,"started":false,"groupName":"Netherlands Eredivisie","startDate":"2019-04-21T10:15:00"},{"eventId":528051,"poolId":336,"position":3,"scoreHome":null,"scoreAway":null,"cancelled":false,"name":"Ankaragucu - Torku Konyaspor","live":false,"started":false,"groupName":"Turkey Super Lig","startDate":"2019-04-21T10:30:00"},{"eventId":527502,"poolId":336,"position":4,"scoreHome":null,"scoreAway":null,"cancelled":false,"name":"Arminia Bielefeld - Ingolstadt","live":false,"started":false,"groupName":"Germany Bundesliga 2","startDate":"2019-04-21T11:30:00"},{"eventId":527470,"poolId":336,"position":5,"scoreHome":null,"scoreAway":null,"cancelled":false,"name":"Jahn Regensburg - FC Magdeburg","live":false,"started":false,"groupName":"Germany Bundesliga 2","startDate":"2019-04-21T11:30:00"},{"eventId":527460,"poolId":336,"position":6,"scoreHome":null,"scoreAway":null,"cancelled":false,"name":"Getafe - Sevilla","live":false,"started":false,"groupName":"Spain Primera Division","startDate":"2019-04-21T12:00:00"},{"eventId":527398,"poolId":336,"position":7,"scoreHome":null,"scoreAway":null,"cancelled":false,"name":"Everton - Manchester United","live":false,"started":false,"groupName":"England Premier League","startDate":"2019-04-21T12:30:00"},{"eventId":527603,"poolId":336,"position":8,"scoreHome":null,"scoreAway":null,"cancelled":false,"name":"Fortuna Sittard - NAC Breda","live":false,"started":false,"groupName":"Netherlands Eredivisie","startDate":"2019-04-21T12:30:00"},{"eventId":527761,"poolId":336,"position":9,"scoreHome":null,"scoreAway":null,"cancelled":false,"name":"Sturm Graz - Wolfsberger AC","live":false,"started":false,"groupName":"Austria Bundesliga","startDate":"2019-04-21T12:30:00"},{"eventId":527482,"poolId":336,"position":10,"scoreHome":null,"scoreAway":null,"cancelled":false,"name":"Toulouse FC - Lille","live":false,"started":false,"groupName":"France Ligue 1","startDate":"2019-04-21T13:00:00"},{"eventId":528270,"poolId":336,"position":11,"scoreHome":null,"scoreAway":null,"cancelled":false,"name":"Enosis - Anorthosis","live":false,"started":false,"groupName":"Cyprus Division 1","startDate":"2019-04-21T14:00:00"},{"eventId":527874,"poolId":336,"position":12,"scoreHome":null,"scoreAway":null,"cancelled":false,"name":"Lommel United - Roeselare","live":false,"started":false,"groupName":"Belgium Division 2","startDate":"2019-04-21T14:00:00"},{"eventId":527485,"poolId":336,"position":13,"scoreHome":null,"scoreAway":null,"cancelled":false,"name":"Reims - St Etienne","live":false,"started":false,"groupName":"France Ligue 1","startDate":"2019-04-21T15:00:00"},{"eventId":528043,"poolId":336,"position":14,"scoreHome":null,"scoreAway":null,"cancelled":false,"name":"Alanyaspor - Fenerbahce","live":false,"started":false,"groupName":"Turkey Super Lig","startDate":"2019-04-21T16:00:00"},{"eventId":527566,"poolId":336,"position":15,"scoreHome":null,"scoreAway":null,"cancelled":false,"name":"Anderlecht - Gent","live":false,"started":false,"groupName":"Belgium Pro League","startDate":"2019-04-21T16:00:00"},{"eventId":527503,"poolId":336,"position":16,"scoreHome":null,"scoreAway":null,"cancelled":false,"name":"Real Betis - Valencia","live":false,"started":false,"groupName":"Spain Primera Division","startDate":"2019-04-21T18:45:00"},{"eventId":528068,"poolId":336,"position":17,"scoreHome":null,"scoreAway":null,"cancelled":false,"name":"Corinthians - Sao Paulo","live":false,"started":false,"groupName":"Brazil Paulista A1","startDate":"2019-04-21T19:00:00"}]}""")
dataset = input("Enter paste dataset")
collect(dataset)