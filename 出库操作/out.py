import threading

import pymysql.cursors
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
import tkinter.messagebox as messagebox
import time



class Out:

    def bf_goMainPage(self):
        self.goMainPage()
    def __init__(self, goMainPage,ID):
        self.goMainPage=goMainPage
        self.ID = ID#工号
        self.root = Tk()
        self.root.title('出库操作')
        self.root.geometry('400x320+50+150')

        self.top_title = Label(self.root, text='出库操作', bg='SkyBlue', font=('楷体', 20), width=70, height=2)
        self.top_title.pack()
        #获取信息
        self.var_outid = StringVar()
        self.var_Id = StringVar()
        self.var_name=''
        self.var_type = ''
        self.var_position = StringVar()
        self.var_number = StringVar()
        self.var_danwei = ''
        self.var_price = StringVar()
        self.var_time = ''
        self.var_supplyer = ''

        self.right_top_id_label = Label(text="出库单号：", font=('楷体', 15)).place(x=20, y=80)
        self.right_top_id_entry = Entry(textvariable=self.var_outid, font=('楷体', 15)).place(x=130, y=80)
        self.right_top_name_label = Label(text="货物代码：", font=('楷体', 15)).place(x=20, y=120)
        self.right_top_name_entry = Entry(textvariable=self.var_Id, font=('楷体', 15)).place(x=130, y=120)
        self.right_top_name_label = Label(text="存放库位：", font=('楷体', 15)).place(x=20, y=160)
        self.right_top_name_entry = Entry(textvariable=self.var_position, font=('楷体', 15)).place(x=130, y=160)
        self.right_top_name_label = Label(text="出库总量：", font=('楷体', 15)).place(x=20, y=200)
        self.right_top_name_entry = Entry(textvariable=self.var_number, font=('楷体', 15)).place(x=130, y=200)
        self.right_top_name_label = Label(text="出库单价：", font=('楷体', 15)).place(x=20, y=240)
        self.right_top_name_entry = Entry(textvariable=self.var_price, font=('楷体', 15)).place(x=130, y=240)
        self.right_top_button1 = ttk.Button(text='确定', width=10, command=self.new_row_out).place(x=100, y=280)
        self.right_top_button2 = ttk.Button(text='返回', width=10, command=self.bf_goMainPage).place(x=230, y=280)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)  # 捕捉右上角关闭点击

        self.root.mainloop()
        self.password=''
    def exit(self):
        exit()


    def new_row_out(self):
        #
        timeStr = time.strftime('%Y.%m.%d %H:%M:%S')
        self.var_time = timeStr
        if self.var_Id.get() != '' and self.var_outid.get()!=''  and self.var_position.get()!='' and self.var_number.get()!='' and self.var_price.get()!='' :
            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='goods',  # 自己创建的数据库名称
                                 charset='utf8')
            sql = "SELECT * FROM 链接表 WHERE 货物代码 = '%s'" % (self.var_Id.get())
            cursor = db.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            db.close()
            print(results)
            if results == ():
                messagebox.showinfo('提示！', '不存在该货物编号，请核对！')
            else:
                self.var_name = results[0][1]
                self.var_type = results[0][2]
                self.var_danwei = results[0][3]
                self.var_supplyer = results[0][4]
                db = pymysql.connect(host='localhost',
                                     port=3306,
                                     user='root',
                                     passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                     db='goods',  # 自己创建的数据库名称
                                     charset='utf8')
                sql = "SELECT * FROM 出库单 WHERE 出库单编号 = '%s'" % (self.var_outid.get())
                cursor = db.cursor()
                cursor.execute(sql)

                db.commit()
                results = cursor.fetchall()
                # print(results)
                db.close()  # 关闭数据库连接
                if results != ():
                    if results[0][0] == self.var_outid.get():
                        messagebox.showinfo('提示！', '已经存在该出库单编号，请核对！')

                else:
                    #查找是不是数量不对
                    db = pymysql.connect(host='localhost',
                                         port=3306,
                                         user='root',
                                         passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                         db='goods',  # 自己创建的数据库名称
                                         charset='utf8')
                    cursor = db.cursor()  # 使用cursor()方法获取操作游标
                    sql = "SELECT * FROM 仓库 WHERE 货物代码 = '%s' and 货物名称='%s' and 货物类型='%s' and 存放库位='%s'  and 计量单位='%s' and 供应商='%s' " % (
                        self.var_Id.get(),self.var_name,self.var_type,self.var_position.get(),self.var_danwei,self.var_supplyer)
                    #print(sql)
                    try:
                        cursor.execute(sql)  # 执行sql语句

                        db.commit()
                        results = cursor.fetchall()
                    except:
                        db.rollback()
                        messagebox.showinfo('提示！', '请填写正确出库信息，不存在该货物！')
                    #print(results)
                    db.close()
                    data=()
                    if results!=():
                        data=((self.var_Id.get(),self.var_name,self.var_type,self.var_position.get(),results[0][4],self.var_danwei,self.var_supplyer),)
                        #print(data)
                        if data==results:
                            if int(self.var_number.get())-int(results[0][4])>0:
                                messagebox.showinfo('提示！', '库存数量为'+results[0][4]+',出库数量大于库存数量！')
                            else:

                                #进行减法操作
                                db = pymysql.connect(host='localhost',
                                                 port=3306,
                                                 user='root',
                                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                                 db='goods',  # 自己创建的数据库名称
                                                 charset='utf8')
                                sql = "INSERT INTO 出库单(出库单编号,货物代码,货物名称,货物类型,存放库位,出库总量,计量单位,出库单价,出库时间,供应商,经办人)  VALUES ('%s', '%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s')" % (
                                    self.var_outid.get(), self.var_Id.get(), self.var_name, self.var_type, self.var_position.get(), self.var_number.get(), self.var_danwei, self.var_price.get(), self.var_time, self.var_supplyer, self.ID)  # SQL 插入语句
                                #print(sql)
                                cursor = db.cursor()  # 使用cursor()方法获取操作游标

                                try:
                                    try:
                                        db.ping(reconnect=True)
                                        #print("done")
                                    except:
                                        print('wrong')
                                    cursor.execute(sql)
                                    db.commit()
                                    messagebox.showinfo('提示！', '出库成功！')

                                except:
                                    db.rollback()
                                    #exit()
                                    print('error')
                                #db.ping(reconnect=True)

                                db.close()  # 关闭数据库连接
                                # 如果库存数量为0 则删除库存记录

                                if int(self.var_number.get())-int(results[0][4])==0:
                                    #print(self.var_number.get())
                                    #print(results[0][4])
                                    db = pymysql.connect(host='localhost',
                                                         port=3306,
                                                         user='root',
                                                         passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                                         db='goods',  # 自己创建的数据库名称
                                                         charset='utf8')
                                    cursor = db.cursor()  # 使用cursor()方法获取操作游标
                                    sql = "DELETE  FROM 仓库 WHERE 仓库.货物代码 = '%s' and 仓库.货物名称='%s' and 仓库.货物类型='%s' and 仓库.存放库位='%s' and 仓库.库存总量='0' and 仓库.计量单位='%s' and 仓库.供应商='%s' " % (
                                        self.var_Id.get(), self.var_name, self.var_type, self.var_position.get(),
                                        self.var_danwei, self.var_supplyer)
                                    #sql = "DELETE  FROM 仓库 LIMIT 库存总量='0'"

                                    print(sql)
                                    cursor.execute(sql)
                                    db.commit()# 执行sql语句
                                    db.close()

                    else:

                        messagebox.showinfo('提示！', '请填写正确出库信息，不存在该货物！')


        else:
            messagebox.showinfo('提示！', '请填写完整出库信息，不允许留空！')
        #将入库单数据写入入库单数据库

if __name__ == '__main__':
    #root = Tk()
    Out(None, ID=0)
    #root.mainloop()