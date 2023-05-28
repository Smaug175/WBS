import pymysql.cursors
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
import tkinter.messagebox as messagebox
import time


class SerM_Page(object):

    def bf_MainPage(self):
        self.goMainPage()
    def bf_goChange(self):
        self.goChange()
    def bf_goNew(self):
        self.goNew()
    def bf_goSer(self):
        self.goSer()
    def bf_goDele(self):
        self.goDele()

    def __init__(self,goMainPage, goChange,goNew,goSer,goDele,ID):
        self.ID=ID
        self.goMainPage=goMainPage
        self.goChange=goChange
        self.goNew=goNew
        self.goSer=goSer
        self.goDele=goDele
        self.root = tk.Tk()
        self.root.title('查询链表模块')
        self.root.geometry('700x600+50+150')

        def getTime():
            timeStr = time.strftime('%Y.%m.%d %H:%M:%S')
            Rtime.configure(text=timeStr)
            self.root.after(1000, getTime)

        timeStr = time.strftime('%Y.%m.%d %H:%M:%S')
        print(timeStr)
        Rtime = Label(self.root, text='')
        Rtime.pack(pady=25)
        getTime()

        label = Label(self.root, text="链表查询", font=("楷体", 30))
        label.pack(pady=10)  # pady=100 界面的长度

        # 按钮
        Button(self.root, text="返回主页", font=tkFont.Font(size=16), command=self.bf_MainPage, width=20,
               height=2, fg='white', bg='gray').place(x=400, y=400)
        Button(self.root, text="新建链表", font=tkFont.Font(size=16), command=self.bf_goNew, width=20,
               height=2, fg='white', bg='gray').place(x=100, y=400)
        Button(self.root, text="链表查询", font=tkFont.Font(size=16), command=self.bf_goSer, width=20,
               height=2, fg='white', bg='gray').place(x=100, y=300)
        Button(self.root, text="修改链表", font=tkFont.Font(size=16), command=self.bf_goChange, width=20,
               height=2, fg='white', bg='gray').place(x=400, y=300)
        Button(self.root, text="删除链表", font=tkFont.Font(size=16), command=self.bf_goDele, width=20,
               height=2, fg='white', bg='gray').place(x=100, y=500)

        self.root.mainloop()


if __name__ == '__main__':
    root = Tk()
    SerM_Page(None,None,None,None,ID=1)
    root.mainloop()