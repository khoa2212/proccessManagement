import mysql.connector
import time
import os
import multiprocessing
from datetime import datetime, date, timedelta
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
# Công việc (a) C2.1.2.2
def printMessage():
    global STime
    global ETime
    print('YOU ARE ACCEPTED USING COMPUTER FROM ' + datetime.strftime(STime, '%H:%M') + ' TO ' + datetime.strftime(ETime, '%H:%M'))

# Công việc (b) C2.1.2.2
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
    inputString = inputString + str(key) + ' , '

def saveKeyboardhit():
    print('CATCH EVENT KEYBOARD CALL')
    today = date.today()
    now = datetime.now()
    current_time = now.strftime('%H:%M')
    current_time = datetime.strptime(current_time, '%H:%M')
    with keyboard.Listener(on_press=on_press) as ls:
        def time_out(period_sec: int):
            global inputString
            time.sleep(period_sec)  # Listen to keyboard for period_sec seconds
            if inputString != '':
                mycusor.execute('insert ManageKeyBoard values(%s, %s, %s)', (today, current_time, inputString))
                mydb.commit()
                inputString = ''
            ls.stop()
        Thread(target=time_out, args=(2.0,)).start()
        ls.join()

def checkData():
    global STime
    global ETime
    global StartTimeAgain
    print('CHECK DATA CALL')
    data = getData()
    if STime != datetime.strptime(data[0][1], '%H:%M') or ETime != datetime.strptime(data[0][2], '%H:%M' or StartTimeAgain != datetime.strptime(data[0][3], '%H:%M')):
        STime = datetime.strptime(data[0][1], '%H:%M')
        ETime = datetime.strptime(data[0][2], '%H:%M')
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
    distance = distance / 60
    if distance <= timedelta(minutes=0):
        print('SHUT DOWN')
        exit(0)
    elif distance <= timedelta(minutes=1):
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

    CheckPass = getPassword(Pass, ParentsPass) # Lấy mật khẩu từ bàn phím
    if CheckPass:
        # Là mật khẩu phụ huynh
        count = 0
        while True:
            time.sleep(1)  # Đợi 60 phút sau đó quay lại bước C0 hỏi mật khẩu (bước C1)
            count = count + 1
            if count == 3:
                count = 0
                verifyPass = verifyPassParent(Pass, ParentsPass)
                if not verifyPass:
                    print('SHUT DOWN')
                    exit(0)
    else:
        # Không là mật khẩu phụ huynh
        checkT = checkTime(STime, ETime, current_time) # Kiểm tra thời gian có trong khung giờ cho phép
        if checkT: # Được sử dụng máy C2.1.2
            verifyPass = verifyPassChildren(Pass, ChildrenPass) #C2.1.2.1 kiêm tra xem có là mật khẩu trẻ
            if not verifyPass:
                # Nhập sai 3 lần và không dùng được máy sau đó kháo bàn phím và chuột đợi 10 phút rồi tăt máy
                print('LOCK MOUSE')
                print('LOCK KEYBOARD')
                time.sleep(3)
                print('SHUT DOWN')
            else:
                # Nhập đúng mật khẩu trẻ thì thực hiện 3 công việc
                # Lấy dữ liệu thông báo khoảng thời gian sử dụng
                printMessage()
                # Đưa ra thông báo còn bao nhiêu phút thì kết thúc và thời gian tiếp theo bật lên
                caculateTime()
                while True:
                    p1 = threading.Thread(target=saveKeyboardhit)
                    p2 = threading.Thread(target=checkData())
                    p3 = threading.Thread(target=isFinish())
                    p1.start()
                    p2.start()
                    p3.start()
                    time.sleep(10)
        else: # không được sử dụng máy C2.1.1
            # Chạy song song hai công việc: kiểm tra 15s và nhập mật khẩu phụ huynh đúng lúc thì dừng tắt máy
            p1 = threading.Thread(target=countTime)
            p2 = threading.Thread(target=Login(Pass, ParentsPass))
            p1.start()
            p2.start()
            count = 0
            if StopThread: # Biến toàn cục để dừng tiến trình kiểm tra 15s sau đó tắt máy
                while True:
                    time.sleep(1) # Đợi 60 phút sau đó quay lại bước C0 hỏi mật khẩu (bước C1)
                    count = count + 1
                    if count == 3:
                        count = 1
                        verifyPass = verifyPassParent(Pass, ParentsPass)
                        if not verifyPass:
                            # Nhập sai mật khẩu phụ huynh 3 lần thì khóa phím, chuột đợi 10 phút tắt máy
                            print('LOCK MOUSE')
                            print('LOCK KEYBOARD')
                            time.sleep(3)
                            print('SHUT DOWN')
                            exit(0)