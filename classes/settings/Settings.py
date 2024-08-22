# Multi-frame tkinter application v2.3
import os
import sys
sys.path.insert(0, "..")
from classes.components.Cable import *

def init():
    global conList
    global card_list
    global mbCm
    global ursaCm
    global tConCm
    global psuCm
    global panelCm
    global emiTapeList
    global ferList
    global wlan_modules
    global wlan_modules_specs            
    global cable_dict
    global ferrit_dict
    global emi_tape_dict


    # do not put '-' in an where in or nearby to connector names. It will mess up the tag classification methods.
    # conList = ['LVDS','VBY1','MLVDS','WIFI','DC','AC','FPC','BT_ANT','WF_ANT','SPK']
    conList = ['LVDS','VBY1','MLVDS','WIFI','DC','AC','FPC','BT_ANT','WF_ANT','SPK', 'USB', 'HDMI', 'TER', 'SAT','TER&SAT', 'IRKEY', 'BACKLIGHT']
    card_list = ['mb', 'ursa', 'psu', 'tcon', 'wlan', 'xBoard', 'IRKEYMODULE', 'SPEAKER', 'pnl', 'LEDBAR']
    # 5cm * 1cm = [5,1]
    emiTapeList = [ [5,1], [5,5], [7,1] ]
    ferList = [ [2,3], [1,3] ]
    wlan_modules = ['ZJW920R','WDX920R','WDR920R','ZZX920R','WSC920R','WQR920R','WQS920R']
    wlan_modules_specs={'ZJW920R':[3,7,(0.8,1.4)],
                        'WDX920R':[4.65,4,(0.3,3.2)],
                        'WDR920R':[4.65,4,(0.3,3.2)],
                        'ZZX920R':[3,7,(0.8,1.4)],
                        'WSC920R':[4.65,4,(0.3,3.2)],
                        'WQR920R':[4.65,4,(0.3,3.2)],
                        'WQS920R':[4.65,4,(0.3,3.2)]}#X'te en (cm),Y'de boy cm, konektör koordinat (x,y) cm)

    mbCm = 30
    ursaCm = 30
    tConCm = 30
    psuCm = 30
    panelCm = 10
    
    ## for Cable types Array reference please check the Excel File
    cable_dict = {
        'LVDS-mb-tcon': 0,
        'LVDS-mb-ursa': 1,
        'LVDS-mb-xBoard': 2,
        'LVDS-ursa-tcon': 3,
        'LVDS-ursa-xBoard': 4,
        'LVDS-tcon-xBoard': 5,
        'LVDS-xBoard-xBoard': 6,
        'VBY1-mb-tcon': 7,
        'VBY1-mb-ursa': 8,
        'VBY1-mb-xBoard': 9,
        'VBY1-ursa-tcon': 10,
        'VBY1-ursa-xBoard': 11,
        'VBY1-tcon-xBoard': 12,
        'VBY1-xBoard-xBoard': 13,
        'MLVDS-mb-xBoard': 14,
        'MLVDS-ursa-xBoard': 15,
        'MLVDS-tcon-xBoard': 16,
        'MLVDS-xBoard-xBoard': 17,
        'WIFI-mb-wlan': 18,
        'WIFI-ursa-wlan': 19,
        'DC-psu-mb': 20,
        'DC-psu-ursa': 21,
        'DC-psu-tcon': 22,
        'DC-psu-xBoard': 23,
        'DC-psu-wlan': 24,
        'DC-mb-ursa': 25,
        'DC-mb-tcon': 26,
        'DC-mb-xBoard': 27,
        'DC-mb-wlan': 28,
        'DC-ursa-tcon': 29,
        'DC-ursa-xBoard': 30,
        'DC-ursa-wlan': 31,
        'DC-tcon-xBoard': 32,
        'DC-tcon-wlan': 33,
        'DC-xBoard-xBoard': 34,
        'AC-psu': 35,
        'FPC-psu-mb': 36,
        'FPC-mb-ursa': 37,
        'BT_ANT-mb': 38,
        'BT_ANT-wlan': 39,
        'WF_ANT-mb': 40,
        'WF_ANT-wlan': 41,   
        'SPK-mb': 42,
        'SPK-ursa': 43, 
        'HDMI-ursa-mb': 44,   
        'HDMI-mb-tcon': 45,   
        'HDMI-ursa-tcon': 46,  
        'IRKEY-mb': 47,   
        'IRKEY-ursa': 48,   
        'MLVDS-mb-pnl': 49,
        'MLVDS-ursa-pnl': 50,
        'MLVDS-tcon-pnl': 51,
        'LVDS-mb-pnl': 52,
        'LVDS-ursa-pnl': 53,
        'LVDS-tcon-pnl': 54,
        'BACKLIGHT-mb': 55,
        'BACKLIGHT-psu': 56,
        'MLVDS-pnl-pnl': 57
    }

    #shield map also be applied
    #Translit map also be applied

    ferrit_dict = {
        'LVDS-mb-tcon': 0,
        'LVDS-mb-ursa': 1,
        'LVDS-mb-xBoard': 2,
        'LVDS-ursa-tcon': 3,
        'LVDS-ursa-xBoard': 4,
        'LVDS-tcon-xBoard': 5,
        'LVDS-xBoard-xBoard': 6,
        'VBY1-mb-tcon': 7,
        'VBY1-mb-ursa': 8,
        'VBY1-mb-xBoard': 9,
        'VBY1-ursa-tcon': 10,
        'VBY1-ursa-xBoard': 11,
        'VBY1-tcon-xBoard': 12,
        'VBY1-xBoard-xBoard': 13,
        'MLVDS-mb-xBoard': 14,
        'MLVDS-ursa-xBoard': 15,
        'MLVDS-tcon-xBoard': 16,
        'MLVDS-xBoard-xBoard': 17,
        'WIFI-mb-wlan': 18,
        'WIFI-ursa-wlan': 19,
        'DC-psu-mb': 20,
        'DC-psu-ursa': 21,
        'DC-psu-tcon': 22,
        'DC-psu-xBoard': 23,
        'DC-psu-wlan': 24,
        'DC-mb-ursa': 25,
        'DC-mb-tcon': 26,
        'DC-mb-xBoard': 27,
        'DC-mb-wlan': 28,
        'DC-ursa-tcon': 29,
        'DC-ursa-xBoard': 30,
        'DC-ursa-wlan': 31,
        'DC-tcon-xBoard': 32,
        'DC-tcon-wlan': 33,
        'DC-xBoard-xBoard': 34,
        'AC-psu': 35,
        'FPC-psu-mb': 36,
        'FPC-mb-ursa': 37,
        'BT_ANT-mb': 38,
        'BT_ANT-wlan': 39,
        'WF_ANT-mb': 40,
        'WF_ANT-wlan': 41,   
        'SPK-mb': 42,
        'SPK-ursa': 43, 
        'HDMI-ursa-mb': 44,   
        'HDMI-mb-tcon': 45,   
        'HDMI-ursa-tcon': 46,  
        'IRKEY-mb': 47,   
        'IRKEY-ursa': 48, 
        'MLVDS-mb-pnl': 49,
        'MLVDS-ursa-pnl': 50,
        'MLVDS-tcon-pnl': 51,
        'LVDS-mb-pnl': 52,
        'LVDS-ursa-pnl': 53,
        'LVDS-tcon-pnl': 54,     
        'BACKLIGHT-mb': 55,
        'BACKLIGHT-psu': 56        
    }

    emi_tape_dict = {
        'LVDS-mb-tcon': 0,
        'LVDS-mb-ursa': 1,
        'LVDS-mb-xBoard': 2,
        'LVDS-ursa-tcon': 3,
        'LVDS-ursa-xBoard': 4,
        'LVDS-tcon-xBoard': 5,
        'LVDS-xBoard-xBoard': 6,
        'VBY1-mb-tcon': 7,
        'VBY1-mb-ursa': 8,
        'VBY1-mb-xBoard': 9,
        'VBY1-ursa-tcon': 10,
        'VBY1-ursa-xBoard': 11,
        'VBY1-tcon-xBoard': 12,
        'VBY1-xBoard-xBoard': 13,
        'MLVDS-mb-xBoard': 14,
        'MLVDS-ursa-xBoard': 15,
        'MLVDS-tcon-xBoard': 16,
        'MLVDS-xBoard-xBoard': 17,
        'WIFI-mb-wlan': 18,
        'WIFI-ursa-wlan': 19,
        'DC-psu-mb': 20,
        'DC-psu-ursa': 21,
        'DC-psu-tcon': 22,
        'DC-psu-xBoard': 23,
        'DC-psu-wlan': 24,
        'DC-mb-ursa': 25,
        'DC-mb-tcon': 26,
        'DC-mb-xBoard': 27,
        'DC-mb-wlan': 28,
        'DC-ursa-tcon': 29,
        'DC-ursa-xBoard': 30,
        'DC-ursa-wlan': 31,
        'DC-tcon-xBoard': 32,
        'DC-tcon-wlan': 33,
        'DC-xBoard-xBoard': 34,
        'AC-psu': 35,
        'FPC-psu-mb': 36,
        'FPC-mb-ursa': 37,
        'BT_ANT-mb': 38,
        'BT_ANT-wlan': 39,
        'WF_ANT-mb': 40,
        'WF_ANT-wlan': 41,   
        'SPK-mb': 42,
        'SPK-ursa': 43, 
        'HDMI-ursa-mb': 44,   
        'HDMI-mb-tcon': 45,   
        'HDMI-ursa-tcon': 46,  
        'IRKEY-mb': 47,   
        'IRKEY-ursa': 48,
        'psu': 49,
        'mb': 50,
        'ursa': 51,
        'tcon': 52,
        'xBoard': 53,
        'wlan': 54,
        'mb-con-HDMI': 55,
        'mb-con-USB': 56,
        'mb-con-SAT': 57,
        'mb-con-TER': 58,
        'mb-con-TER&SAT': 59,
        'mb-con-LVDS': 60,
        'mb-con-VBY1': 61,
        'mb-con-MLVDS': 62,
        'ursa-con-MLVDS': 63,
        'ursa-con-LVDS': 64,
        'ursa-con-VBY1': 65,
        'tcon-con-LVDS': 66,
        'tcon-con-VBY1': 67,
        'tcon-con-MLVDS': 68,
        'MLVDS-mb-pnl': 69,
        'MLVDS-ursa-pnl': 70,
        'MLVDS-tcon-pnl': 71,
        'LVDS-mb-pnl': 72,
        'LVDS-ursa-pnl': 73,
        'LVDS-tcon-pnl': 74, 
        'BACKLIGHT-mb': 76,
        'BACKLIGHT-psu': 77,
        'MLVDS-pnl-pnl': 78
    }

if __name__ == "__main__":
    app = SampleApp()

    app.mainloop()
