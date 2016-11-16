__author__ = 'cjx'
#--coding:utf-8--

import codecs
import json
import requests
import datetime
from pymongo import MongoClient
from bs4 import BeautifulSoup
import urllib


debug=True #
def log(message):
    if debug:
        print message

def download_image(url,save_path):
    try:
        urllib.urlretrieve(url,save_path)
        log('Downloaded a image: ' + save_path)
    except Exception, e:
        print 'An error catched when download a image:', e

def load_page_html(url):
    log('Get a html page : ' + url)
    return urllib.urlopen(url).read()


def down_page_images(page,save_dir):
    html_context = load_page_html('http://qiubaichengren.com/%d.html' % page)
    soup=BeautifulSoup(html_context)
    for ui_module_div in soup.find_all('div',attrs={'class':'ui-module'}):
        img_tag=ui_module_div.find('img')
        if img_tag is not None and img_tag.has_attr('src') and img_tag.has_attr('alt'):
            alt = img_tag.attrs['alt']
            src = img_tag.attrs['src']
            filename='%s%s' % (alt,src[-4:])
            download_image(src,save_dir+filename)

def download_qbcr(frm=1,page_count=1,save_dir='./image/'):
    for x in range(frm,frm+page_count):
        log('Page : ' + str(x))
        down_page_images(x, save_dir)


def main():
    base_path=''
    download_qbcr(frm=1,page_count=2,save_dir='./image/')#可以分成多线程写

if __name__ == '__main__':
    main()