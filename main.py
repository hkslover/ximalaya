#-*- coding:utf-8 -*-
import requests
from urllib import parse
import json
import tkinter as tk
from concurrent import futures
from tkinter import ttk
from tkinter import EXTENDED
from tkinter import END
Thread1 = futures.ThreadPoolExecutor(max_workers=3)
columns1 = ("TITTLE","ID")
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'}
def open_link():
    Listbox1.delete(0,END)
    Listbox2.delete(0,END)
    link = Entry2.get()
    print(link)
    albumId = link.split('/')[4]
    print(albumId)
    url = 'http://180.153.255.6/mobile/v1/album/track/ts-1534855383505?albumId=' + albumId + '&device=android&isAsc=true&isQueryInvitationBrand=true&pageId=1&pageSize=20&pre_page=0'
    html = requests.get(url)
    all = json.loads(html.text)
    Thread2 = futures.ThreadPoolExecutor(max_workers=1)
    total_pages = all['data']['totalCount']
    list1 = range(1,total_pages)
    for n in list1:
        Thread2.submit(analysis2,albumId,n)
    Text1.insert(END, '> 解析专辑成功，选择一项后，按住shift+鼠标左键单击即可批量选择。\n')
    Text1.see(END)
def download(name,download_url,list_index):
    file_name = name + '.mp3'
    #print(file_name)
    file1 = requests.get(download_url,headers = headers)
    with open(file_name,'wb') as code:
        code.write(file1.content)
    #tkinter.messagebox.showinfo('提示',name + '下载完成!')
    Text1.insert(END, '> ' + file_name + '下载成功\n')
    Text1.see(END)
def pass_download():
    xuanzhong_index = Listbox1.curselection()
    Text1.insert(END, '> ' + str(len(xuanzhong_index)) + '个任务正在下载\n')
    Text1.see(END)
    #print(xuanzhong_index)
    #print(len(playUrl64_list))
    for n in range(0,len(xuanzhong_index)):
        Thread3 = futures.ThreadPoolExecutor(max_workers=1)
        name = Listbox1.get(xuanzhong_index[n])
        url = Listbox2.get(xuanzhong_index[n])
        #print(name,url)
        Thread3.submit(download,name,url,xuanzhong_index[n])
def analysis2(id,pages):
    url = 'http://180.153.255.6/mobile/v1/album/track/ts-1534855383505?albumId=' + id + '&device=android&isAsc=true&isQueryInvitationBrand=true&pageId=' + str(pages) + '&pageSize=20&pre_page=0'
    html = requests.get(url)
    all = json.loads(html.text)
    data = all['data']['list']
    for a in data:
        #print(a)
        title = a['title']
        playUrl64 = a['playUrl64']
        Listbox1.insert(END,title)
        Listbox2.insert(END,playUrl64)
    Thread2.shutdown(wait=True) 
def analysis1(event):#此搜索只是为了搜索总页数，需要进一步提交
    Listbox1.delete(0,END)
    Listbox2.delete(0,END)
    Thread2 = futures.ThreadPoolExecutor(max_workers=1)
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
    Text1.insert(END, '> 解析专辑成功，选择一项后，按住shift+鼠标左键单击即可批量选择。\n')
    Text1.see(END)
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
    #print('demo')
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
    #print(data)
    list1 = range(1,total_pages + 1)
    for n in list1:
        Thread1.submit(search2,name,n)  
    Text1.insert(END, '> 搜索正在进行，双击列表解析对应专辑\n')
    Text1.see(END)
#GUI
windows = tk.Tk()
windows.geometry('870x534')# +34
windows.title('喜马拉雅专辑下载2.0  BY:Snow QQ：2103200855')
windows.resizable(0,0)
Entry1 = tk.Entry(windows)
Entry1.place(height = 34,width = 403,x = 3,y = 6)
Entry2 = tk.Entry(windows)
Entry2.place(height = 34,width = 403,x = 3,y = 40)
Button1 = tk.Button(windows,text='搜索',command = search1)
Button1.place(height = 34,width = 128,x = 421,y = 6)
Button3 = tk.Button(windows,text='打开链接',command = open_link)
Button3.place(height = 34,width = 128,x = 421,y = 40)
Label1 = tk.Label(windows)
Label1.place(height = 38,width = 120,x = 550,y = 5)
Button2 = tk.Button(windows,text='下载选中',command = pass_download)
Button2.place(height = 38,width = 200,x = 673,y = 5)
Text1 = tk.Text(windows)
Text1.place(height = 70,width = 860,x = 3,y = 420+34)
Text1.insert(END, '> 启动成功！\n')
Text1.see(END)
#列表1
treeview1 = ttk.Treeview(windows, height=10, show="headings", columns=columns1)
treeview1.place(height = 366,width = 546,x = 3,y = 47+34)
treeview1.column("TITTLE", width=300, anchor='center')  # 表示列,不显示
treeview1.column("ID", width=300, anchor='center')
treeview1.heading("TITTLE", text="TITTLE")  # 显示表头
treeview1.heading("ID", text="ID")
treeview1.bind('<Double-1>', analysis1)
#列表2
Listbox1 = tk.Listbox(windows,selectmode = EXTENDED)
Listbox1.place(height = 365,width = 306,x = 557,y = 48+34)
Listbox2 = tk.Listbox(windows)
Listbox2.place(height = 0,width = 0,x = 0,y = 0)
windows.mainloop()


