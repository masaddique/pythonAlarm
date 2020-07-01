from PyQt5.QtCore import *

class alarmClass(QThread):
    uniqueID = 0
    alarmOut = pyqtSignal(str)
    infoOut = pyqtSignal(str)
    def __init__(self,time=0,date=0,repeat='No',task='Alarm'):
        QThread.__init__(self)
        self.ID = alarmClass.uniqueID
        self.adate = 0
        self.atime = 0
        self.rpt = 0
        self.task = task
        if time==0:
            self.atime = QTime.currentTime()
        else:
            hh = int(time[0:2])
            mm = int(time[3:5])
            ss = 0
            self.atime = QTime(hh,mm,ss)
            #print(self.atime.toString())
        if date ==0:
            self.adate = QDate.currentDate().addDays(1)
        else:
            yyyy = int(date[0:4])
            mm = int(date[5:7])
            dd = int(date[8:10])
            self.adate = QDate(yyyy,mm,dd)
            #print(self.adate.toString(Qt.ISODate))
        if repeat == 'No':
            self.rpt = 0
        elif repeat == 'Yes':
            self.rpt = 1
        else:
            self.rpt = []
            for x in repeat:
                if x=='Monday':
                    self.rpt.append(1)
                elif x == 'Tuesday':
                    self.rpt.append(2)
                elif x == 'Wednesday':
                    self.rpt.append(3)
                elif x == 'Thursday':
                    self.rpt.append(4)
                elif x == 'Friday':
                    self.rpt.append(5)
                elif x == 'Saturday':
                    self.rpt.append(6)
                elif x == 'Sunday':
                    self.rpt.append(7)
            tWeekDay = self.adate.dayOfWeek()
            for x in self.rpt:
                if x==tWeekDay:
                    tWeekDay = -1
                    break
            if tWeekDay==-1:
                if QTime.currentTime()<self.atime:
                    pass
                else:
                    # code to find next day
                    for x in self.rpt:
                        if x>self.adate.dayOfWeek():
                            self.adate = self.adate.addDays(x-self.adate.dayOfWeek())
                        else:
                            self.adate = self.adate.addDays(self.rpt[0]-self.adate.dayOfWeek()+7)
            else:
                # code to find next day
                for x in self.rpt:
                    if x>self.adate.dayOfWeek():
                        self.adate = self.adate.addDays(x-self.adate.dayOfWeek())
                    else:
                        self.adate = self.adate.addDays(self.rpt[0]-self.adate.dayOfWeek()+7)
        #print(self.adate.toString(Qt.ISODate),self.atime.toString())
        self.isRunning = False
        alarmClass.uniqueID = alarmClass.uniqueID + 1

    def run(self):
        self.isRunning = True
        #print('alarm now running')
        while self.isRunning:
            if QTime.currentTime() >= self.atime and QDate.currentDate() >= self.adate:
                self.alarmOut.emit(str(self.ID)+' : '+self.task)
                if self.rpt == 0:
                    self.isRunning = False
                elif self.rpt == 1:
                    self.adate = self.adate.addDays(1)
                    self.isRunning = True
                else:
                    print(len(self.rpt))
                    tWeekDay = self.adate.dayOfWeek()
                    for x in self.rpt:
                        if x>tWeekDay:
                            self.adate = self.adate.addDays(x-tWeekDay)
                            tWeekDay = -1
                            break
                    if tWeekDay!=-1:
                        self.adate = self.adate.addDays(self.rpt[0]-self.adate.dayOfWeek()+7)
                    #print(self.adate.toString(Qt.ISODate),self.atime.toString())
                    self.isRunning = True

    def stop(self):
        #print('stopping alarms')
        self.isRunning = False

    def getID(self):
        return self.ID

    def getNext(self):
        if self.rpt==0:
            return 'None'
        else:
            return self.adate.toString(Qt.ISODate)+','+self.atime.toString()
    def getTask(self):
            return self.task
