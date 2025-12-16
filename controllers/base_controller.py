
from PyQt5.QtCore import QObject


class BaseController(QObject):
    
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.ui = view.ui
    
    def show_info(self, title: str, message: str):
        self.view.show_message(title, message, "info")
    
    def show_warning(self, title: str, message: str):
        self.view.show_message(title, message, "warning")
    
    def show_error(self, title: str, message: str):
        self.view.show_message(title, message, "error")
    
    def confirm(self, title: str, message: str) -> bool:
        return self.view.confirm_dialog(title, message)
