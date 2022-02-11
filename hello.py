import requests, sys
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/meme', methods=['GET'])
def meme():
    id = request.args.get('id')

    min = sys.maxsize
    page = 1
    while True:
        response = requests.get(
            url=f"https://new.land.naver.com/api/articles/complex/{id}?realEstateType=APT%3AABYG%3AJGC&tradeType=A1&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=false&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&complexNo={id}&buildingNos=&type=list&order=prc",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE2NDQ1ODY5NzIsImV4cCI6MTY0NDU5Nzc3Mn0.jpa_rrmB3Hs2xwqQSfbgPRWcoYq0Bz5i4QUnDRrUYBE"
            })

        datas = response.json()
        if not datas['isMoreData']:
            break

        for article in datas['articleList']:
            if article['area2'] == 84:
                floor = str(article['floorInfo']).split("/")[0]
                if floor.isdigit() and int(floor) < 5:
                    continue
                dealOrWarrantPrc = str(article['dealOrWarrantPrc']).split('억')
                firstPrc = int(dealOrWarrantPrc[0]) * 10000
                secondPrc = 0 if dealOrWarrantPrc[1] == '' else int(str(dealOrWarrantPrc[1]).replace(",", ""))
                if min > firstPrc + secondPrc:
                    min = firstPrc + secondPrc
                    maxArticle = article
        page = page + 1
    return maxArticle['dealOrWarrantPrc']

@app.route('/jeonse', methods=['GET'])
def jeonse():
    id = request.args.get('id')

    max = 0
    page = 1
    while True:
        response = requests.get(
            url=f"https://new.land.naver.com/api/articles/complex/{id}?realEstateType=APT%3AABYG%3AJGC&tradeType=B1&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=false&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&complexNo={id}&buildingNos=&type=list&order=prcDesc",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE2NDQ1ODY5NzIsImV4cCI6MTY0NDU5Nzc3Mn0.jpa_rrmB3Hs2xwqQSfbgPRWcoYq0Bz5i4QUnDRrUYBE"
            })

        datas = response.json()
        if not datas['isMoreData']:
            break

        for article in datas['articleList']:
            if article['area2'] == 84:
                dealOrWarrantPrc = str(article['dealOrWarrantPrc']).split('억')
                firstPrc = int(dealOrWarrantPrc[0]) * 10000
                secondPrc = 0 if dealOrWarrantPrc[1] == '' else int(str(dealOrWarrantPrc[1]).replace(",", ""))
                if max < firstPrc + secondPrc:
                    max = firstPrc + secondPrc
                    maxArticle = article
        page = page + 1
    return maxArticle['dealOrWarrantPrc']

if __name__ == '__main__':
    app.run()
