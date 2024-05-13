
from ppadb.client import Client as AdbClient
import sys
from PySide6.QtGui import QStandardItemModel
from PySide6.QtGui import QStandardItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QListWidget
import pop_window
import pathlib
import os
import time
from fastbootpy import FastbootManager
import subprocess

class MainWindow:
    def __init__(self, window):
        print("===> Init")
        self.window = window
        self.setFunction()
        self.window.radioButton_SMART3.setChecked(False)
        self.window.radioButton_SoundMax.setChecked(True)
        self.window.checkBox_cts.setTristate(False)
        self.window.checkBox_vts.setTristate(False)
        self.window.radioButton_SMART3.setEnabled(False)
        self.window.radioButton_SoundMax.setEnabled(False)
        self.window.checkBox_cts.setCheckState(Qt.CheckState.Checked)

        
    def setFunction(self):    
        self.window.pushButton_FO.clicked.connect(self.do_pushButton_FO)
        self.window.pushButton_FO2.clicked.connect(self.do_pushButton_FO2)
        self.window.pushButton_Refresh.clicked.connect(self.do_pushButton_Refresh)
        self.window.pushButton_WI.clicked.connect(self.do_pushButton_WI)
        self.window.radioButton_SMART3.clicked.connect(self.do_radio_button_click) 
        self.window.radioButton_SoundMax.clicked.connect(self.do_radio_button_click)     
        self.window.checkBox_cts.clicked.connect(self.do_checkbox_click_cts) 
        self.window.checkBox_vts.clicked.connect(self.do_checkbox_click_vts)     

    def show(self):
        self.window.show()

    ###############################################################
    ####
    ################################################################
    def do_pushButton_FO(self):
        print("do_pushButton_FO")
        fn = QFileDialog.getOpenFileName(self.window, 'Select GSI File')
        if fn[0] == '':
            pop_window.display_critical_popup("파일이 선택되지 않았습니다.")
            self.window.label_GSI.setText('-')
        else:
            file_p = pathlib.Path(fn[0])
            print(str(file_p))
            self.window.label_GSI.setText(str(file_p))

    def do_pushButton_FO2(self):
        print("do_pushButton_FO2")
        fn = QFileDialog.getOpenFileName(self.window, 'Select Bootloader File')
        if fn[0] == '':
            pop_window.display_critical_popup("파일이 선택되지 않았습니다.")
            self.window.label_BI.setText('-')
        else:
            file_p = pathlib.Path(fn[0])
            print(str(file_p))
            self.window.label_BI.setText(str(file_p))

    def do_pushButton_Refresh(self):
        print("do_pushButton_Refresh")
        self.window.listWidget_dev.clear()
        client = AdbClient(host="127.0.0.1", port=5037)
        self.devices = client.devices()
        if len(self.devices) < 1:
            pop_window.display_critical_popup("연결된 디바이스가 없습니다.")

        for dev in self.devices:
            self.window.listWidget_dev.addItem(dev.serial)
            fs_command = "adb shell getprop vendor.skb.dhcp.eth0.ipaddress"
            result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
            print(result)

        ## test_item = {"adb", "def", "kkk"}
        ## for test in test_item:
        ##    self.window.listWidget_dev.addItem(test)

    def do_radio_button_click(self):
        if self.window.radioButton_SMART3.isChecked() == True:
            self.window.radioButton_SoundMax.setChecked(False)
        else : 
            self.window.radioButton_SoundMax.setChecked(True)
        
    def do_checkbox_click_cts(self):
        if self.window.checkBox_cts.checkState() == Qt.CheckState.Checked:
            self.window.checkBox_vts.setCheckState(Qt.CheckState.Unchecked)
        else : 
            self.window.checkBox_vts.setCheckState(Qt.CheckState.Checked)

    def do_checkbox_click_vts(self):
        if self.window.checkBox_vts.checkState() == Qt.CheckState.Checked:
            self.window.checkBox_cts.setCheckState(Qt.CheckState.Unchecked)
        else : 
            self.window.checkBox_cts.setCheckState(Qt.CheckState.Checked)

    #########################################################
    def do_pushButton_WI(self):        
        print("do_pushButton_WI")
        dev_serial = self.window.listWidget_dev.currentItem().text()
        self.reboot_bootloader(dev_serial)
        time.sleep(10)
        
        if self.window.checkBox_cts.checkState() == Qt.CheckState.Checked: ## for cts_on_gsi
            self.fastboot_step_1()
            time.sleep(10)
            self.fastboot_step_2(self.window.label_GSI.text())
            time.sleep(10)
            self.fastboot_step_3()
            time.sleep(10)
        else :
            self.fastboot_step_1()
            time.sleep(10)
            self.fastboot_step_vts(self.window.label_BI.text(), self.window.label_GSI.text())

    #########################################################
    def reboot_bootloader(self, selected_dev_serial):      
        if len(self.devices) < 1:
            pop_window.display_critical_popup("연결된 디바이스가 없습니다.")
        
        for dev in self.devices:
            if dev.serial == selected_dev_serial:
                print("finded devices")
                ret = dev.shell("reboot bootloader")
                return

        pop_window.display_critical_popup("선택한 디바이스를 찾을수 없습니다.")

    #########################################################
    ## fastboot
    def fastboot_step_1(self):
        fs_command = 'fastboot devices'
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        fs_command = 'fastboot flashing unlock'
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        fs_command = 'fastboot flashing unlock_critical'
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        fs_command = 'fastboot reboot fastboot'
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)

    def fastboot_step_2(self, system_image_path):
        fs_command = 'fastboot flash system '+ system_image_path
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        fs_command = 'fastboot -w'
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        fs_command = 'fastboot reboot bootloader'
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        
    def fastboot_step_3(self):
        fs_command = 'fastboot flashing lock'
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        fs_command = 'fastboot flashing lock_critical'
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        fs_command = 'fastboot reboot'
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)


    def fastboot_step_vts(self, bl_image, system_image_path):
        fs_command = 'fastboot flashing unlock'
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        fs_command = 'fastboot flashing unlock_critical'
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result) 
        fs_command = 'fastboot flash boot '+ bl_image
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        fs_command = 'fastboot reboot fastboot'
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        time.sleep(10)
        fs_command = 'fastboot flash system ' + system_image_path
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        fs_command = 'fastboot -w'
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        fs_command = 'fastboot reboot'
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
            
###############################################################
#### MainLoop()
################################################################
if  __name__ == "__main__":
    app = QApplication(sys.argv)

    ui_file_name = "Gsi_writer.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)

    MW = MainWindow(window)
    MW.show()
    sys.exit(app.exec())


