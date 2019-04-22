# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
import time
import urllib
#import comment
from mafengwoSpider.items import MafengwospiderItem, SpotItem, CommentItem
pattern = re.compile(r'\d+')

def decrypt(t):
    hl = hashlib.md5()
    hl.update(t)
    return hl.hexdigest()[2:12]
def get_comment_url(page, poi):
    t=1555857288382
    times = str(time.time()).split('.')
    t = int(times[0] + times[1][:3])
    qdata='{"_ts":"'+str(t)+'","params":"{"poi_id":"'+ str(poi)  +'","page":'+str(page)+',"just_comment":1}"}c9d6618dbc657b41a66eb0af952906f1'
    sn=decrypt(qdata.encode('utf-8'))
    params = '{"poi_id":"' + str(poi) + '","page":' + str(page)  + ',"just_comment":1}'
    params =urllib.parse.quote(params)
    url = "http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?"
    querystring = {"callback":"jQuery181011036861119045205_1553502048335",
               "params":params,
               "_ts":t,
               "_sn":sn,
               "_":t+1}

    url=url+"callback"+'='+querystring['callback']+'&'+'_ts'+'='+str(querystring['_ts'])+'&'+"params"+'='+querystring['params']+'&'+'_'+'='+str(querystring['_'])+'_sn'+'='+str(querystring['_sn'])
    return url
class MafengwoSpider(scrapy.Spider):
    name = 'mafengwo'
    allowed_domains = ['mafengwo.cn']
    start_urls = ['http://www.mafengwo.cn/mdd/']
    headers = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    }
    def parse(self, response):
        items = []
        flag = True
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        for column in response.xpath('/html/body/div[2]/div[2]/div/div[3]/div[1]/div'):
            for each in column.xpath('./dl'):
                item = MafengwospiderItem()
                if flag:
                    flag = False
                    continue
                    name = each.xpath('./dt/text()').extract()
                    flag = False
                    href = ''
                else:
                    names = each.xpath('./dt/a/text()').extract()
                    hrefs = each.xpath('./dt/a/@href').extract()
                for i in range(0, len(names)):
                    item = MafengwospiderItem()
                    href = hrefs[i]
                    href = pattern.findall(href)[0]
                    href = 'http://www.mafengwo.cn/mdd/citylist/' + href + '.html'
                    info = each.xpath('./dd/a/text()').extract()
                    item['name'] = names[i]
                    #item['info'] = ' '.join(info)
                    item['href'] = href
                    items.append(item)
        for item in items:
            yield scrapy.Request(url=item['href'], meta={'meta_1':item}, headers=self.headers,callback=self.city_parse)

    def city_parse(self, response):
        items = []
        meta_1 = response.meta['meta_1']
        mddid = pattern.findall(meta_1['href'])[0]
        try:
            pages = int(pattern.findall(response.xpath('//*[@class="count"]/text()')[0].extract())[0])
        except Exception as e:
            s = response.body
            body = s.decode('unicode-escape').replace('\\','').replace('\n','').encode()
            response = response.replace(body=body,url='')
            pages = int(pattern.findall(response.xpath('//*[@class="count"]/text()')[0].extract())[0])
            #from scrapy.shell import inspect_response
            #inspect_response(response, self)
            #print(response.text)
            #print(s.encode('utf-8').decode('utf-8').encode('utf-8').decode('utf-8'))
        page = int(pattern.findall(response.xpath('//*[@class="pg-current"]/text()')[0].extract())[0])
        citys = response.xpath('//*[@class="item "]')
        #print(citys)
        if page < pages:
            #print(page)
            ts = 1555855599396
            times = str(time.time()).split('.')
            ts = int(times[0] + times[1][:3])
            tdata = '{"_ts":' + str(ts) + ', "mddid":' + mddid + ' , "page":' + str(page + 1) + '}c9d6618dbc657b41a66eb0af952906f1'
            sn=decrypt(tdata.encode('utf-8'))
            #print(sn)
            #print(11111)
            for city in citys:
                item = MafengwospiderItem()
                cityname = city.xpath('.//div[@class="title"]/text()')[0].extract().strip()
                href = 'http://www.mafengwo.cn/jd/' + pattern.findall(city.xpath('.//div[@class="img"]/a/@href')[0].extract())[0] + '/gonglve.html'
                #print(cityname)
            #print(cityname)
                item['cityname'] = cityname
                item['name'] = meta_1['name']
                item['page'] = page
                item['href'] = href
                item['mddid'] = int(pattern.findall(city.xpath('.//div[@class="img"]/a/@href')[0].extract())[0])
                items.append(item)
            for item in items:
                yield scrapy.Request(url=item['href'], meta={'meta_1':item}, headers=self.headers,callback=self.spot_is)
            yield scrapy.FormRequest(
                url = 'http://www.mafengwo.cn/mdd/base/list/pagedata_citylist',
                headers = self.headers,
                meta = {'meta_1': meta_1},
                formdata = {'mddid' : str(mddid),'page' : str(page + 1),'ts': str(ts),'_sn' : str(sn)},
                callback = self.city_parse
            )
    
    def spot_is(self, response):
        if len(re.findall('poi', response.url)) > 0:
            print(response.url)
            return;
        meta_1 = response.meta['meta_1']
        yield meta_1
        ts = 1555855599396
        times = str(time.time()).split('.')
        ts = int(times[0] + times[1][:3])
        qdata = '{"_ts":"' + str(ts) + '","iMddid":"' + str(pattern.findall(meta_1['href'])[0]) + '","iPage":"' + str(1) + '","iTagId":"0","sAct":"KMdd_StructWebAjax|GetPoisByTag"}c9d6618dbc657b41a66eb0af952906f1'
        sn=decrypt(qdata.encode('utf-8'))
        yield scrapy.FormRequest(
                url = 'http://www.mafengwo.cn/ajax/router.php',
                headers = self.headers,
                meta = {'meta_1': meta_1},
                formdata = {'sAct': 'KMdd_StructWebAjax|GetPoisByTag','iMddid': str(pattern.findall(meta_1['href'])[0]),'_ts':str(ts),'iPage': str(1),'iTagId': '0','_sn': str(sn)},
                callback = self.spot_parse
        )
    def spot_parse(self, response):
        meta_1 = response.meta['meta_1']
        mddid = meta_1['mddid']
        cityname = meta_1['cityname']
        s = response.body
        body = s.decode('unicode-escape').replace('\\','').replace('\n','').encode()
        response = response.replace(body=body,url='')
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        #print(response.text)
        if len(response.xpath('//*[@class="count"]/span/text()')) == 0:
            pages = 1
            page = 0
        else:
            pages = int(response.xpath('//*[@class="count"]/span/text()')[0].extract())
            page = int((response.xpath('//*[@class="pg-current"]/text()')[0].extract())) 
        print(pages,page)
        if page < pages:
            ts = 1555669294627
            times = str(time.time()).split('.')
            ts = int(times[0] + times[1][:3])
            
            qdata = '{"_ts":"' + str(ts) + '","iMddid":"' + str(pattern.findall(meta_1['href'])[0]) + '","iPage":"' + str(1) + '","iTagId":"0","sAct":"KMdd_StructWebAjax|GetPoisByTag"}c9d6618dbc657b41a66eb0af952906f1'
            sn=decrypt(qdata.encode('utf-8'))
            spots = response.xpath('//li')
            for spot in spots:
                spotItem = SpotItem()
                spotname = spot.xpath('.//a/@title')[0].extract()
                spothref = spot.xpath('.//a/@href')[0].extract()
                print(spotname)
                spotItem['spotname'] = spotname
                spotItem['cityname'] = cityname
                spotItem['spothref'] = 'http://www.mafengwo.cn' + spothref
                spotItem['mddid'] = mddid
                yield spotItem
                poi = pattern.findall(spotItem['spothref'])[0]
                page = 1
                headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
                headers['Referer'] = spotItem['spothref']
                print(headers)
                for i in range(0, 5):
                    url = get_comment_url(i + 1, poi)
                    yield scrapy.Request(url=url, meta={'meta_1':spotItem}, headers=headers,callback=self.parse_comment)
            yield scrapy.FormRequest(
                url = 'http://www.mafengwo.cn/ajax/router.php',
                headers = self.headers,
                meta = {'meta_1': meta_1},
                formdata = {'sAct': 'KMdd_StructWebAjax|GetPoisByTag','iMddid': str(mddid),'_ts':str(ts),'iPage': str(page + 1),'iTagId': '0','_sn': str(sn)},
                callback = self.spot_parse
        )
    def parse_comment(self, response):
        s = response.body
        body = s.decode('unicode-escape').replace('\\','').replace('\n','').encode()
        #response = response.replace(body=body,url='')
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        response = response.replace(body=body,url='')
        comments = response.xpath('//*[@class="rev-item comment-item clearfix"]')
        if len(comments) == 0:
            return
        meta_1 = response.meta['meta_1']
        spotname = meta_1['spotname']
        for comment in comments:
            commentItem = CommentItem() 
            comment_user = comment.xpath('.//*[@class="name"]/text()')[0].extract()
            comment_text = comment.xpath('.//*[@class="rev-txt"]/text()')[0].extract()
            meta_1 = response.meta['meta_1']
            spotname = meta_1['spotname']
            commentItem['comment_user'] = comment_user
            commentItem['comment_text'] = comment_text
            commentItem['spot_name'] = spotname
            yield commentItem
