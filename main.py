import sys
import platform
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *

# GUI FILE - Import module giao diện
from app_modules import * \
    
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        UIFunctions.removeTitleBar(True)

        self.setWindowTitle('Cyber Cafe Manager - Admin')
        UIFunctions.labelTitle(self, 'Cyber Cafe Manager - Admin')
        UIFunctions.labelDescription(self, 'Trạng thái: Server Online')

        startSize = QSize(1200, 800)
        self.resize(startSize)
        self.setMinimumSize(startSize)

        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))

        self.ui.btn_open_file.clicked.connect(self.Button)
        self.ui.btn_save.clicked.connect(self.Button)
        self.ui.btn_new.clicked.connect(self.Button)
        self.ui.btn_new_user.clicked.connect(self.Button)
        self.ui.btn_settings.clicked.connect(self.Button)

        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        UIFunctions.selectStandardMenu(self, "btn_dashboard") 

        def moveWindow(event):
            if UIFunctions.returStatus() == 1:
                UIFunctions.maximize_restore(self)
            if event.buttons() == Qt.MouseButton.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
                self.dragPos = event.globalPosition().toPoint()
                event.accept()

        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow

        UIFunctions.uiDefinitions(self)

        self.populate_machines()

        self.show()

    def populate_machines(self):
        if hasattr(self.ui, 'gridLayout_machines'):
            machines = [
                {"name": "Máy 01", "status": "Online", "user": "1"},
                {"name": "Máy 02", "status": "Offline", "user": "2"},
                {"name": "Máy 03", "status": "Offline", "user": "3"},
                {"name": "Máy 04", "status": "Online", "user": "4"},
                {"name": "Máy 05", "status": "Maintenance", "user": "5"},
                {"name": "Máy VIP 1", "status": "Online", "user": "tien an cut"},
            ]

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
            print("gridLayout_machines")

    def create_machine_card(self, data):
        frame = QFrame()
        frame.setMinimumSize(250, 150)
        
        bg_color = "rgb(44, 49, 60)" 
        status_color = "gray"
        if data['status'] == 'Online':
            bg_color = "rgb(20, 60, 40)" 
            status_color = "#00FF00" 
        elif data['status'] == 'Maintenance':
            bg_color = "rgb(60, 40, 20)"
            status_color = "orange"

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
        
        lbl_name = QLabel(f"{data['name']}")
        lbl_name.setStyleSheet("font-size: 18px; font-weight: bold; color: white; border: none; background: transparent;")
        layout.addWidget(lbl_name)
        
        lbl_status = QLabel(f"Status: {data['status']}")
        lbl_status.setStyleSheet(f"color: {status_color}; font-weight: bold; border: none; background: transparent;")
        layout.addWidget(lbl_status)
        
        if data['user']:
            lbl_user = QLabel(f"User: {data['user']}")
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

    def Button(self):
        btnWidget = self.sender()
        btnName = btnWidget.objectName()

        UIFunctions.resetStyle(self, btnName)
        btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        if btnName == "btn_dashboard":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.labelPage(self, "Tổng quan")
        
        elif btnName == "btn_machines":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home) 
            UIFunctions.labelPage(self, "Quản lý Máy trạm")

        elif btnName == "btn_services":
            UIFunctions.labelPage(self, "Dịch vụ & Đồ ăn")
            
        elif btnName == "btn_members":
            UIFunctions.labelPage(self, "Quản lý Hội viên")

        elif btnName == "btn_settings":
            if hasattr(self.ui, 'page_settings'):
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_settings)
            UIFunctions.labelPage(self, "Cài đặt hệ thống")


    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def resizeEvent(self, event):
        self.resizeFunction()
        return super(MainWindow, self).resizeEvent(event)
    
    def resizeFunction(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())