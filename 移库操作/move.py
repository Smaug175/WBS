import pymysql.cursors
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
import tkinter.messagebox as messagebox
import time
from tkintertable import TableCanvas, TableModel
import tkinter as tk
from tinui.TinUI import TinUI

class Move():

    def bf_goMainPage(self):
        self.goMainPage()

    def __init__(self, goMainPage, ID):
        self.goMainPage = goMainPage
        self.ID = ID  # 工号
        self.root = Tk()

        self.root.title('移库操作')
        self.root.geometry('500x180+50+150')

        self.top_title = Label(self.root, text='请输入库存位置，查找当前位置货物', bg='SkyBlue', font=('楷体', 20), width=70, height=1)
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
        self.var_position = StringVar()
        self.var_new = StringVar()


        self.right_top_id_labelsrg = Label(text="原库存位置：", font=('楷体', 15)).place(x=50, y=40)
        self.right_top_id_entrysrg = Entry(textvariable=self.var_position, font=('楷体', 15)).place(x=170, y=40)
        self.right_top_id_labelsrg = Label(text="移至新位置：", font=('楷体', 15)).place(x=50, y=80)
        self.right_top_id_entrysrg = Entry(textvariable=self.var_new, font=('楷体', 15)).place(x=170, y=80)
        self.right_top_button3srg = ttk.Button(text='执行', width=10, command=self.new_move).place(x=160, y=120)
        self.right_top_button3srg = ttk.Button(text='返回', width=10, command=self.bf_goMainPage).place(x=300, y=120)
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

    def new_move(self):#查询单个

        if  self.var_position.get() != '' and self.var_new.get()!='':
            self.data = []
            self.data.append(('货物代码', '货物名称', '货物类型', '存放库位', '库存总量', '计量单位', '供应商'))
            db = pymysql.connect(host='localhost',
                                         port=3306,
                                         user='root',
                                         passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                         db='goods',  # 自己创建的数据库名称
                                         charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "SELECT * FROM 仓库 WHERE 存放库位 = '%s'" % (self.var_position.get())
            #print(sql)
            db.ping(reconnect=True)
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
            results = cursor.fetchall()
            db.close()
            print(results)
            if results==():
                messagebox.showinfo('提示！', '原位置不存在货物信息，请核对！')
            else:
                db = pymysql.connect(host='localhost',
                                     port=3306,
                                     user='root',
                                     passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                     db='goods',  # 自己创建的数据库名称
                                     charset='utf8')
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                sql = "SELECT * FROM 仓库 WHERE 存放库位 = '%s'" % (self.var_new.get())
                # print(sql)
                db.ping(reconnect=True)
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                results = cursor.fetchall()
                db.close()
                print(results)
                if results != ():
                    messagebox.showinfo('提示！', '新位置有货物信息，请核对！')
                else:
                    db = pymysql.connect(host='localhost',
                                         port=3306,
                                         user='root',
                                         passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                         db='goods',  # 自己创建的数据库名称
                                         charset='utf8')
                    cursor = db.cursor()  # 使用cursor()方法获取操作游标
                    sql = "update 仓库 \n" \
                            "set 仓库.存放库位='%s'"\
                            "where 仓库.存放库位='%s' " % (self.var_new.get(),self.var_position.get())
                    # print(sql)
                    db.ping(reconnect=True)

                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                    db.close()
                    db = pymysql.connect(host='localhost',
                                         port=3306,
                                         user='root',
                                         passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                         db='goods',  # 自己创建的数据库名称
                                         charset='utf8')
                    cursor = db.cursor()  # 使用cursor()方法获取操作游标
                    sql = "SELECT * FROM 仓库 WHERE 存放库位 = '%s'" % (self.var_new.get())
                    # print(sql)
                    db.ping(reconnect=True)
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                    results = cursor.fetchall()
                    db.close()
                    for row in results:
                        self.Id.append(row[0])
                        self.name.append(row[1])
                        self.type.append(row[2])
                        self.position.append(row[3])
                        self.num.append(row[4])
                        self.danwei.append(row[5])
                        self.supplyer.append(row[6])
                        self.data.append(row)
                    #messagebox.showinfo('提示！', '修改成功，请重新启动')
                    a = Tk()
                    a.title('新位置')
                    a.geometry('715x150+450+450')
                    b = TinUI(a, bg='white')
                    b.pack(fill='both', expand=True)
                    b.add_table((0, 0),data = self.data)
                    messagebox.showinfo('提示！', '移库成功')

        else:
            messagebox.showinfo('提示！', '请填写完整修改信息，不能为空')
        # 将入库单数据写入入库单数据库





if __name__ == '__main__':
    # root = Tk()
    Move(None, ID=1)
    # root.mainloop()