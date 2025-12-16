# Internet Cafe Management - Server

Ứng dụng quản lý quán Internet Cafe phía Server.

## Cấu trúc thư mục (MVC)

```
internet-cafe-management/
├── app.py                  # Entry point
├── main.py                 # Entry point cũ (deprecated)
├── requirements.txt        # Dependencies
├── config/                 # Cấu hình
│   ├── __init__.py
│   └── settings.py         # Các hằng số cấu hình
├── models/                 # Model layer - xử lý data
│   ├── __init__.py
│   ├── database.py         # Kết nối MongoDB
│   ├── user_model.py       # Model User
│   └── computer_model.py   # Model Computer
├── views/                  # View layer - giao diện
│   ├── __init__.py
│   ├── main_window.py      # Cửa sổ chính
│   ├── components/         # Các widget component
│   │   ├── __init__.py
│   │   └── machine_card.py # Card hiển thị máy
│   └── ui/                 # Generated UI files
│       ├── __init__.py
│       ├── ui_main.py
│       ├── ui_styles.py
│       ├── ui_functions.py
│       ├── app_functions.py
│       ├── app_modules.py
│       └── files_rc.py
├── controllers/            # Controller layer - logic
│   ├── __init__.py
│   ├── base_controller.py
│   ├── user_controller.py
│   ├── computer_controller.py
│   └── main_controller.py
└── services/               # Services
    ├── __init__.py
    └── socket_service.py   # Socket server
```

## Cài đặt

```bash
# Tạo virtual environment
python -m venv .venv

# Activate
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Cài đặt dependencies
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
python app.py
```

## Tính năng

- Quản lý máy tính trong quán
- Quản lý người dùng
- Điều khiển máy từ xa (Lock/Unlock/Shutdown)
- Kết nối MongoDB Atlas
- Socket server cho client kết nối

## Công nghệ

- Python 3.10+
- PyQt5 5.15.11
- MongoDB (pymongo)
- Socket TCP/IP
