#-*- coding:utf-8 -*-
import requests
from urllib import parse
import json
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import os
import hashlib
import time
import random
#备用方案1
#关键字搜索1https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={}&pageNum=1
#获取下载链接1https://www.ximalaya.com/revision/play/v1/audio?id={搜索1ID}&ptype=1
#获取下载链接2 http://mobwsa.ximalaya.com/mobile/playlist/album/page?albumId={}&pageId=1
#关键字搜索http://searchwsa.ximalaya.com/front/v1?appid=0&condition=relation&core=chosen2&device=android&deviceId=9a68144e-de5b-3c60-be5e-adce947ab5ff&kw={}&live=true&needSemantic=true&network=wifi&operator=1&page=1&paidFilter=false&plan=c&recall=normal&rows=20&search_version=2.8&spellchecker=true&version=6.6.48&voiceAsinput=false
columns1 = ("TITTLE","ID")
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'}
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
        tkinter.messagebox.showerror('错误','请检查网络是否畅通')
        return 0
    return sign
def open_link():
    Listbox1.delete(0,END)
    Listbox2.delete(0,END)
    link = Entry2.get()
    try:
        albumId = link.split('/')[4]
    except:
        tkinter.messagebox.showerror('错误','请输入正确的链接')
        return 0
    url = 'http://mobwsa.ximalaya.com/mobile/playlist/album/page?albumId=' + albumId + '&pageId=1'
    try:
        html = requests.get(url)
        all = json.loads(html.text)
        maxPageId = all['maxPageId']
        list1 = range(1,maxPageId + 1)
        for n in list1:
            url = 'http://mobwsa.ximalaya.com/mobile/playlist/album/page?albumId=' + albumId + '&pageId=' + str(n)
            html = requests.get(url)
            all = json.loads(html.text)
            data = all['list']
            for a in data:
                title = a['title']
                playUrl64 = a['playUrl64']
                Listbox1.insert(END,title)
                Listbox2.insert(END,playUrl64)
    except:
        tkinter.messagebox.showerror('错误','请检查网络是否畅通')
        return 0
    Text1.insert(END, '> 解析线程结束\n')
    Text1.see(END)
def download():
    global path
    xuanzhong_index = Listbox1.curselection()
    Text1.insert(END, '> ' + str(len(xuanzhong_index)) + '个任务正在下载\n')
    Text1.see(END)
    for n in range(0,len(xuanzhong_index)):
        name = Listbox1.get(xuanzhong_index[n])
        url = Listbox2.get(xuanzhong_index[n])
        file_name = path + '\\' + name + '.mp3'
        file1 = requests.get(url,headers = headers)
        with open(file_name,'wb') as code:
            code.write(file1.content)
        Text1.insert(END, '> ' + file_name + '下载成功\n')
        Text1.see(END)
def solve():
    Text1.insert(END, '> 解析线程开始\n')
    Text1.see(END)
    Listbox1.delete(0,END)
    Listbox2.delete(0,END)
    for item in treeview1.selection():
        item_text = treeview1.item(item,'values')
        albumId = item_text[1]
    url = 'http://mobwsa.ximalaya.com/mobile/playlist/album/page?albumId=' + albumId + '&pageId=1'
    try:
        html = requests.get(url)
        all = json.loads(html.text)
        maxPageId = all['maxPageId']
        list1 = range(1,maxPageId + 1)
        for n in list1:
            url = 'http://mobwsa.ximalaya.com/mobile/playlist/album/page?albumId=' + albumId + '&pageId=' + str(n)
            html = requests.get(url)
            all = json.loads(html.text)
            data = all['list']
            for a in data:
                title = a['title']
                playUrl64 = a['playUrl64']
                Listbox1.insert(END,title)
                Listbox2.insert(END,playUrl64)
    except:
        tkinter.messagebox.showerror('错误','请检查网络是否畅通')
        return 0
    Text1.insert(END, '> 解析线程结束\n')
    Text1.see(END) 
def clear_list(tree):
    x=tree.get_children()
    for item in x:
        tree.delete(item)
def search(): #按照关键词进行搜索
    Text1.insert(END, '> 搜索线程开始\n')
    Text1.see(END)
    clear_list(treeview1)
    name = parse.quote(Entry1.get())
    url = 'https://www.ximalaya.com/revision/search?core=album&kw='+ name + '&spellchecker=true&rows=20&condition=relation&device=iPhone'
    head = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
           'xm-sign':xm_md5()}
    try:
        html = requests.get(url,headers = head)
        all = json.loads(html.text)
        total_pages = all['data']['result']['response']['totalPage']
        pages_list = range(1,total_pages + 1)
        for n in pages_list:
            url = 'https://www.ximalaya.com/revision/search?core=album&kw=' + name + '&page='+ str(n) + '&spellchecker=true&rows=20&condition=relation&device=iPhone'
            html = requests.get(url,headers = head)
            all = json.loads(html.text)
            data = all['data']['result']['response']['docs']
            for x in data:
                title = x['title']
                id = x['id']
                treeview1.insert('', 'end',values=(title,id))
    except:
        tkinter.messagebox.showerror('错误','请检查网络是否畅通')
        return 0
    Text1.insert(END, '> 搜索线程结束\n')
    Text1.see(END)
def set_dir():
    global path
    path = tkinter.filedialog.askdirectory()
    Entry3.delete(0,END)
    Entry3.insert(END,path)
def pass_download():
    threading.Thread(target=download).start()
def open_link_button_click():
    threading.Thread(target=open_link).start()
def treeview1_click(event):
    threading.Thread(target=solve).start()
def search_button_click():
    threading.Thread(target=search).start()
def set_dir_click():
    threading.Thread(target=set_dir).start()
#GUI
windows = tk.Tk()
windows.geometry('917x564')# +34+306
windows.title('喜马拉雅专辑下载4.2 BY:Snow')
windows.resizable(0,0)
Label1 = tk.Label(windows)
Label1.place(height = 22,width = 904,x = 5,y = 420)
Entry1 = tk.Entry(windows)
Entry1.place(height = 34,width = 531,x = 4,y = 5)
Entry2 = tk.Entry(windows)
Entry2.place(height = 34,width = 531,x = 4,y = 42)
Entry3 = tk.Entry(windows)
Entry3.place(height = 34,width = 531,x = 4,y = 80)
path = os.getcwd()
Entry3.insert(END,path)
Button1 = tk.Button(windows,text='搜索',command = search_button_click)
Button1.place(height = 34,width = 123,x = 539,y = 5)
Button2 = tk.Button(windows,text='下载选中',command = pass_download)
Button2.place(height = 109,width = 246,x = 664,y = 5)
Button3 = tk.Button(windows,text='打开链接',command = open_link_button_click)
Button3.place(height = 34,width = 123,x = 539,y = 43)
Button4 = tk.Button(windows,text='选择目录',command = set_dir_click)
Button4.place(height = 34,width = 123,x = 539,y = 80)
Text1 = tk.Text(windows)
Text1.place(height = 88,width = 904,x = 5,y = 469)
Text1.insert(END, '> 启动成功！\n')
Text1.see(END)
#列表1
treeview1 = ttk.Treeview(windows, height=10, show="headings", columns=columns1)
treeview1.place(height = 299,width = 530,x = 5,y = 116)
treeview1.column("TITTLE", width=330, anchor='center')  # 表示列,不显示
treeview1.column("ID", width=200, anchor='center')
treeview1.heading("TITTLE", text="TITTLE")  # 显示表头
treeview1.heading("ID", text="ID")
treeview1.bind('<Double-1>', treeview1_click)
Scrollbar1 = tk.Scrollbar(treeview1)
Scrollbar1.pack(side=RIGHT, fill=Y)
#列表2
Listbox1 = tk.Listbox(windows,selectmode = EXTENDED)
Listbox1.place(height = 299,width = 370,x = 539,y = 116)
Scrollbar2 = tk.Scrollbar(Listbox1)
Scrollbar2.pack(side=RIGHT, fill=Y)
Listbox2 = tk.Listbox(windows)
Listbox2.place(height = 0,width = 0,x = 0,y = 0)
treeview1.config(yscrollcommand=Scrollbar1.set)
Listbox1.config(yscrollcommand=Scrollbar2.set)
Scrollbar1.config(command = treeview1.yview)
Scrollbar2.config(command = Listbox1.yview)
if __name__ == '__main__':
    windows.mainloop()