import pymysql.cursors
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
import tkinter.messagebox as messagebox
import time
from tkintertable import TableCanvas, TableModel
import tkinter as tk
from tinui.TinUI import TinUI

class Change():

    def bf_goM_Page(self):
        try:
            self.a.destroy()
        except:
            pass
        self.goM_Page()

    def __init__(self, goM_Page, ID):
        self.goM_Page = goM_Page
        self.ID = ID  # 工号
        self.root = Tk()

        self.root.title('链接修改')
        self.root.geometry('500x330+50+150')

        self.top_title = Label(self.root, text='请先查询是否存在该链接\n货物代码不允许修改', bg='SkyBlue', font=('楷体', 20), width=70, height=2)
        self.top_title.pack()
        # 获取信息
        self.var_Id = StringVar()
        self.var_name = StringVar()
        self.var_type = StringVar()
        self.var_danwei = StringVar()
        self.var_supplyer = StringVar()

        self.right_top_id_labelsrg4 = Label(text="货物代码：", font=('楷体', 15)).place(x=70, y=70)
        self.right_top_id_entrysrg4 = Entry(textvariable=self.var_Id, font=('楷体', 15)).place(x=170, y=70)
        self.top_title4 = Label(self.root, text='', bg='Gray', font=('楷体', 5), width=1000,
                               height=1).place(x=0,y=100)
        self.right_top_button3srg4 = ttk.Button(text='查找', width=10, command=self.Sere_1).place(x=390, y=70)
        self.right_top_name_label4 = Label(text="货物名称：", font=('楷体', 15)).place(x=70, y=120)
        self.right_top_name_entry4 = Entry(textvariable=self.var_name, font=('楷体', 15)).place(x=170, y=120)
        self.right_top_name_label4 = Label(text="货物类型：", font=('楷体', 15)).place(x=70, y=160)
        self.right_top_name_entr4y = Entry(textvariable=self.var_type, font=('楷体', 15)).place(x=170, y=160)
        self.right_top_name_label4 = Label(text="计量单位：", font=('楷体', 15)).place(x=70, y=200)
        self.right_top_name_entry4 = Entry(textvariable=self.var_danwei, font=('楷体', 15)).place(x=170, y=200)
        self.right_top_name_label4 = Label(text="供应商：", font=('楷体', 15)).place(x=70, y=240)
        self.right_top_name_entry4 = Entry(textvariable=self.var_supplyer, font=('楷体', 15)).place(x=170, y=240)
        self.right_top_button3srg4 = ttk.Button(text='执行', width=10, command=self.Update_1).place(x=160, y=280)
        self.right_top_button3srg4 = ttk.Button(text='返回', width=10, command=self.bf_goM_Page).place(x=300, y=280)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)  # 捕捉右上角关闭点击

        self.root.mainloop()
        self.password = ''

    def exit(self):
        exit()

    def add_table(self, pos: tuple, outline='#E1E1E1', fg='black', bg='white', data=[['1', '2-', '3'], ['a', 'b', 'c']],
                  minwidth=100, font=('微软雅黑', 12)):  # 绘制表格
        def get_max_height(widths: dict):
            height = 0
            for i in widths.values():
                height = i[1] if i[1] > height else height
            # 重新绘制
            for back in widths.keys():
                self.delete(widths[back][0])
                x1, y1, x2 = widths[back][2]
                y2 = y1 + height
                newback = self.create_rectangle((x1, y1, x2, y2), outline=outline, fill=bg)
                self.lower(newback)
            return height

        title_num = len(data[0])  # 获取表头个数
        end_x, end_y = pos  # 起始位置
        height = 0
        line_width = {}  # 获取每列的固定宽度
        count = 1
        for i in data[0]:
            title = self.create_text((end_x, end_y), anchor='nw', text=i, fill=fg, font=font)
            bbox = self.bbox(title)
            if bbox[2] - bbox[0] <= 100:
                width = 100
            else:
                width = bbox[2] - bbox[0]
            line_width[count] = width
            height = bbox[3] - bbox[1]
            self.create_rectangle((end_x, end_y, end_x + width, end_y + height), outline=outline, fill=bg)
            end_x = end_x + width + 2
            count += 1
            self.tkraise(title)
        end_y = pos[1] + height + 2
        for line in data[1:]:
            count = 1
            a_dict = {}
            end_x = pos[0]
            height = 0
            for a in line:
                width = line_width[count]
                cont = self.create_text((end_x, end_y), anchor='nw', text=a, fill=fg, width=width, font=font)
                bbox = self.bbox(cont)
                height = bbox[3] - bbox[1]
                back = self.create_rectangle((end_x, end_y, end_x + width, end_y + height), outline=outline, fill=bg)
                self.tkraise(cont)
                a_dict[count] = (back, height, (end_x, end_y, end_x + width))  # (end_x,end_y,width)为重新绘制确定位置范围
                end_x = end_x + width + 2
                count += 1
            height = get_max_height(a_dict)
            end_y = end_y + height + 2
        return None

    def Sere_1(self):#查询单个是不是存在这个链接
        try:
            self.a.destroy()
        except:
            pass

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
            self.data = []
            self.data.append(('货物代码', '货物名称', '货物类型', '计量单位', '供应商'))

            cursor.execute(sql)  # 执行sql语句
            results = cursor.fetchall()
            print(results)
            if results==():
                messagebox.showinfo('提示！', '不存在该链接信息，请核对！')
            else:
                for row in results:
                    self.data.append(row)

                db.ping(reconnect=True)
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                db.close()  # 关闭数据库连接
                #messagebox.showinfo('提示！', '修改成功，请重新启动')
                self.a = Tk()
                self.a.geometry('500x50+450+50')
                b = TinUI(self.a, bg='white')
                b.pack(fill='both', expand=True)
                #b.add_table((0, 0),
                            #data=(self.Id, self.name, self.type, self.position, self.num, self.danwei, self.supplyer))
                b.add_table((0, 0),data = self.data)

        else:
            messagebox.showinfo('提示！', '请输入货物代码，不能为空！')
        # 将入库单数据写入入库单数据库

    def Update_1(self):
        try:
            self.a.destroy()
        except:
            pass

        if  self.var_Id.get() != ''  and self.var_name.get() != '' and self.var_type.get() != '' and self.var_danwei.get() != '' and self.var_supplyer.get() != '':

            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='goods',  # 自己创建的数据库名称
                                 charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "SELECT * FROM 链接表 WHERE 货物代码 = '%s'" % (self.var_Id.get())
            print(sql)
            self.data = []
            self.data.append(('货物代码', '货物名称', '货物类型', '计量单位', '供应商'))

            cursor.execute(sql)  # 执行sql语句
            results = cursor.fetchall()
            print(results)
            if results == ():
                messagebox.showinfo('提示！', '不存在该链接信息，请核对！')
            else:

                db = pymysql.connect(host='localhost',
                                             port=3306,
                                             user='root',
                                             passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                             db='goods',  # 自己创建的数据库名称
                                             charset='utf8')
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                sql = "update 链接表 \n" \
                      "set 链接表.货物名称='%s',链接表.货物类型='%s',链接表.计量单位='%s',链接表.供应商='%s'\n" \
                      "where 链接表.货物代码='%s' " % (
                          self.var_name.get(), self.var_type.get(), self.var_danwei.get(), self.var_supplyer.get(),self.var_Id.get())
                            # SQL 查询语句
                print(sql)
                cursor.execute(sql)  # 执行sql语句
                db.ping(reconnect=True)
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                db.close()  # 关闭数据库连接
                messagebox.showinfo('提示！', '修改成功!')

                db = pymysql.connect(host='localhost',
                                     port=3306,
                                     user='root',
                                     passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                     db='goods',  # 自己创建的数据库名称
                                     charset='utf8')
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                sql = "SELECT * FROM 链接表 WHERE 货物代码 = '%s'" % (self.var_Id.get())
                print(sql)
                self.data = []
                self.data.append(('货物代码', '货物名称', '货物类型', '计量单位', '供应商'))

                cursor.execute(sql)  # 执行sql语句
                results = cursor.fetchall()
                print(results)
                if results == ():
                    messagebox.showinfo('提示！', '不存在该链接信息，请核对！')
                else:
                    for row in results:
                        self.data.append(row)

                    db.ping(reconnect=True)
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                    db.close()  # 关闭数据库连接
                    # messagebox.showinfo('提示！', '修改成功，请重新启动')
                    self.a = Tk()
                    self.a.geometry('500x50+450+50')
                    b = TinUI(self.a, bg='white')
                    b.pack(fill='both', expand=True)
                    # b.add_table((0, 0),
                    # data=(self.Id, self.name, self.type, self.position, self.num, self.danwei, self.supplyer))
                    b.add_table((0, 0), data=self.data)

        else:
            messagebox.showinfo('提示！', '请输入完整信息，不能为空！')
        # 将入库单数据写入入库单数据库




if __name__ == '__main__':
    # root = Tk()
    Change(None, ID=1)
    # root.mainloop()