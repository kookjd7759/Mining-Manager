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

# get random 4 digit number
def getVerifyingCode():
    code = ''
    for _ in range(0, 4):
        code += str(random.randrange(0, 10))
    return code

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init()
    
    # Move this window to middle of screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    # window initialize function
    def init(self):
        grid = QGridLayout()
        grid.addWidget(self.createGroup_webhook(), 0, 0)
        grid.addWidget(self.createGroup_option(), 1, 0)
        grid.addWidget(self.createGroup_under(), 2, 0)
        self.setLayout(grid)

        self.setWindowIcon(QIcon('./Mining Manager/Icon/Title_Icon.png'))
        self.setWindowTitle('Mining Manager')
        self.setMaximumSize(900, 300)
        self.setMinimumSize(900, 300)
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

        cb_checkingTime = QComboBox(self)
        for time in DB.CheckingTime_list:
            cb_checkingTime.addItem(str(time))
        cb_checkingTime.activated[str].connect(self.cb_checkingTime_onActivated)

        cb_checkingTime.setCurrentText(str(DB.loadCheckingTime()))
        cb_label = QLabel('CheckingTime (min)')

        vbox = QVBoxLayout()
        vbox.addWidget(cb_label)
        vbox.addWidget(cb_checkingTime)
        groupbox.setLayout(vbox)

        return groupbox
    
    def createGroup_under(self):
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
    

    def btn_start_function(self):
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
        ans = QMessageBox.information(self, 'Information', 'Are you sure deleting your WebHook link on this program ?', QMessageBox.Yes | QMessageBox.No)
        if ans == QMessageBox.Yes:
            DB.saveWEBHOOK('')
            qApp.exit(RESTARTCODE)
    
    def btn_ConnectionTest_function(self):
        WEBHOOK = DB.loadWEBHOOK()
        verifyingCode = getVerifyingCode()
        program_sendMessage = threading.Thread(target=Discord.send_message, 
                              args=(WEBHOOK, f'VerifyingCode : {verifyingCode}'))
        program_sendMessage.start()
        QMessageBox.information(self, 'Information', f'sent verifying Code {verifyingCode} to this WebHook link', QMessageBox.Yes)


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