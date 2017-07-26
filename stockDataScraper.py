from bs4 import BeautifulSoup

import webbrowser
import requests

def get_market():
    supported_markets = ["NASDAQ", "TSE", "NYSE", "FRA", "TYO"]
    market = "xyz"
    while market not in supported_markets:
        market = input("Market (NASDAQ, TSE, NYSE, FRA, TYO):")
        market = market.upper()
    
    return market

def get_ticker_data(market):
    url = input("Ticker: ")
    r = requests.get("https://www.google.com/finance/historical?q="+ market + "%3A" + url)             
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    raw_data = []

    for link in soup.find_all("td", {"class": "lm"}):
        raw_data.append(link.text)

    if raw_data == []:
        print("Enter a valid ticker")
        get_ticker_data(market)

    return raw_data, url

def manipulate_raw_data(raw_data):
    data = raw_data[0]
    new_data = data.split('\n')

    dates = []
    opens = []
    highs = []
    lows = []
    closes = []
    volumes = []
    info = [dates, opens, highs, lows, closes, volumes]

    for y in range(6):
        for x in range(y,len(new_data), 7):
            info[y].append(new_data[x])

    for x in range(len(dates)):
        print(dates[x],"\t",opens[x],"\t",highs[x],"\t",lows[x],"\t",closes[x],"\t",volumes[x])

    return dates, opens, highs, lows, closes, volumes

def get_avg_volume(volumes):
    total = 0
    for x in range(len(volumes)):
        if type(volumes[x]==str and not volumes[x]=="-"):
            holder = volumes[x].split(',')
            a = ""
            for x in range(len(holder)):
                a += holder[x]

            total += int(a)
            
    print("Avg daily volume:", round(total/len(volumes),0))

def get_high(highs):
    int_highs = []
    for x in range(len(highs)):
        if type(highs[x]==str):
            holder = highs[x].split('.')
            a = ""
            for x in range(len(holder)):
                a += holder[x]
            if not a == "-":
                int_highs.append(int(a))

    print("30 Day High:", round(max(int_highs)/100,2))

def get_low(lows):
    int_lows = []
    for x in range(len(lows)):
        if type(lows[x]==str):
            holder = lows[x].split('.')
            a = ""
            for x in range(len(holder)):
                a += holder[x]

            if not a == "-":
                int_lows.append(int(a))

    print("30 Day low:", round(min(int_lows)/100,2))

def open_website(url, market):
    r = requests.get("https://www.google.com/finance?q="+market+"%3A"+url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    found = False

    for link in soup.find_all("a", id="fs-chome"):
        found = True
        webbrowser.open(link.text)

    if not found:
        print("Website not available.")

def get_news(url, market):
    
    r = requests.get("http://www.google.com/finance/company_news?q="+market+"%3A"+url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    titles_list = []
    links_list = []
    authors_list = []
    dates_list = []

    for link in soup.findAll('span', {"class":"name"}):
        titles_list.append(link.text)

    for link in soup.findAll("a", id="n-cn-"):
        links_list.append(link['href'])

    for link in soup.findAll('span', {"class":"src"}):
        authors_list.append(link.text)

    for link in soup.findAll('span', {"class":"date"}):
        dates_list.append(link.text)

    for x in range(len(titles_list)):
        print ("\n"+str(x+1)+")",titles_list[x][1:-1])
        print ("-"+authors_list[x])
        print (dates_list[x])

    open_news_article = input("Enter the article you would like to open (0 to open none): ")
    open_news_article = int(open_news_article)
    while open_news_article < 0 or open_news_article > len(titles_list)+1: 
        open_news_article = input("Please enter a valid number: ")

    if open_news_article != 0:
        webbrowser.open(links_list[open_news_article-1])

user_quit = ""

while user_quit != "y":
    market = get_market()
    raw_data, url = get_ticker_data(market)
    dates, opens, highs, lows, closes, volumes = manipulate_raw_data(raw_data)
    get_avg_volume(volumes)
    get_high(highs)
    get_low(lows)
    open_site = input("Open website (y/n): ")
    if open_site.lower() == "y":
        open_website(url, market)
    user_get_news = input("Get news (y/n): ")
    user_get_news = user_get_news.lower()
    if user_get_news == "y":
        get_news(url, market)
    user_quit = input("\nQuit (y/n):")
    user_quit = user_quit.lower()
    print("\n\n\n\n")
