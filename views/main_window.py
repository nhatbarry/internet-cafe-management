
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QLabel, QPushButton

from views.ui.ui_main import Ui_MainWindow
from views.ui.ui_functions import UIFunctions
from config.settings import WINDOW_TITLE, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        UIFunctions.removeTitleBar(True)
        self.setWindowTitle(WINDOW_TITLE)
        UIFunctions.labelTitle(self, WINDOW_TITLE)
        UIFunctions.labelDescription(self, 'Kết nối: MongoDB Atlas')
        
        start_size = QSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(start_size)
        self.setMinimumSize(start_size)
        
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        UIFunctions.selectStandardMenu(self, "btn_dashboard")
        
        self._setup_drag_window()
        
        UIFunctions.uiDefinitions(self)
    
    def _setup_drag_window(self):
        def move_window(event):
            if UIFunctions.returStatus() == 1:
                UIFunctions.maximize_restore(self)
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
        
        self.ui.frame_label_top_btns.mouseMoveEvent = move_window
    
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
    
    def resizeEvent(self, event):
        return super().resizeEvent(event)
    
    
    def show_message(self, title: str, message: str, msg_type: str = "info"):
        from PyQt5.QtWidgets import QMessageBox
        
        if msg_type == "info":
            QMessageBox.information(self, title, message)
        elif msg_type == "warning":
            QMessageBox.warning(self, title, message)
        elif msg_type == "error":
            QMessageBox.critical(self, title, message)
    
    def confirm_dialog(self, title: str, message: str) -> bool:
        from PyQt5.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self, title, message,
            QMessageBox.Yes | QMessageBox.No
        )
        return reply == QMessageBox.Yes
    
    def update_status(self, message: str):
        UIFunctions.labelDescription(self, message)
