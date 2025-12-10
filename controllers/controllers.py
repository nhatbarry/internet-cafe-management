from PyQt5.QtCore import QObject
from ui.app_modules import UIFunctions

from controllers.controllers_member import MembersController
from controllers.controllers_computers import ComputersController

class MainController(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window 
        self.ui = main_window.ui
        self.db = main_window.db 

        self.members_controller = MembersController(main_window)
        self.computers_controller = ComputersController(main_window)

        self.init_connections()

    def init_connections(self):
        self.ui.btn_open_file.clicked.connect(self.handle_menu_click)
        self.ui.btn_save.clicked.connect(self.handle_menu_click)
        self.ui.btn_new.clicked.connect(self.handle_menu_click)
        self.ui.btn_new_user.clicked.connect(self.handle_menu_click)
        self.ui.btn_settings.clicked.connect(self.handle_menu_click)
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self.mw, 220, True))

        self.ui.btn_add_user.clicked.connect(self.members_controller.add_user)
        self.ui.btn_edit_user.clicked.connect(self.members_controller.update_user)
        self.ui.btn_delete_user.clicked.connect(self.members_controller.delete_user)
        self.ui.btn_clear_input.clicked.connect(self.members_controller.clear_form)
        self.ui.table_users.itemClicked.connect(self.members_controller.fill_form_from_table)

        self.ui.btn_add_machine.clicked.connect(self.computers_controller.add_computer)
        self.ui.btn_edit_machine.clicked.connect(self.computers_controller.update_computer)
        self.ui.btn_delete_machine.clicked.connect(self.computers_controller.delete_computer)
        self.ui.btn_clear_machine.clicked.connect(self.computers_controller.clear_form)
        self.ui.table_machines.itemClicked.connect(self.computers_controller.fill_form_from_table)

    def handle_menu_click(self):
        btnWidget = self.sender()
        btnName = btnWidget.objectName()
        UIFunctions.resetStyle(self.mw, btnName)
        btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        if btnName == "btn_dashboard":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.labelPage(self.mw, "Tổng quan")
        
        elif btnName == "btn_machines":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_machines)
            UIFunctions.labelPage(self.mw, "Quản lý Máy trạm")
            self.computers_controller.load_computers_to_table()

        elif btnName == "btn_members":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_members)
            UIFunctions.labelPage(self.mw, "Quản lý Hội viên")
            
            self.members_controller.load_users_to_table()

        elif btnName == "btn_services":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_services)
            UIFunctions.labelPage(self.mw, "Dịch vụ")
            
        elif btnName == "btn_settings":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_settings)
            UIFunctions.labelPage(self.mw, "Cài đặt")