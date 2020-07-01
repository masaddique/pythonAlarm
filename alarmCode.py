from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtWidgets
from alarmClass import alarmClass


class alarmInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('alarm.ui',self)
        self.show()
        self.exitBtn = self.findChild(QPushButton, 'exitBtn')
        self.exitBtn.clicked.connect(self.exitFunction)
        self.saveBtn = self.findChild(QPushButton, 'saveBtn')
        self.saveBtn.clicked.connect(self.saveFunction)
        self.addBtn = self.findChild(QToolButton, 'addBtn')
        self.addBtn.clicked.connect(self.addAlarmFunction)
        self.delBtn = self.findChild(QToolButton, 'delBtn')
        self.delBtn.clicked.connect(self.delAlarmFunction)
        self.inTime = self.findChild(QTimeEdit,'timeEdit')
        self.inDate = self.findChild(QDateEdit,'dateEdit')
        self.onceRadio = self.findChild(QRadioButton,'onceRadio')
        self.repeatRadio = self.findChild(QRadioButton,'repeatRadio')
        self.weekChk = self.findChildren(QCheckBox)
        self.desText = self.findChild(QPlainTextEdit,'desText')
        self.alarmList = self.findChild(QTableWidget,'alarmList')
        self.alarmList.cellClicked.connect(self.cellSelectFunction)
        self.timeLabel = self.findChild(QLabel,'timeLabel')

        self.alarmThread = []
        self.alarmString = []
        self.alarmThreadCount = 0

        self.selectedCellX = -1
        self.selectedCellY = -1

        self.onceRadio.setChecked(True)
        self.inTime.setTime(QTime.currentTime())
        self.inDate.setDate(QDate.currentDate())

        self.clockTimer = QTimer(self)
        self.clockTimer.setInterval(1000)
        self.clockTimer.timeout.connect(self.updateClock)
        self.clockTimer.start()

        #ac  = alarmClass()
        #ac.alarmOut.connect(self.alarmHasGone)

    def saveFunction(self):
        pass

    def alarmHasGone(self,info):
        QMessageBox.information(self, 'info','Alarm ' + info)

    def exitFunction(self):
        for x in self.alarmThread:
            x.stop()
        self.close()

    def cellSelectFunction(self, x=0, y=0):
        #QMessageBox.information(self,'info',str(x) +','+str(y))
        self.selectedCellX = x
        self.selectedCellY = y

    def addAlarmFunction(self):
        rptStr = ''
        if self.onceRadio.isChecked():
            rptStr = 'No'
            weeks = 'No'
        elif self.repeatRadio.isChecked():
            weeks = []
            for x in self.weekChk:
                if x.isChecked():
                    weeks.append(x.text())
                    rptStr = rptStr + x.text() + ','
            if len(weeks)==7:
                rptStr = 'Daily'
                weeks = 'Daily'
        des = self.desText.toPlainText()


        self.alarmThread.append(alarmClass(self.inTime.time().toString(),self.inDate.date().toString(Qt.ISODate),weeks,des))
        #print(len(self.alarmThread), self.alarmThreadCount)
        self.alarmThread[self.alarmThreadCount].alarmOut.connect(self.alarmHasGone)
        self.alarmThread[self.alarmThreadCount].start()
        self.alarmThreadCount = 1 + self.alarmThreadCount

        n = self.alarmList.rowCount()
        self.alarmList.insertRow(n)
        self.alarmList.setItem(n,0,QTableWidgetItem(str(n+1)))
        self.alarmList.setItem(n,1,QTableWidgetItem(str(self.alarmThread[self.alarmThreadCount-1].getID())))
        self.alarmList.setItem(n,2,QTableWidgetItem(des))
        self.alarmList.setItem(n,3,QTableWidgetItem(self.inTime.time().toString()))
        self.alarmList.setItem(n,4,QTableWidgetItem(self.inDate.date().toString(Qt.ISODate)))
        self.alarmList.setItem(n,5,QTableWidgetItem(rptStr))
        self.inTime.setTime(QTime.currentTime())
        self.inDate.setDate(QDate.currentDate())
        #self.alarmThreadCount = self.alarmThreadCount + 1


    def delAlarmFunction(self):
        if self.selectedCellX==-1:
            return
        resp = QMessageBox.information(self,'????', 'Do you really want to delete this alarm???', QMessageBox.Yes|QMessageBox.No)
        if resp == QMessageBox.Yes:
            IDtoDelete = int(self.alarmList.item(self.selectedCellX,1).text())
            i = -1
            j = 0
            for x in self.alarmThread:
                if IDtoDelete==x.getID():
                   i = j
                j = j + 1
            if i!=-1:
                self.alarmThread[i].stop()
                self.alarmThread.pop(i)
                self.alarmThreadCount = self.alarmThreadCount - 1
                self.alarmList.removeRow(self.selectedCellX)
                self.alarmThreadCount = self.alarmThreadCount - 1
                for x in range(self.alarmList.rowCount()):
                    self.alarmList.setItem(x,0,QTableWidgetItem(str(x+1)))
                self.selectedCellX = -1
            else:
                QMessageBox.information(self,'info','Error while deleting alarm???',QMessageBox.Yes)

    def updateClock(self):
        self.timeLabel.setText(QTime.currentTime().toString())

app = QApplication(sys.argv)
window = alarmInterface()
sys.exit(app.exec())
