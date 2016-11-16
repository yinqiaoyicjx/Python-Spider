# encoding: utf-8

import re
import random
import httplib
from abc import ABCMeta, abstractmethod
from urllib2 import HTTPError, URLError
import headers
import requests
from bs4 import BeautifulSoup
import time

class Proxy:
    def __init__(self,protocol,ip,port):
        self.protocol=protocol
        self.ip=ip
        self.port=port

    def assemble(self):
        return '{}://{}:{}'.format(self.protocol,self.ip,self.port)

class IProxyFinder:

    __metaclass__ = ABCMeta

    @abstractmethod
    def find(self):
        '''return a list of proxy objects'''

        pass

class MimiProxyFinder(IProxyFinder):

    def __init__(self):
        self.urls=['http://www.mimiip.com/gngao/{}'.format(i) for i in range(1,10)]

    def find(self):
        header=headers.make_headers()
        proxies=[]
        try:
            url=random.choice(self.urls)
        except IOError:
            return proxies
        context=requests.get(url,headers = header).content
        soup=BeautifulSoup(context)
        ip_list_soup=soup.find_all('tr')
        for ipproxy in ip_list_soup[1:]:
            try:
                items=ipproxy.find_all('td')
                item=[]
                for it in items:
                    item.append(it.getText())
                proxies.append(Proxy(item[4],item[0],item[1]))
            except IndexError:
                pass
            except AttributeError:
                pass
        return proxies

class XiciProxyFinder(IProxyFinder):

    def __init__(self):
        self.urls=['http://www.xicidaili.com/nt/{}'.format(i) for i in range(1,10)]

    def find(self):
        header=headers.make_headers()
        proxies=[]
        try:
            url=random.choice(self.urls)
        except IOError:
            return proxies
        context=requests.get(url,headers = header).content
        soup=BeautifulSoup(context)
        ip_list_soup=soup.find_all('tr')
        for ipproxy in ip_list_soup[1:]:
            try:
                items=ipproxy.find_all('td')
                item=[]
                for it in items:
                    item.append(it.getText())
                proxies.append(Proxy(item[5],item[1],item[2]))
            except IndexError:
                pass
            except AttributeError:
                pass
        return proxies

class KuaidailiProxyFinder(IProxyFinder):

    def __init__(self):
        self.urls=['http://www.kuaidaili.com/free/inha/{}'.format(i) for i in range(1,10)]

    def find(self):
        header=headers.make_headers()
        proxies=[]
        try:
            url=random.choice(self.urls)
        except IOError:
            return proxies
        context=requests.get(url,headers = header).content
        soup=BeautifulSoup(context)
        ip_list_soup=soup.find_all('tr')
        for ipproxy in ip_list_soup[1:]:
            try:
                items=ipproxy.find_all('td')
                item=[]
                for it in items:
                    item.append(it.getText())
                proxies.append(Proxy(item[3],item[0],item[1]))
            except IndexError:
                pass
            except AttributeError:
                pass
        return proxies


class ProxyPool:

    def __init__(self,finder=MimiProxyFinder(),test_url='http://www.baidu.com'):
        #self.source_page='http://www.mimiip.com/gngao/'
        self.pool=set()
        self.test_url=test_url
        self.finder=finder

    def refresh(self):
        self.pool=set(filter(lambda p:self.is_alive(p),self.pool))
        if len(self.pool) < 10:
            new_proxies=filter(lambda x:self.is_alive(x), self.finder.find())
            for new_proxy in new_proxies:
                self.pool.add(new_proxy)


    def random_proxy(self):
        return random.choice(list(self.pool))

    def is_alive(self,proxy):

        print 'juding '+ proxy.assemble()

        try:
            header=headers.make_headers()
            proxies={proxy.protocol:proxy.assemble()}
            example=requests.get(self.test_url,headers = header,proxies = proxies,timeout=15)
        except (IOError, HTTPError):
            return False

        return True
test=KuaidailiProxyFinder()
s=test.find()
list=[i.assemble() for i in s]
print list






