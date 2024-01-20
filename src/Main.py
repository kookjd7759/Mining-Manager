import sys
import random
import time
import datetime
import threading
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import DB
import Web
import Discord
import Style

VERSION = 'v1.0.0-Alpha'

RESTARTCODE = 100
ERRORTEXT = 'ERROR::-1'

STOP_BTN_NAME = 'Stop'
START_BTN_NAME = 'Start'
QUIT_BTN_NAME = 'Quit'
RESTART_BTN_NAME = 'Restart'

OPTION_GB_NAME = 'Option'
WEBHOOK_GB_NAME = 'WebHook'
CONSOLE_GB_NAME = 'Excution Console'

WINDOWSIZE_H = 900
WINDOWSIZE_V = 580

OPTION_WHEN_LIST = ['Connection loss / Hash reduction', 'Add device', 'Remove device']
OPTION_INFO_LIST = ['Device / Mining pool', 'time', 'Hash', 'Discovered problem', 'Presumptive problem']

def getNowTime():
    return datetime.datetime.now()

def getAddedTime(min):
    return getNowTime() + datetime.timedelta(minutes=min)



def getSetting(webhook, time, when_seq, info_seq):
    OK = Style.toBlue('O')
    NO = Style.toRed('X')

    stList = []
    stList.append('[Webhook]')
    stList.append(f') {Style.toLink(webhook)}')
    if Discord.connectionTest(webhook) == -1:
        stList.append(ERRORTEXT)
        return stList
    
    stList.append('[Checking time]')
    stList.append(f') {time} (min)')

    stList.append('[When]')
    for i in range(0, len(OPTION_WHEN_LIST)):
        st = f') {OPTION_WHEN_LIST[i]} '
        if when_seq[i] == '1':
            st += OK
        else:
            st += NO
        stList.append(st)
        
    stList.append('[Info]')
    for i in range(0, len(OPTION_INFO_LIST)):
        st = f') {OPTION_INFO_LIST[i]} '
        if info_seq[i] == '1':
            st += OK
        else:
            st += NO
        stList.append(st)
    
    return stList

def getErrorTxt(text):
    return Style.toRed(f'Error occurred :: \"{text}\"')

def getOneNetworkState(key):
    webreturn = Web.connection_test(Web.Url_dictionary[key][0])
    if webreturn == 200:
        return f'-> {Style.toGreen("Connected")}'
    else:
        return f'-> {Style.toRed(f"Disconnected {webreturn}")}'

# check the DataBase option setting format
def CheckingData():
    print('CheckingData()::Checking the Data format from option DataBase')
    when_seq = DB.loadWhen()
    info_seq = DB.loadInfo()
    time = DB.loadCheckingTime()
    if len(OPTION_WHEN_LIST) != len(when_seq) or len(OPTION_INFO_LIST) != len(info_seq) or time == '':
        print(' = Reset')
        DB.Reset_default_values()
        return False
    print(' = Clear')
    return True



class Timer(QThread):
    checking_signal = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.on = True
        self.sec = 0
        self.target_sec = -1
    
    def run(self):
        print('Start running Timer')
        print(f'self.target_sec = {self.target_sec}')
        while self.on == True:
            time.sleep(1)
            self.sec += 1
            print(f'time.. {self.sec}')

            if self.sec >= self.target_sec:
                print(f'Checking signal emit !!')
                self.checking_signal.emit()
                self.sec = 0
    
    def end(self):
        self.on = False
        self.quit()
        self.wait(5000)
        self.sec = 0


class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init()

        self.console = self.findChild(QTextEdit)
        self.gb_webhook = self.findChildren(QGroupBox)[0]
        self.gb_option = self.findChildren(QGroupBox)[1]
        self.gb_console = self.findChildren(QGroupBox)[3]

        self.btn_quit = self.findChildren(QPushButton)[4]
        self.btn_restart = self.findChildren(QPushButton)[5]
        self.btn_start = self.findChildren(QPushButton)[6]
        self.btn_stop = self.findChildren(QPushButton)[7]
        
        self.timer = Timer(self)
        self.timer.checking_signal.connect(self.run_process_check)
    
    # Move this window to middle of screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    # window initialize function
    def init(self):
        DB.DBinit()
        if CheckingData() == False:
            QMessageBox.information(self, 'Information', 'Option setting was reset.\nBecause option Data from DataBase unmatched the Normal format', QMessageBox.Yes)
        grid = QGridLayout()
        grid.addWidget(self.createGroup_webhook(), 0, 0)
        grid.addWidget(self.createGroup_option(), 1, 0)
        grid.addWidget(self.createGroup_myMenu(), 2, 0)
        grid.addWidget(self.createGroup_excute(), 3, 0)

        self.setLayout(grid)

        self.setWindowIcon(QIcon('./Mining Manager/Image/Icon/Title_Icon.png'))
        self.setWindowTitle(f'Mining Manager {VERSION}')
        self.setMaximumSize(WINDOWSIZE_H, WINDOWSIZE_V)
        self.setMinimumSize(WINDOWSIZE_H, WINDOWSIZE_V)
        self.center()

        self.show()
    


    # print to console
    def console_out(self, text):
        QCoreApplication.processEvents()
        self.console.append(text)
        self.console.repaint()

    def run_process_check(self):
        self.btn_stop.setDisabled(True) # freeze

        nowTime = getNowTime().strftime("%H:%M:%S (%Y-%m-%d)")
        nextTime = getAddedTime(int(DB.loadCheckingTime())).strftime("%Y-%m-%d %H:%M:%S")

        self.console_out(Style.toBold('Start checking'))
        self.console_out(f'Current time : {nowTime}')

        ### Main checking roop start
        for key in Web.Url_dictionary:
            self.console_out(Style.toBold(Style.toLink(key)))
            workerList = Web.getList(key)
            workerStr = f'Worker List : {str(workerList)}'
            
            self.console_out(f'Workers Size : {len(workerList)}')
            self.console_out(workerStr)
        ### Main checking roop end
            
        self.console_out(Style.toBold(f'Next checking time : {nextTime}'))
        self.console_out('')

        self.btn_stop.setEnabled(True) # unfreeze

    def run_process_init(self):
        self.btn_stop.setDisabled(True) # freeze

        ### program start
        self.console_out(f'=== Program start === <{getNowTime().strftime("%Y-%m-%d %H:%M:%S")}>\n')

        ### load and print option setting
        # load
        self.console_out('Loading data ...')
        webhook = DB.loadWEBHOOK()
        checktime = DB.loadCheckingTime()
        when_seq = DB.loadWhen()
        info_seq = DB.loadInfo()
        # print
        stList = getSetting(webhook, checktime, when_seq, info_seq)
        for st in stList:
            if st == ERRORTEXT:
                self.console_out('-> ' + Style.toRed(f"Disconnected"))
                self.console_out(getErrorTxt('The Webhook Link is not available'))
                return
            else:
                self.console_out(st)
        self.console_out('')
        
        ### check network connection in web site List
        self.console_out(f'Checking Network connection ({len(Web.Url_dictionary)})')
        idx = 1
        for key in Web.Url_dictionary:
            self.console_out(f'[{idx}/{len(Web.Url_dictionary)}] {key}')
            self.console_out(f'url : {Style.toLink(Web.Url_dictionary[key][0])}')
            self.console_out(getOneNetworkState(key))
            idx += 1
        self.console_out('')

        self.btn_stop.setEnabled(True) # unfreeze

    def run_process_mainLoop(self):
        self.run_process_check()
        self.timer.on = True
        self.timer.target_sec = int(DB.loadCheckingTime()) * 60
        self.timer.start()
    
    def run(self):
        self.run_process_init()
        self.run_process_mainLoop()

    def run_process_exit(self):
        self.timer.end()


    
    # create webhook group box
    def createGroup_webhook(self):
        groupbox = QGroupBox(WEBHOOK_GB_NAME)
        WEBHOOK = DB.loadWEBHOOK()
        label_webhook = QLabel(WEBHOOK)

        btn_edit = QPushButton('Edit', self)
        btn_edit.clicked.connect(self.btn_edit_function)
        btn_delete = QPushButton('Delete', self)
        btn_delete.clicked.connect(self.btn_delete_function)
        btn_test = QPushButton('Connection Test', self)
        btn_test.clicked.connect(self.btn_ConnectionTest_function)

        vbox = QVBoxLayout()
        vbox.addWidget(label_webhook)

        hbox = QHBoxLayout()
        hbox.addWidget(btn_edit)
        hbox.addWidget(btn_delete)
        hbox.addWidget(btn_test)
        vbox.addLayout(hbox)

        groupbox.setLayout(vbox)
        return groupbox
    
    # create option group box
    def createGroup_option(self):
        groupbox = QGroupBox(OPTION_GB_NAME)

        cb_label = QLabel('CheckingTime (min)')
        cb_checkingTime = QComboBox(self)
        for time in DB.CheckingTime_list:
            cb_checkingTime.addItem(str(time))
        cb_checkingTime.activated[str].connect(self.cb_checkingTime_onActivated)
        cb_checkingTime.setCurrentText(str(DB.loadCheckingTime()))
        btn_settingReset = QPushButton('Reset default values', self)
        btn_settingReset.clicked.connect(self.btn_settingReset_function)

        vbox_checkTime = QVBoxLayout()
        vbox_checkTime.addWidget(cb_label)
        vbox_checkTime.addWidget(cb_checkingTime)
        vbox_checkTime.addStretch(1)
        vbox_checkTime.addWidget(btn_settingReset)
        
        notification_label = QLabel('Receive notifications when')
        checkBox_whenList = []
        chechBox_whenData = DB.loadWhen()
        for checkBox in OPTION_WHEN_LIST:
            checkBox_whenList.append(QCheckBox(checkBox, self))
        
        for i in range(0, len(OPTION_WHEN_LIST)):
            if chechBox_whenData[i] == '1':
                checkBox_whenList[i].toggle()
            checkBox_whenList[i].stateChanged.connect(self.checkBox_optionUpdate_function)

        vbox_alert = QVBoxLayout()
        vbox_alert.addWidget(notification_label)
        for checkBox in checkBox_whenList:
            vbox_alert.addWidget(checkBox)
        vbox_alert.addStretch(1)

        info_label = QLabel('Receive following information')
        checkBox_infoList = []
        chechBox_infoData = DB.loadInfo()
        for checkBox in OPTION_INFO_LIST:
            checkBox_infoList.append(QCheckBox(checkBox, self))
            
        for i in range(0, len(OPTION_INFO_LIST)):
            if chechBox_infoData[i] == '1':
                checkBox_infoList[i].toggle()
            checkBox_infoList[i].stateChanged.connect(self.checkBox_optionUpdate_function)

        vbox_info = QVBoxLayout()
        vbox_info.addWidget(info_label)
        for checkBox in checkBox_infoList:
            vbox_info.addWidget(checkBox)
        vbox_info.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox_checkTime)
        hbox.addLayout(vbox_alert)
        hbox.addLayout(vbox_info)
        groupbox.setLayout(hbox)

        return groupbox
    
    # create menu group box
    def createGroup_myMenu(self):
        groupbox = QGroupBox()
        groupbox.setFlat(True)

        btn_quit = QPushButton(QUIT_BTN_NAME)
        btn_quit.clicked.connect(self.btn_quit_function)
        btn_restart = QPushButton(RESTART_BTN_NAME)
        btn_restart.clicked.connect(self.btn_restart_function)

        vbox_L = QVBoxLayout()
        vbox_L.addWidget(btn_quit)
        vbox_L.addWidget(btn_restart)

        btn_start = QPushButton(START_BTN_NAME)
        btn_start.clicked.connect(self.btn_start_function)
        btn_stop = QPushButton(STOP_BTN_NAME)
        btn_stop.setDisabled(True)
        btn_stop.clicked.connect(self.btn_stop_function)
        
        vbox_M = QVBoxLayout()
        vbox_M.addWidget(btn_start)
        vbox_M.addWidget(btn_stop)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox_L)
        hbox.addLayout(vbox_M)
        groupbox.setLayout(hbox)

        return groupbox
    
    # create excute group box
    def createGroup_excute(self):
        groupbox = QGroupBox(CONSOLE_GB_NAME)
        txtBrowser_consol = QTextEdit()
        txtBrowser_consol.setReadOnly(True)
        vbox = QVBoxLayout()
        vbox.addWidget(txtBrowser_consol)
        groupbox.setLayout(vbox)

        return groupbox



    def btn_start_function(self):
        self.console.clear()

        self.btn_stop.setEnabled(True)
        self.btn_quit.setDisabled(True)
        self.btn_restart.setDisabled(True)
        self.btn_start.setDisabled(True)
        
        self.gb_webhook.setDisabled(True)
        self.gb_option.setDisabled(True)

        self.run()

    def btn_stop_function(self):
        self.console_out('Close the Program . . .')
        self.btn_stop.setDisabled(True)
        self.btn_quit.setEnabled(True)
        self.btn_restart.setEnabled(True)
        self.btn_start.setEnabled(True)
        
        self.gb_webhook.setEnabled(True)
        self.gb_option.setEnabled(True)
        
        self.run_process_exit()

    def btn_quit_function(self):
        qApp.exit(0)

    def btn_restart_function(self):
        qApp.exit(RESTARTCODE)
    
    def btn_edit_function(self):
        text, ok = QInputDialog.getText(self, 'Edit WebHook', 'Enter the WebHook url')
        WEBHOOK = text
        if ok:
            DB.saveWEBHOOK(WEBHOOK)
            qApp.exit(RESTARTCODE)
    
    def btn_delete_function(self):
        ans = QMessageBox.information(self, 'Information', 'Are you sure delete WebHook link on this program ?', QMessageBox.Yes | QMessageBox.No)
        if ans == QMessageBox.Yes:
            DB.saveWEBHOOK('')
            qApp.exit(RESTARTCODE)
    
    def btn_ConnectionTest_function(self):
        WEBHOOK = DB.loadWEBHOOK()
        verifyingCode = ''
        for _ in range(0, 4):
            verifyingCode += str(random.randrange(0, 10))
        program = Discord.send_message(WEBHOOK, f'VerifyingCode : {verifyingCode}')
        if program == -1:
            QMessageBox.warning(self, 'Webhook Error', f'The Webhook link is not work. Check the Webhook Link')
        else:
            QMessageBox.information(self, 'Information', f'sent verifying Code {verifyingCode} to this WebHook link', QMessageBox.Yes)

    def btn_settingReset_function(self):
        ans = QMessageBox.information(self, 'Information', 'Are you sure reset setting to a default value ?', QMessageBox.Yes | QMessageBox.No)
        if ans == QMessageBox.Yes:
            DB.Reset_default_values()
            qApp.exit(RESTARTCODE)



    def checkBox_optionUpdate_function(self):
        option_when_seq = ''
        option_info_seq = ''
        checkBox_list = self.findChildren(QCheckBox)
        for checkBox_name in OPTION_WHEN_LIST:
            for find_checkBox in checkBox_list:
                if checkBox_name == find_checkBox.text():
                    if find_checkBox.isChecked():
                        option_when_seq += '1'
                    else:
                        option_when_seq += '0'
                        
        for checkBox_name in OPTION_INFO_LIST:
            for find_checkBox in checkBox_list:
                if checkBox_name == find_checkBox.text():
                    if find_checkBox.isChecked():
                        option_info_seq += '1'
                    else:
                        option_info_seq += '0'
        
        DB.saveWhen(option_when_seq)
        DB.saveInfo(option_info_seq)

    def cb_checkingTime_onActivated(self, time):
        DB.saveCheckingTime(time)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    while True:
        ex = MyWindow()
        program_return = app.exec_()
        ex.close()
        if program_return == RESTARTCODE:
            print('Program restarting ...')
            continue
        else:
            print('Quit the program')
            break
    
        
