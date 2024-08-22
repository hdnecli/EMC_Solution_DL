# Multi-frame tkinter application v2.3
import os
import sys
import pandas as pd
sys.path.insert(0, "..")
import tkinter as tk
from tkinter import *
import shelve
from classes.settings import Settings as st
from pathlib import Path
import logging
from tkinter import *
import tkinter as tk
import tkinter.filedialog
from tkinter.messagebox import showinfo
import tkinter.messagebox as tkmb
import traceback
import pyarrow as pa
import pyarrow.parquet as pq

class LearnDatabase():
    def __init__(self):
        self.isDbExist = False
        isDbTended = False
        p = Path(__file__).parents[2]
        self.path = os.path.join(p, 'mem\\learnDb')
        self.parquetPath = os.path.join(p, 'mem\\data.parquet')
        self.tvcPath = os.path.join(p, 'mem\\tvcDb')
        self.check_point = 'SikerSikör'
        try:
            print("bu path: ", self.path)
            with shelve.open(self.path, writeback=True) as db:
                self.makeDb()
        except Exception as e:
            print("makeDb çalışmadı")
            print(e)

    def tendDb(self):
        print("tendDB ye girdi")
        with shelve.open(self.path, writeback=True) as db:
            maxElementLen = 0
            minElementLen = 1
            for i in db.keys():
                if len(db[i]) > maxElementLen:
                    maxElementLen = len(db[i])
            for i in db.keys():
                if len(db[i]) < maxElementLen:
                    diff = maxElementLen - len(db[i])
                    for k in range(diff):
                        db[i].append(None)
                    print(i, " dizinine ", diff, " kadar None eklendi")
        db.close()

    def makeDb(self):
        db = shelve.open(self.path, writeback=True)
        if ('ranking' not in db):
            with shelve.open(self.path, writeback=True) as db:
                db['inch'] = []
                db['tvConfigCode'] = []
                db['mbCode'] = []
                db['mbCords'] = []

                db['mbMap'] = []

                db['pnlCode'] = []
                db['cell_code'] = []
                db['panel_vendor'] = []
                db['mbScrewCords'] = []
                db['mbScrewMap'] = []
                db['mbConCords'] = []

                db['isPsuAdded'] = []
                db['isUrsaAdded'] = []
                db['isTconAdded'] = []
                db['isWlanAdded'] = []

                db['psuCode'] = []
                db['psuCords'] = []

                db['psuMap'] = []

                db['psuScrewCords'] = []
                db['psuScrewMap'] = []
                db['psuConCords'] = []

                db['ursaCode'] = []
                db['ursaCords'] = []

                db['ursaMap'] = []

                db['ursaScrewCords'] = []
                db['ursaScrewMap'] = []
                db['ursaConCords'] = []

                db['wlanCode'] = []
                db['wlanCords'] = []

                db['wlanMap'] = []

                db['wlanScrewCords'] = []
                db['wlanScrewMap'] = []
                db['wlanConCords'] = []

                db['cableShapes'] = []
                db['cableShields'] = []
                db['cableTypes'] = []
                db['cableWidths'] = []
                #db['cableCords'] = []
                #db['cableTransparencies'] = []
                db['cable_map'] = []
                db['cable_trns_map'] = []
                db['cable_single_shield_map'] = []
                db['cable_double_shield_map'] = []
                db['cable_circle_shield_map'] = []
                db['cableTags'] = []

                db['emiTapeCords'] = []
                db['emiTapeTags'] = []
                db['emi_tape_map'] = []

                db['ferriteCords'] = []
                db['ferriteTags'] = []
                db['ferrit_map'] = []

                db['vData'] = []  #float list
                db['hData'] = []  #float list
                db['remBiasH'] = [] # avarage of horizontal radiation // DNTIC
                db['remBiasV'] = [] # avarage of vertical radiation // DNTIC
                db['freqMarginH'] = [] # horizontal frequencies set which doesn't met 3dB margin
                db['freqMarginV'] = [] # vertical frequencies set which doesn't met 3dB margin
                db['freqCriticH'] = [] # horizontal frequencies set which has a margin m -> 3dB > m >= 6dB
                db['freqCriticV'] = [] # vertical frequencies set which has a margin m -> 3dB > m >= 6dB
                db['freqPotentialH'] = [] # horizontal frequencies set which has a margin m -> 6dB > m >= 9dB
                db['freqPotentialV'] = [] # vertical frequencies set which has a margin m -> 6dB > m >= 9dB
                db['ranking'] = [] # ranking of the result from a scale from 1 to 100
        else:
            print("makeDB olmadı")
        db.sync()
        db.close()
        #self.db = db
        print("DB oluşturuldu")


# what to add more
# opencell tech / vendor / resolution
# speaker wattage
# panel power
# PSU IC freq
# LED DRV IC Freq
# backlight power
# mainboard power
# mainboard features / memc / dts / smart backlight etc
# wifi power / ac?n?
# BT 5,4,3?
# RAM clk / size
# ursa power / specs / features / ram specs
# panel ssc specs
# does PSU has EARTH?
# is mainboard 3in1 or 2in1
#DVBS DVBT hangisi?
##    @staticmethod
    def add(self, tvc_code, graph1):
        x_s = 160 #x_scale divides X on Tv to smaller scales bigger x_s get the smaller discrete are gets
        y_s = 90 #y_scale divides Y on Tv to smaller scales bigger y_s get the smaller discrete are gets
        cable_dict = st.cable_dict
        emi_tape_dict = st.emi_tape_dict
        ferrit_dict = st.ferrit_dict
        check_point = "SikerSikör"
        try:
##            db = shelve.open(self.path, writeback=True)
            idx = 0
            with shelve.open(self.tvcPath, writeback=False) as tvc_db:
                idx = tvc_db['tvConfigCode'].index(tvc_code)
                with shelve.open(self.path, writeback=True) as db:
                    check_point = 'inch' 
                    db['inch'].append(tvc_db['inch'][idx]) #20 - 150 #int8
                    inch = tvc_db['inch'][idx]
                    check_point = 'tvConfigCode' 
                    db['tvConfigCode'].append(tvc_code) #string
                    check_point = 'mbCode'
                    db['mbCode'].append(tvc_db['mbCode'][idx]) #string
                    check_point = 'mbCords'
                    db['mbCords'].append(tvc_db['mbCords'][idx]) #float16
                    mbCords = tvc_db['mbCords'][idx]
                    tmpMbMap = self.convertCardCordsTo2DMatrix(mbCords, inch, x_s, y_s)
                    check_point = 'mbMap'
                    db['mbMap'].append(tmpMbMap) #float16
                    check_point = 'pnlCode'
                    db['pnlCode'].append(tvc_db['pnlCode'][idx])  #string
                    check_point = 'cell_code'
                    db['cell_code'].append(tvc_db['cell_code'][idx]) #string
                    check_point = 'panel_vendor'
                    db['panel_vendor'].append(tvc_db['panel_vendor'][idx]) #string
                    check_point = 'mbScrewCords'
                    db['mbScrewCords'].append(tvc_db['mbScrewCords'][idx]) #float16
                    mbScrewCords = tvc_db['mbScrewCords'][idx]
                    tmp_screw_cords = self.convertScrewCordsTo2DMatrix(mbScrewCords, inch, x_s, y_s)
                    check_point = 'mbScrewMap'
                    db['mbScrewMap'].append(tmp_screw_cords) #float16
                    check_point = 'mbConCords'
                    db['mbConCords'].append(tvc_db['mbConCords'][idx]) #float16
                    check_point = 'isPsuAdded'
                    db['isPsuAdded'].append(tvc_db['isPsuAdded'][idx]) #bool
                    check_point = 'isUrsaAdded'
                    db['isUrsaAdded'].append(tvc_db['isUrsaAdded'][idx])  #bool
                    check_point = 'isTconAdded'
                    db['isTconAdded'].append(tvc_db['isTconAdded'][idx]) #bool
                    check_point = 'isWlanAdded'
                    db['isWlanAdded'].append(tvc_db['isWlanAdded'][idx]) #bool
                    check_point = 'psuCode'
                    db['psuCode'].append(tvc_db['psuCode'][idx]) #string
                    check_point = 'psuCords'
                    db['psuCords'].append(tvc_db['psuCords'][idx]) #float16
                    psuCords = tvc_db['psuCords'][idx]
                    tmpPsuMap = self.convertCardCordsTo2DMatrix(psuCords, inch, x_s, y_s)
                    check_point = 'psuMap'
                    db['psuMap'].append(tmpPsuMap) #float16
                    check_point = 'psuScrewCords'
                    db['psuScrewCords'].append(tvc_db['psuScrewCords'][idx])  #float16
                    psuScrewCords = tvc_db['psuScrewCords'][idx]
                    tmp_psu_screw_cords = self.convertScrewCordsTo2DMatrix(psuScrewCords, inch, x_s, y_s)
                    check_point = 'psuScrewMap'
                    db['psuScrewMap'].append(tmp_psu_screw_cords)  #float16
                    check_point = 'psuConCords'
                    db['psuConCords'].append(tvc_db['psuConCords'][idx]) #float16
                    check_point = 'ursaCode'
                    db['ursaCode'].append(tvc_db['ursaCode'][idx])  #string
                    check_point = 'ursaCords'
                    db['ursaCords'].append(tvc_db['ursaCords'][idx])  #float16
                    ursaCords = tvc_db['ursaCords'][idx]
                    tmpUrsaMap = self.convertCardCordsTo2DMatrix(ursaCords, inch, x_s, y_s)
                    check_point = 'ursaMap'
                    db['ursaMap'].append(tmpUrsaMap) #float16
                    check_point = 'ursaScrewCords'
                    db['ursaScrewCords'].append(tvc_db['ursaScrewCords'][idx]) #float16
                    ursaScrewCords = tvc_db['ursaScrewCords'][idx]
                    tmp_ursa_screw_cords = self.convertScrewCordsTo2DMatrix(ursaScrewCords, inch, x_s, y_s)
                    check_point = 'ursaScrewMap'
                    db['ursaScrewMap'].append(tmp_ursa_screw_cords) #float16
                    check_point = 'ursaConCords'
                    db['ursaConCords'].append(tvc_db['ursaConCords'][idx]) #float16
                    check_point = 'wlanCode'
                    db['wlanCode'].append(tvc_db['wlanCode'][idx]) #string
                    check_point = 'wlanCords'
                    db['wlanCords'].append(tvc_db['wlanCords'][idx]) #float16
                    wlanCords = tvc_db['wlanCords'][idx]
                    tmpWlanMap = self.convertCardCordsTo2DMatrix(wlanCords, inch, x_s, y_s)
                    check_point = 'wlanMap'
                    db['wlanMap'].append(tmpWlanMap)  #float16
                    check_point = 'wlanScrewCords'
                    db['wlanScrewCords'].append(tvc_db['wlanScrewCords'][idx])  #float16
                    wlanScrewCords = tvc_db['wlanScrewCords'][idx]
                    tmp_wlan_screw_cords = self.convertScrewCordsTo2DMatrix(wlanScrewCords, inch, x_s, y_s)
                    check_point = 'wlanScrewMap'
                    db['wlanScrewMap'].append(tmp_wlan_screw_cords)  #float16
                    check_point = 'wlanConCords'
                    db['wlanConCords'].append(tvc_db['wlanConCords'][idx])  #float16
                    check_point = 'cableShapes'
                    db['cableShapes'].append(tvc_db['cableShapes'][idx])  #int8 #normalde text olarak saklıyoruz. Gerek yok. enumarate gerekebilir
                    check_point = 'cableShields'
                    db['cableShields'].append(tvc_db['cableShields'][idx]) #int8 #normalde text olarak saklıyoruz. Gerek yok. enumarate gerekebilir
                    check_point = 'cableTypes'
                    db['cableTypes'].append(tvc_db['cableTypes'][idx]) #int8 #normalde text olarak saklıyoruz. Gerek yok. enumarate gerekebilir
                    check_point = 'cableWidths'
                    db['cableWidths'].append(tvc_db['cableWidths'][idx]) #uint8 ya da drop
                    check_point = 'cableTags'
                    db['cableTags'].append(tvc_db['cableTags'][idx]) #string ama drop edebiliriz
                    cable_tags = tvc_db['cableTags'][idx]
                    cab_cords = tvc_db['cableCords'][idx]
                    cab_trns_lst = tvc_db['cableTransparencies'][idx]
                    cable_shield = tvc_db['cableShields'][idx]
                    arr_3D = [[[0 for i in range(y_s)] for j in range(x_s)] for k in range(64)]
                    arr_3D_single_shield = [[[0 for i in range(y_s)] for j in range(x_s)] for k in range(64)]
                    arr_3D_double_shield = [[[0 for i in range(y_s)] for j in range(x_s)] for k in range(64)]
                    arr_3D_circle_shield = [[[0 for i in range(y_s)] for j in range(x_s)] for k in range(64)]
                    arr_3D_trans = [[[0 for i in range(y_s)] for j in range(x_s)] for k in range(64)]
                    for i in range(len(cab_cords)):
                        map_index = self.findCableIndex(cable_tags[i])
                        if map_index == -1:
                            continue
                        tmp_cab_map, tmp_cab_trns_map = self.convertCableCordsTo2DMatrix(cab_cords[i], cab_trns_lst[i], inch, x_s, y_s)
                        arr_3D[map_index] = tmp_cab_map
                        arr_3D_trans[map_index] = tmp_cab_trns_map
                        if cable_shield[i] == 'SS':
                            arr_3D_single_shield[map_index] = tmp_cab_map
                        elif cable_shield[i] == 'DS':
                            arr_3D_double_shield[map_index] = tmp_cab_map
                        elif cable_shield[i] == 'CS':
                            arr_3D_circle_shield[map_index] = tmp_cab_map
                    check_point = 'cable_map'
                    db['cable_map'].append(arr_3D) #int8
                    check_point = 'cable_trns_map'
                    db['cable_trns_map'].append(arr_3D_trans) #int8
                    check_point = 'cable_single_shield_map'
                    db['cable_single_shield_map'].append(arr_3D_single_shield) #int8
                    check_point = 'cable_double_shield_map'
                    db['cable_double_shield_map'].append(arr_3D_double_shield) #int8
                    check_point = 'cable_circle_shield_map'
                    db['cable_circle_shield_map'].append(arr_3D_circle_shield) #int8
                    check_point = 'emiTapeCords'
                    db['emiTapeCords'].append(tvc_db['emiTapeCords'][idx]) #float16
                    check_point = 'emiTapeTags'
                    db['emiTapeTags'].append(tvc_db['emiTapeTags'][idx])  #string ama drop edebiliriz
                    arr_3D_emi = [[[0 for i in range(y_s)] for j in range(x_s)] for k in range(96)]
                    emi_tags = tvc_db['emiTapeTags'][idx]
                    emi_cords = tvc_db['emiTapeCords'][idx]
                    for i in range(len(emi_cords)):
                        map_index = self.findEmiTapeIndex(emi_tags[i])
                        tmp_emi_map = self.convertEmiCordsTo2DMatrix(emi_cords[i], inch, x_s, y_s)
                        for k in map_index:
                            if k == -1:
                                continue
                            try:
                                for q in range(len(tmp_emi_map)):
                                    for w in range(len(tmp_emi_map[0])):
                                        if tmp_emi_map[q][w] == 1:
                                            arr_3D_emi[k][q][w] = 1
                            except:
                                print("emi_cords sıçıyo!")
                    check_point = 'emi_tape_map'
                    db['emi_tape_map'].append(arr_3D_emi)  #float16
                    check_point = 'ferriteCords'
                    db['ferriteCords'].append(tvc_db['ferriteCords'][idx]) #float16
                    check_point = 'ferriteTags'
                    db['ferriteTags'].append(tvc_db['ferriteTags'][idx]) #string ama drop edebiliriz
                    arr_3D_ferrit = [[[0 for i in range(y_s)] for j in range(x_s)] for k in range(64)]
                    ferrit_tags = tvc_db['ferriteTags'][idx]
                    ferrit_cords = tvc_db['ferriteCords'][idx]
                    for i in range(len(ferrit_cords)):
                        map_index = self.findEmiTapeIndex(ferrit_tags[i])
                        tmp_ferrit_map = self.convertEmiCordsTo2DMatrix(ferrit_cords[i], inch, x_s, y_s)
                        for k in map_index:
                            if k == -1:
                                continue
                            try:
                                for q in range(len(tmp_ferrit_map)):
                                    for w in range(len(tmp_ferrit_map[0])):
                                        if tmp_ferrit_map[q][w] == 1:
                                            arr_3D_ferrit[k][q][w] = 1
                            except:
                                print("ferrit_cords sıçıyo!")
                    check_point = 'ferrit_map'
                    db['ferrit_map'].append(arr_3D_ferrit) #float16


                    sumV = 0
                    sumH = 0
                    freqMarginV = []
                    freqMarginH = []
                    freqCriticV = []
                    freqCriticH = []
                    freqPotentialV = []
                    freqPotentialH = []

                    for x in range(971):
                        if x <= 201: # limit 40

                            if graph1.vrtData[x] >= 37:
                                freqMarginV.append(x+30)
                            elif graph1.vrtData[x] >= 34:
                                freqCriticV.append(x+30)
                            elif graph1.vrtData[x] >= 31:
                                freqPotentialV.append(x+30)

                            if graph1.hrzData[x] >= 37:
                                freqMarginH.append(x+30)
                            elif graph1.hrzData[x] >= 34:
                                freqCriticH.append(x+30)
                            elif graph1.hrzData[x] >= 31:
                                freqPotentialH.append(x+30)

                        else: # limit 47

                            if graph1.vrtData[x] >= 44:
                                freqMarginV.append(x+30)
                            elif graph1.vrtData[x] >= 41:
                                freqCriticV.append(x+30)
                            elif graph1.vrtData[x] >= 38:
                                freqPotentialV.append(x+30)

                            if graph1.hrzData[x] >= 44:
                                freqMarginH.append(x+30)
                            elif graph1.hrzData[x] >= 41:
                                freqCriticH.append(x+30)
                            elif graph1.hrzData[x] >= 38:
                                freqPotentialH.append(x+30)

                        sumV += graph1.vrtData[x]
                        sumH += graph1.hrzData[x]

                    remBiasH = sumH / 971
                    remBiasV = sumV / 971

                    self.freqMarginV = freqMarginV
                    self.freqCriticV = freqCriticV
                    self.freqPotentialV = freqPotentialV
                    self.freqMarginH = freqMarginH
                    self.freqCriticH = freqCriticH
                    self.freqPotentialH = freqPotentialH
                    self.remBiasH = remBiasH
                    self.remBiasV = remBiasV
                    #ranking determines the risk of the result
                    self.ranking = (len(freqMarginV)+len(freqMarginH))*16 + (len(freqCriticV)+len(freqCriticH))*9 + (len(freqPotentialV)+len(freqPotentialH))*4

                    tempArr = [0]*971
                    for x in freqMarginV:
                        tempArr[x-30] = 1
                    self.freqMarginV = tempArr

                    tempArr = [0]*971
                    for x in freqCriticV:
                        tempArr[x-30] = 1
                    self.freqCriticV = tempArr

                    tempArr = [0]*971
                    for x in freqPotentialV:
                        tempArr[x-30] = 1
                    self.freqPotentialV = tempArr

                    tempArr = [0]*971
                    for x in freqMarginH:
                        tempArr[x-30] = 1
                    self.freqMarginH = tempArr

                    tempArr = [0]*971
                    for x in freqCriticH:
                        tempArr[x-30] = 1
                    self.freqCriticH = tempArr

                    tempArr = [0]*971
                    for x in freqPotentialH:
                        tempArr[x-30] = 1
                    self.freqPotentialH = tempArr


                    ## Outputs
                    check_point = 'vData'
                    db['vData'].append(graph1.vrtData) #float16
                    # print("vData: ", graph1.vrtData)
                    check_point = 'hData'
                    db['hData'].append(graph1.hrzData) #float16
                    # print("hData: ", graph1.hrzData)
                    check_point = 'remBiasH'
                    db['remBiasH'].append(self.remBiasH) #float16
                    # print("remBiasH: ", self.remBiasH)
                    check_point = 'remBiasV'
                    db['remBiasV'].append(self.remBiasV) #float16
                    # print("remBiasV: ", self.remBiasV)
                    check_point = 'freqMarginH'
                    db['freqMarginH'].append(self.freqMarginH) #bool yani int8
                    # print("freqMarginH: ", self.freqMarginH)
                    check_point = 'freqMarginV'
                    db['freqMarginV'].append(self.freqMarginV) #bool yani int8
                    # print("freqMarginV: ", self.freqMarginV)
                    check_point = 'freqCriticH'
                    db['freqCriticH'].append(self.freqCriticH) #bool yani int8
                    # print("freqCriticH: ", self.freqCriticH)
                    check_point = 'freqCriticV'
                    db['freqCriticV'].append(self.freqCriticV) #bool yani int8
                    # print("freqCriticV: ", self.freqCriticV)
                    check_point = 'freqPotentialH'
                    db['freqPotentialH'].append(self.freqPotentialH) #bool yani int8
                    # print("freqPotentialH: ", self.freqPotentialH)
                    check_point = 'freqPotentialV'
                    db['freqPotentialV'].append(self.freqPotentialV) #bool yani int8
                    # print("freqPotentialV: ", self.freqPotentialV)
                    check_point = 'ranking'
                    db['ranking'].append(self.ranking) #float16
                    # print("ranking: ", self.ranking)


                tkmb.showinfo("BİTTİ", "Orjinal Datalar yüklendi!")
                db.close()
            tvc_db.close()
        except Exception as e:
            self.check_point = check_point
            print(check_point, " i yazamadan sıçtı gitti!")
            print(e)
            try:
                db.close()
                tvc_db.close()
            except:
                print("db close tvc_db close")
            if self.instantCorrect() == 1:
                print("database e kaydederken bir sorun oldu ve son kayıtlar başarıyla geri alındı. Bir daha dene!")
            elif self.instantCorrect() == -1:
                print("database e kaydederken bir sorun oldu ve ciddi bir problem oldu. Database Handler ile kayıtları detaylı inceleyip müdahale et!")
            traceback.print_exc()

    def addParquet(self, tvc_code, graph1, test_name): # tvc_db kısmının altı parquet yapılacak
        x_s = 160 #x_scale divides X on Tv to smaller scales bigger x_s get the smaller discrete are gets
        y_s = 90 #y_scale divides Y on Tv to smaller scales bigger y_s get the smaller discrete are gets
        cable_dict = st.cable_dict
        emi_tape_dict = st.emi_tape_dict
        ferrit_dict = st.ferrit_dict
        check_point = "SikerSikör"
        try:
##            db = shelve.open(self.path, writeback=True)
            idx = 0
            with shelve.open(self.tvcPath, writeback=False) as tvc_db:
                idx = tvc_db['tvConfigCode'].index(tvc_code)
                df_parquet = pd.read_parquet(self.parquetPath)                
                temp_dic = {}
                check_point = 'inch' 
                temp_dic[check_point] = [tvc_db['inch'][idx]] #20 - 150 #int8
                inch = tvc_db['inch'][idx]
                check_point = 'tvConfigCode' 
                temp_dic[check_point] = [tvc_code] #string
                check_point = 'mbCode'
                temp_dic[check_point] = [tvc_db['mbCode'][idx]] #string
                check_point = 'mbCords'
                temp_dic[check_point] = [tvc_db['mbCords'][idx]] #float16
                mbCords = tvc_db['mbCords'][idx]
                tmpMbMap = self.convertCardCordsTo2DMatrix(mbCords, inch, x_s, y_s)
                check_point = 'mbMap'
                temp_dic[check_point] = [tmpMbMap] #float16
                check_point = 'pnlCode'
                temp_dic[check_point] = (tvc_db['pnlCode'][idx])  #string
                check_point = 'cell_code'
                temp_dic[check_point] = [tvc_db['cell_code'][idx]] #string
                check_point = 'panel_vendor'
                temp_dic[check_point] = [tvc_db['panel_vendor'][idx]] #string
                check_point = 'mbScrewCords'
                temp_dic[check_point] = [tvc_db['mbScrewCords'][idx]] #float16
                mbScrewCords = tvc_db['mbScrewCords'][idx]
                tmp_screw_cords = self.convertScrewCordsTo2DMatrix(mbScrewCords, inch, x_s, y_s)
                check_point = 'mbScrewMap'
                temp_dic[check_point] = [tmp_screw_cords] #float16
                check_point = 'mbConCords'
                temp_dic[check_point] = [tvc_db['mbConCords'][idx]] #float16
                check_point = 'isPsuAdded'
                temp_dic[check_point] = [tvc_db['isPsuAdded'][idx]] #bool
                check_point = 'isUrsaAdded'
                temp_dic[check_point] = [tvc_db['isUrsaAdded'][idx]]  #bool
                check_point = 'isTconAdded'
                temp_dic[check_point] = [tvc_db['isTconAdded'][idx]] #bool
                check_point = 'isWlanAdded'
                temp_dic[check_point] = [tvc_db['isWlanAdded'][idx]] #bool
                check_point = 'psuCode'
                temp_dic[check_point] = [tvc_db['psuCode'][idx]] #string
                check_point = 'psuCords'
                temp_dic[check_point] = [tvc_db['psuCords'][idx]] #float16
                psuCords = tvc_db['psuCords'][idx]
                tmpPsuMap = self.convertCardCordsTo2DMatrix(psuCords, inch, x_s, y_s)
                check_point = 'psuMap'
                temp_dic[check_point] = [tmpPsuMap] #float16
                check_point = 'psuScrewCords'
                temp_dic[check_point] = [tvc_db['psuScrewCords'][idx]]  #float16
                psuScrewCords = tvc_db['psuScrewCords'][idx]
                tmp_psu_screw_cords = self.convertScrewCordsTo2DMatrix(psuScrewCords, inch, x_s, y_s)
                check_point = 'psuScrewMap'
                temp_dic[check_point] = [tmp_psu_screw_cords]  #float16
                check_point = 'psuConCords'
                temp_dic[check_point] = [tvc_db['psuConCords'][idx]] #float16
                check_point = 'ursaCode'
                temp_dic[check_point] = [tvc_db['ursaCode'][idx]]  #string
                check_point = 'ursaCords'
                temp_dic[check_point] = [tvc_db['ursaCords'][idx]]  #float16
                ursaCords = tvc_db['ursaCords'][idx]
                tmpUrsaMap = self.convertCardCordsTo2DMatrix(ursaCords, inch, x_s, y_s)
                check_point = 'ursaMap'
                temp_dic[check_point] = [tmpUrsaMap] #float16
                check_point = 'ursaScrewCords'
                temp_dic[check_point] = [tvc_db['ursaScrewCords'][idx]] #float16
                ursaScrewCords = tvc_db['ursaScrewCords'][idx]
                tmp_ursa_screw_cords = self.convertScrewCordsTo2DMatrix(ursaScrewCords, inch, x_s, y_s)
                check_point = 'ursaScrewMap'
                temp_dic[check_point] = [tmp_ursa_screw_cords] #float16
                check_point = 'ursaConCords'
                temp_dic[check_point] = [tvc_db['ursaConCords'][idx]] #float16
                check_point = 'wlanCode'
                temp_dic[check_point] = [tvc_db['wlanCode'][idx]] #string
                check_point = 'wlanCords'
                temp_dic[check_point] = [tvc_db['wlanCords'][idx]] #float16
                wlanCords = tvc_db['wlanCords'][idx]
                tmpWlanMap = self.convertCardCordsTo2DMatrix(wlanCords, inch, x_s, y_s)
                check_point = 'wlanMap'
                temp_dic[check_point] = [tmpWlanMap]  #float16
                check_point = 'wlanScrewCords'
                temp_dic[check_point] = [tvc_db['wlanScrewCords'][idx]]  #float16
                wlanScrewCords = tvc_db['wlanScrewCords'][idx]
                tmp_wlan_screw_cords = self.convertScrewCordsTo2DMatrix(wlanScrewCords, inch, x_s, y_s)
                check_point = 'wlanScrewMap'
                temp_dic[check_point] = [tmp_wlan_screw_cords]  #float16
                check_point = 'wlanConCords'
                temp_dic[check_point] = [tvc_db['wlanConCords'][idx]]  #float16
                check_point = 'cableShapes'
                temp_dic[check_point] = [tvc_db['cableShapes'][idx]]  #int8 #normalde text olarak saklıyoruz. Gerek yok. enumarate gerekebilir
                check_point = 'cableShields'
                temp_dic[check_point] = [tvc_db['cableShields'][idx]] #int8 #normalde text olarak saklıyoruz. Gerek yok. enumarate gerekebilir
                check_point = 'cableTypes'
                temp_dic[check_point] = [tvc_db['cableTypes'][idx]] #int8 #normalde text olarak saklıyoruz. Gerek yok. enumarate gerekebilir
                check_point = 'cableWidths'
                temp_dic[check_point] = [tvc_db['cableWidths'][idx]] #uint8 ya da drop
                check_point = 'cableTags'
                temp_dic[check_point] = [tvc_db['cableTags'][idx]] #string ama drop edebiliriz
                cable_tags = tvc_db['cableTags'][idx]
                cab_cords = tvc_db['cableCords'][idx]
                cab_trns_lst = tvc_db['cableTransparencies'][idx]
                cable_shield = tvc_db['cableShields'][idx]
                arr_3D = [[[0 for i in range(y_s)] for j in range(x_s)] for k in range(64)]
                arr_3D_single_shield = [[[0 for i in range(y_s)] for j in range(x_s)] for k in range(64)]
                arr_3D_double_shield = [[[0 for i in range(y_s)] for j in range(x_s)] for k in range(64)]
                arr_3D_circle_shield = [[[0 for i in range(y_s)] for j in range(x_s)] for k in range(64)]
                arr_3D_trans = [[[0 for i in range(y_s)] for j in range(x_s)] for k in range(64)]
                for i in range(len(cab_cords)):
                    map_index = self.findCableIndex(cable_tags[i])
                    if map_index == -1:
                        continue
                    tmp_cab_map, tmp_cab_trns_map = self.convertCableCordsTo2DMatrix(cab_cords[i], cab_trns_lst[i], inch, x_s, y_s)
                    arr_3D[map_index] = tmp_cab_map
                    arr_3D_trans[map_index] = tmp_cab_trns_map
                    if cable_shield[i] == 'SS':
                        arr_3D_single_shield[map_index] = tmp_cab_map
                    elif cable_shield[i] == 'DS':
                        arr_3D_double_shield[map_index] = tmp_cab_map
                    elif cable_shield[i] == 'CS':
                        arr_3D_circle_shield[map_index] = tmp_cab_map
                check_point = 'cable_map'
                temp_dic[check_point] = [arr_3D] #int8
                check_point = 'cable_trns_map'
                temp_dic[check_point] = [arr_3D_trans] #int8
                check_point = 'cable_single_shield_map'
                temp_dic[check_point] = [arr_3D_single_shield] #int8
                check_point = 'cable_double_shield_map'
                temp_dic[check_point] = [arr_3D_double_shield] #int8
                check_point = 'cable_circle_shield_map'
                temp_dic[check_point] = [arr_3D_circle_shield] #int8
                check_point = 'emiTapeCords'
                temp_dic[check_point] = [tvc_db['emiTapeCords'][idx]]#float16
                check_point = 'emiTapeTags'
                temp_dic[check_point] = [tvc_db['emiTapeTags'][idx]]  #string ama drop edebiliriz
                arr_3D_emi = [[[0 for i in range(y_s)] for j in range(x_s)] for k in range(96)]
                emi_tags = tvc_db['emiTapeTags'][idx]
                emi_cords = tvc_db['emiTapeCords'][idx]
                for i in range(len(emi_cords)):
                    map_index = self.findEmiTapeIndex(emi_tags[i])
                    tmp_emi_map = self.convertEmiCordsTo2DMatrix(emi_cords[i], inch, x_s, y_s)
                    for k in map_index:
                        if k == -1:
                            continue
                        try:
                            for q in range(len(tmp_emi_map)):
                                for w in range(len(tmp_emi_map[0])):
                                    if tmp_emi_map[q][w] == 1:
                                        arr_3D_emi[k][q][w] = 1
                        except:
                            print("emi_cords sıçıyo!")
                check_point = 'emi_tape_map'
                temp_dic[check_point] = [arr_3D_emi]  #float16
                check_point = 'ferriteCords'
                temp_dic[check_point] = [tvc_db['ferriteCords'][idx]] #float16
                check_point = 'ferriteTags'
                temp_dic[check_point] = [tvc_db['ferriteTags'][idx]] #string ama drop edebiliriz
                arr_3D_ferrit = [[[0 for i in range(y_s)] for j in range(x_s)] for k in range(64)]
                ferrit_tags = tvc_db['ferriteTags'][idx]
                ferrit_cords = tvc_db['ferriteCords'][idx]
                for i in range(len(ferrit_cords)):
                    map_index = self.findEmiTapeIndex(ferrit_tags[i])
                    tmp_ferrit_map = self.convertEmiCordsTo2DMatrix(ferrit_cords[i], inch, x_s, y_s)
                    for k in map_index:
                        if k == -1:
                            continue
                        try:
                            for q in range(len(tmp_ferrit_map)):
                                for w in range(len(tmp_ferrit_map[0])):
                                    if tmp_ferrit_map[q][w] == 1:
                                        arr_3D_ferrit[k][q][w] = 1
                        except:
                            print("ferrit_cords sıçıyo!")
                check_point = 'ferrit_map'
                temp_dic[check_point] = [arr_3D_ferrit] #float16


                sumV = 0
                sumH = 0
                freqMarginV = []
                freqMarginH = []
                freqCriticV = []
                freqCriticH = []
                freqPotentialV = []
                freqPotentialH = []

                for x in range(971):
                    if x <= 201: # limit 40

                        if graph1.vrtData[x] >= 37:
                            freqMarginV.append(x+30)
                        elif graph1.vrtData[x] >= 34:
                            freqCriticV.append(x+30)
                        elif graph1.vrtData[x] >= 31:
                            freqPotentialV.append(x+30)

                        if graph1.hrzData[x] >= 37:
                            freqMarginH.append(x+30)
                        elif graph1.hrzData[x] >= 34:
                            freqCriticH.append(x+30)
                        elif graph1.hrzData[x] >= 31:
                            freqPotentialH.append(x+30)

                    else: # limit 47

                        if graph1.vrtData[x] >= 44:
                            freqMarginV.append(x+30)
                        elif graph1.vrtData[x] >= 41:
                            freqCriticV.append(x+30)
                        elif graph1.vrtData[x] >= 38:
                            freqPotentialV.append(x+30)

                        if graph1.hrzData[x] >= 44:
                            freqMarginH.append(x+30)
                        elif graph1.hrzData[x] >= 41:
                            freqCriticH.append(x+30)
                        elif graph1.hrzData[x] >= 38:
                            freqPotentialH.append(x+30)

                    sumV += graph1.vrtData[x]
                    sumH += graph1.hrzData[x]

                remBiasH = sumH / 971
                remBiasV = sumV / 971

                self.freqMarginV = freqMarginV
                self.freqCriticV = freqCriticV
                self.freqPotentialV = freqPotentialV
                self.freqMarginH = freqMarginH
                self.freqCriticH = freqCriticH
                self.freqPotentialH = freqPotentialH
                self.remBiasH = remBiasH
                self.remBiasV = remBiasV
                #ranking determines the risk of the result
                self.ranking = (len(freqMarginV)+len(freqMarginH))*16 + (len(freqCriticV)+len(freqCriticH))*9 + (len(freqPotentialV)+len(freqPotentialH))*4

                tempArr = [0]*971
                for x in freqMarginV:
                    tempArr[x-30] = 1
                self.freqMarginV = tempArr

                tempArr = [0]*971
                for x in freqCriticV:
                    tempArr[x-30] = 1
                self.freqCriticV = tempArr

                tempArr = [0]*971
                for x in freqPotentialV:
                    tempArr[x-30] = 1
                self.freqPotentialV = tempArr

                tempArr = [0]*971
                for x in freqMarginH:
                    tempArr[x-30] = 1
                self.freqMarginH = tempArr

                tempArr = [0]*971
                for x in freqCriticH:
                    tempArr[x-30] = 1
                self.freqCriticH = tempArr

                tempArr = [0]*971
                for x in freqPotentialH:
                    tempArr[x-30] = 1
                self.freqPotentialH = tempArr

                ## Outputs
                check_point = 'test_name'
                temp_dic[check_point] = [test_name] #output ismi cekme
                check_point = 'vData'
                temp_dic[check_point] = [graph1.vrtData] #float16
                # print("vData: ", graph1.vrtData)
                check_point = 'hData'
                temp_dic[check_point] = [graph1.hrzData] #float16
                # print("hData: ", graph1.hrzData)
                check_point = 'remBiasH'
                temp_dic[check_point] = [self.remBiasH] #float16
                # print("remBiasH: ", self.remBiasH)
                check_point = 'remBiasV'
                temp_dic[check_point] = [self.remBiasV] #float16
                # print("remBiasV: ", self.remBiasV)
                check_point = 'freqMarginH'
                temp_dic[check_point] = [self.freqMarginH] #bool yani int8
                # print("freqMarginH: ", self.freqMarginH)
                check_point = 'freqMarginV'
                temp_dic[check_point] = [self.freqMarginV] #bool yani int8
                # print("freqMarginV: ", self.freqMarginV)
                check_point = 'freqCriticH'
                temp_dic[check_point] = [self.freqCriticH] #bool yani int8
                # print("freqCriticH: ", self.freqCriticH)
                check_point = 'freqCriticV'
                temp_dic[check_point] = [self.freqCriticV] #bool yani int8
                # print("freqCriticV: ", self.freqCriticV)
                check_point = 'freqPotentialH'
                temp_dic[check_point] = [self.freqPotentialH] #bool yani int8
                # print("freqPotentialH: ", self.freqPotentialH)
                check_point = 'freqPotentialV'
                temp_dic[check_point] = [self.freqPotentialV] #bool yani int8
                # print("freqPotentialV: ", self.freqPotentialV)
                check_point = 'ranking'
                temp_dic[check_point] = [self.ranking] #float16
                # print("ranking: ", self.ranking)
                df_updated = df_parquet.append(pd.DataFrame(temp_dic), ignore_index=True)
                df_updated = df_updated.astype(str) 
                df_updated.columns = df_updated.columns.astype(str) 
                table = pa.Table.from_pandas(df_updated)
                pq.write_table(table, self.parquetPath)
                
                tkmb.showinfo("BİTTİ", "Orjinal Datalar yüklendi!")
            tvc_db.close()
        except Exception as e:
            self.check_point = check_point
            print(check_point, " i yazamadan sıçtı gitti!")
            print(e)
            try:
                tvc_db.close()
            except:
                print("tvc_db close")
            if self.instantCorrect() == 1:
                print("database e kaydederken bir sorun oldu ve son kayıtlar başarıyla geri alındı. Bir daha dene!")
            elif self.instantCorrect() == -1:
                print("database e kaydederken bir sorun oldu ve ciddi bir problem oldu. Database Handler ile kayıtları detaylı inceleyip müdahale et!")
            traceback.print_exc()
    
    def instantCorrect(self):
        with shelve.open(self.path, writeback=True) as db:
            first_keys_len = len(db[list(db.keys())[0]])
            max_key_len = 0
            for i in db.keys():
                if max_key_len < len(db[i]):
                    max_key_len = len(db[i])
            if max_key_len != first_keys_len:
                print("first_keys_len: ", first_keys_len, " max_key_len: ", max_key_len)
            keys_to_pop = []
            for i in db.keys():
                if len(db[i]) < max_key_len:
                    diff = max_key_len - len(db[i])
                    if diff > 1:
                        print("1 den fazla kaymış! hemen database'i incele!")
                        return -1
                    elif diff == 1:
                        keys_to_pop.append(i)
            for i in range(len(keys_to_pop)):
                db[keys_to_pop[i]].pop()
            return 1
            

##    @staticmethod
    def showSome(self):
        with shelve.open(self.path) as db:
            for i in db.keys():
                print("column ", i, " length: ", len(db[i]))
            for i in db.keys():
                print("column ", i, " elements: ")
                for k in range(len(db[i])):
                    print(db[i][k])
        db.close()

    # def convertCableCordsTo2DMatrix(self, cartesian_cords, transList, inch, x_w, y_w):
    def convertCableCordsTo2DMatrix(self, cartesian_cords, transList, inch, x_w, y_w):
        arr_2D = [[0 for i in range(y_w)] for j in range(x_w)]
        arr_2D_trans = [[0 for i in range(y_w)] for j in range(x_w)]
        x_width_cm = inch * 2.54 / 18.357559 * 16 # 16^2 + 9^2 = 18.35^2
        cm_step = x_width_cm / x_w
        for i in range(len(cartesian_cords) - 1):
            x1 = cartesian_cords[i][0]
            x2 = cartesian_cords[i+1][0]
            y1 = cartesian_cords[i][1]
            y2 = cartesian_cords[i+1][1]
            y_diff = (y2 - y1)
            x_diff = (x2 - x1)
            tangent = 0
            if x_diff != 0:
                tangent = y_diff / x_diff
            if abs(x_diff) >= abs(y_diff):
                lgt = int(abs(x_diff) / cm_step * 10) + 1
                step = cm_step / 10
                if x_diff < 0:
                    step = step * (-1)
                for j in range(lgt):
                    x_tmp = x1 + j * step
                    y_tmp = y1 + tangent * j * step
                    x_int = int(x_tmp / cm_step)
                    y_int = int(y_tmp / cm_step)
                    val = 1
                    if transList[i]:
                        # val = 2
                        arr_2D_trans[x_int][y_int] = val
                    arr_2D[x_int][y_int] = val
            else:
                lgt = int(abs(y_diff) / cm_step * 10) + 1
                step = cm_step / 10
                if y_diff < 0:
                    step = step * (-1)
                for j in range(lgt):
                    y_tmp = y1 + j * step
                    if tangent != 0:
                        x_tmp = x1 + j * step / tangent
                    else:
                        x_tmp = x1
                    x_int = int(x_tmp / cm_step)
                    y_int = int(y_tmp / cm_step)
                    val = 1
                    if transList[i]:
                        # val = 2
                        arr_2D_trans[x_int][y_int] = val
                    arr_2D[x_int][y_int] = val

        return arr_2D, arr_2D_trans

    def findCableIndex(self, tag):
        # card_list = ['mb', 'ursa', 'psu', 'tcon', 'wlan', 'xBoard']
        card_list = st.card_list
        # conList = ['LVDS','VBY1','MLVDS','WIFI','DC','AC','FPC','BT_ANT','WF_ANT','SPK', 'USB', 'HDMI', 'TER', 'SAT','TER&SAT', 'IRKEY']
        conList = st.conList
        cable_dict = st.cable_dict
        keys = tag.split('-')
        tmp_chc = []
        if keys[0] in conList:
            # print("girdi")
            tmp_chc.append(keys[0])
            for i in card_list:
                if i in tag:
                    tmp_chc.append(i)
            # print(tmp_chc)
            if len(tmp_chc) == 3:
                tmp_key1 = tmp_chc[0] + '-' + tmp_chc[1] + '-' + tmp_chc[2]
                tmp_key2 = tmp_chc[0] + '-' + tmp_chc[2] + '-' + tmp_chc[1]
                print(tmp_key1)
                if tmp_key1 in cable_dict:
                    return cable_dict[tmp_key1]
                elif tmp_key2 in cable_dict:
                    return cable_dict[tmp_key2]
            elif len(tmp_chc) == 2:
                tmp_key1 = tmp_chc[0] + '-' + tmp_chc[1]
                if tmp_key1 in cable_dict:
                    return cable_dict[tmp_key1]
            return -1
        else:
            return -1

    def convertScrewCordsTo2DMatrix(self, cartesian_cords, inch, x_w, y_w):
        arr_2D = [[0 for i in range(y_w)] for j in range(x_w)]
        x_width_cm = inch * 2.54 / 18.357559 * 16 # 16^2 + 9^2 = 18.35^2
        cm_step = x_width_cm / x_w
        if cartesian_cords == None:
            return arr_2D
        for i in range(len(cartesian_cords)):
            x1 = cartesian_cords[i][0]
            y1 = cartesian_cords[i][1]
            x_int = int(x1 / cm_step)
            y_int = int(y1 / cm_step)
            arr_2D[x_int][y_int] = 1
        return arr_2D

    def convertCardCordsTo2DMatrix(self, cartesian_cords, inch, x_w, y_w):
        arr_2D = [[0 for i in range(y_w)] for j in range(x_w)]
        x_width_cm = inch * 2.54 / 18.357559 * 16 # 16^2 + 9^2 = 18.35^2
        cm_step = x_width_cm / x_w

        if cartesian_cords == None:
            return arr_2D

        x1 = cartesian_cords[0]
        x2 = cartesian_cords[2]
        y1 = cartesian_cords[1]
        y2 = cartesian_cords[3]

        x_min = min(int(x1/cm_step), int(x2/cm_step))
        x_max = max(int(x1/cm_step), int(x2/cm_step))
        y_min = min(int(y1/cm_step), int(y2/cm_step))
        y_max = max(int(y1/cm_step), int(y2/cm_step))

        for i in range(x_max - x_min + 1):
            for j in range(y_max - y_min + 1):
                arr_2D[x_min + j][y_min + i] = 1
        return arr_2D

    def convertEmiCordsTo2DMatrix(self, cartesian_cords, inch, x_w, y_w):
        arr_2D = [[0 for i in range(y_w)] for j in range(x_w)]
        x_width_cm = inch * 2.54 / 18.357559 * 16 # 16^2 + 9^2 = 18.35^2
        cm_step = x_width_cm / x_w

        if cartesian_cords == None:
            return arr_2D

        x1 = cartesian_cords[0]
        x2 = cartesian_cords[2]
        y1 = cartesian_cords[1]
        y2 = cartesian_cords[3]

        x_min = min(int(x1/cm_step), int(x2/cm_step))
        x_max = max(int(x1/cm_step), int(x2/cm_step))
        y_min = min(int(y1/cm_step), int(y2/cm_step))
        y_max = max(int(y1/cm_step), int(y2/cm_step))

        for i in range(x_max - x_min + 1):
            for j in range(y_max - y_min + 1):
                arr_2D[x_min + i][y_min + j] = 1
        return arr_2D

    def findEmiTapeIndex(self, tag):
        card_list = st.card_list
        conList = st.conList
        emi_tape_dict = st.emi_tape_dict
        keys = tag.split(',')
        tmp_keys = []
        tmp_chc = []
        if 'backplane' not in keys:
            return [-1]
        for i in range(len(keys)):
            if keys[i] == 'backplane':
                continue
            if keys[i] == 'mainboard':
                tmp_keys.append('mb')
                continue

            tmp_strng_arr = keys[i].split('-')
            if '-con' in keys[i]:
                tmp_card = ""
                for j in card_list:
                    if j in tmp_strng_arr[0]:
                        tmp_card = j
                tmp_string  = tmp_card + '-' + tmp_strng_arr[1] + '-' + tmp_strng_arr[3]
                tmp_keys.append(tmp_string)
                continue

            if len(tmp_strng_arr) == 1:
                for j in card_list:
                    if j in keys[i]:
                        tmp_keys.append(j)
                        continue

            if len(tmp_strng_arr) > 1:
                tmp_str = ""
                tmp_cards = []
                for j in conList:
                    if j in keys[i]:
                        for k in card_list:
                            if k in keys[i]:
                                tmp_cards.append(k)
                        if len(tmp_cards) == 1:
                            tmp_str = j + '-' + tmp_cards[0]
                            tmp_keys.append(tmp_str)
                        if len(tmp_cards) == 2:
                            tmp_str = j + '-' + tmp_cards[0] + '-' + tmp_cards[1]
                            tmp_keys.append(tmp_str)
                            tmp_str2 = j + '-' + tmp_cards[1] + '-' + tmp_cards[0]
                            tmp_keys.append(tmp_str2)
        tmp_indexes = []
        for i in range(len(tmp_keys)):
            if tmp_keys[i] not in emi_tape_dict:
                continue
            tmp_index = emi_tape_dict[tmp_keys[i]]
            if tmp_index != -1:
                tmp_indexes.append(tmp_index)
        if len(tmp_indexes) > 0:
            return tmp_indexes
        return [-1]

    def findFerritIndex(self, tag):
        card_list = st.card_list
        conList = st.conList
        ferrit_dict = st.ferrit_dict
        keys = tag.split(',')
        tmp_keys = []
        tmp_chc = []
        for i in range(len(keys)):
            if keys[i] == 'backplane':
                continue
            if keys[i] == 'mainboard':
                continue
            tmp_strng_arr = keys[i].split('-')
            if '-con' in keys[i]:
                continue

            if len(tmp_strng_arr) == 1:
                continue

            if len(tmp_strng_arr) > 1:
                tmp_str = ""
                tmp_cards = []
                for j in conList:
                    if j in keys[i]:
                        for k in card_list:
                            if k in keys[i]:
                                tmp_cards.append(k)
                        if len(tmp_cards) == 1:
                            tmp_str = j + '-' + tmp_cards[0]
                            tmp_keys.append(tmp_str)
                        if len(tmp_cards) == 2:
                            tmp_str = j + '-' + tmp_cards[0] + '-' + tmp_cards[1]
                            tmp_keys.append(tmp_str)
                            tmp_str2 = j + '-' + tmp_cards[1] + '-' + tmp_cards[0]
                            tmp_keys.append(tmp_str2)
        tmp_indexes = []
        for i in range(len(tmp_keys)):
            if tmp_keys[i] not in ferrit_dict:
                continue
            tmp_index = ferrit_dict[tmp_keys[i]]
            if tmp_index != -1:
                tmp_indexes.append(tmp_index)
        if len(tmp_indexes) > 0:
            return tmp_indexes
        return [-1]

if __name__ == "__main__":
    app = SampleApp()

    app.mainloop()
