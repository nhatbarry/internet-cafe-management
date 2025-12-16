
import socket
import threading
from PyQt5.QtCore import QObject, pyqtSignal
from config.settings import SOCKET_PORT, SOCKET_HOST


class SocketService(QObject):
    
    client_connected = pyqtSignal(str)   
    client_disconnected = pyqtSignal(str)  
    message_received = pyqtSignal(str, str) 
    
    def __init__(self, host: str = SOCKET_HOST, port: int = SOCKET_PORT):
        super().__init__()
        self.host = host
        self.port = port
        self.clients = {}
        self.server = None
        self._running = False
    
    def start(self):
        thread = threading.Thread(target=self._listen, daemon=True)
        thread.start()
    
    def stop(self):
        self._running = False
        if self.server:
            self.server.close()
    
    def _listen(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(50)
        self._running = True
        
        print(f"Server Socket đang chạy tại {self.host}:{self.port}...")
        
        while self._running:
            try:
                client_socket, address = self.server.accept()
                ip_address = address[0]
                
                self.clients[ip_address] = client_socket
                print(f"Máy trạm {ip_address} đã kết nối!")
                self.client_connected.emit(ip_address)
                
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, ip_address),
                    daemon=True
                )
                client_thread.start()
                
            except Exception as e:
                if self._running:
                    print(f" Lỗi accept: {e}")
    
    def _handle_client(self, client_socket: socket.socket, ip_address: str):
        while self._running:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Nhận từ {ip_address}: {message}")
                    self.message_received.emit(ip_address, message)
                else:
                    break
            except:
                break
        
        self._remove_client(ip_address)
    
    def _remove_client(self, ip_address: str):
        if ip_address in self.clients:
            try:
                self.clients[ip_address].close()
            except:
                pass
            del self.clients[ip_address]
            print(f"Máy {ip_address} đã ngắt kết nối")
            self.client_disconnected.emit(ip_address)
    
    def send_command(self, target_ip: str, command: str) -> bool:
        if target_ip not in self.clients:
            print(f"Máy {target_ip} chưa kết nối!")
            return False
        
        try:
            self.clients[target_ip].send(command.encode('utf-8'))
            print(f"Đã gửi '{command}' tới {target_ip}")
            return True
        except Exception as e:
            print(f"Lỗi gửi tới {target_ip}: {e}")
            self._remove_client(target_ip)
            return False
    
    def broadcast(self, command: str):
        disconnected = []
        for ip in self.clients:
            if not self.send_command(ip, command):
                disconnected.append(ip)
        
        for ip in disconnected:
            self._remove_client(ip)
    
    def is_client_connected(self, ip_address: str) -> bool:
        return ip_address in self.clients
    
    def get_connected_clients(self) -> list:
        return list(self.clients.keys())
