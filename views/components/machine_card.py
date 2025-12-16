
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal


class MachineCard(QFrame):
    
    detail_clicked = pyqtSignal(dict)
    
    def __init__(self, machine_data: dict, parent=None):
        super().__init__(parent)
        self.data = machine_data
        self._setup_ui()
    
    def _setup_ui(self):
        self.setMinimumSize(250, 160)
        
        is_active = self.data.get('is_active', False)
        user = self.data.get('user')
        
        if is_active and user:
            bg_color = "rgb(20, 60, 40)"  
            status_text = "Đang sử dụng"
            status_color = "#00FF00"
        elif is_active:
            bg_color = "rgb(40, 60, 80)" 
            status_text = "Online"
            status_color = "#00BFFF"
        else:
            bg_color = "rgb(44, 49, 60)"
            status_text = "Offline"
            status_color = "gray"
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 10px;
                border: 1px solid rgb(60, 65, 75);
            }}
            QFrame:hover {{
                border: 1px solid rgb(85, 170, 255);
            }}
        """)
        
        layout = QVBoxLayout(self)
        
        machine_name = self.data.get('computer_name', 'Unknown PC')
        lbl_name = QLabel(f"🖥️ {machine_name}")
        lbl_name.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: white; "
            "border: none; background: transparent;"
        )
        layout.addWidget(lbl_name)
        
        ip_addr = self.data.get('ip_address', '0.0.0.0')
        lbl_ip = QLabel(f"IP: {ip_addr}")
        lbl_ip.setStyleSheet(
            "font-size: 11px; color: #aaa; border: none; background: transparent;"
        )
        layout.addWidget(lbl_ip)
        
        lbl_status = QLabel(f"Status: {status_text}")
        lbl_status.setStyleSheet(
            f"color: {status_color}; font-weight: bold; "
            "border: none; background: transparent;"
        )
        layout.addWidget(lbl_status)
        
        if user:
            lbl_user = QLabel(f"User: {user}")
            lbl_user.setStyleSheet("color: #ccc; border: none; background: transparent;")
            layout.addWidget(lbl_user)
        else:
            layout.addStretch()
        
        btn_detail = QPushButton("Chi tiết")
        btn_detail.setStyleSheet("""
            QPushButton {
                background-color: rgb(85, 170, 255);
                color: white;
                border-radius: 5px;
                padding: 5px;
                border: none;
            }
            QPushButton:hover { background-color: rgb(100, 190, 255); }
        """)
        btn_detail.clicked.connect(lambda: self.detail_clicked.emit(self.data))
        layout.addWidget(btn_detail)
    
    def update_data(self, new_data: dict):
        self.data = new_data
        while self.layout().count():
            child = self.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self._setup_ui()
