#-*- coding:utf-8 -*-
import requests
from urllib import parse
import json
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import EXTENDED
from tkinter import END
import os
columns1 = ("TITTLE","ID")
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'}
def open_link():
    Listbox1.delete(0,END)
    Listbox2.delete(0,END)
    link = Entry2.get()
    albumId = link.split('/')[4]
    url = 'http://180.153.255.6/mobile/v1/album/track/ts-1534855383505?albumId=' + albumId + '&device=android&isAsc=true&isQueryInvitationBrand=true&pageId=1&pageSize=20&pre_page=0'
    html = requests.get(url)
    all = json.loads(html.text)
    #Thread2 = futures.ThreadPoolExecutor(max_workers=1)
    total_pages = all['data']['totalCount']
    pages_list = range(1,total_pages + 1)
    for n in pages_list:
        url = 'https://www.ximalaya.com/revision/search?core=album&kw=' + name + '&page='+ str(n) + '&spellchecker=true&rows=20&condition=relation&device=iPhone'
        #print(url)
        html = requests.get(url,headers = headers)
        all = json.loads(html.text)
        data = all['data']['result']['response']['docs']
        #print(data)    
        for x in data:
            title = x['title']
            id = x['id']
            treeview1.insert('', 'end',values=(title,id))
    Text1.insert(END, '> 解析专辑成功\n')
    Text1.see(END)
def download():
    path = os.getcwd()
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
    url = 'http://180.153.255.6/mobile/v1/album/track/ts-1534855383505?albumId=' + albumId + '&device=android&isAsc=true&isQueryInvitationBrand=true&pageId=1&pageSize=20&pre_page=0'
    html = requests.get(url)
    all = json.loads(html.text)
    total_counts = all['data']['totalCount']
    maxPageId = all['data']['maxPageId']
    #last_page_totals = int(total_counts)%20
    list1 = range(1,maxPageId + 1)
    for n in list1:
        url = 'http://180.153.255.6/mobile/v1/album/track/ts-1534855383505?albumId=' + albumId + '&device=android&isAsc=true&isQueryInvitationBrand=true&pageId=' + str(n) + '&pageSize=20&pre_page=0'
        html = requests.get(url)
        all = json.loads(html.text)
        data = all['data']['list']
        for a in data:
            #print(a)
            title = a['title']
            playUrl64 = a['playUrl64']
            Listbox1.insert(END,title)
            Listbox2.insert(END,playUrl64) 
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
    html = requests.get(url,headers = headers)
    all = json.loads(html.text)
    #data = all['data']['result']['response']['docs']
    total_pages = all['data']['result']['response']['totalPage']
    #print(data)
    pages_list = range(1,total_pages + 1)
    for n in pages_list:
        url = 'https://www.ximalaya.com/revision/search?core=album&kw=' + name + '&page='+ str(n) + '&spellchecker=true&rows=20&condition=relation&device=iPhone'
        #print(url)
        html = requests.get(url,headers = headers)
        all = json.loads(html.text)
        data = all['data']['result']['response']['docs']
        #print(data)    
        for x in data:
            title = x['title']
            id = x['id']
            treeview1.insert('', 'end',values=(title,id))
    Text1.insert(END, '> 搜索线程结束\n')
    Text1.see(END)
def pass_download():
    threading.Thread(target=download).start()
def open_link_button_click():
    threading.Thread(target=open_link).start()
def treeview1_click(event):
    threading.Thread(target=solve).start()
def search_button_click():
    threading.Thread(target=search).start()
#GUI
windows = tk.Tk()
windows.geometry('917x564')# +34+306
windows.title('喜马拉雅专辑下载3.0 beta  BY:Snow')
windows.resizable(0,0)
canvas = tk.Canvas(windows,bg="white")
canvas.place(height = 88,width = 904,x = 5,y = 469)
Label1 = tk.Label(windows,text = '这里有个进度条 待更新')
Label1.place(height = 22,width = 904,x = 5,y = 420)
Entry1 = tk.Entry(windows)
Entry1.place(height = 34,width = 531,x = 4,y = 5)
Entry2 = tk.Entry(windows)
Entry2.place(height = 34,width = 531,x = 4,y = 42)
Entry3 = tk.Entry(windows)
Entry3.place(height = 34,width = 531,x = 4,y = 80)
Button1 = tk.Button(windows,text='搜索',command = search_button_click)
Button1.place(height = 34,width = 123,x = 539,y = 5)
Button2 = tk.Button(windows,text='下载选中',command = pass_download)
Button2.place(height = 109,width = 246,x = 664,y = 5)
Button3 = tk.Button(windows,text='打开链接',command = open_link_button_click)
Button3.place(height = 34,width = 123,x = 539,y = 43)
Button4 = tk.Button(windows,text='选择目录')
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
#列表2
Listbox1 = tk.Listbox(windows,selectmode = EXTENDED)
Listbox1.place(height = 299,width = 370,x = 539,y = 116)
Listbox2 = tk.Listbox(windows)
Listbox2.place(height = 0,width = 0,x = 0,y = 0)
if __name__ == '__main__':
    windows.mainloop()
    


