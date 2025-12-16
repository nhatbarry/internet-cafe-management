
from controllers.base_controller import BaseController
from controllers.user_controller import UserController
from controllers.computer_controller import ComputerController
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
        
        self.computer_model = ComputerModel()
        
        self._init_connections()
        
        self._load_initial_data()
    
    def set_socket_service(self, socket_service):
        self.socket = socket_service
        self.computer_controller.set_socket_service(socket_service)
        
        if socket_service:
            socket_service.client_connected.connect(self._on_client_connected)
            socket_service.client_disconnected.connect(self._on_client_disconnected)
    
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
            UIFunctions.labelPage(self.view, "Dịch vụ")
        
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
            card = MachineCard(machine)
            card.detail_clicked.connect(self._on_machine_detail_clicked)
            self.ui.gridLayout_machines.addWidget(card, row, col)
            
            col += 1
            if col >= MACHINES_PER_ROW:
                col = 0
                row += 1
    
    def _on_machine_detail_clicked(self, machine_data: dict):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_machines)
        UIFunctions.labelPage(self.view, "Quản lý Máy trạm")
        
        self.ui.txt_comp_id.setText(str(machine_data.get("computer_id", "")))
        self.ui.txt_comp_name.setText(machine_data.get("computer_name", ""))
        self.ui.txt_comp_ip.setText(machine_data.get("ip_address", ""))
        self.ui.chk_comp_active.setChecked(machine_data.get("is_active", False))
        
        self.computer_controller.load_computers_to_table()
    
    def _on_client_connected(self, ip_address: str):
        self.computer_model.set_status_by_ip(ip_address, True)
        self.refresh_machine_grid()
        self.view.update_status(f"✅ Máy {ip_address} đã kết nối")
    
    def _on_client_disconnected(self, ip_address: str):
        self.computer_model.set_status_by_ip(ip_address, False)
        self.refresh_machine_grid()
        self.view.update_status(f"⚠️ Máy {ip_address} đã ngắt kết nối")
