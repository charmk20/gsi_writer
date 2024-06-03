
import sys
from ppadb.client import Client as AdbClient
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QIODevice, Qt, QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QListWidget
import pop_window
import pathlib
import os
import time
import subprocess

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        current_directory = os.getcwd()
        ui_path = os.path.join(os.path.dirname(__file__), "Gsi_writer.ui")
        
        try:
            uic.loadUi(ui_path,self)
        except:
            print(f'load Gsi_writter.ui ========> {current_directory}')
       
        self.setFixedSize(QSize(635, 787))
        print("===> Init")
        self.setFunction()
        self.radioButton_SMART3.setChecked(False)
        self.radioButton_SoundMax.setChecked(True)
        self.checkBox_cts.setTristate(False)
        self.checkBox_vts.setTristate(False)
        self.radioButton_SMART3.setEnabled(False)
        self.radioButton_SoundMax.setEnabled(False)
        self.checkBox_cts.setCheckState(Qt.CheckState.Checked)
        self.pushButton_FO2.setEnabled(False)
        self.label_BI.setEnabled(False)

        
    def setFunction(self):    
        self.pushButton_FO.clicked.connect(self.do_pushButton_FO)
        self.pushButton_FO2.clicked.connect(self.do_pushButton_FO2)
        self.pushButton_FO3.clicked.connect(self.do_pushButton_FO3)
        self.pushButton_Refresh.clicked.connect(self.do_pushButton_Refresh)
        self.pushButton_WI.clicked.connect(self.do_pushButton_WI)
        self.radioButton_SMART3.clicked.connect(self.do_radio_button_click) 
        self.radioButton_SoundMax.clicked.connect(self.do_radio_button_click)     
        self.checkBox_cts.clicked.connect(self.do_checkbox_click_cts) 
        self.checkBox_vts.clicked.connect(self.do_checkbox_click_vts)  
        self.checkBox_SUSD.clicked.connect(self.do_checkbox_click_SUSD)
       

    ###############################################################
    ####
    ################################################################
    def do_pushButton_FO(self):
        print("do_pushButton_FO")
        fn = QFileDialog.getOpenFileName(self, 'Select GSI File')
        if fn[0] == '':
            pop_window.display_critical_popup("파일이 선택되지 않았습니다.")
            self.label_GSI.setText('-')
        else:
            file_p = pathlib.Path(fn[0])
            print(str(file_p))
            self.label_GSI.setText(str(file_p))

    def do_pushButton_FO2(self):
        print("do_pushButton_FO2")
        fn = QFileDialog.getOpenFileName(self, 'Select Bootloader File')
        if fn[0] == '':
            pop_window.display_critical_popup("파일이 선택되지 않았습니다.")
            self.label_BI.setText('-')
        else:
            file_p = pathlib.Path(fn[0])
            print(str(file_p))
            self.label_BI.setText(str(file_p))

    def do_pushButton_FO3(self):
        print("do_pushButton_FO3")
        fn = QFileDialog.getExistingDirectory(self, 'Select Folder which is included Image Files')
        if fn == '':
            pop_window.display_critical_popup("파일이 선택되지 않았습니다.")
            self.label_BI.setText('-')
        else:
            file_p = pathlib.Path(fn)
            print(str(file_p))
            self.label_SUSD.setText(str(file_p))

    def do_pushButton_Refresh(self):
        print("do_pushButton_Refresh")
        self.adb_connection()
        self.listWidget_dev.clear()

        try: 
            client = AdbClient(host="127.0.0.1", port=5037)
            self.devices = client.devices()
        except:
            pop_window.display_critical_popup("연결된 디바이스가 없습니다.")
            return
        
        if len(self.devices) < 1:
            pop_window.display_critical_popup("연결된 디바이스가 없습니다.")

        for dev in self.devices:
            self.listWidget_dev.addItem(dev.serial)
            fs_command = "adb shell getprop vendor.skb.dhcp.eth0.ipaddress"
            result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
            print(result)

        ## test_item = {"adb", "def", "kkk"}
        ## for test in test_item:
        ##    self.window.listWidget_dev.addItem(test)

    def do_radio_button_click(self):
        if self.radioButton_SMART3.isChecked() == True:
            self.radioButton_SoundMax.setChecked(False)
        else : 
            self.radioButton_SoundMax.setChecked(True)
        
    def do_checkbox_click_cts(self):
        if self.checkBox_cts.checkState() == Qt.CheckState.Checked:
            self.checkBox_vts.setCheckState(Qt.CheckState.Unchecked)
            self.checkBox_SUSD.setCheckState(Qt.CheckState.Unchecked)
            self.pushButton_FO.setEnabled(True)
            self.pushButton_FO2.setEnabled(False)
            self.pushButton_FO3.setEnabled(False)
            self.label_BI.setText('-')
            self.label_BI.setEnabled(False)
            self.label_SUSD.setText('-')
            self.label_SUSD.setEnabled(False)

    #    else : 
    #        self.checkBox_vts.setCheckState(Qt.CheckState.Checked)
    #        self.checkBox_SDSU.setCheckState(Qt.CheckState.Unchecked)
    #        self.pushButton_FO2.setEnabled(True)
    #        self.label_BI.setEnabled(True)
#
    def do_checkbox_click_vts(self):
        if self.checkBox_vts.checkState() == Qt.CheckState.Checked:
            self.checkBox_cts.setCheckState(Qt.CheckState.Unchecked)
            self.checkBox_SUSD.setCheckState(Qt.CheckState.Unchecked)
            self.pushButton_FO.setEnabled(True)
            self.pushButton_FO2.setEnabled(True)
            self.pushButton_FO3.setEnabled(False)
            self.label_GSI.setEnabled(True)
            self.label_BI.setEnabled(True)
            self.label_SUSD.setEnabled(False)
            self.label_SUSD.setText('-')
    #    else : 
    #        self.checkBox_cts.setCheckState(Qt.CheckState.Checked)
    #        self.pushButton_FO2.setEnabled(False)
    #        self.label_BI.setEnabled(False)

    def do_checkbox_click_SUSD(self):
        if self.checkBox_SUSD.checkState() == Qt.CheckState.Checked:
            self.checkBox_cts.setCheckState(Qt.CheckState.Unchecked)
            self.checkBox_vts.setCheckState(Qt.CheckState.Unchecked)
            self.pushButton_FO.setEnabled(False)
            self.pushButton_FO2.setEnabled(False)
            self.pushButton_FO3.setEnabled(True)
            self.label_GSI.setEnabled(False)
            self.label_BI.setEnabled(False)
            self.label_SUSD.setEnabled(True)
            self.label_GSI.setText('-')
            self.label_BI.setText('-')
    #    else : 
    #        self.checkBox_cts.setCheckState(Qt.CheckState.Checked)
    #        self.pushButton_FO2.setEnabled(False)
    #        self.label_BI.setEnabled(False)



    def adb_connection(self):
        adb_run = 'adb.exe devices'
        result = subprocess.run(adb_run, shell=True, capture_output=True, text=True)
        print(f"adb.exe devices result ==> {result.returncode}")
        

    #########################################################
    def do_pushButton_WI(self):        
        print("do_pushButton_WI")
        dev_serial = self.listWidget_dev.currentItem().text()
        self.reboot_bootloader(dev_serial)
        time.sleep(10)
        
        if self.checkBox_cts.checkState() == Qt.CheckState.Checked: ## for cts_on_gsi
            self.fastboot_step_1()
            time.sleep(10)
            self.fastboot_step_2(self.label_GSI.text())
            time.sleep(10)
            self.fastboot_step_3()
            time.sleep(10)
        elif self.checkBox_vts.checkState() == Qt.CheckState.Checked:
            self.fastboot_step_vts(self.label_BI.text(), self.label_GSI.text())
        elif self.checkBox_SUSD.checkState() == Qt.CheckState.Checked:
            self.fastboot_step_normal_image(self.label_SUSD.text())   
        

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
        fs_command = 'fastboot devices'
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
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

    def fastboot_step_normal_image(img_folder):
        dtbo        = "dtbo " + img_folder + "/dtbo.img" 
        vbmeta      = "vbmeta " + img_folder + "/vbmeta.img"
        vbmeta_system = "vbmeta_system " + img_folder + "/vbmeta_system.img"
        boot        = "boot " + img_folder + "/boot.img"
        recovery    = "recovery " +  img_folder + "/recovery.img"
        super       = "super " + img_folder + "/super_empty.img"
        system      = "system " + img_folder + "/system.img"
        vendor      = "vendor " + img_folder + "/vendor.img"
        product     = "product " + img_folder + "/product.img"
        userdata    = "userdata " + img_folder + "/userdata.img"

        pre_steps = {"devices", "flash unlock", "flash unlock_critical", "erase misc", "reboot-bootloader"}    
        img_step1 = {dtbo, vbmeta, vbmeta_system, boot, recovery, super}
        img_step2 = {system, vendor, product, userdata }
        end_steps = {"flashing lock", "fastboot flashing lock_critical", "fastboot reboot"}

        ## pre step
        for pre_step in pre_steps:
            fs_command = pre_step
            result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
            print(result)
            time.sleep(10)

        ## write image1 step
        for img in img_step1:
            fs_command = img
            result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
            print(result)

        ## reboot bootloader
        fs_command = 'fastboot reboot-fastboot'
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        time.sleep(10)

        ## write image2 step
        for img in img_step2:
            fs_command = img
            result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
            print(result)
    
        ## reboot bootloader
        fs_command = 'fastboot reboot-fastboot'
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        time.sleep(10)

        for end_step in end_steps:
            fs_command = end_step
            result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
            print(result)

                
###############################################################
#### MainLoop()
################################################################
if  __name__ == "__main__":
    app = QApplication(sys.argv)

    MW = MainWindow()
    MW.show()
    sys.exit(app.exec())


