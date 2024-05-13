from PySide6.QtWidgets import QMessageBox

def display_critical_popup(message):
    msg = QMessageBox()
    msg.setWindowTitle("Warnning")
    msg.setText(message)
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setStyleSheet('QMessageBox QLabel {font: bold 12pt "pretendard";}')
    ## msg.setStyleSheet("background-color: rgb(0, 0, 0);color: rgb(255, 255, 255);")
    ## msg.setBaseSize(1000, 400)
    x = msg.exec()

def display_information_popup(message):
    msg = QMessageBox()
    msg.setWindowTitle("Information")
    msg.setText(message)
    msg.setIcon(QMessageBox.Icon.Information)
    ## msg.setStyleSheet("background-color: rgb(0, 0, 0);color: rgb(255, 255, 255);")
    ## msg.setBaseSize(1000, 400)
    msg.setStyleSheet('QMessageBox QLabel {font: bold 12pt "pretendard";}')
    x = msg.exec()