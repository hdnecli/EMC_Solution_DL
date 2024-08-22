import sys
sys.path.append('\Lib\site-packages')
import cv2
##import tkinter
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import matplotlib.pyplot as plot
'exec(%matplotlib inline)'
import tabula
from tabula.io import read_pdf
import math
import time
import shelve
from classes.Graphs import *
from classes.components.MainboardGui import MainboardGui as mbGui
from classes.components.PsuGui import PsuGui as psuGui
from classes.components.UrsaGui import UrsaGui as ursaGui
from classes.components.PanelGui import PanelGui as panelGui
from classes.components.TconGui import TconGui as tconGui
from classes.components.TVconfigGui import TVconfigGui as tvGui
from classes.components.LogGui import LogGui as logGui
from classes.db.LearnDatabase import LearnDatabase as learnDb

from classes.settings import Settings as st
import tensorflow as tf
from pdf2image import convert_from_path
from pdf2image import convert_from_bytes

from tkinter import *
import tkinter as tk
import tkinter.filedialog
from tkinter.messagebox import showinfo


import sklearn
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

from pathlib import Path
from PIL import ImageTk, Image

maxNum = 1e+12
__poppler_path = r'D:/Users/26015017/OneDrive - ARÇELİK A.Ş/Desktop/DeepLearnEMC/poppler-0.68.0\bin'
st.init()  # set global variables

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        self.title("Welcome to EMC Deep Learning Application")
        self.geometry('1000x500')
        self.pdf_File = None
        self.bind("<Configure>", self.on_resize)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(row=0, column=0, sticky="nsew")

    def on_resize(self, event=None):
        #self._frame.on_resize()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Ne işlem yapılacak?").grid(row=0,column=0)
        tk.Button(self, text="Öğret",
                          command=lambda: master.switch_frame(PageOne)).grid(row=1,column=0)
        tk.Button(self, text="Öğren",
                          command=lambda: master.switch_frame(PageTwo)).grid(row=2,column=0)
        tk.Button(self, text="Tanımla",
                          command=lambda: master.switch_frame(PageThree)).grid(row=3,column=0)

    def on_resize(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        root = master
        tk.Label(self, text="Önce ilk ürün test sonucunu sonra modiflileri yükleyin. bu yazı 6 col boyunca görülmeli").grid(row=0,column=0,columnspan = 9)
        tk.Button(self, text="Ana Sayfaya Dön",
                  command=lambda: master.switch_frame(StartPage)).grid(row=1,column=0)

        '''
        tk.Label(self, text="XLS").grid(row = 3, column = 1)
        xlsButton = tk.Button(self, text="Dosya Sec",
                  command=lambda: self.xlsUpload())
        xlsButton.grid(row=4,column=1)
        self.xlsButton = xlsButton
        self.xlsUC = False  # xls Uploaded correctly / parameters entered correctly?
        '''
        tk.Label(self, text="PDF").grid(row = 2, column = 0)
        pdfButton = tk.Button(self, text="Dosya Sec",
                  command=lambda: self.pdfUpload())
        pdfButton.grid(row=3,column=0)
        self.pdfButton = pdfButton
        self.xlsCh = False
        self.pdfCh = False

        buttonYukle = tk.Button(self, text="Shelve Yükle", command=self.yukle)
        buttonYukle.grid(row=3,column=1)

        buttonYukleParquet = tk.Button(self, text="Parquet Yükle ", command=self.yukleParquet)
        buttonYukleParquet.grid(row=3,column=3)
        
        tvFr = tk.Frame(self, width=850, height= 500, highlightbackground="red", highlightcolor="red", highlightthickness=1)
        tvFr.grid(row = 4, column = 0, columnspan = 4, sticky='nsew')

        emiDelButton = tk.Button(self, text="EMI Tape Sil",
                  command=lambda: self.emiTapeSil())
        #Log a silmekle ilgili komutları açıkla
        emiDelButton.grid(row=4,column=4)
        emiDelButton['state'] = 'disabled'
        self.emiDelButton = emiDelButton

        emiAddButton = tk.Button(self, text="EMI Tape Ekle",
                  command=lambda: self.emiTapeEkle())
        #Log a eklemekle ilgili komutları açıkla
        emiAddButton.grid(row=4,column=5)
        emiAddButton['state'] = 'disabled'
        self.emiAddButton = emiAddButton

        self.update()

        self.tv = tvGui(tvFr, root)

        tvConfigPath = 'mem\\tvcDb'
        with shelve.open(tvConfigPath, writeback=True) as tvcDb:
            tvcCodes = tvcDb['tvConfigCode']
        tvcDb.close()

        self.tvc = tk.StringVar(self)
        self.tvc.set("Chose") # default value

        tk.Label(self, text="TV configs").grid(row=2,column=2,sticky=W)

        self.pnlClk = False

        tk.OptionMenu(self, self.tvc, *tvcCodes).grid(row=3,column=2,sticky=W)
        tk.Button(self, text="Select",
                  command=lambda: [self.setTVCButtons(), self.tv.showTVC(self.tvc.get())]).grid(row=3,column=2,sticky=W)

        logFr = tk.Frame(self, height= 100, highlightbackground="green", highlightcolor="black", highlightthickness=1)
        logFr.grid(row = 5, column = 0, columnspan = 4, sticky='nsew')

        self.logger = logGui(logFr)
        self.tv.loggerObj = self.logger

        self.update()

    def pdfUpload(self):
        if(self.pdfButton["text"] != "Dosya Sec"):
            print("Dosya'yı bir daha seciyorsunuz")
        self.pdf_File = tk.filedialog.askopenfilename(initialdir = "/Users/26015017/Desktop/",title ="Dosya Seçin",filetypes = [("pdf files","*.pdf")])
        pdf_file_divs = [x.strip() for x in self.pdf_File.split('/')]
        pdf_file_name = pdf_file_divs[-1]
        self.pdfButton.config(text=pdf_file_name)
        self.pdf_file_name = pdf_file_name
        self.nameOutput = self.pdf_File.split("/")[-1].split()[0]
        if pdf_file_name == '':
            self.pdfCh = False
        else:
            self.pdfCh = True

    def yukle(self):
        if (self.pdfCh and self.tv.showTVC_called):
            pdf2PNG = convert_from_path(self.pdf_File, 500, poppler_path = r'poppler-0.68.0\bin')
            tabula.convert_into(self.pdf_File, "images//ex2.csv", output_format="csv", pages='all')
            #tabula.convert_into(self.pdf_File, "images/ex2.csv", output_format="csv", pages='all', encoding="utf-8")
            pdf2PNG[0].save('images/temp/ex2.png', 'PNG')
            img = cv2.imread('images/temp/ex2.png')
            graph1 = BasicGraph(1, img)
            ldb = learnDb()
            ldb = learnDb()
            ldb.add(self.tv.tvcName, graph1)

        else:
            showinfo("Hata!!!", "Bütün seçimler yapılmalı")

    def yukleParquet(self): 
        if (self.pdfCh and self.tv.showTVC_called):
            pdf2PNG = convert_from_path(self.pdf_File, 500, poppler_path = r'poppler-0.68.0\bin')
            tabula.convert_into(self.pdf_File, "images//ex2.csv", output_format="csv", pages='all')
            pdf2PNG[0].save('images/temp/ex2.png', 'PNG')
            img = cv2.imread('images/temp/ex2.png')
            graph1 = BasicGraph(1, img) 
            test_name = self.nameOutput  
            ldb = learnDb()
            ldb = learnDb()
            ldb.addParquet(self.tv.tvcName, graph1, test_name = test_name)   
        else:
            showinfo("Hata!!!", "Bütün seçimler yapılmalı") 

    def emiTapeSil(self):
        if self.tv.showTVC_called:  ## if show TVC is called only then operate
            if self.emiDelButton['bg'] != 'green':
                self.logger.addTxtDown("silmek istediğin EMI Tapenin üzerine bir kere tıkla")
                self.resetButtons()
                self.shutOffAllModes()
                self.emiDelButton['bg'] = 'green'
                self.tv.emiDelMode = True
            else:
                self.resetButtons()
                self.shutOffAllModes()
                self.emiDelButton['bg'] = 'red'
                self.tv.emiDelMode = False
            print("showTVC_called!")

    def emiTapeEkle(self):
        if self.tv.showTVC_called:
            if self.emiAddButton['bg'] != 'green':
                self.logger.addTxtDown("EMI Tape eklemek için ekrana bir kez tıkla, yerleştirmek istediğin bölgeye gelince ikinci kez tıkladığında EMI Tape yerleşmiş olacak")
                self.resetButtons()
                self.shutOffAllModes()
                self.emiAddButton['bg'] = 'green'
                self.tv.emtMode = True
                self.tv.emiAddMode = True
            else:
                self.shutOffAllModes()
                self.resetButtons()
                self.emiAddButton['bg'] = 'red'
                self.tv.emiAddMode = False
            print("showTVC_called!")

    def resetButtons(self):
        if self.tv.showTVC_called:
            self.emiDelButton['bg'] = 'red'
            self.emiAddButton['bg'] = 'red'
            self.tv.emiAddMode = False
            self.tv.emiDelMode = False

    def setTVCButtons(self):
        self.emiDelButton['state'] = 'normal'
        self.emiAddButton['state'] = 'normal'
        self.update()

    def shutOffAllModes(self):
        self.tv.cableMode = False
        self.tv.detCnOn = False
        self.tv.emtMode = False
        self.tv.ferMode = False

    def on_resize(self):
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page two").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
 
    def on_resize(self):
        pass

class PageThree(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page three").grid(row=1,column=1)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).grid(row=2,column=1)


        tk.Button(self, text="Mainboard",
                  command=lambda: mbGui()).grid(row=3,column=1)

        tk.Button(self, text="PSU",
                  command=lambda: psuGui()).grid(row=4,column=1)

        tk.Button(self, text="Ursa",
                  command=lambda: ursaGui()).grid(row=5,column=1)

        tk.Button(self, text="Panel",
                  command=lambda: panelGui()).grid(row=6,column=1)

        tk.Button(self, text="Tcon",
                  command=lambda: tconGui()).grid(row=7,column=1)

        tk.Button(self, text="TV config",
                  command=lambda: master.switch_frame(TVconfigPage)).grid(row=8,column=1)


    def on_resize(self):
        pass

class TVconfigPage(tk.Frame):

    def __init__(self, master):
        root = master
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is Tv config page").grid(row=1, sticky=W, column=1, columnspan = 3)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).grid(row=2, sticky=W, column=1, columnspan = 3)
        tk.Button(self, text="Return",
                  command=lambda: master.switch_frame(PageThree)).grid(row=3, sticky=W, column=1, columnspan = 3)

        tvFr = tk.Frame(self, width=850, height= 500, highlightbackground="red", highlightcolor="red", highlightthickness=1)
        tvFr.grid(row = 1, column = 4, rowspan = 10, sticky='nsew')
        self.update()
        print("w: ",tvFr.winfo_width())
        print("h: ",tvFr.winfo_height())

        # self.tv = tvGui(tvFr)
        self.tv = tvGui(tvFr, root)

        variable = tk.StringVar(self)
        variable.set("Chose") # default value

        lists = ['a','b','c']

        pnlPath = 'mem\panelDb'
        with shelve.open(pnlPath, writeback=True) as pnlDb:
            pnlCodes = pnlDb['kabin_code']
            cell_codes = pnlDb['panel_code']
            vendor_codes = pnlDb['panel_vendor']
        pnlDb.close()

        self.panel = tk.StringVar(self)
        self.panel.set("Chose") # default value
        self.cell = tk.StringVar(self)
        self.cell.set("Chose") # default value

        tk.Label(self, text="Panels").grid(row=4,column=1,sticky=W)

        self.pnlClk = False

        tk.OptionMenu(self, self.panel, *pnlCodes).grid(row=4,column=2,sticky=W)
        tk.Button(self, text="Put",
                  command=lambda: self.tv.addPanel(self.panel.get(), self.cell.get())).grid(row=4,column=3,sticky=W)

        tk.Label(self, text="Cells").grid(row=5,column=1,sticky=W)
        self.cellClk = False
        tk.OptionMenu(self, self.cell, *cell_codes).grid(row=5,column=2,sticky=W)

##tvGui.addPanel(panel.get())

        mbPath = 'mem\mbDb'
        with shelve.open(mbPath, writeback=True) as mbDb:
            mbCodes = mbDb['code']
        mbDb.close()

        self.mb = tk.StringVar(self)
        self.mb.set("Chose") # default value

        tk.Label(self, text="Mainboards").grid(row=6,column=1,sticky=W)
        tk.OptionMenu(self, self.mb, *mbCodes).grid(row=6, column=2)
        tk.Button(self, text="Put",
                  command=lambda: self.tv.addMB(self.mb.get())).grid(row=6,column=3,sticky=W)


        psuPath = 'mem\psuDb'
        with shelve.open(psuPath, writeback=True) as psuDb:
            psuCodes = psuDb['code']
        psuDb.close()

        psu = tk.StringVar(self)
        psu.set("Chose") # default value

        tk.Label(self, text="PSUs").grid(row=7,column=1,sticky=W)
        tk.OptionMenu(self, psu, *psuCodes).grid(row=7, column=2)
        tk.Button(self, text="Put",
                  command=lambda: self.tv.addPSU(psu.get())).grid(row=7,column=3,sticky=W)


        ursaPath = 'mem\\ursaDb'
        with shelve.open(ursaPath, writeback=True) as ursaDb:
            ursaCodes = ursaDb['code']
        ursaDb.close()

        ursa = tk.StringVar(self)
        ursa.set("Chose") # default value

        tk.Label(self, text="Ursas").grid(row=8,column=1,sticky=W)
        tk.OptionMenu(self, ursa, *ursaCodes).grid(row=8, column=2)
        tk.Button(self, text="Put",
                  command=lambda: self.tv.addUrsa(ursa.get())).grid(row=8,column=3,sticky=W)


        wlan = tk.StringVar(self)
        wlan.set("Chose") # default value
        wlan_modules = st.wlan_modules

        tk.Label(self, text="WLANs").grid(row=9,column=1,sticky=W)
        tk.OptionMenu(self, wlan, *wlan_modules).grid(row=9, column=2)
        tk.Button(self, text="Put",
                  command=lambda: self.tv.addWlan(wlan.get())).grid(row=9,column=3,sticky=W)

        conns = st.conList

        cable = tk.StringVar(self)
        cable.set("Chose") # default value

        # tk.Label(self, text="Cables").grid(row=9,column=1,sticky=W)
##        tk.OptionMenu(self, cable, *conns).grid(row=9, column=2)
##        self.cableBtn = tk.Button(self, text="Do Cables", bg='red', command=lambda: tv.addCable())
        self.emitapeBtn = tk.Button(self, text="Do EMI tapes", bg='red', command=lambda: self.emtClc())
        self.emitapeBtn.grid(row=10,column=1,sticky=W)

        self.emtMode = False

        self.ferBtn = tk.Button(self, text="Do Ferrits", bg='red', command=lambda: self.ferClc())
        self.ferBtn.grid(row=10,column=2,sticky=W)

        self.ferMode = False

        self.cableBtn = tk.Button(self, text="Do Cables", bg='red', command=lambda: self.cabClc())
        self.cableBtn.grid(row=10,column=3,sticky=W)

        delDict = {
            "panel" : pnlPath,
            "mainboard" : mbPath,
            "ursa" : ursaPath,
            "psu" : psuPath
        }
        self.delDict = delDict
        # print("delDict.keys(): ", delDict.keys())
        delList = list(delDict.keys())
        # print("dict KEys: ", delList)
        tmpLst = []
        for i in delList:
            # print(i)
            tmpLst.append(i)
            i = str(i)
            # print(i)
        # print("tmpLst: ", tmpLst)
        delObj = tk.StringVar(self)
        delObj.set("Chose to Delete")

        self.delItem = tk.StringVar(self)
        self.delItem.set("Chose") # default value

        self.selPath = None
        self.tempList = ['Test']

        # firstObj = Menu(self, 'tempList', delObj, *delList)
        tk.Label(self, text = "Category").grid(row=11, column=1, sticky=N)
        firstObj = Menu(self, 'tempList', 'Choose', *delList)
        firstObj.grid(row=11, column=1, sticky=S)


        # self.secObj = tk.OptionMenu(self, self.delItem, self.tempList, status = 'hidden')
        tk.Label(self, text = "Item").grid(row=11, column=2, sticky=N)
        self.secObj = tk.OptionMenu(self, self.delItem, *self.tempList)
        self.secObj.grid(row=11, column=2, sticky=S)

        tk.Button(self, text="Delete", bg='red', command=lambda: self.delSel(self.delItem.get())).grid(row=11, column=3)

        logFr = tk.Frame(self, width=800, height= 100, highlightbackground="green", highlightcolor="black", highlightthickness=1)
        logFr.grid(row = 12, column = 4, sticky='nsew')

        self.saveBtn = tk.Button(self, text="Save", bg='yellow', command=lambda: self.saveTvConfig())
        self.saveBtn.grid(row=12,column=1,sticky=NW)

        self.logger = logGui(logFr)
        self.tv.loggerObj = self.logger

        self.isCableAdded = False

    def emtClc(self):
        if self.emitapeBtn['bg'] == 'green':
            self.emitapeBtn['bg'] = 'red'
            self.tv.emtMode = False
        else:
            if self.tv.isMbAdded and not self.tv.isZoomed and self.isCableAdded:
                self.emitapeBtn['bg'] = 'green'
                self.ferBtn['bg'] = 'red'
                self.cableBtn['bg'] = 'red'
                self.tv.cableMode = False
                self.tv.detCnOn = False
                self.tv.emtMode = True
                self.tv.ferMode = False

    def saveTvConfig(self):
        self.tv.saveMaterials()

    def combine_funcs(*funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func

    def ferClc(self):
        if self.ferBtn['bg'] == 'green':
            self.ferBtn['bg'] = 'red'
            self.tv.ferMode = False
        else:
            if self.tv.isMbAdded and not self.tv.isZoomed and self.isCableAdded:
                self.ferBtn['bg'] = 'green'
                self.cableBtn['bg'] = 'red'
                self.emitapeBtn['bg'] = 'red'
                self.tv.cableMode = False
                self.tv.detCnOn = False
                self.tv.emtMode = False
                self.tv.ferMode = True

    def cabClc(self):
        if self.cableBtn['bg'] == 'green':
            self.cableBtn['bg'] = 'red'
            self.tv.cableMode = False
            self.tv.detCnOn = False
        else:
            if self.tv.isMbAdded and not self.tv.isZoomed:
                self.cableBtn['bg'] = 'green'
                self.ferBtn['bg'] = 'red'
                self.emitapeBtn['bg'] = 'red'
                if not self.isCableAdded:
                    self.tv.addCable()
                    self.isCableAdded = True
                self.tv.cableMode = True
                self.tv.detCnOn = True
                self.tv.emtMode = False
                self.tv.ferMode = False

    def update_option_menu(self):
        menu = self.secObj["menu"]
        menu.delete(0, "end")
        for string in self.tempList:
            menu.add_command(label=string,
                             command=lambda value=string: self.delItem.set(value))

    def test(self, arr):
        print("tested")
        print("tempList: ", arr)

    def delSel(self, code):
        if self.selPath is not None:
            # print("selPath: ", self.selPath)
            with shelve.open(self.selPath, writeback=True) as slDb:
                # print("dB before: ", slDb)
                i = slDb["code"].index(code)
                for key in slDb:
                    slDb[key].pop(i)
                # print("dB after: ", slDb)
            slDb.close()
            self.update_option_menu()

    def on_resize(self):
        pass

class Menu(OptionMenu):
    def __init__(self, master, attrname, status, *options):
    # def __init__(self, master, attrname, objName, status, *options):
        self.var = StringVar(master)
        self.var.set(status)
        self._master = master
        self._attrname = attrname
        # self._objName = objName
        OptionMenu.__init__(self, master, self.var, *options, command=self.option_handle)

    @property
    def value(self):
        return self._master.__getattribute__(self._attrname)
    @value.setter
    def value(self,newvalue):
        self._master.__setattr__(self._attrname,newvalue)
        self._master.update_option_menu()

    def option_handle(self, selected):
        print("selected: ", selected)
        # print("master.delDict[selected]: ", master.delDict[selected])
        self._master.selPath = self._master.delDict[selected]
        with shelve.open(self._master.delDict[selected], writeback=True) as slDb:
            print("slDb['code']: ", slDb['code'])
            slCodes = slDb['code']
            print("slCodes: ", slCodes)
        slDb.close()

        self.value = slCodes

    def on_resize(self):
        pass


if __name__ == "__main__":
    app = SampleApp()

    app.mainloop()

cv2.waitKey(0)
cv2.destroyAllWindows()