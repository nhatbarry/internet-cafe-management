from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

class ComputersController(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window 
        self.ui = main_window.ui
        self.db = main_window.db

    def load_computers_to_table(self):
        """ Lấy danh sách máy từ DB và đổ vào bảng """
        computers = self.db.get_all_computers()
        self.ui.table_machines.setRowCount(0) 
        
        for row_idx, comp in enumerate(computers):
            self.ui.table_machines.insertRow(row_idx)
            
            self.ui.table_machines.setItem(row_idx, 0, QTableWidgetItem(str(comp.get("computer_id"))))
            self.ui.table_machines.setItem(row_idx, 1, QTableWidgetItem(str(comp.get("computer_name"))))
            self.ui.table_machines.setItem(row_idx, 2, QTableWidgetItem(str(comp.get("ip_address"))))
            is_active = comp.get("is_active", False)
            status_text = "Hoạt động" if is_active else "Bảo trì/Tắt"
            self.ui.table_machines.setItem(row_idx, 3, QTableWidgetItem(status_text))
            user = comp.get("user")
            user_text = user if user else "Trống"
            self.ui.table_machines.setItem(row_idx, 4, QTableWidgetItem(user_text))

    def add_computer(self):
        name = self.ui.txt_comp_name.text()
        ip = self.ui.txt_comp_ip.text()
        is_active = self.ui.chk_comp_active.isChecked()

        if not name or not ip:
            QMessageBox.warning(self.mw, "Lỗi", "Vui lòng nhập Tên máy và IP!")
            return

        self.db.add_computer(name, ip, is_active)
        self.load_computers_to_table()
        self.clear_form()
        QMessageBox.information(self.mw, "Thành công", "Đã thêm máy trạm mới!")

    def update_computer(self):
        cid = self.ui.txt_comp_id.text()
        if not cid:
            return
        
        name = self.ui.txt_comp_name.text()
        ip = self.ui.txt_comp_ip.text()
        is_active = self.ui.chk_comp_active.isChecked()

        self.db.update_computer(cid, name, ip, is_active)
        self.load_computers_to_table()
        QMessageBox.information(self.mw, "Thành công", "Cập nhật máy trạm xong!")

    def delete_computer(self):
        cid = self.ui.txt_comp_id.text()
        if not cid:
            QMessageBox.warning(self.mw, "Lỗi", "Hãy chọn máy cần xóa!")
            return
            
        confirm = QMessageBox.question(self.mw, "Xác nhận", 
                                     f"Bạn có chắc muốn xóa máy ID {cid}?", 
                                     QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.db.delete_computer(cid)
            self.load_computers_to_table()
            self.clear_form()

    def fill_form_from_table(self):
        """ Khi bấm vào bảng -> Đổ dữ liệu xuống ô nhập """
        row = self.ui.table_machines.currentRow()
        if row >= 0:
            self.ui.txt_comp_id.setText(self.ui.table_machines.item(row, 0).text())
            self.ui.txt_comp_name.setText(self.ui.table_machines.item(row, 1).text())
            self.ui.txt_comp_ip.setText(self.ui.table_machines.item(row, 2).text())
            
            status_text = self.ui.table_machines.item(row, 3).text()
            self.ui.chk_comp_active.setChecked(status_text == "Hoạt động")

    def clear_form(self):
        self.ui.txt_comp_id.clear()
        self.ui.txt_comp_name.clear()
        self.ui.txt_comp_ip.clear()
        self.ui.chk_comp_active.setChecked(True)