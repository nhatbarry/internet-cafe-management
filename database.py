# database.py
from pymongo import MongoClient
import datetime

class Database:
    def __init__(self):
        try:
            self.client = MongoClient("mongodb+srv://nhatbarry_db_user:A5fvCiLouoY0yFWi@cluster0.g42qlnp.mongodb.net/?appName=Cluster0")
            self.db = self.client["internet_cafe"] 
            self.col_computers = self.db["computers"] 
            self.col_users = self.db["users"]   
            
        except Exception as e:
            print(f"Lỗi kết nối: {e}")

    def get_all_users(self):
        return list(self.col_users.find().sort("user_id", 1))

    def add_user(self, username, password, balance, is_vip):
        last_user = self.col_users.find_one(sort=[("user_id", -1)])
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
        self.col_users.insert_one(new_user)

    def update_user(self, user_id, username, password, balance, is_vip):
        self.col_users.update_one(
            {"user_id": int(user_id)},
            {"$set": {
                "username": username,
                "password": password,
                "balance": float(balance),
                "is_vip": is_vip
            }}
        )

    def delete_user(self, user_id):
        self.col_users.delete_one({"user_id": int(user_id)})

    def get_all_computers(self):
        return list(self.col_computers.find().sort("computer_id", 1))

    def add_computer(self, name, ip, is_active):
        last_comp = self.col_computers.find_one(sort=[("computer_id", -1)])
        new_id = 1 if not last_comp else last_comp["computer_id"] + 1
        
        new_comp = {
            "computer_id": new_id,
            "computer_name": name,
            "ip_address": ip,
            "is_active": is_active,
            "user": None
        }
        self.col_computers.insert_one(new_comp)

    def update_computer(self, comp_id, name, ip, is_active):
        self.col_computers.update_one(
            {"computer_id": int(comp_id)},
            {"$set": {
                "computer_name": name,
                "ip_address": ip,
                "is_active": is_active
            }}
        )

    def delete_computer(self, comp_id):
        self.col_computers.delete_one({"computer_id": int(comp_id)})