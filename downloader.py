from tkinter import *
from tkinter.ttk import * 
from typing import Dict
import requests
from urllib import parse
import json
import threading
import tkinter.filedialog
import tkinter.messagebox
import os
import hashlib
import time
import random
#关键字搜索1https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={}&pageNum=1
#获取下载链接1https://www.ximalaya.com/revision/play/v1/audio?id={搜索1ID}&ptype=1
#获取下载链接2 http://mobwsa.ximalaya.com/mobile/playlist/album/page?albumId={}&pageId=1
#关键字搜索http://searchwsa.ximalaya.com/front/v1?appid=0&condition=relation&core=chosen2&device=android&deviceId=9a68144e-de5b-3c60-be5e-adce947ab5ff&kw={}&live=true&needSemantic=true&network=wifi&operator=1&page=1&paidFilter=false&plan=c&recall=normal&rows=20&search_version=2.8&spellchecker=true&version=6.6.48&voiceAsinput=false
class WinGUI(Tk):
    widget_dic: Dict[str, Widget] = {}
    def __init__(self):
        super().__init__()
        # ttkbootstrap 组件本地化
        self.__win()
        self.widget_dic["tk_label_llknlo8l"] = self.__tk_label_llknlo8l(self)
        self.widget_dic["tk_input_album_name"] = self.__tk_input_album_name(self)
        self.widget_dic["tk_button_search"] = self.__tk_button_search(self)
        self.widget_dic["tk_label_llknm11x"] = self.__tk_label_llknm11x(self)
        self.widget_dic["tk_label_llknm4wv"] = self.__tk_label_llknm4wv(self)
        self.widget_dic["tk_input_album_link"] = self.__tk_input_album_link(self)
        self.widget_dic["tk_input_download_path"] = self.__tk_input_download_path(self)
        self.widget_dic["tk_button_open_link"] = self.__tk_button_open_link(self)
        self.widget_dic["tk_button_set_path"] = self.__tk_button_set_path(self)
        self.widget_dic["tk_table_search_table"] = self.__tk_table_search_table(self)
        self.widget_dic["tk_table_download_table"] = self.__tk_table_download_table(self)
        self.widget_dic["tk_button_download_all"] = self.__tk_button_download_all(self)
        self.widget_dic["tk_button_download_select"] = self.__tk_button_download_select(self)
        self.widget_dic["tk_button_back"] = self.__tk_button_back(self)
        self.widget_dic["tk_button_next"] = self.__tk_button_next(self)
        self.widget_dic["tk_label_page_num"] = self.__tk_label_page_num(self)
        self.widget_dic["tk_label_details_page_num"] = self.__tk_label_details_page_num(self)
        self.widget_dic["tk_button_details_back"] = self.__tk_button_details_back(self)
        self.widget_dic["tk_button_details_next"] = self.__tk_button_details_next(self)
    def __win(self):
        self.title("喜马拉雅专辑下载 Snow")
        # 设置窗口大小、居中
        width = 1062
        height = 534
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)
        # 自动隐藏滚动条
    def scrollbar_autohide(self,bar,widget):
        self.__scrollbar_hide(bar,widget)
        widget.bind("<Enter>", lambda e: self.__scrollbar_show(bar,widget))
        bar.bind("<Enter>", lambda e: self.__scrollbar_show(bar,widget))
        widget.bind("<Leave>", lambda e: self.__scrollbar_hide(bar,widget))
        bar.bind("<Leave>", lambda e: self.__scrollbar_hide(bar,widget))
    
    def __scrollbar_show(self,bar,widget):
        bar.lift(widget)
    def __scrollbar_hide(self,bar,widget):
        bar.lower(widget)
    
    def vbar(self,ele, x, y, w, h, parent):
        sw = 15 # Scrollbar 宽度
        x = x + w - sw
        vbar = Scrollbar(parent)
        ele.configure(yscrollcommand=vbar.set)
        vbar.config(command=ele.yview)
        vbar.place(x=x, y=y, width=sw, height=h)
        self.scrollbar_autohide(vbar,ele)
    def __tk_label_llknlo8l(self,parent):
        label = Label(parent,text="专辑名",anchor="center", )
        label.place(x=20, y=10, width=50, height=30)
        return label
    def __tk_input_album_name(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=80, y=10, width=150, height=30)
        return ipt
    def __tk_button_search(self,parent):
        btn = Button(parent, text="搜索", takefocus=False,)
        btn.place(x=240, y=10, width=50, height=30)
        return btn
    def __tk_label_llknm11x(self,parent):
        label = Label(parent,text="专辑链接",anchor="center", )
        label.place(x=20, y=50, width=50, height=30)
        return label
    def __tk_label_llknm4wv(self,parent):
        label = Label(parent,text="下载目录",anchor="center", )
        label.place(x=770, y=40, width=50, height=30)
        return label
    def __tk_input_album_link(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=80, y=50, width=150, height=30)
        return ipt
    def __tk_input_download_path(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=830, y=40, width=150, height=30)
        return ipt
    def __tk_button_open_link(self,parent):
        btn = Button(parent, text="打开", takefocus=False,)
        btn.place(x=240, y=50, width=50, height=30)
        return btn
    def __tk_button_set_path(self,parent):
        btn = Button(parent, text="选择", takefocus=False,)
        btn.place(x=990, y=40, width=50, height=30)
        return btn
    def __tk_table_search_table(self,parent):
        # 表头字段 表头宽度
        columns = {"ID":56,"专辑名":395,"专辑ID":113}
        tk_table = Treeview(parent, show="headings", columns=list(columns),)
        for text, width in columns.items():  # 批量设置列属性
            tk_table.heading(text, text=text, anchor='center')
            tk_table.column(text, anchor='center', width=width, stretch=False)  # stretch 不自动拉伸
        
        tk_table.place(x=20, y=130, width=566, height=393)
        self.vbar(tk_table, 20, 130, 566, 393,parent)
        return tk_table
    def __tk_table_download_table(self,parent):
        # 表头字段 表头宽度
        columns = {"序号":44,"标题":313,"状态":89}
        tk_table = Treeview(parent, show="headings", columns=list(columns),)
        for text, width in columns.items():  # 批量设置列属性
            tk_table.heading(text, text=text, anchor='center')
            tk_table.column(text, anchor='center', width=width, stretch=False)  # stretch 不自动拉伸
        
        tk_table.place(x=600, y=130, width=449, height=393)
        self.vbar(tk_table, 600, 130, 449, 393,parent)
        return tk_table
    def __tk_button_download_all(self,parent):
        btn = Button(parent, text="下载全部", takefocus=False,)
        btn.place(x=680, y=90, width=70, height=30)
        return btn
    def __tk_button_download_select(self,parent):
        btn = Button(parent, text="下载选中", takefocus=False,)
        btn.place(x=600, y=90, width=70, height=30)
        return btn
    def __tk_button_back(self,parent):
        btn = Button(parent, text="上一页", takefocus=False,)
        btn.place(x=420, y=90, width=76, height=30)
        return btn
    def __tk_button_next(self,parent):
        btn = Button(parent, text="下一页", takefocus=False,)
        btn.place(x=510, y=90, width=76, height=30)
        return btn
    def __tk_label_page_num(self,parent):
        label = Label(parent,text="",anchor="center", )
        label.place(x=310, y=90, width=96, height=30)
        return label
    def __tk_label_details_page_num(self,parent):
        label = Label(parent,text="",anchor="center", )
        label.place(x=770, y=90, width=96, height=30)
        return label
    def __tk_button_details_back(self,parent):
        btn = Button(parent, text="上一页", takefocus=False,)
        btn.place(x=880, y=90, width=76, height=30)
        return btn
    def __tk_button_details_next(self,parent):
        btn = Button(parent, text="下一页", takefocus=False,)
        btn.place(x=970, y=90, width=76, height=30)
        return btn
class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.album_name = None
        self.current_page = 1
        self.total_pages_nums = None
        self.download_url = []
        self.details_current_page = 1
        self.details_total_pages_nums = None
        self.albumId = None
        self.__event_bind()
        self.download_path = os.getcwd()
        self.widget_dic["tk_input_download_path"].insert(END,self.download_path)
    def xm_md5(self):
        url = 'https://www.ximalaya.com/revision/time'
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
                'Host': 'www.ximalaya.com',
                'Accept-Encoding': 'gzip, deflate, br'}
        response = requests.get(url, headers = headers)
        nowTime = str(round(time.time()*1000))
        sign = str(hashlib.md5("himalaya-{}".format(response.text).encode()).hexdigest()) + "({})".format(str(round(random.random()*100))) + response.text + "({})".format(str(round(random.random()*100))) + nowTime
        return sign
    def search_pages(self):
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
                   'xm-sign':self.xm_md5()
                   }
        url = 'https://www.ximalaya.com/revision/search?core=album&kw=' + self.album_name + '&page='+ str(self.current_page) + '&spellchecker=true&rows=20&condition=relation&device=iPhone'
        response = requests.get(url,headers = headers)
        json_data = json.loads(response.text)
        data = json_data['data']['result']['response']['docs']
        return data
    def search(self):
        for item in self.widget_dic["tk_table_search_table"].get_children():
            self.widget_dic["tk_table_search_table"].delete(item)
        self.album_name = parse.quote(self.widget_dic["tk_input_album_name"].get())
        if self.album_name == '':
            tkinter.messagebox.showerror('错误','请输入关键词')
            return
        url = 'https://www.ximalaya.com/revision/search?core=album&kw='+ self.album_name + '&spellchecker=true&rows=20&condition=relation&device=iPhone'
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
                   'xm-sign':self.xm_md5()
                   }
        response = requests.get(url,headers = headers)
        json_data = json.loads(response.text)
        self.total_pages_nums = json_data['data']['result']['response']['totalPage']
        if self.total_pages_nums >= 1:
            data = self.search_pages()
            for i,_ in enumerate(data):
                self.widget_dic["tk_table_search_table"].insert('', 'end',values=(i+1,_['title'],_['id']))
            self.widget_dic["tk_label_page_num"]['text'] = "{0}页-共{1}页".format(str(self.current_page),str(self.total_pages_nums))
    def change_pages_nums(self,direction):
        update_flag = 0
        if direction == 0 and self.current_page != 1:
            self.current_page -= 1
            update_flag = 1
        elif direction == 1 and self.current_page != self.total_pages_nums:
            self.current_page += 1
            update_flag = 1
        if(update_flag):
            for item in self.widget_dic["tk_table_search_table"].get_children():
                self.widget_dic["tk_table_search_table"].delete(item)
            data = self.search_pages()
            for i,_ in enumerate(data):
                self.widget_dic["tk_table_search_table"].insert('', 'end',values=(i+1,_['title'],_['id']))
            self.widget_dic["tk_label_page_num"]['text'] = "{0}页-共{1}页".format(str(self.current_page),str(self.total_pages_nums))
    def details_change_pages_nums(self,direction):
        update_flag = 0
        if direction == 0 and self.details_current_page != 1:
            self.details_current_page -= 1
            update_flag = 1
        elif direction == 1 and self.details_current_page != self.details_total_pages_nums:
            self.details_current_page += 1
            update_flag = 1
        if(update_flag):
            for item in self.widget_dic["tk_table_download_table"].get_children():
                self.widget_dic["tk_table_download_table"].delete(item)
            url = 'http://mobwsa.ximalaya.com/mobile/playlist/album/page?albumId=' + self.albumId + '&pageId=' + str(self.details_current_page)
            response = requests.get(url)
            data = json.loads(response.text)['list']
            for i,_ in enumerate(data):
                self.download_url.append(_['playUrl64'])
                self.widget_dic["tk_table_download_table"].insert('', 'end',values=((i+1)+(self.details_current_page-1)*20,_['title']))
            self.widget_dic["tk_label_details_page_num"]['text'] = "{0}页-共{1}页".format(str(self.details_current_page),str(self.details_total_pages_nums))
    def get_details(self,link):
        self.download_url.clear()
        if link == 1:
            pass
        else:
            for item in self.widget_dic["tk_table_search_table"].selection():
                item_text = self.widget_dic["tk_table_search_table"].item(item,'values')
                self.albumId = item_text[2]
        for item in self.widget_dic["tk_table_download_table"].get_children():
            self.widget_dic["tk_table_download_table"].delete(item)
        url = 'http://mobwsa.ximalaya.com/mobile/playlist/album/page?albumId=' + self.albumId + '&pageId=1'
        response = requests.get(url)
        self.details_total_pages_nums = json.loads(response.text)['maxPageId']
        if self.details_total_pages_nums >= 1:
            url = 'http://mobwsa.ximalaya.com/mobile/playlist/album/page?albumId=' + self.albumId + '&pageId=' + str(self.details_current_page)
            response = requests.get(url)
            data = json.loads(response.text)['list']
            for i,_ in enumerate(data):
                self.widget_dic["tk_table_download_table"].insert('', 'end',values=((i+1)+(self.details_current_page-1)*20,_['title']))
                self.download_url.append(_['playUrl64'])
            self.widget_dic["tk_label_details_page_num"]['text'] = "{0}页-共{1}页".format(str(self.details_current_page),str(self.details_total_pages_nums))
    def download_all(self):
        self.widget_dic["tk_button_download_all"].config(state="disabled")
        self.widget_dic["tk_button_download_select"].config(state="disabled")
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'}
        for item in self.widget_dic["tk_table_download_table"].get_children():
            self.widget_dic["tk_table_download_table"].set(item, column="状态", value="下载中")
            download_url_index = int(self.widget_dic["tk_table_download_table"].set(item, "序号")) - 1
            title = str(download_url_index + 1) + '.' + self.widget_dic["tk_table_download_table"].set(item, "标题")
            file_name = self.download_path + '\\' + title + '.mp3'
            if not os.path.exists(file_name):
                audio_file = requests.get(self.download_url[download_url_index],headers = headers)
                with open(file_name,'wb') as f:
                    f.write(audio_file.content)
            self.widget_dic["tk_table_download_table"].set(item, column="状态", value="完成")  
        self.widget_dic["tk_button_download_all"].config(state="normal")
        self.widget_dic["tk_button_download_select"].config(state="normal")
    def download_select(self):
        self.widget_dic["tk_button_download_all"].config(state="disabled")
        self.widget_dic["tk_button_download_select"].config(state="disabled")
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'}
        selected_index = self.widget_dic["tk_table_download_table"].selection()
        for i in selected_index:
            self.widget_dic["tk_table_download_table"].set(i, column="状态", value="下载中")
            download_url_index = int(self.widget_dic["tk_table_download_table"].set(i, "序号")) - 1
            title = str(download_url_index + 1) + '.' + self.widget_dic["tk_table_download_table"].set(i, "标题")
            file_name = self.download_path + '\\' + title + '.mp3'
            if not os.path.exists(file_name):
                audio_file = requests.get(self.download_url[download_url_index],headers = headers)
                with open(file_name,'wb') as f:
                    f.write(audio_file.content)
            self.widget_dic["tk_table_download_table"].set(i, column="状态", value="完成")
        self.widget_dic["tk_button_download_all"].config(state="normal")
        self.widget_dic["tk_button_download_select"].config(state="normal")
    def set_dir(self):
        self.download_path = tkinter.filedialog.askdirectory()
        self.widget_dic["tk_input_download_path"].delete(0,END)
        self.widget_dic["tk_input_download_path"].insert(END,self.download_path)
    def open_link(self):
        link = self.widget_dic["tk_input_album_link"].get()
        try:
            self.albumId = link.split('/')[-1]
        except:
            tkinter.messagebox.showerror('错误','请输入正确的链接')
            return
        self.get_details(1)
    def search_button_click(self,evt):
        threading.Thread(target=self.search).start()
    def open_link_button_click(self,evt):
        threading.Thread(target=self.open_link).start()
    def set_path_button_click(self,evt):
        threading.Thread(target=self.set_dir).start()
    def download_all_button_click(self,evt):
        threading.Thread(target=self.download_all).start()
    def download_select_button_click(self,evt):
        threading.Thread(target=self.download_select).start()
    def back_pages_button_click(self,evt):
        threading.Thread(target=self.change_pages_nums,args=(0,)).start()
    def next_pages_button_click(self,evt):
        threading.Thread(target=self.change_pages_nums,args=(1,)).start()
    def search_table_double_click(self,evt):
        threading.Thread(target=self.get_details,args=(0,)).start()
    def details_back_pages_button_click(self,evt):
        threading.Thread(target=self.details_change_pages_nums,args=(0,)).start()
    def details_next_pages_button_click(self,evt):
        threading.Thread(target=self.details_change_pages_nums,args=(1,)).start()
    def __event_bind(self):
        self.widget_dic["tk_button_search"].bind('<Button-1>',self.search_button_click)
        self.widget_dic["tk_button_open_link"].bind('<Button-1>',self.open_link_button_click)
        self.widget_dic["tk_button_set_path"].bind('<Button-1>',self.set_path_button_click)
        self.widget_dic["tk_button_download_all"].bind('<Button-1>',self.download_all_button_click)
        self.widget_dic["tk_button_download_select"].bind('<Button-1>',self.download_select_button_click)
        self.widget_dic["tk_button_back"].bind('<Button-1>',self.back_pages_button_click)
        self.widget_dic["tk_button_next"].bind('<Button-1>',self.next_pages_button_click)  
        self.widget_dic["tk_table_search_table"].bind('<Double-1>', self.search_table_double_click)
        self.widget_dic["tk_button_details_back"].bind('<Button-1>',self.details_back_pages_button_click)
        self.widget_dic["tk_button_details_next"].bind('<Button-1>',self.details_next_pages_button_click)
        pass
if __name__ == "__main__":
    win = Win()
    win.mainloop()