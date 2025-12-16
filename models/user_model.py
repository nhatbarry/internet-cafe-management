
from typing import List, Optional, Dict, Any
from models.database import DatabaseConnection
from config.settings import COLLECTION_USERS


class UserModel:
    
    def __init__(self):
        db = DatabaseConnection()
        self.collection = db.get_collection(COLLECTION_USERS)
    
    def get_all(self) -> List[Dict[str, Any]]:
        return list(self.collection.find().sort("user_id", 1))
    
    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        return self.collection.find_one({"user_id": int(user_id)})
    
    def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        return self.collection.find_one({"username": username})
    
    def create(self, username: str, password: str, balance: float = 0, is_vip: bool = False) -> int:
        last_user = self.collection.find_one(sort=[("user_id", -1)])
        new_id = 1 if not last_user else last_user["user_id"] + 1
        
        new_user = {
            "user_id": new_id,
            "username": username,
            "password": password,
            "balance": float(balance),
            "remaining_time": 0,
            "is_vip": is_vip,
            "last_login": None
        }
        self.collection.insert_one(new_user)
        return new_id
    
    def update(self, user_id: int, data: Dict[str, Any]) -> bool:
        result = self.collection.update_one(
            {"user_id": int(user_id)},
            {"$set": data}
        )
        return result.modified_count > 0
    
    def delete(self, user_id: int) -> bool:
        result = self.collection.delete_one({"user_id": int(user_id)})
        return result.deleted_count > 0
    
    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        return self.collection.find_one({
            "username": username,
            "password": password
        })
    
    def update_balance(self, user_id: int, amount: float) -> bool:
        result = self.collection.update_one(
            {"user_id": int(user_id)},
            {"$inc": {"balance": amount}}
        )
        return result.modified_count > 0
