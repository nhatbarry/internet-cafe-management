
from typing import List, Optional, Dict, Any
from models.database import DatabaseConnection
from config.settings import COLLECTION_COMPUTERS


class ComputerModel:
    
    def __init__(self):
        db = DatabaseConnection()
        self.collection = db.get_collection(COLLECTION_COMPUTERS)
    
    def get_all(self) -> List[Dict[str, Any]]:
        return list(self.collection.find().sort("computer_id", 1))
    
    def get_by_id(self, computer_id: int) -> Optional[Dict[str, Any]]:
        return self.collection.find_one({"computer_id": int(computer_id)})
    
    def get_by_ip(self, ip_address: str) -> Optional[Dict[str, Any]]:
        return self.collection.find_one({"ip_address": ip_address})
    
    def get_active_computers(self) -> List[Dict[str, Any]]:
        return list(self.collection.find({"is_active": True}).sort("computer_id", 1))
    
    def create(self, name: str, ip_address: str, is_active: bool = False) -> int:
        last_comp = self.collection.find_one(sort=[("computer_id", -1)])
        new_id = 1 if not last_comp else last_comp["computer_id"] + 1
        
        new_computer = {
            "computer_id": new_id,
            "computer_name": name,
            "ip_address": ip_address,
            "is_active": is_active,
            "user": None,
            "session_start": None
        }
        self.collection.insert_one(new_computer)
        return new_id
    
    def update(self, computer_id: int, data: Dict[str, Any]) -> bool:
        result = self.collection.update_one(
            {"computer_id": int(computer_id)},
            {"$set": data}
        )
        return result.modified_count > 0
    
    def delete(self, computer_id: int) -> bool:
        result = self.collection.delete_one({"computer_id": int(computer_id)})
        return result.deleted_count > 0
    
    def set_status(self, computer_id: int, is_active: bool) -> bool:
        return self.update(computer_id, {"is_active": is_active})
    
    def set_status_by_ip(self, ip_address: str, is_active: bool) -> bool:
        result = self.collection.update_one(
            {"ip_address": ip_address},
            {"$set": {"is_active": is_active}}
        )
        return result.modified_count > 0
    
    def assign_user(self, computer_id: int, username: str) -> bool:
        return self.update(computer_id, {"user": username, "is_active": True})
    
    def release_user(self, computer_id: int) -> bool:
        return self.update(computer_id, {"user": None, "session_start": None})
