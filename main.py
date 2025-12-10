import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QLabel, QPushButton

app = QApplication(sys.argv)

from ui.files_rc import qInitResources
qInitResources()

# GUI FILE
from ui.app_modules import *
from controllers.controllers import MainController

from database import Database 

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = Database()

        UIFunctions.removeTitleBar(True)
        self.setWindowTitle('Cyber Cafe Manager - Admin')
        UIFunctions.labelTitle(self, 'Cyber Cafe Manager - Admin')
        UIFunctions.labelDescription(self, 'Kết nối: MongoDB Localhost')

        startSize = QSize(1200, 800)
        self.resize(startSize)
        self.setMinimumSize(startSize)

        self.controller = MainController(self)

        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        UIFunctions.selectStandardMenu(self, "btn_dashboard") 

        def moveWindow(event):
            if UIFunctions.returStatus() == 1:
                UIFunctions.maximize_restore(self)
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow

        UIFunctions.uiDefinitions(self)

        self.populate_machines()

        self.show()

    def populate_machines(self):
        if hasattr(self.ui, 'gridLayout_machines'):
            for i in reversed(range(self.ui.gridLayout_machines.count())): 
                self.ui.gridLayout_machines.itemAt(i).widget().setParent(None)

            machines = self.db.get_all_computers() 

            row = 0
            col = 0
            for machine in machines:
                card = self.create_machine_card(machine)
                self.ui.gridLayout_machines.addWidget(card, row, col)
                col += 1
                if col > 2: 
                    col = 0
                    row += 1
        else:
            print("Chưa có gridLayout_machines trong UI")

    def create_machine_card(self, data):
        frame = QFrame()
        frame.setMinimumSize(250, 160) 
        
        is_active = data.get('is_active', False) 
        
        if is_active:
            bg_color = "rgb(20, 60, 40)" 
            status_text = "Online"
            status_color = "#00FF00"  
        else:
            bg_color = "rgb(44, 49, 60)"  
            status_text = "Offline"
            status_color = "gray"      

        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 10px;
                border: 1px solid rgb(60, 65, 75);
            }}
            QFrame:hover {{
                border: 1px solid rgb(85, 170, 255);
            }}
        """)
        
        layout = QVBoxLayout(frame)
        
        machine_name = data.get('computer_name', 'Unknown PC')
        lbl_name = QLabel(f"🖥️ {machine_name}")
        lbl_name.setStyleSheet("font-size: 18px; font-weight: bold; color: white; border: none; background: transparent;")
        layout.addWidget(lbl_name)
        
        ip_addr = data.get('ip_address', '0.0.0.0')
        lbl_ip = QLabel(f"IP: {ip_addr}")
        lbl_ip.setStyleSheet("font-size: 11px; color: #aaa; border: none; background: transparent;")
        layout.addWidget(lbl_ip)

        lbl_status = QLabel(f"Status: {status_text}")
        lbl_status.setStyleSheet(f"color: {status_color}; font-weight: bold; border: none; background: transparent;")
        layout.addWidget(lbl_status)
        
        user_name = data.get('user') 
        if user_name:
            lbl_user = QLabel(f"User: {user_name}")
            lbl_user.setStyleSheet("color: #ccc; border: none; background: transparent;")
            layout.addWidget(lbl_user)
        else:
            layout.addStretch() 

        btn = QPushButton("Chi tiết")
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(85, 170, 255);
                color: white;
                border-radius: 5px;
                padding: 5px;
                border: none;
            }
            QPushButton:hover { background-color: rgb(100, 190, 255); }
        """)
        layout.addWidget(btn)
        
        return frame

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def resizeEvent(self, event):
        return super(MainWindow, self).resizeEvent(event)

if __name__ == "__main__":
    window = MainWindow()
    sys.exit(app.exec_())