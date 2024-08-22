# Multi-frame tkinter application v2.3
import os
import sys
sys.path.insert(0, "..")
from tkinter import *
import tkinter as tk
import tkinter.filedialog
from tkinter.messagebox import showinfo
import shelve
from classes.settings import Settings as st
from pathlib import Path
import traceback

class UrsaDatabase():
    def __init__(self):
        self.isDbExist = False
        isDbTended = False
        p = Path(__file__).parents[2]
        self.path = os.path.join(p, 'mem\\ursaDb')
        try:
            print("bu path: ", self.path)
            with shelve.open(self.path, writeback=True) as mbDb:
                if ('inc' not in mbDb):
                    self.isDbExist = False
                    self.makeDb()
                else:
                    self.tendDb()
        except:
            traceback.print_exc()
            print("boyle bi db yok dolayısıyla yeni oluşturuluyor")
            self.makeDb()
            print("DB OLUŞTURULDU")


    def makeDb(self):
        mbDb = shelve.open(self.path, writeback=True)
        if ('inc' not in mbDb):
            with shelve.open(self.path, writeback=True) as mbDb:
                mbDb['code'] = []  #mainboard code
                #AF
                mbDb['version'] = []  #version code
                #7
                mbDb['xSize'] = []  #width
                #21
                mbDb['ySize'] = []  #length
                #15
                mbDb['screwCo'] = []  #screw coordinates
                #[x,y]
                mbDb['conCo'] = []  #connector coordinates with types
                #[[x,y],usb]
                mbDb['inc'] = []  #includes
                # tcon + leddriver
        mbDb.close()
        self.mbDb = mbDb
        print("DB oluşturuldu")

    def tendDb(self):
        print("Henüz bu fonksiyon yazılmadı")

##    @staticmethod
    def addUrsa(self, mb):
        try:
##            mbDb = shelve.open(self.path, writeback=True)
            with shelve.open(self.path, writeback=True) as mbDb:
                mbDb['code'].append(mb.code)
                print("az önce bu code'a girdi: ", mbDb['code'])
                mbDb['version'].append(mb.version)
                mbDb['xSize'].append(mb.xS)
                mbDb['ySize'].append(mb.yS)
                mbDb['screwCo'].append(mb.screwCo)
                mbDb['conCo'].append(mb.conCo)
                mbDb['inc'].append(mb.includes)
            mbDb.close()
        except:
            traceback.print_exc()
            print("addUrsa çalışmadı")

##    @staticmethod
    def showSome(self):
        with shelve.open(self.path) as mbDb:
            for i in mbDb.keys():
                print("column ", i, " length: ", len(mbDb[i]))
            for i in mbDb.keys():
                print("column ", i, " elements: ")
                for k in range(len(mbDb[i])):
                    print(mbDb[i][k])
        mbDb.close()


if __name__ == "__main__":
    app = SampleApp()

    app.mainloop()
