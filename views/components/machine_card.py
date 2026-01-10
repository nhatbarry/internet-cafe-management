
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QScrollArea, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QScreen


class MachineCard(QFrame):
    
    detail_clicked = pyqtSignal(dict)
    
    def __init__(self, machine_data: dict, parent=None):
        super().__init__(parent)
        self.data = machine_data
        self._setup_ui()
    
    def _setup_ui(self):
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        
        if screen_size.width() >= 1920:
            card_width = 320
            card_height = 260
        else:
            card_width = 280
            card_height = 220
            
        self.setFixedSize(card_width, card_height)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
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
        layout.setSpacing(3)
        
        machine_name = self.data.get('computer_name', 'Unknown PC')
        lbl_name = QLabel(f"🖥️ {machine_name}")
        lbl_name.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: white; "
            "border: none; background: transparent;"
        )
        layout.addWidget(lbl_name)
        
        ip_addr = self.data.get('ip_address', '0.0.0.0')
        lbl_ip = QLabel(f"IP: {ip_addr}")
        lbl_ip.setStyleSheet(
            "font-size: 10px; color: #aaa; border: none; background: transparent;"
        )
        layout.addWidget(lbl_ip)
        
        lbl_status = QLabel(f"Status: {status_text}")
        lbl_status.setStyleSheet(
            f"font-size: 11px; color: {status_color}; font-weight: bold; "
            "border: none; background: transparent;"
        )
        layout.addWidget(lbl_status)
        
        if user:
            lbl_user = QLabel(f"User: {user}")
            lbl_user.setStyleSheet(
                "font-size: 10px; color: #ccc; border: none; background: transparent;"
            )
            lbl_user.setWordWrap(True)
            layout.addWidget(lbl_user)
        
        support_messages = self.data.get('support_messages', [])
        if support_messages:
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setMaximumHeight(100)
            scroll_area.setStyleSheet("""
                QScrollArea {
                    border: 1px solid rgb(60, 65, 75);
                    background: transparent;
                    border-radius: 5px;
                }
                QScrollBar:vertical {
                    background: rgb(52, 59, 72);
                    width: 8px;
                    border-radius: 4px;
                }
                QScrollBar::handle:vertical {
                    background: rgb(85, 170, 255);
                    border-radius: 4px;
                }
            """)
            
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout(scroll_widget)
            scroll_layout.setSpacing(2)
            scroll_layout.setContentsMargins(5, 5, 5, 5)
            
            for msg in support_messages:
                text = msg.get('text', '')
                is_read = msg.get('read', False)
                timestamp = msg.get('timestamp', '')
                
                is_order = 'order' in text.lower() or 'đã order' in text.lower()
                
                if is_order:
                    msg_color = "#4CAF50"
                    icon = "🛒"
                else:
                    msg_color = "#FFB74D"
                    icon = "🔔"
                
                font_weight = "normal" if is_read else "bold"
                msg_label = QLabel(f"{icon} [{timestamp}] {text}")
                msg_label.setStyleSheet(
                    f"color: {msg_color}; font-weight: {font_weight}; "
                    "font-size: 10px; border: none; background: transparent; "
                    "padding: 3px;"
                )
                msg_label.setWordWrap(True)
                scroll_layout.addWidget(msg_label)
            
            scroll_layout.addStretch()
            scroll_area.setWidget(scroll_widget)
            layout.addWidget(scroll_area)
        
        layout.addStretch()
        
        btn_detail = QPushButton("Chi tiết")
        btn_detail.setStyleSheet("""
            QPushButton {
                background-color: rgb(85, 170, 255);
                color: white;
                border-radius: 5px;
                padding: 5px;
                border: none;
                font-size: 11px;
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
