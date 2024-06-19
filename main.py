
import sys
from ppadb.client import Client as AdbClient
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QIODevice, Qt, QSize, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QListWidget
import pop_window
import pathlib
import os
import time
import subprocess
import threading

class MainWindow(QMainWindow):

    # 시스널 정의 
    noti_signal = pyqtSignal(str) 

    def __init__(self):
        super(MainWindow, self).__init__()
        current_directory = os.getcwd()
        ui_path = os.path.join(os.path.dirname(__file__), "Gsi_writer.ui")
        
        try:
            uic.loadUi(ui_path,self)
        except:
            print(f'load Gsi_writter.ui ========> {current_directory}')
       
        self.setFixedSize(QSize(635, 990))
        self.noti_signal.connect(self.noti_signal_handler)
        
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
        self.pushButton_FO3.setEnabled(False)
        self.label_SUSD.setEnabled(False)
        self.progressBar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #8f8f91;
                border-radius: 5px;
                background-color: #e0e0e0;
            }

            QProgressBar::chunk {
                background-color: #0000FF;
                width: 10px;
                margin: 0.5px;
            }
        """)
        self.progressBar.setValue(0)
        self.image_writing = False

        
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

        self.noti_signal.emit("-")
        self.noti_signal.emit('P00')

        ## test_item = {"adb", "def", "kkk"}
        ## for test in test_item:
        ##     self.listWidget_dev.addItem(test)
        ## 
        ## return
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
            fs_command = 'adb -s ' + dev.serial +' shell getprop vendor.skb.dhcp.eth0.ipaddress'
            result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
            print(result)

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
        
    def do_pushButton_WI(self):     
        self.noti_signal.emit('P00')
        self.pb_thread = threading.Thread(target=self.do_pushButton_WI_TH, daemon=True)
        self.pb_thread.start()
        self.pushButton_WI.setEnabled(False)
    
    #########################################################
    def do_pushButton_WI_TH(self):        
        print("do_pushButton_WI")

        select_items = self.listWidget_dev.selectedItems()
        if len(select_items) == 0:
            self.noti_signal.emit("SelNoDev")
            self.pushButton_WI.setEnabled(True)
            return
        
        if self.checkBox_cts.checkState() == Qt.CheckState.Checked:
            p = pathlib.Path(self.label_GSI.text())
            if p.exists():
                gsi_image = self.label_GSI.text()
            else:
                self.noti_signal.emit("WrongGsiPath")
                self.pushButton_WI.setEnabled(True)
                return
            
        elif self.checkBox_vts.checkState() == Qt.CheckState.Checked:
            p = pathlib.Path(self.label_GSI.text())
            if p.exists():
                gsi_image = self.label_GSI.text()
            else:
                self.noti_signal.emit("WrongGsiPath")
                self.pushButton_WI.setEnabled(True)
                return
            
            p = pathlib.Path(self.label_BI.text())
            if p.exists():
                bi_image = self.label_BI.text()
            else:
                self.noti_signal.emit("WrongBiPath")
                self.pushButton_WI.setEnabled(True)
                return
        elif self.checkBox_SUSD.checkState() == Qt.CheckState.Checked:
            p = pathlib.Path(self.label_SUSD.text())
            if p.exists():
                susd_folder = self.label_SUSD.text()
            else:
                self.noti_signal.emit("WrongSUSDPath")
                self.pushButton_WI.setEnabled(True)
                return
        else:
            self.noti_signal.emit("NoCheckBox")

        for select_item in select_items:
            self.reboot_bootloader(select_item.text())
            time.sleep(10)
            if self.checkBox_cts.checkState() == Qt.CheckState.Checked: ## for cts_on_gsi
                self.fastboot_cts_on_GSI(self.label_GSI.text())
            elif self.checkBox_vts.checkState() == Qt.CheckState.Checked:
                self.fastboot_step_vts(self.label_BI.text(), self.label_GSI.text())
            elif self.checkBox_SUSD.checkState() == Qt.CheckState.Checked:
                self.fastboot_step_normal_image(self.label_SUSD.text())   
            else :
                pop_window.display_critical_popup("Flash 할 이미지를 선택해 주세요")
        
        self.pushButton_WI.setEnabled(True)
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
    def fastboot_cts_on_GSI(self, system_image_path):
        system_image_path = pathlib.Path(system_image_path)
        fs_command = 'fastboot devices'
        self.noti_signal.emit(fs_command)
        self.noti_signal.emit('P10')
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        
        fs_command = 'fastboot flashing unlock'
        self.noti_signal.emit(fs_command)
        self.noti_signal.emit('P20')
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        
        fs_command = 'fastboot flashing unlock_critical'
        self.noti_signal.emit(fs_command)
        self.noti_signal.emit('P30')
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        
        fs_command = 'fastboot -w'
        self.noti_signal.emit('P40')
        self.noti_signal.emit(fs_command)
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)

        fs_command = 'fastboot reboot fastboot'
        self.noti_signal.emit(fs_command)
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        time.sleep(10)
        self.noti_signal.emit('P50')

        fs_command = 'fastboot delete-logical-partition product_a'
        self.noti_signal.emit('P60')
        self.noti_signal.emit(fs_command)
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)

        fs_command = 'fastboot delete-logical-partition product_b'
        self.noti_signal.emit('P70')
        self.noti_signal.emit(fs_command)
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)

        fs_command = 'fastboot delete-logical-partition product'
        self.noti_signal.emit('P70')
        self.noti_signal.emit(fs_command)
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)

        fs_command = 'fastboot flash system '+ system_image_path
        self.noti_signal.emit('P80')
        self.noti_signal.emit(fs_command)
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)

        fs_command = 'fastboot reboot'
        self.noti_signal.emit('P90')
        self.noti_signal.emit(fs_command)
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        
        time.sleep(2)
        self.noti_signal.emit('Completed')
        self.noti_signal.emit('P100')

    def fastboot_step_vts(self, bl_image, system_image_path):
        bl_image = pathlib.Path(bl_image)
        system_image_path = pathlib.Path(system_image_path)

        fs_command = 'fastboot devices'
        self.noti_signal.emit(fs_command)
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        fs_command = 'fastboot flashing unlock'
        self.noti_signal.emit(fs_command)
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        fs_command = 'fastboot flashing unlock_critical'
        self.noti_signal.emit(fs_command)
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result) 
        self.noti_signal.emit('P10')
        fs_command = 'fastboot flash boot '+ bl_image
        self.noti_signal.emit(fs_command)
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        self.noti_signal.emit('P40')
        fs_command = 'fastboot reboot fastboot'
        self.noti_signal.emit(fs_command)
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        time.sleep(10)
        self.noti_signal.emit('P60')
        self.noti_signal.emit(fs_command)
        fs_command = 'fastboot flash system ' + system_image_path
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        self.noti_signal.emit('P80')
        fs_command = 'fastboot -w'
        self.noti_signal.emit(fs_command)
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        self.noti_signal.emit('P90')
        fs_command = 'fastboot reboot'
        self.noti_signal.emit(fs_command)
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        time.sleep(1)
        self.noti_signal.emit('P100')
        self.noti_signal.emit('Completed')

    def fastboot_step_normal_image(self, img_folder):
        img_folder  = pathlib.Path(img_folder)
        dtbo        = "dtbo " + str(os.path.join(img_folder, 'dtbo.img')) 
        vbmeta      = "vbmeta " + str(os.path.join(img_folder, 'vbmeta.img'))
        vbmeta_system = "vbmeta_system " + str(os.path.join(img_folder, 'vbmeta_system.img'))
        boot        = "boot " + str(os.path.join(img_folder, 'boot.img'))
        recovery    = "recovery " + str(os.path.join(img_folder, 'recovery.img'))
        super       = "super " + str(os.path.join(img_folder, 'super_empty.img'))
        system      = "system " + str(os.path.join(img_folder, 'system.img'))
        vendor      = "vendor " + str(os.path.join(img_folder, 'vendor.img'))
        product     = "product " + str(os.path.join(img_folder, 'product.img'))
        userdata    = "userdata " + str(os.path.join(img_folder, 'userdata.img'))

        pre_steps = ['devices', 'flashing unlock', 'flashing unlock_critical', 'erase misc', 'reboot-bootloader']   
        img_step1 = [dtbo, vbmeta, vbmeta_system, boot, recovery, super]
        img_step2 = [system, vendor, product, userdata ]
        end_steps = ["flashing lock", "flashing lock_critical", "reboot"]

        ## pre step
        self.noti_signal.emit('P10')
        for pre_step in pre_steps:
            fs_command = "fastboot " + pre_step
            self.noti_signal.emit(fs_command)
            result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
            print(result)
        self.noti_signal.emit('P30')
        time.sleep(10)

        ## write image1 step
        for img in img_step1:
            fs_command = "fastboot flash " + img
            self.noti_signal.emit(fs_command)
            result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
            print(result)
        self.noti_signal.emit('P60')
        
        ## reboot bootloader
        fs_command = 'fastboot reboot-fastboot'
        self.noti_signal.emit(fs_command)
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        time.sleep(25)
        self.noti_signal.emit('P70')

        fs_command = 'fastboot create-logical-partition product 562535424'
        self.noti_signal.emit(fs_command)
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)

        ## write image2 step
        for img in img_step2:
            fs_command = "fastboot flash " + img
            self.noti_signal.emit(fs_command)
            result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
            print(result)

        self.noti_signal.emit('P90')    

        ## reboot bootloader
        fs_command = 'fastboot reboot-bootloader'
        self.noti_signal.emit(fs_command)
        result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
        print(result)
        time.sleep(10)

        for end_step in end_steps:
            fs_command = "fastboot " + end_step
            self.noti_signal.emit(fs_command)
            result = subprocess.run(fs_command, shell=True, capture_output=True, text=True)
            print(result)

        self.noti_signal.emit('P100')    
        self.noti_signal.emit('Completed')

    # 시그널 핸들러 정의
    def noti_signal_handler(self, message):
        if message == "P00":
            self.progressBar.setValue(00)
        elif message == "P10":
            self.progressBar.setValue(10)
        elif message == "P20":
            self.progressBar.setValue(20)
        elif message == "P30":
            self.progressBar.setValue(30)
        elif message == "P40":
            self.progressBar.setValue(40)
        elif message == "P50":
            self.progressBar.setValue(50)
        elif message == "P60":
            self.progressBar.setValue(60)    
        elif message == "P70":
            self.progressBar.setValue(70)
        elif message == "P80":
            self.progressBar.setValue(80)
        elif message == "P90":
            self.progressBar.setValue(90)
        elif message == "P100":
            self.progressBar.setValue(100)
        elif message == "SelNoDev":
            pop_window.display_critical_popup('선택한 디바이스가 없습니다.\n디바이스를 선택하세요 !')
        elif message == "WrongGsiPath":
            pop_window.display_critical_popup('올바른 GSI Image 아니거나 잘못된 경로 입니다 !')
        elif message == "WrongBiPath":    
            pop_window.display_critical_popup('올바른 Bootloader Image 아니거나 잘못된 경로 입니다 !')
        elif message == "WrongSUSDPath":   
            pop_window.display_critical_popup('올바른 Image 폴더가 아니거나 잘못된 경로 입니다 !')
        elif message == "NoCheckBox":
            pop_window.display_critical_popup('작업이 선택되지 않았으니 작업을 선택해 주세요')
        else :
            dsip = "status : " + message
            self.label_status.setText(dsip)

###############################################################
#### MainLoop()
################################################################
if  __name__ == "__main__":
    app = QApplication(sys.argv)

    MW = MainWindow()
    MW.show()
    sys.exit(app.exec())


