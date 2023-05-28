
import pymysql.cursors
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
import tkinter.messagebox as messagebox
import time

# 连接数据库
from 主界面.Application import Application
from 主界面.mainpage import StartPage
# 主页面


# 注册不放在这里
'''
class zhuce:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁子界面
        self.window = tk.Tk()
        self.window.title('注册用户')
        self.window.geometry('450x350+600+150')

        self.top_title = Label(self.window, text='请输入用户名和密码', bg='SkyBlue', font=('楷体', 20), width=70, height=2)
        self.top_title.pack()

        self.var_id = StringVar()
        self.var_password = StringVar()
        self.right_top_id_label = Label(text="用户名", font=('楷体', 15)).pack(pady=15)
        self.right_top_id_entry = Entry(textvariable=self.var_id, font=('楷体', 15)).pack()

        self.right_top_name_label = Label(text="密码", font=('楷体', 15)).pack(pady=15)
        self.right_top_name_entry = Entry(textvariable=self.var_password, font=('楷体', 15)).pack()

        self.right_top_button1 = ttk.Button(text='确定', width=20, command=self.insert).pack(pady=30)
        self.right_top_button2 = ttk.Button(text='返回', width=20, command=self.back).pack()
        self.window.protocol("WM_DELETE_WINDOW", self.exit)  # 捕捉右上角关闭点击
        self.id=''
    def back(self,):
        Sign_In(self.window)  # 显示主窗口 销毁本窗口
    def exit(self):
        exit()

    def insert(self):
        if self.var_id.get() != '':
            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='customer',  # 自己创建的数据库名称
                                 charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "SELECT * FROM 客户 WHERE Id = '%s'" % (self.var_id.get())  # SQL 查询语句
            try:
                cursor.execute(sql)  # 执行sql语句
                results = cursor.fetchall()
                for row in results:
                    self.id = ''+row[0]
                db.commit()  # 提交到数据库执行
                db.close()  # 关闭数据库连接

                if self.var_id.get()==self.id :
                    messagebox.showinfo('提示', '用户已经存在')
                    self.window.protocol("WM_DELETE_WINDOW", self.exit)
                    self.id=''
                else:
                    if self.var_id.get() != '' and self.var_password.get() != '':
                        db = pymysql.connect(host='localhost',
                                             port=3306,
                                             user='root',
                                             passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                             db='customer',  # 自己创建的数据库名称
                                             charset='utf8')
                        cursor = db.cursor()  # 使用cursor()方法获取操作游标
                        sql = "INSERT INTO 客户(Id,password)  VALUES ('%s', '%s')" % (
                        self.var_id.get(), self.var_password.get())  # SQL 插入语句
                        cursor.execute(sql)  # 执行sql语句
                        db.commit()  # 提交到数据库执行
                        messagebox.showinfo('提示！', '入库成功！')
                        db.close()  # 关闭数据库连接
                        Sign_In(self.window)
                    else:
                        messagebox.showinfo('提示！', '请填写完整信息！')
            except:
                pass
                messagebox.showinfo('提示', '数据库连接失败！')
        else:
            messagebox.showinfo('提示', '请填写完整信息！')

'''

# 客户登录
class Sign_In:

    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁子界面
        self.window = tk.Tk()
        self.window.title('欢迎登录库存管理系统')
        self.window.geometry('400x250+50+150')

        self.Id = StringVar()
        self.Password=StringVar()
        self.id = ''
        self.password = ''

        #进行查询
        #Button(self.window, text="库存清单", font=tkFont.Font(size=12), command=lambda: cangkudan(self.window), width=20,
        #       height=2, fg='white', bg='gray').place(x=20, y=70)
        self.right_top_name_label = Label(text="请输入账户密码", font=('楷体', 20)).pack(pady=20)
        self.right_top_name_label = Label(text="账户：", font=('楷体', 15)).place(x=60,y=100)
        self.right_top_name_entry = Entry(textvariable=self.Id, font=('楷体', 15)).place(x=130,y=100)
        self.right_top_name_label = Label(text="密码：", font=('楷体', 15)).place(x=60,y=150)
        self.right_top_name_entry = Entry(textvariable=self.Password,  show='*',font=('楷体', 15)).place(x=130,y=150)
        self.right_top_button3 = ttk.Button(text='确定', width=10, command=self.new_row).place(x=110,y=210)
        #self.right_top_button4 = ttk.Button(text='注册', width=20, command=self.back).pack()
        self.right_top_button4 = ttk.Button(text='退出', width=10, command=self.exit).place(x=240,y=210)
        self.window.protocol("WM_DELETE_WINDOW", self.exit)

        self.window.mainloop()

    #def back(self):
        #zhuce(self.window)
    def exit(self):
        exit()

    def new_row(self):
        if self.Id.get() != '':
            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='manager',  # 自己创建的数据库名称
                                 charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "SELECT * FROM 客户 WHERE Id = '%s'" % (self.Id.get())  # SQL 查询语句
            try:
                cursor.execute(sql)  # 执行sql语句
                results = cursor.fetchall()
                for row in results:
                    self.id = ''+row[0]
                    self.password = '' + row[1]
                db.commit()  # 提交到数据库执行
                db.close()  # 关闭数据库连接
                if self.id=='':
                    messagebox.showinfo('提示', '不存在该用户信息')
                    self.id = ''
                    self.password = ''
                if self.Id.get()==self.id and self.Password.get()==self.password:
                    #self.window.destroy()
                    ID=self.Id.get()
                    Application(self.window,ID=ID)
                    self.window.protocol("WM_DELETE_WINDOW", self.exit)
                    self.id=''
                    self.password= ''
                elif self.Id.get()==self.id and self.Password.get()!=self.password:
                    messagebox.showinfo('提示', '密码错误')
                    self.window.protocol("WM_DELETE_WINDOW", self.exit)

                    self.id = ''
                    self.password = ''
            except:
                pass
                #messagebox.showinfo('提示', '数据库连接失败！')
        else:
            messagebox.showinfo('提示', '请填写您的信息！')







if __name__ == '__main__':
    window = tk.Tk()
    Sign_In(window)

