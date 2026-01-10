
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QPixmap
from controllers.base_controller import BaseController
from models.service_model import ServiceModel
import os


class ServiceController(BaseController):
    
    def __init__(self, view):
        super().__init__(view)
        self.model = ServiceModel()
        self.current_image_path = ""
    
    def load_services_to_table(self):
        """Load tất cả dịch vụ vào bảng"""
        services = self.model.get_all()
        self.ui.table_services.setRowCount(0)
        
        for row_idx, service in enumerate(services):
            self.ui.table_services.insertRow(row_idx)
            self.ui.table_services.setItem(row_idx, 0, QTableWidgetItem(str(service.get("service_id", ""))))
            self.ui.table_services.setItem(row_idx, 1, QTableWidgetItem(str(service.get("service_name", ""))))
            self.ui.table_services.setItem(row_idx, 2, QTableWidgetItem(str(service.get("description", ""))))
            self.ui.table_services.setItem(row_idx, 3, QTableWidgetItem(str(service.get("price", 0))))
            self.ui.table_services.setItem(row_idx, 4, QTableWidgetItem(str(service.get("image_path", ""))))
    
    def add_service(self):
        """Thêm dịch vụ mới"""
        service_name = self.ui.txt_service_name.text().strip()
        description = self.ui.txt_service_desc.toPlainText().strip()
        price = self.ui.txt_service_price.text().strip() or "0"
        image_path = self.current_image_path
        
        if not service_name:
            self.show_warning("Lỗi", "Vui lòng nhập tên dịch vụ!")
            return
        
        try:
            price = float(price)
        except ValueError:
            self.show_warning("Lỗi", "Giá bán phải là số!")
            return
        
        if self.model.get_by_name(service_name):
            self.show_warning("Lỗi", f"Dịch vụ '{service_name}' đã tồn tại!")
            return
        
        self.model.create(service_name, description, price, image_path)
        self.load_services_to_table()
        self.clear_form()
        self.show_info("Thành công", "Đã thêm dịch vụ mới!")
    
    def update_service(self):
        """Cập nhật dịch vụ"""
        service_id = self.ui.txt_service_id.text().strip()
        if not service_id:
            self.show_warning("Lỗi", "Vui lòng chọn dịch vụ cần sửa!")
            return
        
        service_name = self.ui.txt_service_name.text().strip()
        if not service_name:
            self.show_warning("Lỗi", "Vui lòng nhập tên dịch vụ!")
            return
        
        try:
            price = float(self.ui.txt_service_price.text() or 0)
        except ValueError:
            self.show_warning("Lỗi", "Giá bán phải là số!")
            return
        
        data = {
            "service_name": service_name,
            "description": self.ui.txt_service_desc.toPlainText().strip(),
            "price": price,
            "image_path": self.current_image_path
        }
        
        if self.model.update(int(service_id), data):
            self.load_services_to_table()
            self.show_info("Thành công", "Đã cập nhật dịch vụ!")
        else:
            self.show_error("Lỗi", "Không thể cập nhật!")
    
    def delete_service(self):
        """Xóa dịch vụ"""
        service_id = self.ui.txt_service_id.text().strip()
        if not service_id:
            self.show_warning("Lỗi", "Vui lòng chọn dịch vụ cần xóa!")
            return
        
        if not self.confirm("Xác nhận", f"Bạn có chắc muốn xóa dịch vụ ID {service_id}?"):
            return
        
        if self.model.delete(int(service_id)):
            self.load_services_to_table()
            self.clear_form()
            self.show_info("Thành công", "Đã xóa dịch vụ!")
        else:
            self.show_error("Lỗi", "Không thể xóa!")
    
    def fill_form_from_table(self):
        """Điền form từ dòng được chọn trong bảng"""
        row = self.ui.table_services.currentRow()
        if row < 0:
            return
        
        self.ui.txt_service_id.setText(self.ui.table_services.item(row, 0).text())
        self.ui.txt_service_name.setText(self.ui.table_services.item(row, 1).text())
        self.ui.txt_service_desc.setPlainText(self.ui.table_services.item(row, 2).text())
        self.ui.txt_service_price.setText(self.ui.table_services.item(row, 3).text())
        
        image_path = self.ui.table_services.item(row, 4).text()
        self.current_image_path = image_path
        if image_path and os.path.exists(image_path):
            self.display_image(image_path)
        else:
            self.clear_image()
    
    def browse_image(self):
        """Chọn ảnh từ file system"""
        file_name, _ = QFileDialog.getOpenFileName(
            self.view,
            "Chọn ảnh",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_name:
            self.current_image_path = file_name
            self.display_image(file_name)
    
    def display_image(self, image_path: str):
        """Hiển thị ảnh trong label"""
        if hasattr(self.ui, 'lbl_service_image'):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.ui.lbl_service_image.size(),
                    aspectRatioMode=1,
                    transformMode=1
                )
                self.ui.lbl_service_image.setPixmap(scaled_pixmap)
    
    def clear_image(self):
        """Xóa ảnh hiển thị"""
        if hasattr(self.ui, 'lbl_service_image'):
            self.ui.lbl_service_image.clear()
            self.ui.lbl_service_image.setText("Chưa có ảnh")
    
    def clear_form(self):
        """Xóa toàn bộ form"""
        self.ui.txt_service_id.clear()
        self.ui.txt_service_name.clear()
        self.ui.txt_service_desc.clear()
        self.ui.txt_service_price.clear()
        self.current_image_path = ""
        self.clear_image()
