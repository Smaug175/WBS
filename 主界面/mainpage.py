
import pymysql.cursors
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
import tkinter.messagebox as messagebox
import time


class StartPage(object):
    def bf_goInPut(self):
        self.goInPut()
    def bf_goOut(self):
        self.goOut()
    def bf_goInfPer(self):
        self.goInfPer()
    def bf_goInfSer_APP(self):
        self.goInfSer_APP()
    def bf_goMove(self):
        self.goMove()
    def bf_goSerM_Page(self):
        self.goM_Page()
    def bf_goSee(self):
        self.goSee()

    def __init__(self, goInPut,goOut,goInfPer,goInfSer_APP,goMove,goSerM_Page,ID,goSee):
        self.ID=ID
        self.goInPut=goInPut
        self.goInfPer=goInfPer
        self.goInfSer_APP=goInfSer_APP
        self.goOut=goOut
        self.goMove=goMove
        self.goM_Page=goSerM_Page
        self.goSee=goSee

        self.root = tk.Tk()
        self.root.title('仓库管理系统')
        self.root.geometry('700x600+50+150')

        def getTime():
            timeStr = time.strftime('%Y.%m.%d %H:%M:%S')
            Rtime.configure(text=timeStr)
            self.root.after(1000, getTime)

        Rtime = Label(self.root, text='')
        Rtime.pack(pady=25)
        getTime()

        label = Label(self.root, text="仓库管理系统", font=("楷体", 30))
        label.pack(pady=10)  # pady=100 界面的长度

        # 按钮
        Button(self.root, text="链表查询", font=tkFont.Font(size=16), command=self.bf_goSerM_Page, width=20,
               height=2, fg='white', bg='gray').place(x=100, y=500)
        Button(self.root, text="入库操作", font=tkFont.Font(size=16), command=self.bf_goInPut, width=20,
               height=2, fg='white', bg='gray').place(x=100, y=200)
        Button(self.root, text="出库操作", font=tkFont.Font(size=16), command=self.bf_goOut, width=20,
               height=2, fg='white', bg='gray').place(x=100, y=300)
        Button(self.root, text="移库操作", font=tkFont.Font(size=16), command=self.bf_goMove, width=20,
               height=2, fg='white', bg='gray').place(x=100, y=400)
        Button(self.root, text="个人信息查询", font=tkFont.Font(size=16), command=self.bf_goInfPer, width=20,
               height=2, fg='white', bg='gray').place(x=400, y=300)
        Button(self.root, text="信息查询", font=tkFont.Font(size=16), command=self.bf_goInfSer_APP, width=20,
               height=2, fg='white', bg='gray').place(x=400, y=200)
        Button(self.root, text="业务查询", font=tkFont.Font(size=16), command=self.bf_goSee, width=20,
               height=2, fg='white', bg='gray').place(x=400, y=400)
        Button(self.root, text="退出系统", font=tkFont.Font(size=16), command=self.root.destroy, width=20,
               height=2, fg='white', bg='gray').place(x=400, y=500)

        self.root.mainloop()


if __name__ == '__main__':
    root = Tk()
    StartPage(None,None,None,None,None,None,ID=0)
    root.mainloop()