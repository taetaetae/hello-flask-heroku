import requests, sys
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello dduzi!'

@app.route('/meme', methods=['GET'])
def meme():
    id = request.args.get('id')

    min = sys.maxsize
    page = 1
    maxArticle = []

    while True:
        if maxArticle :
            break
        resposne = requests.get(
            url=f"https://m.land.naver.com/complex/getComplexArticleList?hscpNo={id}&tradTpCd=A1&order=prc&page={page}",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Referer": "https://m.land.naver.com/"
            }
        ).json()

        for article in resposne['result']['list']:
            if "84" in article['spc2'] :
                floor = str(article['flrInfo']).split("/")[0]
                if floor.isdigit() and int(floor) < 5:
                    continue
                dealOrWarrantPrc = str(article['prcInfo']).split('억')
                firstPrc = int(dealOrWarrantPrc[0]) * 10000
                secondPrc = 0 if dealOrWarrantPrc[1] == '' else int(str(dealOrWarrantPrc[1]).replace(",", ""))
                if min > firstPrc + secondPrc:
                    min = firstPrc + secondPrc
                    maxArticle = article
        page = page + 1
    return str(min)

@app.route('/jeonse', methods=['GET'])
def jeonse():
    id = request.args.get('id')

    max = 0
    page = 1
    minArticle = []

    while True:
        if minArticle :
            break
        resposne = requests.get(
            url=f"https://m.land.naver.com/complex/getComplexArticleList?hscpNo={id}&tradTpCd=B1&order=prc_&page={page}",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Referer": "https://m.land.naver.com/"
            }
        ).json()

        for article in resposne['result']['list']:
            if "84" in article['spc2'] :
                dealOrWarrantPrc = str(article['prcInfo']).split('억')
                firstPrc = int(dealOrWarrantPrc[0]) * 10000
                secondPrc = 0 if dealOrWarrantPrc[1] == '' else int(str(dealOrWarrantPrc[1]).replace(",", ""))
                if max < firstPrc + secondPrc:
                    max = firstPrc + secondPrc
                    minArticle = article
        page = page + 1
    return str(max)

if __name__ == '__main__':
    app.run()
