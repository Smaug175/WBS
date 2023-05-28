import pymysql.cursors
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
import tkinter.messagebox as messagebox
import time
from tkintertable import TableCanvas, TableModel
import tkinter as tk
from tinui.TinUI import TinUI

class Dele():

    def bf_goM_Page(self):
        self.goM_Page()

    def __init__(self, goM_Page, ID):
        self.goM_Page = goM_Page
        self.ID = ID  # 工号
        self.root = Tk()

        self.root.title('链接删除')
        self.root.geometry('500x120+50+150')

        self.top_title = Label(self.root, text='请输入需要删除链接的货物代码', bg='SkyBlue', font=('楷体', 20), width=70, height=1)
        self.top_title.pack()
        # 获取信息
        self.Id = []
        self.name = []
        self.type = []
        self.position = []
        self.num=[]
        self.danwei=[]
        self.supplyer=[]
        self.data=[]
        self.var_Id = StringVar()

        self.right_top_id_labelsrg3 = Label(text="货物代码：", font=('楷体', 15)).place(x=70, y=40)
        self.right_top_id_entrysrg3 = Entry(textvariable=self.var_Id, font=('楷体', 15)).place(x=170, y=40)
        self.right_top_button3srg3 = ttk.Button(text='执行', width=10, command=self.dele_1).place(x=160, y=80)
        self.right_top_button3srg3 = ttk.Button(text='返回', width=10, command=self.bf_goM_Page).place(x=300, y=80)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)  # 捕捉右上角关闭点击

        self.root.mainloop()
        self.password = ''

    def exit(self):
        exit()

    def dele_1(self):#查询单个

        if  self.var_Id.get() != '':

            db = pymysql.connect(host='localhost',
                                         port=3306,
                                         user='root',
                                         passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                         db='goods',  # 自己创建的数据库名称
                                         charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "SELECT * FROM 链接表 WHERE 货物代码 = '%s'" % (self.var_Id.get())
            print(sql)
            cursor.execute(sql)  # 执行sql语句
            results = cursor.fetchall()
            db.commit()  # 提交到数据库执行
            db.close()
            print(results)
            if results==():
                messagebox.showinfo('提示！', '不存在该货物信息，请核对！')
            else:
                db = pymysql.connect(host='localhost',
                                     port=3306,
                                     user='root',
                                     passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                     db='goods',  # 自己创建的数据库名称
                                     charset='utf8')
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                sql = "DELETE FROM 链接表 WHERE 货物代码 = '%s'" % (self.var_Id.get())
                print(sql)
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                db.close()

                messagebox.showinfo('提示！', '删除成功！')
        else:
            messagebox.showinfo('提示！', '请填写完整修改信息，不能为空！')
        # 将入库单数据写入入库单数据库

if __name__ == '__main__':
    # root = Tk()
    Dele(None, ID=1)
    # root.mainloop()