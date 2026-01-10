
from typing import List, Optional, Dict, Any
from models.database import DatabaseConnection
from config.settings import COLLECTION_SERVICES


class ServiceModel:
    
    def __init__(self):
        db = DatabaseConnection()
        self.collection = db.get_collection(COLLECTION_SERVICES)
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Lấy tất cả dịch vụ"""
        return list(self.collection.find().sort("service_id", 1))
    
    def get_by_id(self, service_id: int) -> Optional[Dict[str, Any]]:
        """Lấy dịch vụ theo ID"""
        return self.collection.find_one({"service_id": int(service_id)})
    
    def get_by_name(self, service_name: str) -> Optional[Dict[str, Any]]:
        """Lấy dịch vụ theo tên"""
        return self.collection.find_one({"service_name": service_name})
    
    def create(self, service_name: str, description: str, price: float, image_path: str = "") -> int:
        """Tạo dịch vụ mới"""
        last_service = self.collection.find_one(sort=[("service_id", -1)])
        new_id = 1 if not last_service else last_service["service_id"] + 1
        
        new_service = {
            "service_id": new_id,
            "service_name": service_name,
            "description": description,
            "price": float(price),
            "image_path": image_path
        }
        self.collection.insert_one(new_service)
        return new_id
    
    def update(self, service_id: int, data: Dict[str, Any]) -> bool:
        """Cập nhật thông tin dịch vụ"""
        result = self.collection.update_one(
            {"service_id": int(service_id)},
            {"$set": data}
        )
        return result.modified_count > 0
    
    def delete(self, service_id: int) -> bool:
        """Xóa dịch vụ"""
        result = self.collection.delete_one({"service_id": int(service_id)})
        return result.deleted_count > 0
