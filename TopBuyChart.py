import requests
import re
user_prices = {}
prices = []
json=[]

# scraps USD to IRR
request_Exchange = requests.get('http://www.o-xe.com/')
USD_IRR = re.findall(r'\d,\d{3}', request_Exchange.text)[11]
USD_IRR = re.findall(r'\d', USD_IRR)
USD_IRR = int(USD_IRR[0]+USD_IRR[1]+USD_IRR[2]+USD_IRR[3])*10

# BTC fair price gets the BTC price n adds 1 percent more as a compensation of fees
request_BTC = requests.get("https://api.coinbase.com/v2/prices/spot?currency=USD")
BTC = round(float(request_BTC.json()['data']['amount']) * 1.01010101010101 * float(USD_IRR),2)
#exchanging.ir buying prices
exchanging = requests.get('https://exchanging.ir/buy/')
exchanging = re.findall(r'<id>3</id>\r\s.*\d+',exchanging.text)
exchanging = int((re.findall(r'\d+',exchanging[0])[1]))*10000
user_prices['exchanging'] = ['exchanging.ir', exchanging]

sellers='https://localbitcoins.com/buy-bitcoins-online/IR/iran-islamic-republic-of/national-bank-transfer/.json'
request = requests.get(sellers)
json.append(request.json()['data']['ad_list'])
firstPage_ads = request.json()['data']['ad_count']
#Checks the other pages' contents
while 'pagination' in request.json():
    try:
        request = requests.get(request.json()['pagination']['next'])
        json.append(request.json()['data']['ad_list'])
    except:
        break
length = len(json[0])
for i in range(len(json)-1):
    length += 1
# the whole idea of this part of code is held brief in 2 last lines of the loop
for i in range(length-(firstPage_ads-1)):
    it=i
    for i in range(len(json[it])):
        feed_back_score = int(json[it][i]['data']['profile']['feedback_score'])
        trade_count = json[it][i]['data']['profile']['trade_count']
        trade_count = int(re.findall(r'\d+', trade_count)[0])
        username = json[it][i]['data']['profile']['username']
        price = json[it][i]['data']['temp_price']
        ad = json[it][i]['data']['ad_id']

        if feed_back_score > 95 and trade_count > 3:
            user_prices[username] = [ad, price]

minprice = []
# minimum of buy prices
for i in user_prices.values():
    prices.append(float(i[1]))
prices.sort()

#finds the 1st and 2nd smallest price
minprice.append(prices[0])
minprice.append(prices[prices.count(prices[0])])

# gives the best (user+price+ad+interest level))
print('** Best selling Prices - buy from these guys n sell just a bit lower **')
print('fair pure price is: '+ str(BTC)+' IRR'+'\n')

for it in minprice:
    for i in user_prices.keys():
        if float(user_prices[i][1]) == float(it):
            ad_number = str(user_prices[i][0])
            if type(user_prices[i][0]) == str:
                print(str(i)+': '+str(user_prices[i][1])+ '\n' +' ad: '+ user_prices[i][0])
            else:
                print(str(i)+': '+str(user_prices[i][1])+ '\n' +' ad: '+'https://localbitcoins.com/ad/'+ad_number)
            Benefit = float(user_prices[i][1])*100/float(BTC)-100
            print('Sells '+str(round(Benefit,2))+'% +'+'\n')