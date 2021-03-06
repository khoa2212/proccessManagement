import mysql.connector
import time
import os
from datetime import datetime, date
import threading
from pynput import keyboard
from threading import Thread
import dropbox
from dropbox.files import WriteMode
from pathlib import Path
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
    mycusor.execute('select ID, Time_format(StartTime, "%H:%i") , Time_format(EndTime, "%H:%i"), Time_format(StartTimeAgain, "%H:%i") from ManageTime')
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


#-----------------------------------------------------------------------
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
        print('SHUT DOWN')

#---------------------------------------------------------------
# C??ng vi???c (a) C2.1.2.2
def printMessage():
    global STime
    global ETime
    print('YOU ARE ACCEPTED USING COMPUTER FROM ' + datetime.strftime(STime, '%H:%M') + ' TO ' + datetime.strftime(ETime, '%H:%M'))

# C??ng vi???c (b) C2.1.2.2
def caculateTime():
    global STime
    global ETime
    global StartTimeAgain

    now = datetime.now()
    current_time = now.strftime('%H:%M')
    current_time = datetime.strptime(current_time, '%H:%M')
    distance = ETime - current_time
    print('TIME LEFT: ' + str(distance.total_seconds() / 60))
    print('YOU CAN TURN ON COMPUTER AGAIN IN: ' + datetime.strftime(StartTimeAgain, '%H:%M'))

def on_press(key):
    global inputString
    # print(f"Key pressed: {key}")
    inputString = inputString + str(key) + ', '


def writeCharacterToFile(inputTime, inputDay, keyboardString):
    f = open('DataKeyBoard.txt', 'a')
    f.write(
        'Day: ' + str(inputDay) + ' Time: ' + inputTime + ' KeyBoard: ' + str(keyboardString.encode('utf-8')) + '\n')
    Token = 'sl.BACAlYPG-VEauQ4mtvkglcU6kNbfrCbr-VO267rkdHG5p5YZcVp4KseycQVW3Kk8vXylpudMIQzx6-sQBPFwsnP8AdExhqu6rIB-2K5BQltNYuwHvAi-WmtYccSwnBKzVUIYPsxObLVZ'
    f.close()
    if os.stat("DataKeyBoard.txt").st_size != 0:
        dbx = dropbox.Dropbox(Token)
        with open('DataKeyBoard.txt', 'rb') as file:
            dbx.files_upload(file.read(), '/upload.txt', mode=WriteMode('overwrite'))

def saveKeyboardhit():
    print('CATCH EVENT KEYBOARD CALL')
    today = date.today()
    now = datetime.now()
    current_time = now.strftime('%H:%M')
    with keyboard.Listener(on_press=on_press) as ls:
        def time_out(period_sec: int):
            global inputString
            time.sleep(period_sec)  # Listen to keyboard for period_sec seconds
            if inputString != '':
                writeCharacterToFile(str(today), current_time, inputString)
                # mycusor.execute('insert ManageKeyBoard values(%s, %s, %s)', (today, current_time, inputString))
                # mydb.commit()
                inputString = ''
            ls.stop()
        Thread(target=time_out, args=(2.0,)).start()
        ls.join()

def checkData():
    global STime
    global ETime
    global StartTimeAgain
    print('CHECK DATA CALL')
    mydb.commit()
    data = getData()
    print(datetime.strptime(data[0][2], '%H:%M'))
    if STime != datetime.strptime(data[0][1], '%H:%M') or ETime != datetime.strptime(data[0][2], '%H:%M'):
        STime = datetime.strptime(data[0][1], '%H:%M')
        ETime = datetime.strptime(data[0][2], '%H:%M')
        StartTimeAgain = datetime.strptime(data[0][3], '%H:%M')
        printMessage()
        caculateTime()

def isFinish():
    global ETime
    global StartTimeAgain

    print('CHECK FINSIHTIME CALL')
    now = datetime.now()
    current_time = now.strftime('%H:%M')
    current_time = datetime.strptime(current_time, '%H:%M')
    distance = ETime - current_time
    distance = distance.total_seconds() / 60
    if distance <= 0:
        print('SHUT DOWN')
        exit(0)
    elif distance <= 1:
        caculateTime()

if __name__ == '__main__':
    StopThread = False
    ChildrenPass = '123'
    ParentsPass = '1234'
    Pass = ''
    inputString = ''
    now = datetime.now()
    current_time = now.strftime('%H:%M')
    data = getData()
    STime = data[0][1]
    ETime = data[0][2]
    StartTimeAgain = data[0][3]
    current_time = datetime.strptime(current_time, '%H:%M')
    STime = datetime.strptime(STime, '%H:%M')
    ETime = datetime.strptime(ETime, '%H:%M')
    StartTimeAgain = datetime.strptime(StartTimeAgain, '%H:%M')

    CheckPass = getPassword(Pass, ParentsPass) # L???y m???t kh???u t??? b??n ph??m
    if CheckPass:
        # L?? m???t kh???u ph??? huynh
        count = 0
        while True:
            time.sleep(1)  # ?????i 60 ph??t sau ???? quay l???i b?????c C0 h???i m???t kh???u (b?????c C1)
            count = count + 1
            if count == 3:
                count = 0
                verifyPass = verifyPassParent(Pass, ParentsPass)
                if not verifyPass:
                    print('SHUT DOWN')
                    exit(0)
    else:
        # Kh??ng l?? m???t kh???u ph??? huynh
        checkT = checkTime(STime, ETime, current_time) # Ki???m tra th???i gian c?? trong khung gi??? cho ph??p
        if checkT: # ???????c s??? d???ng m??y C2.1.2
            verifyPass = verifyPassChildren(Pass, ChildrenPass) #C2.1.2.1 ki??m tra xem c?? l?? m???t kh???u tr???
            if not verifyPass:
                # Nh???p sai 3 l???n v?? kh??ng d??ng ???????c m??y sau ???? kh??o b??n ph??m v?? chu???t ?????i 10 ph??t r???i t??t m??y
                print('LOCK MOUSE')
                print('LOCK KEYBOARD')
                time.sleep(3)
                print('SHUT DOWN')
            else:
                # Nh???p ????ng m???t kh???u tr??? th?? th???c hi???n 3 c??ng vi???c
                # L???y d??? li???u th??ng b??o kho???ng th???i gian s??? d???ng
                printMessage()
                # ????a ra th??ng b??o c??n bao nhi??u ph??t th?? k???t th??c v?? th???i gian ti???p theo b???t l??n
                caculateTime()
                while True:
                    p1 = threading.Thread(target=saveKeyboardhit)
                    p2 = threading.Thread(target=checkData())
                    p3 = threading.Thread(target=isFinish())
                    p1.start()
                    p2.start()
                    p3.start()
                    time.sleep(10)
        else: # kh??ng ???????c s??? d???ng m??y C2.1.1
            # Ch???y song song hai c??ng vi???c: ki???m tra 15s v?? nh???p m???t kh???u ph??? huynh ????ng l??c th?? d???ng t???t m??y
            p1 = threading.Thread(target=countTime)
            p2 = threading.Thread(target=Login(Pass, ParentsPass))
            p1.start()
            p2.start()
            count = 0
            if StopThread: # Bi???n to??n c???c ????? d???ng ti???n tr??nh ki???m tra 15s sau ???? t???t m??y
                while True:
                    time.sleep(1) # ?????i 60 ph??t sau ???? quay l???i b?????c C0 h???i m???t kh???u (b?????c C1)
                    count = count + 1
                    if count == 3:
                        count = 1
                        verifyPass = verifyPassParent(Pass, ParentsPass)
                        if not verifyPass:
                            # Nh???p sai m???t kh???u ph??? huynh 3 l???n th?? kh??a ph??m, chu???t ?????i 10 ph??t t???t m??y
                            print('LOCK MOUSE')
                            print('LOCK KEYBOARD')
                            time.sleep(3)
                            print('SHUT DOWN')
                            exit(0)