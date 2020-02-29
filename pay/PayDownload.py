import requests
import json
import execjs
import hashlib
import time
import random
import os
token = open('cookie.txt','r').read()
def xm_md5():
    url = 'https://www.ximalaya.com/revision/time'
    headrer = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
            'Host': 'www.ximalaya.com',
            'Accept-Encoding': 'gzip, deflate, br'}
    try:
        html = requests.get(url, headers = headrer)
        nowTime = str(round(time.time()*1000))
        sign = str(hashlib.md5("himalaya-{}".format(html.text).encode()).hexdigest()) + "({})".format(str(round(random.random()*100))) + html.text + "({})".format(str(round(random.random()*100))) + nowTime
    except:
        print('错误请检查网络是否畅通')
        return 0
    return sign
def getData(albumId):
    url = 'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={}&pageNum={}'.format(albumId,1)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
                'xm-sign': xm_md5()}
    response = requests.get(url,headers = headers)
    json_data =  json.loads(response.text)
    if json_data:
        TotalCount = json_data['data']['trackTotalCount']
        TotalPageNumbs = int(TotalCount)//30 + 1
        #print(TotalPageNumbs)
        for n in range(1,TotalPageNumbs):
            url = 'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={}&pageNum={}'.format(albumId,n)
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
                       'xm-sign': xm_md5()}
            response = requests.get(url,headers = headers)
            json_data = json.loads(response.text)
            tracks = json_data['data']['tracks']
            for x in tracks:
                title = x['title']
                trackId = x['trackId']
                getPlayerUrl(title,trackId)
    else:
        print('错误')
        return 0
def getPlayerUrl(title,trackId):
    global token
    url = 'https://mpay.ximalaya.com/mobile/track/pay/{}?device=pc&isBackend=true&_={}'.format(trackId,str(round(time.time()*1000)))
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
                'xm-sign': xm_md5(),
                'cookie': token} 
    response = requests.get(url,headers = headers)
    data = eval(response.text.replace('\n','').replace('true',"'true'"))
    with open ('get_player_url.js','r') as f:
        js_code = f.read()
    result = execjs.compile(js_code).call('get_player_url',data)
    download(title,result)
    #print(title,result)
def download(name,url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'}
    path = os.getcwd()
    file_name = path + '\\' + name + '.mp3'
    f = requests.get(url,headers = headers)
    with open(file_name,'wb') as code:
        code.write(f.content)
    print('Successfully Download ' + name)
if __name__ == "__main__":
    albumid = input('Please enter your album ID:')
    getData(albumid)