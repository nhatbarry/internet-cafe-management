from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

class MembersController(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window 
        self.ui = main_window.ui
        self.db = main_window.db

    def load_users_to_table(self):
        """ Lấy dữ liệu từ DB đổ vào bảng """
        users = self.db.get_all_users()
        self.ui.table_users.setRowCount(0)
        
        for row_idx, user in enumerate(users):
            self.ui.table_users.insertRow(row_idx)
            self.ui.table_users.setItem(row_idx, 0, QTableWidgetItem(str(user.get("user_id"))))
            self.ui.table_users.setItem(row_idx, 1, QTableWidgetItem(str(user.get("username"))))
            self.ui.table_users.setItem(row_idx, 2, QTableWidgetItem(str(user.get("password"))))
            self.ui.table_users.setItem(row_idx, 3, QTableWidgetItem(str(user.get("balance"))))
            vip_status = "Có" if user.get("is_vip") else "Không"
            self.ui.table_users.setItem(row_idx, 4, QTableWidgetItem(vip_status))

    def add_user(self):
        user = self.ui.txt_username.text()
        pwd = self.ui.txt_password.text()
        bal = self.ui.txt_balance.text()
        is_vip = self.ui.chk_vip.isChecked()

        if not user or not pwd:
            QMessageBox.warning(self.mw, "Lỗi", "Vui lòng nhập tên và mật khẩu!")
            return

        self.db.add_user(user, pwd, bal or 0, is_vip)
        self.load_users_to_table()
        self.clear_form()
        QMessageBox.information(self.mw, "Thành công", "Đã thêm hội viên!")

    def update_user(self):
        uid = self.ui.txt_user_id.text()
        if not uid:
            return
        
        user = self.ui.txt_username.text()
        pwd = self.ui.txt_password.text()
        bal = self.ui.txt_balance.text()
        is_vip = self.ui.chk_vip.isChecked()

        self.db.update_user(uid, user, pwd, bal, is_vip)
        self.load_users_to_table()
        QMessageBox.information(self.mw, "Thành công", "Cập nhật xong!")

    def delete_user(self):
        uid = self.ui.txt_user_id.text()
        if not uid:
            QMessageBox.warning(self.mw, "Lỗi", "Hãy chọn user cần xóa!")
            return
            
        confirm = QMessageBox.question(self.mw, "Xác nhận", "Bạn có chắc muốn xóa?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.db.delete_user(uid)
            self.load_users_to_table()
            self.clear_form()

    def fill_form_from_table(self):
        """ Khi bấm vào bảng -> Đổ dữ liệu xuống ô nhập """
        row = self.ui.table_users.currentRow()
        if row >= 0:
            self.ui.txt_user_id.setText(self.ui.table_users.item(row, 0).text())
            self.ui.txt_username.setText(self.ui.table_users.item(row, 1).text())
            self.ui.txt_password.setText(self.ui.table_users.item(row, 2).text())
            self.ui.txt_balance.setText(self.ui.table_users.item(row, 3).text())
            
            is_vip = self.ui.table_users.item(row, 4).text() == "Có"
            self.ui.chk_vip.setChecked(is_vip)

    def clear_form(self):
        self.ui.txt_user_id.clear()
        self.ui.txt_username.clear()
        self.ui.txt_password.clear()
        self.ui.txt_balance.clear()
        self.ui.chk_vip.setChecked(False)