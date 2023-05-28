import random
import threading
import tkinter

import pymysql.cursors
from tkinter import ttk
from tkinter import *  # 图形界面库
import tkinter.messagebox as messagebox
import time
from tinui.TinUI import TinUI
import cv2
import os
import qrcode
from PIL import Image
from pyzbar import pyzbar
import pyzbar.pyzbar as pyzbar

global CHECKPOINT,QR_INF
CHECKPOINT=[]
QR_INF=''

class ck:
    def check_all(self,event):
        global CHECKPOINT
        if CHECKPOINT==[]:
            for j in range(len(self.results)):
                CHECKPOINT.append(self.results[j][0])
        else:
            CHECKPOINT=[]
    def check_one(self,event):
        k=0
        for j in range(len(CHECKPOINT)):
            if CHECKPOINT[j]==self.bus_id:
                del CHECKPOINT[j]
                k=1
                break
        if k==0:
            CHECKPOINT.append(self.bus_id)
    def __init__(self, b, buss_id,i,result):
        global CHECKPOINT
        self.bus_id=buss_id
        self.yes_no=False
        self.results=result
        b.add_checkbutton((1040, 1 ), text='全选', command=self.check_all)
        b.add_checkbutton((1040, 24 + 23 *i), text='', command=self.check_one)

class SEEBusiness:
    #添加表格，并显示
    def add_table(self, pos: tuple, outline='#E1E1E1', fg='black', bg='white',
                  data=[],
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
    def bf_goMainPage(self):
        try:
            self.a.destroy()
        except:
            pass
        self.goMainPage()
    #显示信息
    def information(self):
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                             db='business',  # 自己创建的数据库名称
                             charset='utf8')
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM 业务信息 "
        #print(sql)
        data = []
        data.append(('业务编码','业务情况','代码', '名称', '类型','位置','总量', '单位','单价', '供应商'))

        cursor.execute(sql)  # 执行sql语句
        self.results = cursor.fetchall()
        #print(self.results)
        if self.results == ():
            messagebox.showinfo('提示！', '不存在该货物信息，请核对！')
        else:
            for row in self.results:
                data.append(row)
            db.ping(reconnect=True)
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
            db.close()  # 关闭数据库连接
            # messagebox.showinfo('提示！', '修改成功，请重新启动')
            self.a=Tk()
            self.a.title('业务查看')
            self.a.geometry('1120x320+150+200')
            b = TinUI(self.a)
            b.pack(fill='both', expand=True)
            b.add_table((0, 0), data=data)
            for i in range(len(self.results)):
                ck(b=b, buss_id=int(self.results[i][0]),i=i,result=self.results)
            #print(self.checkpoint)
            ttk.Button(text='刷新', width=10, command=self.del_add).place(x=150, y=80)
            self.a.protocol("WM_DELETE_WINDOW", self.del_no_add)


    def del_no_add(self):
        global CHECKPOINT
        CHECKPOINT=[]
        self.a.destroy()
        ttk.Button(text='查询', width=10, command=self.new_information).place(x=150, y=80)

    def __init__(self, goMainPage,ID):
        self.goMainPage=goMainPage
        self.root = Tk()
        self.root.title('业务查看')
        self.root.geometry('500x150+50+150')

        self.top_title = Label(self.root, text='业务查看', bg='SkyBlue', font=('楷体', 20), width=70, height=2)
        self.top_title.pack()
        #获取信息
        self.business_ID=1
        self.var_business=''
        self.var_OutIn =''
        self.var_Id = ''
        self.var_name=''
        self.var_type = ''
        self.var_position = ''
        self.var_number = 0
        self.var_danwei = ''
        self.var_price = 0
        timeStr = time.strftime('%Y.%m.%d %H:%M:%S')
        self.var_time = ''
        self.var_supplyer = ''
        self.ID = ID  # 工号
        #self.information()
        self.right_top_button1 = ttk.Button(text='查询', width=10, command=self.new_information).place(x=150, y=80)
        self.right_top_button2 = ttk.Button(text='执行', width=10, command=self.exuct).place(x=260, y=80)
        self.right_top_buttonse = ttk.Button(text='返回', width=10, command=self.bf_goMainPage).place(x=370, y=80)
        self.right_top_buttonse = ttk.Button(text='扫一扫', width=10, command=self.QR_read).place(x=40, y=80)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)  # 捕捉右上角关闭点击

        self.root.mainloop()
        self.password=''
    def exit(self):
        exit()

    def del_add(self):
        global CHECKPOINT
        CHECKPOINT=[]
        self.a.destroy()
        self.new_information()

    def new_information(self):#创建新的业务
        Business=('入库','出库','移库')
        k1=random.randint(0,2)
        self.var_business= Business[k1]
        if self.var_business=='入库':
            # 查询是否已经存在当前的业务编码，如果是则需要将编码转换为最大的编码
            # 由业务编码来决定是否删除数据库中的信息
            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='business',  # 自己创建的数据库名称
                                 charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "SELECT * FROM 业务信息 "
            # print(sql)
            db.ping(reconnect=True)
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
            results = cursor.fetchall()
            db.close()
            #print(results)
            # 得到ID信息
            if results != ():
                self.business_ID = int(results[len(results) - 1][0]) + 1
            #入库时，打开链表，选择货物
            #出库应该打开仓库，选择货物
            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='goods',  # 自己创建的数据库名称
                                 charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            # sql = "SELECT * FROM 仓库 WHERE 货物代码 = '%s'" % (self.var_Id.get())
            sql = "SELECT * FROM 链接表 "
            #print(sql)
            data = []
            db.ping(reconnect=True)
            cursor.execute(sql)  # 执行sql语句
            db.commit()
            results = cursor.fetchall()
            db.close()
            for row in results:
                data.append(row)
            k2=random.randint(0,len(data)-1)
            #print(k2,len(self.data))
            da=data[k2]
            k3 = random.randint(0, 10000)
            k4 = random.randint(0, 10000)
            self.var_Id=da[0];self.var_name=da[1];self.var_type=da[2];self.var_danwei=da[3];
            self.var_supplyer=da[4];self.var_number=k3;self.var_price=k4
            #查询已经有的位置，新建一个位置
            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='goods',  # 自己创建的数据库名称
                                 charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "SELECT * FROM 仓库 "
            # print(sql)
            db.ping(reconnect=True)
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
            results = cursor.fetchall()
            db.close()
            pos=[]
            for i in range(len(results)):
                pos.append(results[i][3])
            #print(pos)得到不被占有的位置
            #得到没有被分配的位置
            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='business',  # 自己创建的数据库名称
                                 charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "SELECT * FROM 业务信息 "
            # print(sql)
            db.ping(reconnect=True)
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
            results1 = cursor.fetchall()
            db.close()
            pos1=[]
            #print(results)
            # 得到位置信息
            if results1 != ():
                for i in range(len(results1)):
                    if results1[i][1]=='移库':
                        px, py = self.divide_pos(results1[i][5])
                        pos1.append(px)
                        pos1.append(py)
                    else:
                        pos1.append(results1[i][5])
            #print(pos,pos1)
            while True:
                p1 = random.randint(1, 9);
                p2 = random.randint(1, 9);
                p3 = random.randint(1, 9)
                p = str(p1) + '-' + str(p2) + '-' + str(p3)
                ii=0
                for i in enumerate(pos):

                    if i[1]==p:

                        pass
                    else:
                        ii+=1
                for i in enumerate(pos1):
                    if i[1]==p:
                        pass
                    else:
                        ii+=1
                if ii==(len(pos)+len(pos1)):
                    #print(ii,len(pos),len(pos1))
                    break
            self.var_position=p#入库位置
        elif self.var_business=='出库':
            # 查询是否已经存在当前的业务编码，如果是则需要将编码转换为最大的编码
            # 由业务编码来决定是否删除数据库中的信息
            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='business',  # 自己创建的数据库名称
                                 charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "SELECT * FROM 业务信息 "
            # print(sql)
            db.ping(reconnect=True)
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
            results = cursor.fetchall()
            db.close()
            #print(results)
            # 得到ID信息
            if results != ():
                self.business_ID = int(results[len(results) - 1][0]) + 1
            #随机选择一个仓库中的数据
            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='goods',  # 自己创建的数据库名称
                                 charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            # sql = "SELECT * FROM 仓库 WHERE 货物代码 = '%s'" % (self.var_Id.get())
            sql = "SELECT * FROM 仓库 "
            # print(sql)
            data = []
            db.ping(reconnect=True)
            cursor.execute(sql)  # 执行sql语句
            db.commit()
            results = cursor.fetchall()
            db.close()
            if results!=():
                k=random.randint(0,len(results)-1)#随机取得其中的一个数据
                data = results[k]
            else:
                messagebox.showinfo('提示！', '仓库无信息！')
            #如果已经存在则将id设为0
            #随机得到其中一个元素
            #print(data)
            k3 = random.randint(1, int(data[4]))
            k4 = random.randint(0, 10000)
            self.var_Id = data[0];
            self.var_name = data[1];
            self.var_type = data[2];
            self.var_position=data[3]
            self.var_danwei = data[5];
            self.var_supplyer = data[6];
            self.var_number = k3;
            self.var_price = k4
            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='business',  # 自己创建的数据库名称
                                 charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "SELECT * FROM 业务信息 "
            # print(sql)
            db.ping(reconnect=True)
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
            results = cursor.fetchall()
            #print(results)
            db.close()
            for env in enumerate(results):
                pos = env[1][5]
                if env[1][1] == '移库':
                    #print(env[1][5])
                    pos, p = self.divide_pos(env[1][5])
                if env[1][2]==self.var_Id and pos==self.var_position:
                    self.business_ID=0
        elif self.var_business=='移库':
            # 查询是否已经存在当前的业务编码，如果是则需要将编码转换为最大的编码
            # 由业务编码来决定是否删除数据库中的信息
            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='business',  # 自己创建的数据库名称
                                 charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "SELECT * FROM 业务信息 "
            # print(sql)
            db.ping(reconnect=True)
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
            results = cursor.fetchall()
            db.close()
            #print(results)
            # 得到ID信息
            if results != ():
                self.business_ID = int(results[len(results) - 1][0]) + 1
            #从仓库随机选择一个货物移动
            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='goods',  # 自己创建的数据库名称
                                 charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            # sql = "SELECT * FROM 仓库 WHERE 货物代码 = '%s'" % (self.var_Id.get())
            sql = "SELECT * FROM 仓库 "
            # print(sql)
            data = []
            db.ping(reconnect=True)
            cursor.execute(sql)  # 执行sql语句
            db.commit()
            results = cursor.fetchall()
            db.close()
            if results!=():
                k = random.randint(0, len(results) - 1)
            else:
                messagebox.showinfo('提示！', '仓库无信息！')
            # 随机得到其中一个元素
            data = results[k]
            # print(data)
            self.var_Id = data[0];
            self.var_name = data[1];
            self.var_type = data[2];
            self.var_position = data[3];#之前的位置
            self.var_danwei = data[5];
            self.var_supplyer = data[6];
            self.var_number = data[4]#全部移动
            self.var_price = '移动无价格'
            #查询是不是已经有了业务
            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='business',  # 自己创建的数据库名称
                                 charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "SELECT * FROM 业务信息 "
            # print(sql)
            db.ping(reconnect=True)
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
            results = cursor.fetchall()
            db.close()
            #判断是不是存在已经被选中过的元素
            for env in enumerate(results):
                pos=env[1][5]
                if env[1][1]=='移库':
                    pos, p = self.divide_pos(env[1][5])
                    #print(pos,p)
                if env[1][2] == self.var_Id and pos == self.var_position:
                    self.business_ID = 0
            # 给出一个新的位置
            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='goods',  # 自己创建的数据库名称
                                 charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "SELECT * FROM 仓库 "
            # print(sql)
            db.ping(reconnect=True)
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
            results = cursor.fetchall()
            db.close()
            pos = []
            for i in range(len(results)):
                pos.append(results[i][3])
            # print(pos)得到不被占有的位置
            # 得到没有被分配的位置
            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='business',  # 自己创建的数据库名称
                                 charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "SELECT * FROM 业务信息 "
            # print(sql)
            db.ping(reconnect=True)
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
            results = cursor.fetchall()
            db.close()
            pos1 = []
            # print(results)
            # 得到位置信息
            if results != ():
                for i in range(len(results)):
                    if results[i][1] == '移库':
                        #print(results[i][5])
                        px, py = self.divide_pos(results[i][5])
                        pos1.append(px)
                        pos1.append(py)
                    else:
                        pos1.append(results[i][5])
            while True:
                p1 = random.randint(1, 9);
                p2 = random.randint(1, 9);
                p3 = random.randint(1, 9)
                p = str(p1) + '-' + str(p2) + '-' + str(p3)
                ii = 0
                for i in enumerate(pos):
                    if i[1] == p:
                        pass
                    else:
                        ii += 1
                for i in enumerate(pos1):
                    if i[1] == p:
                        pass
                    else:
                        ii += 1
                if ii == (len(pos) + len(pos1)):
                    #print(ii, len(pos), len(pos1))
                    break
            self.var_position = self.var_position+'>'+p # 要移动到的下一个位置，入库位置
        #增加业务编码，确保业务不会在自我查询当中重复#所有的位置唯一确定，防止出现位置占用
        #print( self.business_ID,self.var_business,self.var_Id,self.var_name,self.var_type,
        #       self.var_position,self.var_number,self.var_danwei,
        #       self.var_price,self.var_supplyer)
        #插入数据库中
        if self.business_ID==0:
            pass
        else:
            db = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                 db='business',  # 自己创建的数据库名称
                                 charset='utf8')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "INSERT INTO 业务信息(业务编码,业务情况,代码,名称,类型,位置," \
                  "总量,单位,单价,供应商)  VALUES ('%s', '%s', '%s','%s','%s','%s', '%s','%s','%s','%s')" % (
                      self.business_ID,self.var_business, self.var_Id, self.var_name, self.var_type,
                      self.var_position,self.var_number, self.var_danwei,
                      self.var_price, self.var_supplyer)  # SQL 插入语句
            #print(sql)
            db.ping(reconnect=True)
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
            db.close()
            content=str(self.business_ID)+'|'+self.var_business+ '|'+self.var_Id+'|'+self.var_name+'|'+self.var_type+\
                      '|'+self.var_position+'|'+str(self.var_number)+'|'+self.var_danwei+\
                      '|'+str(self.var_price)+'|'+self.var_supplyer
            #print(content)
            save_path='D:\\Desk\\管理信息系统\\WBS\\'+str(self.business_ID)+'.jpg'
            self.make_QR_code(content,save_path)
        self.information()#显示

    def make_QR_code(self,content, save_path=None):
        qr_code_maker = qrcode.QRCode(version=5,
                                      error_correction=qrcode.constants.ERROR_CORRECT_M,
                                      box_size=8,
                                      border=4,
                                      )
        qr_code_maker.add_data(data=content)
        qr_code_maker.make(fit=True)
        img = qr_code_maker.make_image(fill_color="black", back_color="white")
        if save_path:
            img.save(save_path)

    def exuct(self):
        global CHECKPOINT
        if CHECKPOINT==[]:
            messagebox.showinfo('提示！', '未选中任何信息！')
        else:
            ttk.Button(text='查询', width=10, command=self.new_information).place(x=150, y=80)
            for enu in CHECKPOINT:
                db = pymysql.connect(host='localhost',
                                     port=3306,
                                     user='root',
                                     passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                     db='business',  # 自己创建的数据库名称
                                     charset='utf8')
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                sql = "SELECT * FROM 业务信息 where 业务编码='%s'" % (enu)
                # print(sql)
                db.ping(reconnect=True)
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                results = cursor.fetchall()
                db.close()
                if results!=():
                    self.var_business=results[0][1]
                    # 得到ID信息
                    if self.var_business =='入库':
                        self.in_goods(results=results)
                    elif self.var_business =='出库':
                        self.out_goods(results=results)
                    elif self.var_business== '移库':
                        self.move_goods(results=results)

                    save_path = 'D:\\Desk\\管理信息系统\\WBS\\' + str(enu) + '.jpg'#删除二维码
                    try:
                        os.remove(save_path)
                    except:
                        pass
                if results==():
                    messagebox.showinfo('提示！', '该二维码已经过期，请核对！')
            self.business_ID=1
            try:
                self.a.destroy()
            except:
                pass
        CHECKPOINT=[]

    def in_goods(self,results):
        self.var_rukuid=1
        self.business_ID = results[0][0];
        self.var_business = results[0][1];
        self.var_Id = results[0][2];
        self.var_name = results[0][3];
        self.var_type = results[0][4];
        self.var_position = results[0][5];
        self.var_number = results[0][6];
        self.var_danwei = results[0][7];
        self.var_price = results[0][8];
        self.var_supplyer = results[0][9];
        #入库单号安排
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                             db='goods',  # 自己创建的数据库名称
                             charset='utf8')
        sql = "SELECT * FROM 入库单 "
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        db.close()
        if results!=():
            self.var_rukuid=int(results[len(results)-1][0])+1
        timeStr = time.strftime('%Y.%m.%d %H:%M:%S')
        self.var_time = timeStr
        # 防止输错代码与名称
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                             db='goods',  # 自己创建的数据库名称
                             charset='utf8')
        sql = "SELECT * FROM 链接表 WHERE 货物代码 = '%s'" % (self.var_Id)
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        db.close()
        #print(results)
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
            sql = "SELECT * FROM 入库单 WHERE 入库单编号 = '%s'" % (self.var_rukuid)
            cursor = db.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            db.close()
            # print(results)
            if results != ():
                if results[0][0] == self.var_rukuid:
                    messagebox.showinfo('提示！', '已经存在该入库单编号，请核对！')
            else:

                db = pymysql.connect(host='localhost',
                                     port=3306,
                                     user='root',
                                     passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                     db='goods',  # 自己创建的数据库名称
                                     charset='utf8')
                sql = "SELECT * FROM 仓库 WHERE 存放库位 = '%s'" % (self.var_position)
                cursor = db.cursor()
                cursor.execute(sql)
                results = cursor.fetchall()
                #print(results)
                if results != ():
                    if self.var_Id!= results[0][0]:
                        messagebox.showinfo('提示！', '该位置已存在其他货物，请核对！')
                    else:

                        sql = "INSERT INTO 入库单(入库单编号,货物代码,货物名称,货物类型,存放库位,入库总量,计量单位,入库单价,入库时间,供应商,经办人)  VALUES ('%s', '%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s')" % (
                            self.var_rukuid, self.var_Id, self.var_name, self.var_type,
                            self.var_position, self.var_number, self.var_danwei, self.var_price,
                            self.var_time, self.var_supplyer, self.ID)  # SQL 插入语句
                        cursor = db.cursor()  # 使用cursor()方法获取操作游标

                        try:
                            try:
                                db.ping(reconnect=True)
                                #print("c")
                            except:
                                pass
                                #print('n')
                            cursor.execute(sql)
                            db.commit()
                            messagebox.showinfo('提示！', '入库成功！')

                        except:
                            db.rollback()
                            # exit()
                            print('error')
                        # db.ping(reconnect=True)
                else:
                    sql = "INSERT INTO 入库单(入库单编号,货物代码,货物名称,货物类型,存放库位,入库总量,计量单位,入库单价,入库时间,供应商,经办人)  VALUES ('%s', '%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s')" % (
                        self.var_rukuid, self.var_Id, self.var_name, self.var_type,
                        self.var_position, self.var_number, self.var_danwei, self.var_price,
                        self.var_time, self.var_supplyer, self.ID)  # SQL 插入语句
                    cursor = db.cursor()  # 使用cursor()方法获取操作游标

                    try:
                        try:
                            db.ping(reconnect=True)
                            #print("c")
                        except:
                            pass
                            #print('n')
                        cursor.execute(sql)
                        db.commit()
                        messagebox.showinfo('提示！', '入库成功！')

                    except:
                        db.rollback()
                        # exit()
                        print('error')
                    # db.ping(reconnect=True)
                db.close()
        self.remove_ID(id=self.business_ID)
    def out_goods(self,results):
        self.var_outid = 1
        self.business_ID = results[0][0];
        self.var_business = results[0][1];
        self.var_Id = results[0][2];
        self.var_name = results[0][3];
        self.var_type = results[0][4];
        self.var_position = results[0][5];
        self.var_number = results[0][6];
        self.var_danwei = results[0][7];
        self.var_price = results[0][8];
        self.var_supplyer = results[0][9];
        # 入库单号安排
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                             db='goods',  # 自己创建的数据库名称
                             charset='utf8')
        sql = "SELECT * FROM 出库单 "
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        #>>>print(results)
        db.close()
        if results != ():
            self.var_outid = int(results[len(results) - 1][0]) + 1

        timeStr = time.strftime('%Y.%m.%d %H:%M:%S')
        self.var_time = timeStr

        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                             db='goods',  # 自己创建的数据库名称
                             charset='utf8')
        sql = "SELECT * FROM 链接表 WHERE 货物代码 = '%s'" % (self.var_Id)
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        db.close()
        #>>>>print(results)
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
            sql = "SELECT * FROM 出库单 WHERE 出库单编号 = '%s'" % (self.var_outid)
            cursor = db.cursor()
            cursor.execute(sql)

            db.commit()
            results = cursor.fetchall()
            #print(results)
            db.close()  # 关闭数据库连接
            if results != ():
                if results[0][0] == self.var_outid:
                    messagebox.showinfo('提示！', '已经存在该出库单编号，请核对！')
            else:
                # 查找是不是数量不对
                db = pymysql.connect(host='localhost',
                                     port=3306,
                                     user='root',
                                     passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                     db='goods',  # 自己创建的数据库名称
                                     charset='utf8')
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                sql = "SELECT * FROM 仓库 WHERE 货物代码 = '%s' and 货物名称='%s' " \
                      "and 货物类型='%s' and 存放库位='%s'  and 计量单位='%s' and 供应商='%s' " % (
                    self.var_Id, self.var_name, self.var_type, self.var_position, self.var_danwei,
                    self.var_supplyer)
                #print(sql)
                try:
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()
                    results = cursor.fetchall()
                    #>>>>print(results)
                except:
                    db.rollback()
                    messagebox.showinfo('提示！', '请填写正确出库信息，不存在该货物！')
                # print(results)
                db.close()
                data = ()#进不来
                if results != ():
                    data = ((
                            self.var_Id, self.var_name, self.var_type, self.var_position, results[0][4],
                            self.var_danwei, self.var_supplyer),)
                    #print(data)
                    #print(data,results)
                    if data == results:
                        if int(self.var_number) - int(results[0][4]) > 0:
                            messagebox.showinfo('提示！', '库存数量为' + results[0][4] + ',出库数量大于库存数量！')
                        else:

                            # 进行减法操作
                            db = pymysql.connect(host='localhost',
                                                 port=3306,
                                                 user='root',
                                                 passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                                 db='goods',  # 自己创建的数据库名称
                                                 charset='utf8')
                            sql = "INSERT INTO 出库单(出库单编号,货物代码,货物名称,货物类型,存放库位,出库总量,计量单位,出库单价,出库时间,供应商,经办人)  VALUES ('%s', '%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s')" % (
                                self.var_outid, self.var_Id, self.var_name, self.var_type,
                                self.var_position, self.var_number, self.var_danwei,
                                self.var_price, self.var_time, self.var_supplyer, self.ID)  # SQL 插入语句
                            # print(sql)
                            cursor = db.cursor()  # 使用cursor()方法获取操作游标

                            try:
                                try:
                                    db.ping(reconnect=True)
                                    # print("done")
                                except:
                                    print('wrong')
                                cursor.execute(sql)
                                db.commit()
                                messagebox.showinfo('提示！', '出库成功！')

                            except:
                                db.rollback()
                                # exit()
                                print('error')
                            # db.ping(reconnect=True)

                            db.close()  # 关闭数据库连接
                            # 如果库存数量为0 则删除库存记录
                            #print(self.var_number)
                            #print(results[0][4])
                            if int(self.var_number) - int(results[0][4]) == 0:
                                db = pymysql.connect(host='localhost',
                                                     port=3306,
                                                     user='root',
                                                     passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                                     db='goods',  # 自己创建的数据库名称
                                                     charset='utf8')
                                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                                sql = "DELETE  FROM 仓库 WHERE 仓库.货物代码 = '%s' and 仓库.货物名称='%s' and 仓库.货物类型='%s' and 仓库.存放库位='%s' and 仓库.库存总量='0' and 仓库.计量单位='%s' and 仓库.供应商='%s' " % (
                                    self.var_Id, self.var_name, self.var_type, self.var_position,
                                    self.var_danwei, self.var_supplyer)
                                # sql = "DELETE  FROM 仓库 LIMIT 库存总量='0'"

                                #print(sql)
                                cursor.execute(sql)
                                db.commit()  # 执行sql语句
                                db.close()
                else:
                    messagebox.showinfo('提示！', '请填写正确出库信息，不存在该货物！')
        self.remove_ID(self.business_ID)
    def move_goods(self,results):
        self.business_ID = results[0][0];
        self.var_business = results[0][1];
        self.var_Id = results[0][2];
        self.var_name = results[0][3];
        self.var_type = results[0][4];
        self.var_position , self.var_new = self.divide_pos(pos=results[0][5])
        #print(self.var_position , self.var_new)
        self.var_number = results[0][6];
        self.var_danwei = results[0][7];
        self.var_price = results[0][8];
        self.var_supplyer = results[0][9];

        db = pymysql.connect(host='localhost',
                                     port=3306,
                                     user='root',
                                     passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                                     db='goods',  # 自己创建的数据库名称
                                     charset='utf8')
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM 仓库 WHERE 存放库位 = '%s'" % (self.var_position)
        #print(sql)
        db.ping(reconnect=True)
        cursor.execute(sql)  # 执行sql语句
        db.commit()  # 提交到数据库执行
        results = cursor.fetchall()
        db.close()
        #print(results)
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
            sql = "SELECT * FROM 仓库 WHERE 存放库位 = '%s'" % (self.var_new)
            # print(sql)
            db.ping(reconnect=True)
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
            results = cursor.fetchall()
            db.close()
            #print(results)
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
                        "where 仓库.存放库位='%s' " % (self.var_new,self.var_position)
                # print(sql)
                db.ping(reconnect=True)
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                db.close()
                messagebox.showinfo('提示！', '移库成功')
        self.remove_ID(id=self.business_ID)
    def remove_ID(self,id):
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='1753975smaugfire',  # 这个是自己MySQL数据库密码
                             db='business',  # 自己创建的数据库名称
                             charset='utf8')
        sql = "DELETE  FROM 业务信息 where 业务信息.业务编码 ='%s'" % (id)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        results = cursor.fetchall()
        db.close()
    def divide_pos(self,pos):
        for i in range(len(pos)):
            if pos[i]=='>':
                return pos[:i],pos[i+1:]

    def decode(self, image):
        global QR_INF,CHECKPOINT
        QR_INF = ''
        barcodes = pyzbar.decode(image)
        for barcode in barcodes:
            # 提取二维码的边界框的位置
            # 画出图像中条形码的边界框
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (225, 225, 225), 2)

            # 提取二维码数据为字节对象，所以如果我们想在输出图像上
            # 画出来，就需要先将它转换成字符串
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            QR_INF = barcodeData
            # 绘出图像上条形码的数据和条形码类型
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        .5, (225, 225, 225), 2)
            # 向终端打印条形码数据和条形码类型
            #print(QR_INF)#将QR值赋予全局变量当中
            x=''
            for i in enumerate(QR_INF):
                if i[1]=='|':
                    break
                x = x + i[1]
            CHECKPOINT.append(int(x))
            #print(CHECKPOINT)
            #然后删除文件
            #messagebox.showinfo('提示！', QR_INF)
        return image

    def QR_read(self):
        try:
            self.a.destroy()
        except:
            pass
        global QR_INF,CHECKPOINT
        camera = cv2.VideoCapture(0)


        while True:
            # 读取当前帧
            ret, frame = camera.read()
            # 转为灰度图像
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            im = self.decode(gray)

            cv2.waitKey(5)
            cv2.imshow('camera', im)
            # 如果按键q则跳出本次循环
            if QR_INF != '':
                #写进数据库
                self.exuct()
                QR_INF=''
                break
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            if cv2.getWindowProperty("camera", cv2.WND_PROP_AUTOSIZE) < 1:
                break
            # 提示一个文本框就可以了
        camera.release()
        cv2.destroyAllWindows()





if __name__ == '__main__':
    #root = Tk()
    SEEBusiness(None, ID=0)
    #root.mainloop()