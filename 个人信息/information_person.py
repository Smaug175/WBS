import pymysql.cursors
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
import tkinter.messagebox as messagebox
import time


class InforPerson:

    def bf_goMainPage(self):
        self.goMainPage()

    def __init__(self, goMainPage,ID):
        self.goMainPage=goMainPage
        self.ID = ID#工号
        self.root = Tk()
        self.root.title('个人信息查询')
        self.root.geometry('500x320+50+150')

        self.top_title = Label(self.root, text='欢迎您！', bg='SkyBlue', font=('楷体', 20), width=70, height=2)
        self.top_title.pack()
        #获取信息
        self.password=''
        self.name=''
        self.telenum=''
        self.worknumber=''
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                             db='manager',  # 自己创建的数据库名称
                             charset='utf8')
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM 客户 WHERE Id = '%s'" % (self.ID)  # SQL 查询语句
        #print(sql)
        db.ping(reconnect=True)
        cursor.execute(sql)  # 执行sql语句
        results = cursor.fetchall()
        for row in results:
            self.ID = '' + row[0]
            self.password = '' + row[1]
            self.name=''+row[2]
            self.telenum=''+row[3]
            self.worknumber=''+row[4]
        db.commit()  # 提交到数据库执行
        db.close()  # 关闭数据库连接
        #print(self.ID)
        #print(self.worknumber+'21')
        self.var_password = StringVar()
        self.var_name=StringVar()
        self.var_telenum = StringVar()
        self.var_worknumber=StringVar()

        self.right_top_id_label = Label(text="ID  ：", font=('楷体', 15)).place(x=20,y=80)
        self.right_top_id_label = Label(text=self.ID, font=('楷体', 15)).place(x=140, y=80)
        self.right_top_name_label = Label(text="密码：", font=('楷体', 15)).place(x=20,y=120)
        self.right_top_name_label = Label(text="请输入修改后的内容：", font=('楷体', 15)).place(x=220,y=80)
        self.right_top_name_label = Label(text=self.password, font=('楷体', 15),).place(x=140,y=120)
        self.right_top_name_entry = Entry(textvariable=self.var_password, font=('楷体', 15),show='*').place(x=230,y=120)
        self.right_top_name_label = Label(text="姓名：", font=('楷体', 15)).place(x=20, y=160)
        self.right_top_name_label = Label(text=self.name, font=('楷体', 15)).place(x=130, y=160)
        self.right_top_name_entry = Entry(textvariable=self.var_name, font=('楷体', 15)).place(x=230, y=160)
        self.right_top_name_label = Label(text="电话：", font=('楷体', 15)).place(x=20, y=200)
        self.right_top_name_label = Label(text=self.telenum, font=('楷体', 15)).place(x=100, y=200)
        self.right_top_name_entry = Entry(textvariable=self.var_telenum, font=('楷体', 15)).place(x=230, y=200)
        self.right_top_name_label = Label(text="工号：", font=('楷体', 15)).place(x=20, y=240)
        self.right_top_name_label = Label(text=self.worknumber, font=('楷体', 15)).place(x=120, y=240)
        self.right_top_name_entry = Entry(textvariable=self.var_worknumber, font=('楷体', 15)).place(x=230, y=240)

        self.right_top_button311 = ttk.Button(text='提交', width=10, command=self.new_row_inf1).place(x=150, y=280)
        self.right_top_button311 = ttk.Button(text='返回', width=10, command=self.bf_goMainPage).place(x=290, y=280)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)  # 捕捉右上角关闭点击

        self.root.mainloop()
        self.password=''
    def exit(self):
        exit()


    def new_row_inf1(self):
        #
        if self.var_password.get() != '' and self.var_name.get()!=''  and self.var_telenum.get()!='' and self.var_worknumber.get()!='':

            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='manager',  # 自己创建的数据库名称
                                 charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "update 客户 \n" \
                  "set 客户.password='%s',客户.name='%s',客户.telenumber='%s',客户.worknumber='%s'\n" \
                  "where 客户.Id='%s' " % (
                self.var_password.get(),self.var_name.get(),self.var_telenum.get(),self.var_worknumber.get(),self.ID)  # SQL 查询语句
            print(sql)
            db.ping(reconnect=True)
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
            db.close()  # 关闭数据库连接
            messagebox.showinfo('提示！', '修改成功，请重新启动')
            exit()
        else:
            messagebox.showinfo('提示！', '请填写完整修改信息，不能为空')
        #将入库单数据写入入库单数据库

if __name__ == '__main__':
    #root = Tk()
    InforPerson(None,ID=1)
    #root.mainloop()