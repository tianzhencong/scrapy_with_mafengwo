import hashlib
import requests
import urllib
import time
def par(t):
    hl = hashlib.md5()
    hl.update(t)
    return hl.hexdigest()[2:12]
'''
page=1
times = str(time.time()).split('.')
t = int(times[0] + times[1][:3])
qdata='{"_ts":"'+str(t)+'","params":"{"poi_id":"9888","page":'+str(page)+',"just_comment":1}"}c9d6618dbc657b41a66eb0af952906f1'
print(qdata)
sn=par(qdata.encode('utf-8'))
print(sn)
params = '{"poi_id":"9888","page":1,"just_comment":1}'
params =urllib.parse.quote(params)
url = "http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?"
#querystring = {"callback":"jQuery181011036861119045205_1553502048335",
#               "params":"%7B%22poi_id%22%3A%2287950%22%2C%22page%22%3A{}%2C%22just_comment%22%3A1%7D".format(str(page)),
#               "_ts":t,
#               "_sn":sn,
#               "_":t+1}
'''
def get_comment_url(page, poi):
    t=1555857288382
    times = str(time.time()).split('.')
    t = int(times[0] + times[1][:3])
    qdata='{"_ts":"'+str(t)+'","params":"{"poi_id":"'+ str(poi)  +'","page":'+str(page)+',"just_comment":1}"}c9d6618dbc657b41a66eb0af952906f1'
    sn=par(qdata.encode('utf-8'))
    params = '{"poi_id":"' + str(poi) + '","page":' + str(page)  + ',"just_comment":1}'
    params =urllib.parse.quote(params)
    url = "http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?"
    querystring = {"callback":"jQuery18107431196295062483_1555859037406",
               "params":params,
               "_ts":t,
               "_sn":sn,
               "_":t+1}
    for key,value in querystring.items():
        url=url+key+'='+str(value)+'&'
    return url[:-1]
'''
querystring = {"callback":"jQuery181011036861119045205_1553502048335",
               "params":params,
               "_ts":t,
               "_sn":sn,
               "_":t+1}
headers = {
'Referer':"http://www.mafengwo.cn/poi/6328325.html",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
for key,value in querystring.items():
    url=url+key+'='+str(value)+'&'
    #url=url[:-1]
    print(url)
#print(get_comment_url(1, 87950))
url='http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery1810408361146083539_1555860809306&params=%7B%22poi_id%22%3A%222769%22%2C%22page%22%3A2%2C%22just_comment%22%3A1%7D&_ts=1555860825676&_sn=7bf0e73a64&_=1555860825676'
response = requests.request("GET", get_comment_url(1, 6328325), headers=headers)
print(response.text)
'''
def get_url(page, poi):
    return get_comment_url(page, poi)
