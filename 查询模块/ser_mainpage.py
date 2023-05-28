import pymysql.cursors
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
import tkinter.messagebox as messagebox
import time


class SerMainPage(object):

    def bf_MainPage(self):
        self.goMainPage()
    def bf_goSerGoods(self):
        self.goSerGoods()
    def bf_goSerIn(self):
        self.goSerIn()
    def bf_goSerOut(self):
        self.goSerOut()

    def __init__(self,goMainPage, goSerGoods,goSerIn,goSerOut,ID):
        self.ID=ID
        self.goMainPage=goMainPage
        self.goSerGoods=goSerGoods
        self.goSerIn=goSerIn
        self.goSerOut=goSerOut
        self.root = tk.Tk()
        self.root.title('查询模块')
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

        label = Label(self.root, text="信息查询", font=("楷体", 30))
        label.pack(pady=10)  # pady=100 界面的长度

        # 按钮
        Button(self.root, text="返回主页", font=tkFont.Font(size=16), command=self.bf_MainPage, width=20,
               height=2, fg='white', bg='gray').place(x=400, y=400)
        Button(self.root, text="货物查询", font=tkFont.Font(size=16), command=self.bf_goSerGoods, width=20,
               height=2, fg='white', bg='gray').place(x=100, y=400)
        Button(self.root, text="入库记录查询", font=tkFont.Font(size=16), command=self.bf_goSerIn, width=20,
               height=2, fg='white', bg='gray').place(x=100, y=300)
        Button(self.root, text="出库记录查询", font=tkFont.Font(size=16), command=self.bf_goSerOut, width=20,
               height=2, fg='white', bg='gray').place(x=400, y=300)

        self.root.mainloop()


if __name__ == '__main__':
    root = Tk()
    SerMainPage(None,None,1)
    root.mainloop()