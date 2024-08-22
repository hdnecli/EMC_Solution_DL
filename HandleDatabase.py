import os
import sys
sys.path.insert(0, "..")
import tkinter as tk
from tkinter import *
import shelve
from classes.settings import Settings as st
from pathlib import Path
from IPython.display import display
import pandas as pd
import numpy as np
from tabulate import tabulate
from abc import ABC, ABCMeta, abstractmethod
import pyarrow as pa
import pyarrow.parquet as pq
import cv2
from classes.db import LearnDatabase as ldb


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        self.title("Welcome to Database Management Application")
        self.geometry('1000x500')

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Database'i seç").grid(row=1,column=1)
        pnlBt = tk.Button(self, text="Panel",
                          command=lambda: master.switch_frame(PnlPage)).grid()
        mbBt = tk.Button(self, text="MainBoard",
                          command=lambda: master.switch_frame(MbPage)).grid()
        psuBt = tk.Button(self, text="PSU",
                          command=lambda: master.switch_frame(PSUPage)).grid()
        ursaBt = tk.Button(self, text="Ursa",
                          command=lambda: master.switch_frame(UrsaPage)).grid()
        wifiBt = tk.Button(self, text="WiFi",
                          command=lambda: master.switch_frame(WifiPage)).grid()
        tvcBt = tk.Button(self, text="TV Config",
                          command=lambda: master.switch_frame(TVCPage)).grid()
        learnBt = tk.Button(self, text="Learn",
                          command=lambda: master.switch_frame(LearnPage)).grid()

#panel data bütün mü, bütün kolonlar ve satırlar tam mı
#göster (bütün data ilk 5 son 5 / satır / kolon / satır kolon / )
#preprocessingden sonra nasıl görünüyor
#büyüklük nedir
#olmayan veri yönetimi, mean mı koyacaz, none mu, 0 mı, infinite mi,
#kolonda anormal veri var mı?
#yedek alma metodu yaz

#All the commands that are needed for all sorts of computation and modifications
#Take mean or median or zero or Infinite ot None cells
#Get inside the Cell See the Data
#change the datatype; i.e: Change cartesian cordinate to 2D graph
#Modify the cell
#Shift data from index by XXX offset

class DBPage(tk.Frame, metaclass = ABCMeta):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self._db_path = None
        Fr = tk.Frame(self, width=850, height= 500, highlightbackground="red", highlightcolor="red", highlightthickness=1)
        Fr.grid(row = 3, column = 1, columnspan = 10, sticky='nsew')
        tk.Button(self, text="show first 10 S", command=lambda: self.showSome('f10')).grid(row=1,column=1,sticky=W)
        tk.Button(self, text="show last 10 S", command=lambda: self.showSome('l10')).grid(row=1,column=2,sticky=W)
        tk.Button(self, text="show last 10 P", command=lambda: self.showSomeParquet('l10')).grid(row=1,column=3,sticky=W)
        tk.Button(self, text="add None to Missings S", command=lambda: self.addNonetoMissings()).grid(row=1,column=4,sticky=W)
        tk.Button(self, text="add None to Missings P", command=lambda: self.addNonetoMissingsParquet()).grid(row=1,column=5,sticky=W)
        self.dbDelButton = tk.Button(self, text="Delete DB object", command=lambda: self.deleteDFrow())
        self.dbDelButton.grid(row=1,column=7)
        self.dbDelButton['bg'] = 'red'
        tk.Button(self, text="Ana Sayfaya Dön", command=lambda: master.switch_frame(StartPage)).grid(row=2,column=1)
        self.deleteMode = False
        self.rollerCount = 0
        self.pageItemCount = 20
        self.update()

    def deleteDFrow(self):
        if self.dbDelButton['bg'] != 'green':
            self.deleteMode = True
            self.dbDelButton['bg'] = 'green'
        elif self.dbDelButton['bg'] == 'green':
            self.deleteMode = False
            self.dbDelButton['bg'] = 'red'

    def deleteDFrowParquet(self):
        if self.pqDelButton['bg'] != 'green':
            self.deleteModepq = True
            self.pqDelButton['bg'] = 'green'
        elif self.pqDelButton['bg'] == 'green':
            self.deleteModepq = False
            self.pqDelButton['bg'] = 'red'
    
    def showSomeParquet(self, arg):
        table = pq.read_table('mem/data.parquet')
        df = table.to_pandas()
        for column in df.columns:
            print("column ", column, " length: ", len(df[column]))        
        self.df = df
        self.showData(df)

    def showSome(self, arg):
        with shelve.open(self._db_path) as db:
            lastInd = len(db[list(db.keys())[0]])
            if arg == 'f10':
                dict = {}
                for i in db.keys():
                    dict[i] = db[i][self.rollerCount*self.pageItemCount : self.rollerCount*self.pageItemCount+self.pageItemCount]
                    print("column ", i, " length: ", len(db[i]))
                df = pd.DataFrame(dict)
                self.df = df
                # print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
                self.showData(df)
            if arg == 'l10':
                dict = {}
                for i in db.keys():
                    #tempLst = db[i][lastInd - 10 : ]
                    tempLst = db[i]
                    if len(db[i]) < lastInd:
                        diff = lastInd - len(db[i])
                        for g in range(diff):
                            tempLst.append('SİKERSİKÖR')
                    # dict[i] = db[i][lastInd - 10 : ]
                    dict[i] = tempLst
                    print("column ", i, " length: ", len(db[i]))
                df = pd.DataFrame(dict)
                self.df = df
                # print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
                self.showData(df)
        db.close()
        
    def addNonetoMissings(self):
        with shelve.open(self._db_path, writeback=True) as db:
            maxCtr = len(db[list(db.keys())[0]])
            print("maxCtr: ", maxCtr)
            ch = 0
            for i in db.keys():
                if len(db[i]) > maxCtr:
                    maxCtr = len(db[i])
                    ch += 1
                if len(db[i]) < maxCtr:
                    ch += 1
            if ch > 0:
                for i in db.keys():
                    addNum = maxCtr - len(db[i])
                    for k in range(addNum):
                        db[i].append(None)
                        print(i, " added None")

        db.close()

    def addNonetoMissingsParquet(self):
        try:
            path_parquet = 'mem/data.parquet'
            df_parquet = pd.read_parquet(path_parquet)
            nan_count_before = (df_parquet == 'nan').sum().sum()
            df_parquet.replace('nan', None, inplace=True)
            print("Number of None values added:", nan_count_before)
            table = pa.Table.from_pandas(df_parquet)
            pq.write_table(table, path_parquet)
            print('Veritabanına kaydedildi.')
        except:
            print('bozuldu.')

    def scrollFunction(self, event):
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def showData(self, df):
        rootTbl = tk.Tk()

        root_frame=tk.Frame(rootTbl)
        root_frame.grid()

        self.canvas = Canvas(root_frame, height=600, width=850, borderwidth=0, background="#ffffff")
        self.canvas.grid(row = 1, column=1)

        df_frame = tk.Frame(self.canvas)
        key_frame = tk.Frame(self.canvas)
        commands_frame = tk.Frame(self.canvas)
        #df_frame.grid(row=2, column = 2)
        #key_frame.grid(row=2, column = 1)
        #commands_frame.grid(row=2, column = 3)

        v_scrollbar = Scrollbar(root_frame, orient = 'vertical', command = self.canvas.yview)
        v_scrollbar.grid(row=1, column = 2, sticky=N+S+W)
        self.canvas.configure(yscrollcommand = v_scrollbar.set)
        x_scrollbar = Scrollbar(root_frame, orient = 'horizontal', command = self.canvas.xview)
        x_scrollbar.grid(row=2, column = 1, sticky=W+E+N)
        self.canvas.configure(xscrollcommand = x_scrollbar.set)

        self.canvas.create_window((0,0),window=key_frame,anchor='nw')
        self.canvas.create_window((200,0),window=df_frame,anchor='nw')
        df_frame.bind("<Configure>",self.scrollFunction)
        key_frame.bind("<Configure>",self.scrollFunction)
        # tk.Button(commands_frame, text="geri").grid(row=2,column=3,sticky=W)
        # tk.Button(commands_frame, text="ileri").grid(row=2,column=4,sticky=W)
        # code for creating table
        for i in range(len(list(df.keys()))):
            self.e = tk.Label(key_frame, width=10, fg='blue', font=('Arial', 8, 'bold'), bd = 1, borderwidth=1, relief="groove")
            self.e.grid(row=i, column = 1)
            self.e['text'] = str(list(df.keys())[i])
            for j in range(len(df[list(df.keys())[i]])):
                self.e = tk.Label(df_frame, width=10, fg='blue', font=('Arial', 8, 'bold'), bd = 1, borderwidth=1, relief="groove")
                self.e.grid(row=i, column=j)
                self.e.bind("<Button-1>", lambda event, row=i, col=j: self.prosess(row, col))
                if df[list(df.keys())[i]][j] != None:
                    # self.e.insert(END, str(i)+','+str(j)+','+str(df[list(df.keys())[i]][j]))
                    self.e['text'] = str(i)+','+str(j)+','+str(df[list(df.keys())[i]][j])
                else:
                    # self.e.insert(END, str(i)+','+str(j)+','+"NONE")
                    self.e['text'] = str(i)+','+str(j)+','+"NONE"

    def prosess(self, row, col):
        if self.deleteMode:
            with shelve.open(self._db_path, writeback=True) as db:
                first_row = int(input("Kaçıncı satırdan itibaren(ilk satır 0)"))
                last_row = int(input("Kaçıncı satıra kadar(son satır dahil)(ilk satır 0)"))

                count = 0
                for i in self.df.keys():
                    if (count >= first_row) and (count <= last_row) :
                        #print(db[i][col])
                        del db[i][col]
                    count += 1
                print("Done")
        else:
            tmp = self.df[list(self.df.keys())[row]][self.rollerCount*self.pageItemCount + col]
            print(self.df[list(self.df.keys())[row]][col])

        # for i in tmp:
        #     print(i)

    @property
    def db_path(self):
        try:
            return self._db_path
        except AttributeError:
            raise ValueError("db_path not set")
    @db_path.setter
    def db_path(self, value):
        self._db_path = value

class PnlPage(DBPage):
    def __init__(self, master):
        super().__init__(master)
        self._db_path = 'mem\\panelDb'

class MbPage(DBPage):
    def __init__(self, master):
        super().__init__(master)
        self._db_path = 'mem\\mbDb'

class PSUPage(DBPage):
    def __init__(self, master):
        super().__init__(master)
        self._db_path = 'mem\\psuDb'

class UrsaPage(DBPage):
    def __init__(self, master):
        super().__init__(master)
        self._db_path = 'mem\\ursaDb'

class TVCPage(DBPage):
    def __init__(self, master):
        super().__init__(master)
        self._db_path = 'mem\\tvcDb'

class LearnPage(DBPage):
    def __init__(self, master):
        super().__init__(master)
        self._db_path = 'mem\\learnDb'

class pnlPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #root = master
        #self.root = root
        # p = Path(__file__).parent[0]
        # self.path = os.path.join(p, 'mem\\panelDb')
        self.path = 'mem\\panelDb'
        pnlFr = tk.Frame(self, width=850, height= 500, highlightbackground="red", highlightcolor="red", highlightthickness=1)
        pnlFr.grid(row = 2, column = 2, columnspan = 10, sticky='nsew')
        tk.Button(self, text="show first 10", command=lambda: self.showSome('f10')).grid(row=1,column=1,sticky=W)
        tk.Button(self, text="show last 10", command=lambda: self.showSome('l10')).grid(row=1,column=2,sticky=W)
        tk.Button(self, text="add None to Missings", command=lambda: self.addNonetoMissings()).grid(row=1,column=3,sticky=W)
        self.update()

    def showSome(self, arg):
        with shelve.open(self.path) as db:
            if arg == 'f10':
                dict = {}
                for i in db.keys():
                    dict[i] = db[i][:10]
                    print("column ", i, " length: ", len(db[i]))
                df = pd.DataFrame(dict)
                # print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
                self.showData(df)
            if arg == 'l10':
                dict = {}
                for i in db.keys():
                    dict[i] = db[i][-10:]
                    print("column ", i, " length: ", len(db[i]))
                df = pd.DataFrame(dict)
                # print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
                self.showData(df)
        db.close()

    def addNonetoMissings(self):
        with shelve.open(self.path, writeback=True) as db:
            maxCtr = len(db[list(db.keys())[0]])
            print("maxCtr: ", maxCtr)
            ch = 0
            for i in db.keys():
                if len(db[i]) > maxCtr:
                    maxCtr = len(db[i])
                    ch += 1
                if len(db[i]) < maxCtr:
                    ch += 1
            if ch > 0:
                for i in db.keys():
                    addNum = maxCtr - len(db[i])
                    for k in range(addNum):
                        db[i].append(None)
                        print(i, " added None")

        db.close()

    def showData(self, df):
        print("girdi")
        rootTbl = tk.Tk()
        df_frame = tk.Frame(rootTbl)
        key_frame = tk.Frame(rootTbl)
        commands_frame = tk.Frame(rootTbl)
        df_frame.grid(row=2, column = 2)
        key_frame.grid(row=2, column = 1)
        commands_frame.grid(row=2, column = 3)
        tk.Button(commands_frame, text="try").grid(row=1,column=1,sticky=W)
        # code for creating table
        for i in range(len(list(df.keys()))):
            print("i: ", i)
            self.e = tk.Label(key_frame, width=20, fg='blue',
                               font=('Arial',16,'bold'), bd = 2, borderwidth=2, relief="groove")
            self.e.grid(row=i, column = 1)
            self.e['text'] = str(list(df.keys())[i])
            for j in range(len(df[list(df.keys())[i]])):
                self.e = tk.Label(df_frame, width=20, fg='blue',
                               font=('Arial',16,'bold'), bd = 2, borderwidth=2, relief="groove")
                self.e.grid(row=i, column=j)
                if df[list(df.keys())[i]][j] != None:
                    # self.e.insert(END, str(i)+','+str(j)+','+str(df[list(df.keys())[i]][j]))
                    self.e['text'] = str(i)+','+str(j)+','+str(df[list(df.keys())[i]][j])
                else:
                    # self.e.insert(END, str(i)+','+str(j)+','+"NONE")
                    self.e['text'] = str(i)+','+str(j)+','+"NONE"



if __name__ == "__main__":
    app = SampleApp()

    app.mainloop()



cv2.waitKey(0)
cv2.destroyAllWindows()
