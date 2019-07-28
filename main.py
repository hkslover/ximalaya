#-*- coding:utf-8 -*-
import requests
from urllib import parse
import json
import tkinter as tk
from concurrent import futures
from tkinter import ttk
import tkinter.messagebox
Thread1 = futures.ThreadPoolExecutor(max_workers=3)
Thread2 = futures.ThreadPoolExecutor(max_workers=1)
Thread3 = futures.ThreadPoolExecutor(max_workers=10)
columns1 = ("TITTLE","ID")
columns2 = ("TITTLE","playUrl64")
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'}
def download(name,download_url):
    file_name = name + '.mp3'
    #print(file_name)
    file1 = requests.get(download_url,headers = headers)
    with open(file_name,'wb') as code:
        code.write(file1.content)
    tkinter.messagebox.showinfo('提示',name + '下载完成!')
def pass_download(event):
    for item in treeview2.selection():
        item_text = treeview2.item(item,'values')
        name = item_text[0]
        url = item_text[1]
    #print(name)
    #print(url)
    Thread3.submit(download,name,url)
def analysis2(id,pages):
    Label3['text'] = '双击下载 最多同时下载10个文件'
    url = 'http://180.153.255.6/mobile/v1/album/track/ts-1534855383505?albumId=' + id + '&device=android&isAsc=true&isQueryInvitationBrand=true&pageId=' + str(pages) + '&pageSize=20&pre_page=0'
    html = requests.get(url)
    all = json.loads(html.text)
    data = all['data']['list']
    for a in data:
        #print(a)
        title = a['title']
        playUrl64 = a['playUrl64']
        treeview2.insert('', 'end',values=(title,playUrl64))
def analysis1(event):#此搜索只是为了搜索总页数，需要进一步提交
    clear_list(treeview2)
    for item in treeview1.selection():
        item_text = treeview1.item(item,'values')
        albumId = item_text[1]
    url = 'http://180.153.255.6/mobile/v1/album/track/ts-1534855383505?albumId=' + albumId + '&device=android&isAsc=true&isQueryInvitationBrand=true&pageId=1&pageSize=20&pre_page=0'
    html = requests.get(url)
    all = json.loads(html.text)
    total_pages = all['data']['totalCount']
    list1 = range(1,total_pages)
    for n in list1:
        Thread2.submit(analysis2,albumId,n)
        #analysis2(albumId,n)
def search2(name,pages):
    url = 'https://www.ximalaya.com/revision/search?core=album&kw=' + name + '&page='+ str(pages) + '&spellchecker=true&rows=20&condition=relation&device=iPhone'
    #print(url)
    html = requests.get(url,headers = headers)
    all = json.loads(html.text)
    data = all['data']['result']['response']['docs']
    #print(data)    
    for x in data:
        title = x['title']
        id = x['id']
        treeview1.insert('', 'end',values=(title,id))   
def clear_list(tree):
    x=tree.get_children()
    for item in x:
        tree.delete(item)
def search1(): #此搜索只是为了搜索总数和总页数，需要进一步提交
    #print('测试')
    clear_list(treeview1)
    name = parse.quote(Entry1.get())
    url = 'https://www.ximalaya.com/revision/search?core=album&kw='+ name + '&spellchecker=true&rows=20&condition=relation&device=iPhone'
    html = requests.get(url,headers = headers)
    all = json.loads(html.text)
    #data = all['data']['result']['response']['docs']
    total_pages = all['data']['result']['response']['totalPage']
    total = all['data']['result']['response']['total']
    #print(data) 
    Label1['text'] = 'page:' + str(total_pages)
    Label2['text'] = 'total:' + str(total)
    list1 = range(1,total_pages)
    for n in list1:
        Thread1.submit(search2,name,n)
#GUI
windows = tk.Tk()
windows.geometry('870x419')
windows.title('喜马拉雅专辑下载')
windows.resizable(0,0)
Entry1 = tk.Entry(windows,textvariable = '心理罪')
Entry1.place(height = 34,width = 403,x = 3,y = 6)
Button1 = tk.Button(windows,text='搜索',command = search1)
Button1.place(height = 34,width = 128,x = 421,y = 6)
Label1 = tk.Label(windows)
Label1.place(height = 38,width = 60,x = 550,y = 5)
Label2 = tk.Label(windows)
Label2.place(height = 38,width = 60,x = 610,y = 5)
Label3 = tk.Label(windows)
Label3.place(height = 38,width = 200,x = 673,y = 5)
#列表1
treeview1 = ttk.Treeview(windows, height=10, show="headings", columns=columns1)
treeview1.place(height = 366,width = 546,x = 3,y = 47)
treeview1.column("TITTLE", width=300, anchor='center')  # 表示列,不显示
treeview1.column("ID", width=300, anchor='center')
treeview1.heading("TITTLE", text="TITTLE")  # 显示表头
treeview1.heading("ID", text="ID")
treeview1.bind('<Double-1>', analysis1)
#列表2
treeview2 = ttk.Treeview(windows, height=10, show="headings", columns=columns2)
treeview2.place(height = 365,width = 306,x = 557,y = 48)
treeview2.column("TITTLE", width=150, anchor='center')  # 表示列,不显示
#treeview2.column("状态", width=150, anchor='center')
treeview2.column("playUrl64", width=6, anchor='center')
treeview2.heading("TITTLE", text="TITTLE")  # 显示表头
#treeview2.heading("状态", text="状态")
treeview2.heading("playUrl64", text="playUrl64")
treeview2.bind('<Double-1>', pass_download)
#treeview.insert('', 'end',values=("demo tittle1","demo id1"))
#treeview.insert('', 'end',values=("demo tittle2","demo id2"))
windows.mainloop()


