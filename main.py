import mysql.connector
import time
import os
import multiprocessing
from datetime import datetime
import threading
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='andy9999',
    port='3306',
    database='DatabaseProcess'
)
mycusor = mydb.cursor()

ChildrenPass = '123'
ParentsPass = '1234'


def getPassword(Pass):
    Pass = input('Enter your password: ')
    if Pass == ParentsPass:
        return True
    else:
        return False


def verifyPassParent(Pass):
    count = 1
    time.sleep(3)  # dung 60 phut
    Pass = input('Enter your password again to verify you are parents: ')
    if Pass == ParentsPass:
        return True
    else:
        while Pass != ParentsPass:
            print('Enter wrong password wait 3 second to enter again, enter max 3 times')
            count = count + 1
            if count == 3:
                return False
            time.sleep(3)
            Pass = input('Enter your password again to verify you are parents: ')
    return True


def getData():
    mycusor.execute('select ID, Time_format(StartTime, "%H:%i") , Time_format(EndTime, "%H:%i") from ManageTime')
    data = mycusor.fetchall()
    return data


def verifyPassChildren(Pass):
    count = 1
    time.sleep(3)  # dung 60 phut
    Pass = input('Enter your password again to verify you are children: ')
    if Pass == ChildrenPass:
        return True
    else:
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

def Login(Pass):
  CheckPass = getPassword(Pass)
  if CheckPass == True:  # la mat khau phu huynh
      verifyPass = verifyPassParent(Pass)
      if verifyPass == True:
        print('SU DUNG MAY')
      else:
        print('SHUT DOWN')

def countTime():
    count = 1
    while count <= 5:
        count = count + 1
        time.sleep(1)
    print('Shut DOWN')
    return True

if __name__ == '__main__':
    Pass = ''
    #now = datetime.now()
    #current_time = now.strftime('%H:%M')
    # current_time = '6:00'
    #data = getData()
    #STime = data[0][1]
    #ETime = data[0][2]
    STime = '6:00'
    ETime = '6:45'
    current_time = '13:00'
    current_time = datetime.strptime(current_time, '%H:%M')
    STime = datetime.strptime(STime, '%H:%M')
    ETime = datetime.strptime(ETime, '%H:%M')
    CheckPass = getPassword(Pass)
    if CheckPass == True:  # la mat khau phu huynh
        verifyPass = verifyPassParent(Pass)
        if verifyPass == True:
            print('SU DUNG MAY')
        else:
            print('SHUT DOWN')
    else:
        checkT = checkTime(STime, ETime, current_time)
        if checkT == True:
            print('su dung')
        else:
            p1 = threading.Thread(target=countTime)
            p2 = threading.Thread(target=Login(Pass))
            p1.start()
            p2.start()