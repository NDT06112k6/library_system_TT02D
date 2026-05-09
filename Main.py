
import tkinter as tk
from app_manager import AppManager

def main():
    """
    Hàm chính của chương trình.
    Khởi tạo và chạy ứng dụng quản lý thư viện.
    """
    print("Phần mềm đang khởi chạy")
    app = AppManager()
    
    app.run()

if __name__ == "__main__":
    main()