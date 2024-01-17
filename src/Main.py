import sys
import random
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import DB
import Discord

RESTARTCODE = 100
STOP_BTN_NAME = 'Stop'
START_BTN_NAME = 'Start'
OPTION_GB_NAME = 'Option'
WEBHOOK_GB_NAME = 'WebHook'
CONSOLE_GB_NAME = 'Excution Console'

WINDOWSIZE_H = 900
WINDOWSIZE_V = 580

OPTION_WHEN_LIST = ['Connection loss / Hash reduction', 'Adding device', 'Removing device']
OPTION_INFO_LIST = ['Device / Mining pool', 'time', 'Hash', 'Discovered problem', 'Presumptive problem']

# get random 4 digit number
def getVerifyingCode():
    code = ''
    for _ in range(0, 4):
        code += str(random.randrange(0, 10))
    return code

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

class MyWindow(QWidget):

    def run(self):
        browser = self.findChild(QTextBrowser)
        browser.append('start')

    def __init__(self):
        super().__init__()
        self.init()
    
    # Move this window to middle of screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def occurData_Format_problem(self):
        QMessageBox.information(self, 'Information', 'Option setting was reset.\nBecause option Data from DataBase unmatched the Normal format', QMessageBox.Yes)



    # window initialize function
    def init(self):
        if CheckingData() == False:
            self.occurData_Format_problem()
        grid = QGridLayout()
        grid.addWidget(self.createGroup_webhook(), 0, 0)
        grid.addWidget(self.createGroup_option(), 1, 0)
        grid.addWidget(self.createGroup_menu(), 2, 0)
        grid.addWidget(self.createGroup_excute(), 3, 0)
        self.setLayout(grid)

        self.setWindowIcon(QIcon('./Mining Manager/Image/Icon/Title_Icon.png'))
        self.setWindowTitle('Mining Manager')
        self.setMaximumSize(WINDOWSIZE_H, WINDOWSIZE_V)
        self.setMinimumSize(WINDOWSIZE_H, WINDOWSIZE_V)
        self.center()

        self.show()
    


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
    
    def createGroup_menu(self):
        groupbox = QGroupBox()
        groupbox.setFlat(True)

        btn_quit = QPushButton('Quit')
        btn_quit.clicked.connect(self.btn_quit_function)
        btn_restart = QPushButton('Restart')
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
    
    def createGroup_excute(self):
        groupbox = QGroupBox(CONSOLE_GB_NAME)
        groupbox.setDisabled(True)

        txtBrowser_consol = QTextBrowser()
        txtBrowser_consol.setOpenExternalLinks(True)

        vbox = QVBoxLayout()
        vbox.addWidget(txtBrowser_consol)
        groupbox.setLayout(vbox)

        return groupbox


    def btn_start_function(self):
        self.run()
        print('start function')
        button_list = self.findChildren(QPushButton)
        for button in button_list:
            if button.text() == STOP_BTN_NAME:
                button.setEnabled(True)
            elif button.text() == START_BTN_NAME:
                button.setDisabled(True)
        
        qGroupBox_List = self.findChildren(QGroupBox)
        for qGroupBox in qGroupBox_List:
            if qGroupBox.title() == OPTION_GB_NAME or qGroupBox.title() == WEBHOOK_GB_NAME:
                qGroupBox.setDisabled(True)
            elif qGroupBox.title() == CONSOLE_GB_NAME:
                qGroupBox.setEnabled(True)

    def btn_stop_function(self):
        print('stop function')
        button_list = self.findChildren(QPushButton)
        for button in button_list:
            if button.text() == START_BTN_NAME:
                button.setEnabled(True)
            elif button.text() == STOP_BTN_NAME:
                button.setDisabled(True)
                
        qGroupBox_List = self.findChildren(QGroupBox)
        for qGroupBox in qGroupBox_List:
            if qGroupBox.title() == OPTION_GB_NAME or qGroupBox.title() == WEBHOOK_GB_NAME:
                qGroupBox.setEnabled(True)
            elif qGroupBox.title() == CONSOLE_GB_NAME:
                qGroupBox.setDisabled(True)

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
        verifyingCode = getVerifyingCode()
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
        if program_return == RESTARTCODE:
            print('Program restarting ...')
            continue
        else:
            print('Quit the program')
            break