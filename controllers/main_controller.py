
from controllers.base_controller import BaseController
from controllers.user_controller import UserController
from controllers.computer_controller import ComputerController
from controllers.service_controller import ServiceController
from views.ui.ui_functions import UIFunctions
from views.components.machine_card import MachineCard
from models.computer_model import ComputerModel
from config.settings import MACHINES_PER_ROW


class MainController(BaseController):
    
    def __init__(self, view, socket_service=None):
        super().__init__(view)
        
        self.socket = socket_service
        
        self.user_controller = UserController(view)
        self.computer_controller = ComputerController(view, socket_service)
        self.service_controller = ServiceController(view)
        
        self.computer_model = ComputerModel()
        
        self.support_messages = {}
        
        if socket_service:
            socket_service.client_connected.connect(self._on_client_connected)
            socket_service.client_disconnected.connect(self._on_client_disconnected)
            socket_service.message_received.connect(self._on_message_received)
        
        self._init_connections()
        
        self._load_initial_data()
    
    def set_socket_service(self, socket_service):
        self.socket = socket_service
        self.computer_controller.set_socket_service(socket_service)
        
        if not hasattr(self, 'support_messages'):
            self.support_messages = {}
        
        if socket_service:
            socket_service.client_connected.connect(self._on_client_connected)
            socket_service.client_disconnected.connect(self._on_client_disconnected)
            socket_service.message_received.connect(self._on_message_received)
    
    def _init_connections(self):
        self.ui.btn_open_file.clicked.connect(self._handle_menu_click)
        self.ui.btn_save.clicked.connect(self._handle_menu_click)
        self.ui.btn_new.clicked.connect(self._handle_menu_click)
        self.ui.btn_new_user.clicked.connect(self._handle_menu_click)
        self.ui.btn_settings.clicked.connect(self._handle_menu_click)
        self.ui.btn_toggle_menu.clicked.connect(
            lambda: UIFunctions.toggleMenu(self.view, 220, True)
        )
        
        self.ui.btn_add_user.clicked.connect(self.user_controller.add_user)
        self.ui.btn_edit_user.clicked.connect(self.user_controller.update_user)
        self.ui.btn_delete_user.clicked.connect(self.user_controller.delete_user)
        self.ui.btn_clear_input.clicked.connect(self.user_controller.clear_form)
        self.ui.table_users.itemClicked.connect(self.user_controller.fill_form_from_table)
        
        self.ui.btn_add_machine.clicked.connect(self.computer_controller.add_computer)
        self.ui.btn_edit_machine.clicked.connect(self.computer_controller.update_computer)
        self.ui.btn_delete_machine.clicked.connect(self.computer_controller.delete_computer)
        self.ui.btn_clear_machine.clicked.connect(self.computer_controller.clear_form)
        self.ui.table_machines.itemClicked.connect(self.computer_controller.fill_form_from_table)
        
        if hasattr(self.ui, 'btn_add_service'):
            self.ui.btn_add_service.clicked.connect(self.service_controller.add_service)
        if hasattr(self.ui, 'btn_edit_service'):
            self.ui.btn_edit_service.clicked.connect(self.service_controller.update_service)
        if hasattr(self.ui, 'btn_delete_service'):
            self.ui.btn_delete_service.clicked.connect(self.service_controller.delete_service)
        if hasattr(self.ui, 'btn_clear_service'):
            self.ui.btn_clear_service.clicked.connect(self.service_controller.clear_form)
        if hasattr(self.ui, 'btn_browse_image'):
            self.ui.btn_browse_image.clicked.connect(self.service_controller.browse_image)
        if hasattr(self.ui, 'table_services'):
            self.ui.table_services.itemClicked.connect(self.service_controller.fill_form_from_table)
        
        if hasattr(self.ui, 'btn_lock_machine'):
            self.ui.btn_lock_machine.clicked.connect(self.computer_controller.lock_computer)
        if hasattr(self.ui, 'btn_unlock_machine'):
            self.ui.btn_unlock_machine.clicked.connect(self.computer_controller.unlock_computer)
        if hasattr(self.ui, 'btn_shutdown_machine'):
            self.ui.btn_shutdown_machine.clicked.connect(self.computer_controller.shutdown_computer)
    
    def _load_initial_data(self):
        self.refresh_machine_grid()
    
    def _handle_menu_click(self):
        btn_widget = self.sender()
        btn_name = btn_widget.objectName()
        
        UIFunctions.resetStyle(self.view, btn_name)
        btn_widget.setStyleSheet(UIFunctions.selectMenu(btn_widget.styleSheet()))
        
        if btn_name == "btn_dashboard":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.labelPage(self.view, "Tổng quan")
            self.refresh_machine_grid()
        
        elif btn_name == "btn_machines":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_machines)
            UIFunctions.labelPage(self.view, "Quản lý Máy trạm")
            self.computer_controller.load_computers_to_table()
        
        elif btn_name == "btn_members":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_members)
            UIFunctions.labelPage(self.view, "Quản lý Hội viên")
            self.user_controller.load_users_to_table()
        
        elif btn_name == "btn_services":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_services)
            UIFunctions.labelPage(self.view, "Quản lý Dịch vụ")
            self.service_controller.load_services_to_table()
        
        elif btn_name == "btn_settings":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_settings)
            UIFunctions.labelPage(self.view, "Cài đặt")
    
    def refresh_machine_grid(self):
        if not hasattr(self.ui, 'gridLayout_machines'):
            return
        
        while self.ui.gridLayout_machines.count():
            child = self.ui.gridLayout_machines.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        machines = self.computer_model.get_all()
        
        row = 0
        col = 0
        for machine in machines:
            machine_copy = machine.copy()
            ip_address = machine.get('ip_address')
            if ip_address in self.support_messages:
                machine_copy['support_messages'] = self.support_messages[ip_address]
            
            card = MachineCard(machine_copy)
            card.detail_clicked.connect(self._on_machine_detail_clicked)
            self.ui.gridLayout_machines.addWidget(card, row, col)
            
            col += 1
            if col >= MACHINES_PER_ROW:
                col = 0
                row += 1
    
    def _on_machine_detail_clicked(self, machine_data: dict):
        ip_address = machine_data.get("ip_address")
        if ip_address and ip_address in self.support_messages:
            for msg in self.support_messages[ip_address]:
                msg['read'] = True
            self.refresh_machine_grid()
        
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_machines)
        UIFunctions.labelPage(self.view, "Quản lý Máy trạm")
        
        self.ui.txt_comp_id.setText(str(machine_data.get("computer_id", "")))
        self.ui.txt_comp_name.setText(machine_data.get("computer_name", ""))
        self.ui.txt_comp_ip.setText(machine_data.get("ip_address", ""))
        self.ui.txt_comp_price.setText(str(machine_data.get("price", 5000)))
        
        self.computer_controller.load_computers_to_table()
    
    def _on_client_connected(self, ip_address: str):
        computer = self.computer_model.get_by_ip(ip_address)
        if computer:
            success = self.computer_model.set_status_by_ip(ip_address, True)
            if success:
                print(f"✓ Máy '{computer.get('computer_name')}' (ID: {computer.get('computer_id')}) - IP: {ip_address} đã kết nối và chuyển sang trạng thái ONLINE")
                self.view.update_status(f"Máy {computer.get('computer_name')} ({ip_address}) đã kết nối")
            else:
                print(f"✗ Không thể cập nhật trạng thái cho IP: {ip_address}")
                self.view.update_status(f"Lỗi cập nhật trạng thái máy {ip_address}")
        else:
            print(f"⚠ IP {ip_address} kết nối nhưng không có trong danh sách máy trạm")
            self.view.update_status(f"Cảnh báo: IP {ip_address} không xác định đã kết nối")
        
        self.refresh_machine_grid()
        if self.ui.stackedWidget.currentWidget() == self.ui.page_machines:
            self.computer_controller.load_computers_to_table()
    
    def _on_client_disconnected(self, ip_address: str):
        computer = self.computer_model.get_by_ip(ip_address)
        if computer:
            if computer.get('user'):
                self.computer_model.release_user(computer.get('computer_id'))
                print(f"🚪 User {computer.get('user')} đã đăng xuất khỏi {computer.get('computer_name')}")
            
            success = self.computer_model.set_status_by_ip(ip_address, False)
            if success:
                print(f"Máy '{computer.get('computer_name')}' (ID: {computer.get('computer_id')}) - IP: {ip_address} đã ngắt kết nối và chuyển sang trạng thái OFFLINE")
                self.view.update_status(f"Máy {computer.get('computer_name')} ({ip_address}) đã ngắt kết nối")
            else:
                print(f"Không thể cập nhật trạng thái cho IP: {ip_address}")
                self.view.update_status(f"Lỗi cập nhật trạng thái máy {ip_address}")
        else:
            print(f"IP {ip_address} ngắt kết nối nhưng không có trong danh sách máy trạm")
            self.view.update_status(f"IP {ip_address} đã ngắt kết nối")
        
        if ip_address in self.support_messages:
            del self.support_messages[ip_address]
            print(f"🗑️ Đã xóa support messages của {ip_address}")
        
        self.refresh_machine_grid()
        if self.ui.stackedWidget.currentWidget() == self.ui.page_machines:
            self.computer_controller.load_computers_to_table()
    
    def _on_message_received(self, ip_address: str, message: str):
        """Xử lý message nhận được từ client"""
        if message.startswith("SUPPORT:"):
            support_text = message.replace("SUPPORT:", "", 1)
            computer = self.computer_model.get_by_ip(ip_address)
            if computer:
                if ip_address not in self.support_messages:
                    self.support_messages[ip_address] = []
                
                from datetime import datetime
                new_message = {
                    'text': support_text,
                    'read': False,
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                }
                self.support_messages[ip_address].append(new_message)
                
                print(f"📩 Nhận yêu cầu hỗ trợ từ {computer.get('computer_name')} ({ip_address}): {support_text}")
                self.view.update_status(f"Yêu cầu hỗ trợ từ {computer.get('computer_name')}")
                self.refresh_machine_grid()
            else:
                print(f"⚠ Nhận message từ IP không xác định: {ip_address}")
        
        elif message.startswith("LOGIN:"):
            username = message.replace("LOGIN:", "", 1)
            computer = self.computer_model.get_by_ip(ip_address)
            if computer:
                self.computer_model.assign_user(computer.get('computer_id'), username)
                print(f"👤 User {username} đã đăng nhập vào {computer.get('computer_name')} ({ip_address})")
                self.view.update_status(f"{username} đăng nhập vào {computer.get('computer_name')}")
                self.refresh_machine_grid()
                if self.ui.stackedWidget.currentWidget() == self.ui.page_machines:
                    self.computer_controller.load_computers_to_table()
            else:
                print(f"⚠ Nhận LOGIN từ IP không xác định: {ip_address}")
        
        elif message == "GET_PRICE":
            computer = self.computer_model.get_by_ip(ip_address)
            if computer:
                price = computer.get('price', 5000)
                if self.socket and self.socket.send_command(ip_address, f"PRICE:{price}"):
                    print(f"💰 Gửi giá máy {price} VND/h cho {ip_address}")
            else:
                print(f"⚠ Yêu cầu GET_PRICE từ IP không xác định: {ip_address}")
        
        elif message.startswith("ORDER:"):
            parts = message.replace("ORDER:", "", 1).split(":", 2)
            if len(parts) >= 3:
                username = parts[0]
                service_name = parts[1]
                price = parts[2]
                
                computer = self.computer_model.get_by_ip(ip_address)
                if computer:
                    if ip_address not in self.support_messages:
                        self.support_messages[ip_address] = []
                    
                    from datetime import datetime
                    order_message = {
                        'text': f"{username} đã order 1 {service_name} giá {price} VND",
                        'read': False,
                        'timestamp': datetime.now().strftime('%H:%M:%S'),
                        'type': 'order'
                    }
                    self.support_messages[ip_address].append(order_message)
                    
                    print(f"🛒 {username} đặt hàng {service_name} (Giá: {price} VND) từ {computer.get('computer_name')} ({ip_address})")
                    self.view.update_status(f"Đơn hàng mới từ {computer.get('computer_name')}: {service_name}")
                    self.refresh_machine_grid()
                else:
                    print(f"⚠ Nhận ORDER từ IP không xác định: {ip_address}")
            else:
                print(f"⚠ ORDER message format không đúng: {message}")
