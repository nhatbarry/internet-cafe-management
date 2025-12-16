
from PyQt5.QtWidgets import QTableWidgetItem
from controllers.base_controller import BaseController
from models.user_model import UserModel


class UserController(BaseController):
    
    def __init__(self, view):
        super().__init__(view)
        self.model = UserModel()
    
    def load_users_to_table(self):
        users = self.model.get_all()
        self.ui.table_users.setRowCount(0)
        
        for row_idx, user in enumerate(users):
            self.ui.table_users.insertRow(row_idx)
            self.ui.table_users.setItem(row_idx, 0, QTableWidgetItem(str(user.get("user_id", ""))))
            self.ui.table_users.setItem(row_idx, 1, QTableWidgetItem(str(user.get("username", ""))))
            self.ui.table_users.setItem(row_idx, 2, QTableWidgetItem(str(user.get("password", ""))))
            self.ui.table_users.setItem(row_idx, 3, QTableWidgetItem(str(user.get("balance", 0))))
            vip_status = "Có" if user.get("is_vip") else "Không"
            self.ui.table_users.setItem(row_idx, 4, QTableWidgetItem(vip_status))
    
    def add_user(self):
        username = self.ui.txt_username.text().strip()
        password = self.ui.txt_password.text().strip()
        balance = self.ui.txt_balance.text().strip() or "0"
        is_vip = self.ui.chk_vip.isChecked()
        
        if not username or not password:
            self.show_warning("Lỗi", "Vui lòng nhập tên và mật khẩu!")
            return
        
        try:
            balance = float(balance)
        except ValueError:
            self.show_warning("Lỗi", "Số dư phải là số!")
            return
        
        if self.model.get_by_username(username):
            self.show_warning("Lỗi", f"Username '{username}' đã tồn tại!")
            return
        
        self.model.create(username, password, balance, is_vip)
        self.load_users_to_table()
        self.clear_form()
        self.show_info("Thành công", "Đã thêm hội viên mới!")
    
    def update_user(self):
        user_id = self.ui.txt_user_id.text().strip()
        if not user_id:
            self.show_warning("Lỗi", "Vui lòng chọn hội viên cần sửa!")
            return
        
        data = {
            "username": self.ui.txt_username.text().strip(),
            "password": self.ui.txt_password.text().strip(),
            "balance": float(self.ui.txt_balance.text() or 0),
            "is_vip": self.ui.chk_vip.isChecked()
        }
        
        if self.model.update(int(user_id), data):
            self.load_users_to_table()
            self.show_info("Thành công", "Đã cập nhật hội viên!")
        else:
            self.show_error("Lỗi", "Không thể cập nhật!")
    
    def delete_user(self):
        user_id = self.ui.txt_user_id.text().strip()
        if not user_id:
            self.show_warning("Lỗi", "Vui lòng chọn hội viên cần xóa!")
            return
        
        if not self.confirm("Xác nhận", f"Bạn có chắc muốn xóa hội viên ID {user_id}?"):
            return
        
        if self.model.delete(int(user_id)):
            self.load_users_to_table()
            self.clear_form()
            self.show_info("Thành công", "Đã xóa hội viên!")
        else:
            self.show_error("Lỗi", "Không thể xóa!")
    
    def fill_form_from_table(self):
        row = self.ui.table_users.currentRow()
        if row < 0:
            return
        
        self.ui.txt_user_id.setText(self.ui.table_users.item(row, 0).text())
        self.ui.txt_username.setText(self.ui.table_users.item(row, 1).text())
        self.ui.txt_password.setText(self.ui.table_users.item(row, 2).text())
        self.ui.txt_balance.setText(self.ui.table_users.item(row, 3).text())
        self.ui.chk_vip.setChecked(self.ui.table_users.item(row, 4).text() == "Có")
    
    def clear_form(self):
        self.ui.txt_user_id.clear()
        self.ui.txt_username.clear()
        self.ui.txt_password.clear()
        self.ui.txt_balance.clear()
        self.ui.chk_vip.setChecked(False)
