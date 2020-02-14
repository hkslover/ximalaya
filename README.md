# ximalaya
喜马拉雅专辑批量下载

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

![](https://gitee.com/hkslover/blog_img/raw/master/2020/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20200214125951.png)


![](https://gitee.com/hkslover/blog_img/raw/master/%E6%B7%B1%E5%BA%A6%E6%88%AA%E5%9B%BE_%E9%80%89%E6%8B%A9%E5%8C%BA%E5%9F%9F_20191013121609.png)
