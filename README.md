# ximalaya
喜马拉雅专辑批量下载
界面使用https://www.pytk.net/tkinter-helper/布局生成

**xm-sign生成算法**

```python
def xm_md5():
    url = 'https://www.ximalaya.com/revision/time'
    headrer = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
            'Host': 'www.ximalaya.com'}
    html = requests.get(url, headers = headrer)
    nowTime = str(round(time.time()*1000)) #13位时间戳
    sign = str(hashlib.md5("himalaya-{}".format(html.text).encode()).hexdigest()) + "({})".format(str(round(random.random()*100))) + html.text + "({})".format(str(round(random.random()*100))) + nowTime
    return sign
```


