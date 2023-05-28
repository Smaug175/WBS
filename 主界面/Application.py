import pymysql.cursors
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
import tkinter.messagebox as messagebox
import time

from 主界面.mainpage import StartPage
from 入库操作.input_goods import InPut
from 个人信息.information_person import InforPerson
from 查询模块.ser_mainpage import SerMainPage
from 查询模块.ser_goods import SerGoods
from 查询模块.ser_in import SerIn
from 查询模块.ser_out import SerOut
from 出库操作.out import Out
from 移库操作.move import Move
from 链接管理.mpage import SerM_Page
from 链接管理.change import Change
from 链接管理.new import New
from 链接管理.ser import Ser
from 链接管理.dele import Dele
from 业务查看.see import SEEBusiness

class Application(StartPage, InPut,Out, InforPerson, SerMainPage,SerGoods,SerIn,SerOut,Move,SerM_Page,
                  Change,New,Dele,Ser,SEEBusiness):

    def __init__(self,primate_window,ID):
        primate_window.destroy()
        self.root = tk.Tk()
        self.ID = ID
        self.goMainPage()

    def goMainPage(self):
        self.root.destroy()
        StartPage.__init__(self, goInPut=self.goInPut,goOut=self.goOut,goInfPer=self.goInfPer,
                           goInfSer_APP=self.goInfSerMain,goMove=self.goMove,goSerM_Page=self.goSerM_Page,
                           ID=self.ID,goSee=self.goSee)

    def goInPut(self):
        self.root.destroy()
        InPut.__init__(self, goMainPage=self.goMainPage,ID=self.ID)

    def goOut(self):
        self.root.destroy()
        Out.__init__(self, goMainPage=self.goMainPage,ID=self.ID)

    def goMove(self):
        self.root.destroy()
        Move.__init__(self, goMainPage =self.goMainPage,ID=self.ID)

    def goInfPer(self):
        self.root.destroy()
        InforPerson.__init__(self, goMainPage=self.goMainPage,ID=self.ID)

    def goInfSerMain(self):
        self.root.destroy()
        SerMainPage.__init__(self,goMainPage=self.goMainPage,goSerGoods=self.goSerGoods,
                             goSerIn=self.goSerIn,goSerOut=self.goSerOut,ID=self.ID)

    def goSerGoods(self):
        self.root.destroy()
        SerGoods.__init__(self, goInfSerMain=self.goInfSerMain, ID=self.ID)

    def goSerIn(self):
        self.root.destroy()
        SerIn.__init__(self, goInfSerMain=self.goInfSerMain, ID=self.ID)

    def goSerOut(self):
        self.root.destroy()
        SerOut.__init__(self, goInfSerMain=self.goInfSerMain, ID=self.ID)

    def goSerM_Page(self):
        self.root.destroy()
        SerM_Page.__init__(self,goMainPage=self.goMainPage,goChange=self.goChange,
                             goNew=self.goNew,goSer=self.goSer,goDele=self.goDele,ID=self.ID)

    def goNew(self):
        self.root.destroy()
        New.__init__(self, goM_Page=self.goSerM_Page, ID=self.ID)

    def goSer(self):
        self.root.destroy()
        Ser.__init__(self, goM_Page=self.goSerM_Page, ID=self.ID)

    def goChange(self):
        self.root.destroy()
        Change.__init__(self, goM_Page=self.goSerM_Page, ID=self.ID)


    def goDele(self):
        self.root.destroy()
        Dele.__init__(self, goM_Page=self.goSerM_Page, ID=self.ID)

    def goSee(self):
        self.root.destroy()
        SEEBusiness.__init__(self, goMainPage=self.goMainPage,ID=self.ID)


if __name__ == '__main__':
    Application()