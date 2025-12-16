
from PyQt5.QtWidgets import QTableWidgetItem
from controllers.base_controller import BaseController
from models.computer_model import ComputerModel


class ComputerController(BaseController):
    
    def __init__(self, view, socket_service=None):
        super().__init__(view)
        self.model = ComputerModel()
        self.socket = socket_service
    
    def set_socket_service(self, socket_service):
        self.socket = socket_service
    
    def load_computers_to_table(self):
        computers = self.model.get_all()
        self.ui.table_machines.setRowCount(0)
        
        for row_idx, comp in enumerate(computers):
            self.ui.table_machines.insertRow(row_idx)
            self.ui.table_machines.setItem(row_idx, 0, QTableWidgetItem(str(comp.get("computer_id", ""))))
            self.ui.table_machines.setItem(row_idx, 1, QTableWidgetItem(str(comp.get("computer_name", ""))))
            self.ui.table_machines.setItem(row_idx, 2, QTableWidgetItem(str(comp.get("ip_address", ""))))
            
            is_active = comp.get("is_active", False)
            status_text = "Hoạt động" if is_active else "Tắt/Bảo trì"
            self.ui.table_machines.setItem(row_idx, 3, QTableWidgetItem(status_text))
            
            user = comp.get("user") or "Trống"
            self.ui.table_machines.setItem(row_idx, 4, QTableWidgetItem(user))
    
    def add_computer(self):
        name = self.ui.txt_comp_name.text().strip()
        ip = self.ui.txt_comp_ip.text().strip()
        is_active = self.ui.chk_comp_active.isChecked()
        
        if not name or not ip:
            self.show_warning("Lỗi", "Vui lòng nhập Tên máy và IP!")
            return
        
        if self.model.get_by_ip(ip):
            self.show_warning("Lỗi", f"IP '{ip}' đã tồn tại!")
            return
        
        self.model.create(name, ip, is_active)
        self.load_computers_to_table()
        self.clear_form()
        self.show_info("Thành công", "Đã thêm máy trạm mới!")
        
        if hasattr(self.view, 'refresh_machine_grid'):
            self.view.refresh_machine_grid()
    
    def update_computer(self):
        comp_id = self.ui.txt_comp_id.text().strip()
        if not comp_id:
            self.show_warning("Lỗi", "Vui lòng chọn máy cần sửa!")
            return
        
        data = {
            "computer_name": self.ui.txt_comp_name.text().strip(),
            "ip_address": self.ui.txt_comp_ip.text().strip(),
            "is_active": self.ui.chk_comp_active.isChecked()
        }
        
        if self.model.update(int(comp_id), data):
            self.load_computers_to_table()
            self.show_info("Thành công", "Đã cập nhật máy trạm!")
            
            if hasattr(self.view, 'refresh_machine_grid'):
                self.view.refresh_machine_grid()
        else:
            self.show_error("Lỗi", "Không thể cập nhật!")
    
    def delete_computer(self):
        comp_id = self.ui.txt_comp_id.text().strip()
        if not comp_id:
            self.show_warning("Lỗi", "Vui lòng chọn máy cần xóa!")
            return
        
        if not self.confirm("Xác nhận", f"Bạn có chắc muốn xóa máy ID {comp_id}?"):
            return
        
        if self.model.delete(int(comp_id)):
            self.load_computers_to_table()
            self.clear_form()
            self.show_info("Thành công", "Đã xóa máy trạm!")
            
            if hasattr(self.view, 'refresh_machine_grid'):
                self.view.refresh_machine_grid()
        else:
            self.show_error("Lỗi", "Không thể xóa!")
    
    def fill_form_from_table(self):
        row = self.ui.table_machines.currentRow()
        if row < 0:
            return
        
        self.ui.txt_comp_id.setText(self.ui.table_machines.item(row, 0).text())
        self.ui.txt_comp_name.setText(self.ui.table_machines.item(row, 1).text())
        self.ui.txt_comp_ip.setText(self.ui.table_machines.item(row, 2).text())
        self.ui.chk_comp_active.setChecked(
            self.ui.table_machines.item(row, 3).text() == "Hoạt động"
        )
    
    def clear_form(self):
        self.ui.txt_comp_id.clear()
        self.ui.txt_comp_name.clear()
        self.ui.txt_comp_ip.clear()
        self.ui.chk_comp_active.setChecked(True)
    
    
    def lock_computer(self):
        """Khóa máy đang chọn"""
        row = self.ui.table_machines.currentRow()
        if row < 0:
            self.show_warning("Lỗi", "Vui lòng chọn máy cần khóa!")
            return
        
        target_ip = self.ui.table_machines.item(row, 2).text()
        
        if self.socket and self.socket.send_command(target_ip, "LOCK"):
            self.model.set_status_by_ip(target_ip, False)
            self.load_computers_to_table()
            self.show_info("Thành công", f"Đã gửi lệnh khóa tới {target_ip}")
        else:
            self.show_warning("Lỗi", f"Máy {target_ip} chưa kết nối!")
    
    def unlock_computer(self):
        """Mở khóa máy đang chọn"""
        row = self.ui.table_machines.currentRow()
        if row < 0:
            self.show_warning("Lỗi", "Vui lòng chọn máy cần mở khóa!")
            return
        
        target_ip = self.ui.table_machines.item(row, 2).text()
        
        if self.socket and self.socket.send_command(target_ip, "UNLOCK"):
            self.model.set_status_by_ip(target_ip, True)
            self.load_computers_to_table()
            self.show_info("Thành công", f"Đã mở khóa {target_ip}")
        else:
            self.show_warning("Lỗi", f"Máy {target_ip} chưa kết nối!")
    
    def shutdown_computer(self):
        """Tắt máy đang chọn"""
        row = self.ui.table_machines.currentRow()
        if row < 0:
            self.show_warning("Lỗi", "Vui lòng chọn máy cần tắt!")
            return
        
        target_ip = self.ui.table_machines.item(row, 2).text()
        
        if not self.confirm("Xác nhận", f"Bạn có chắc muốn TẮT máy {target_ip}?"):
            return
        
        if self.socket and self.socket.send_command(target_ip, "SHUTDOWN"):
            self.show_info("Thành công", f"Đã gửi lệnh tắt máy tới {target_ip}")
        else:
            self.show_warning("Lỗi", f"Máy {target_ip} chưa kết nối!")
