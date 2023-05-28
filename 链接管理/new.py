import pymysql.cursors
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
import tkinter.messagebox as messagebox
import time
from tkintertable import TableCanvas, TableModel
import tkinter as tk
from tinui.TinUI import TinUI

class New():

    def bf_goM_Page(self):

        self.goM_Page()

    def __init__(self, goM_Page, ID):
        self.goM_Page = goM_Page
        self.ID = ID  # 工号
        self.root = Tk()
        self.root.title('新建链接')
        self.root.geometry('400x320+50+150')

        self.top_title = Label(self.root, text='新建链接\n货物代码必须唯一指定', bg='SkyBlue', font=('楷体', 20), width=70, height=2)
        self.top_title.pack()
        # 获取信息
        self.var_newid = StringVar()
        self.var_name = StringVar()
        self.var_type = StringVar()
        self.var_danwei = StringVar()
        self.var_supplyer = StringVar()


        self.right_top_id_label1 = Label(text="货物代码：", font=('楷体', 15)).place(x=20, y=80)
        self.right_top_id_entry1 = Entry(textvariable=self.var_newid, font=('楷体', 15)).place(x=130, y=80)
        self.right_top_name_label1 = Label(text="货物名称：", font=('楷体', 15)).place(x=20, y=120)
        self.right_top_name_entry1 = Entry(textvariable=self.var_name, font=('楷体', 15)).place(x=130, y=120)
        self.right_top_name_label1 = Label(text="货物类型：", font=('楷体', 15)).place(x=20, y=160)
        self.right_top_name_entry1 = Entry(textvariable=self.var_type, font=('楷体', 15)).place(x=130, y=160)
        self.right_top_name_label1 = Label(text="计量单位：", font=('楷体', 15)).place(x=20, y=200)
        self.right_top_name_entry1 = Entry(textvariable=self.var_danwei, font=('楷体', 15)).place(x=130, y=200)
        self.right_top_name_label1 = Label(text="供应商：", font=('楷体', 15)).place(x=20, y=240)
        self.right_top_name_entry1 = Entry(textvariable=self.var_supplyer, font=('楷体', 15)).place(x=130, y=240)
        self.right_top_button11 = ttk.Button(text='执行', width=10, command=self.new_row_1).place(x=100, y=280)
        self.right_top_button21 = ttk.Button(text='返回', width=10, command=self.bf_goM_Page).place(x=230, y=280)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)  # 捕捉右上角关闭点击

        self.root.mainloop()
        self.password = ''

    def exit(self):
        exit()

    def new_row_1(self):
        #
        if self.var_newid.get() != ''  and self.var_name.get() != '' and self.var_type.get() != '' and self.var_danwei.get() != '' and self.var_supplyer.get() != '':
            # 防止输错代码与名称
            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='goods',  # 自己创建的数据库名称
                                 charset='utf8')
            sql = "SELECT * FROM 链接表 WHERE 货物代码 = '%s'" % (self.var_newid.get())
            cursor = db.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            db.close()
            print(results)
            if results != ():
                messagebox.showinfo('提示！', '已经存在该链接，请核对！')
            else:
                db = pymysql.connect(host='localhost',
                                     port=3306,
                                     user='root',
                                     passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                     db='goods',  # 自己创建的数据库名称
                                     charset='utf8')
                sql = "INSERT INTO 链接表(货物代码,货物名称,货物类型,计量单位,供应商)  VALUES ('%s', '%s','%s','%s','%s')" % (
                    self.var_newid.get(), self.var_name.get(), self.var_type.get(),
                    self.var_danwei.get(), self.var_supplyer.get() )  # SQL 插入语句
                cursor = db.cursor()
                cursor.execute(sql)
                results = cursor.fetchall()
                db.commit()  # 提交到数据库执行
                db.close()
                # print(results)

                messagebox.showinfo('提示！', '新建成功！')



        else:
            messagebox.showinfo('提示！', '请填写完整入库信息，不允许留空！')
        # 将入库单数据写入入库单数据库


if __name__ == '__main__':
    # root = Tk()
    New(None, ID=0)
    # root.mainloop()