
import ssl
import certifi
from pymongo import MongoClient
from config.settings import MONGODB_URI, DATABASE_NAME, COLLECTION_COMPUTERS, COLLECTION_USERS


class DatabaseConnection:
    """Singleton class để quản lý kết nối MongoDB"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        try:
            self.client = MongoClient(
                MONGODB_URI,
                tls=True,
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=30000,
                connectTimeoutMS=30000
            )
            self.db = self.client[DATABASE_NAME]
            self._initialized = True
            print("Đã kết nối MongoDB!")
        except Exception as e:
            print(f"Lỗi kết nối MongoDB: {e}")
            raise
    
    def get_collection(self, collection_name: str):
        return self.db[collection_name]
    
    def close(self):
        if self.client:
            self.client.close()
