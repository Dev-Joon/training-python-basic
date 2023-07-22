# ch08_01_AutoConnect.py
from pywinauto import application
import os, time

def AutoConnect():
    os.system('taskkill /IM coStarter* /F /T')
    os.system('taskkill /IM CpStart* /F /T')
    os.system('taskkill /IM DibServer* /F /T')
    os.system('wmic process where "name like \'%coStarted%\'" call terminate')
    os.system('wmic process where "name like \'%CpStart%\'" call terminate')
    os.system('wmic process where "name like \'%DibServer%\'" call terminate')

    time.sleep(5)
    app = application.Application()
    app.start('C:\CREON\STARTER\coStarter.exe /prj:cp '
            '/id:closeplz /pwd:A511202! /pwdcert:A511202a!@#0130 /autostart')
    time.sleep(5)