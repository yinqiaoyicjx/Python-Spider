__author__ = 'cjx'
#--coding:utf-8--

import codecs
import json
import requests
import datetime
from pymongo import MongoClient
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'http://www.lagou.com/jobs/positionAjax.json?'
num=2
MONGO_CONN=MongoClient(host='localhost',port=27017)
def download_page(url,n):
    POST_DATA={'first':'false','pn':n,'kd':'python'}
    return requests.post(url, data=POST_DATA, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }).content

def save(data):
    data['_id']=data['positionId']
    data['updateTime']=datetime.datetime.now()

    MONGO_CONN['web_crawler']['collection'].update_one(
        filter={'_id':data['_id']},
        update={'$set':data},
        upsert=True
    )

def parse_html(page_json):
    #page_json1=json.dumps(page_json)
    results=page_json['content']['result']
    re=[]
    for wb in results:
        re.append(wb['city'])
        re.append(wb['positionName'])
        re.append(wb['salary'])
        re.append(wb['companyShortName'])
        save(wb)
    return re



def main():
    url = DOWNLOAD_URL
    nn=num

    with codecs.open('movies', 'wb', encoding='utf-8') as fp:
        while nn<=3:
            html = download_page(url,nn)
            movies=parse_html(html)
            fp.write(u'{movies}\n\n'.format(movies='\n'.join(movies)))
            nn+=1


if __name__ == '__main__':
    print download_page(DOWNLOAD_URL,1)

