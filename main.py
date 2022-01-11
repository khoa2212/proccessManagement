import mysql.connector
import time
import os
import multiprocessing
from datetime import datetime, date
import threading
from pynput import keyboard
from threading import Thread

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='andy9999',
    port='3306',
    database='DatabaseProcess'
)
mycusor = mydb.cursor()


def getPassword(Pass, ParentsPass):
    Pass = input('Enter your password: ')
    if Pass == ParentsPass:
        print('YOU ARE ACCEPTED USING COMPUTER')
        return True
    else:
        return False


def verifyPassParent(Pass, ParentsPass):
    count = 0
    Pass = input('Enter your password again to verify you are parents or Enter STOP to stop program: ')
    if Pass == 'STOP':
        exit(0)
    if Pass != ParentsPass:
        while Pass != ParentsPass:
            print('Enter wrong password wait 3 second to enter again, enter max 3 times')
            count = count + 1
            if count == 3:
                return False
            time.sleep(3)
            Pass = input('Enter your password again to verify you are parents or Enter STOP to stop program: ')
            if Pass == 'STOP':
                exit(0)
    print('YOU ARE ACCEPTED USING COMPUTER')
    return True


def getData():
    mycusor.execute('select ID, Time_format(StartTime, "%H:%i") , Time_format(EndTime, "%H:%i") from ManageTime')
    data = mycusor.fetchall()
    return data


def verifyPassChildren(Pass, ChildrenPass):
    count = 0
    Pass = input('Enter your password again to verify you are children: ')
    if Pass != ChildrenPass:
        while Pass != ChildrenPass:
            print('Enter wrong password wait 3 second to enter again, enter max 3 times')
            count = count + 1
            if count == 3:
                return False
            time.sleep(3)
            Pass = input('Enter your password again to verify you are children: ')
    return True


def checkTime(Start, End, current_Time):
    if current_Time >= Start and current_Time <= End:
        return True
    else:
        print('YOU CAN NOT USE COMPUTER AT THIS TIME')
        return False


def Login(Pass, ParentsPass):
    global StopThread
    print('Enter Parents password to stop shutdown')
    CheckPass = getPassword(Pass, ParentsPass)
    if CheckPass == True:  # la mat khau phu huynh
        StopThread = True
    else:
        print('Enter wrong parent password wait a little second to shutdown computer')


def countTime():
    count = 0
    while count <= 5:
        time.sleep(1)
        count = count + 1

    if not StopThread:
        print('Shut DOWN')

def printMessage(STime, ETime): # cong viec a
    print('YOU ARE ACCEPTED USING COMPUTER FROM ' + datetime.strftime(STime, '%H:%M') + ' TO ' + datetime.strftime(ETime, '%H:%M'))

def caculateTime(ETime, current_time):
    distance = ETime - current_time
    print('TIME LEFT: ' + str(distance.total_seconds() / 60))

def on_press(key):
    global inputString
    print(f"Key pressed: {key}")
    inputString = inputString + str(key) + ' , '

def saveKeyboardhit():
    with keyboard.Listener(on_press=on_press) as ls:
        def time_out(period_sec: int):
            time.sleep(period_sec)  # Listen to keyboard for period_sec seconds
            ls.stop()
        Thread(target=time_out, args=(10.0,)).start()
        ls.join()

def checkData(STime, ETime, current_time):
    data = getData()
    if STime != datetime.strptime(data[0][1], '%H:%M') or ETime != datetime.strptime(data[0][2], '%H:%M'):
        STime = datetime.strptime(data[0][1], '%H:%M')
        ETime = datetime.strptime(data[0][2], '%H:%M')
        printMessage(STime, ETime)
        caculateTime(ETime, current_time)

def isFinish(ETime, current_time):
    distance = ETime - current_time
    distance = distance / 60
    if distance <= 0:
        print('SHUTDOWN')
    elif distance <= 1:
        caculateTime(ETime, current_time)

if __name__ == '__main__':
    StopThread = False
    ChildrenPass = '123'
    ParentsPass = '1234'
    Pass = ''
    inputString = ''
    saveKeyboardhit()
    print(inputString)
    # now = datetime.now()
    # current_time = now.strftime('%H:%M')
    # current_time = '6:00'
    # data = getData()
    # STime = data[0][1]
    # ETime = data[0][2]
    STime = '6:00'
    ETime = '6:45'
    current_time = '6:30'
    current_time = datetime.strptime(current_time, '%H:%M')
    STime = datetime.strptime(STime, '%H:%M')
    ETime = datetime.strptime(ETime, '%H:%M')
    CheckPass = getPassword(Pass, ParentsPass)
    if CheckPass:  # la mat khau phu huynh
        count = 0
        while True:
            time.sleep(1)
            count = count + 1
            if count == 3:
                count = 0
                verifyPass = verifyPassParent(Pass, ParentsPass)
                if not verifyPass:
                    print('SHUT DOWN')
                    exit(0)
    else:
        checkT = checkTime(STime, ETime, current_time)
        if checkT:
            verifyPass = verifyPassChildren(Pass, ChildrenPass)
            if not verifyPass:
                print('lock mouse')
                print('lock keyboard')
                time.sleep(3)
                print('SHUT DOWN')
            else:
                printMessage(STime, ETime)
                caculateTime(ETime, current_time)
        else:
            p1 = threading.Thread(target=countTime)
            p2 = threading.Thread(target=Login(Pass, ParentsPass))
            p1.start()
            p2.start()
            count = 0
            if StopThread:
                while True:
                    time.sleep(1)
                    count = count + 1
                    if count == 3:
                        count = 1
                        verifyPass = verifyPassParent(Pass, ParentsPass)
                        if not verifyPass:
                            print('SHUT DOWN')
                            exit(0)