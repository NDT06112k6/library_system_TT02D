
# Import thư viện tkinter để tạo giao diện người dùng
import tkinter as tk
# Import lớp AppManager từ module app_manager để quản lý ứng dụng
from app_manager import AppManager

def main():
    """
    Hàm chính của chương trình.

    Khởi tạo và chạy ứng dụng quản lý thư viện.
    """
    print("Phần mềm đang khởi chạy")
    # Tạo instance AppManager để bắt đầu giao diện
    app = AppManager()
    # Chạy vòng lặp chính của ứng dụng
    app.run()

if __name__ == "__main__":
    # Điểm vào chương trình
    main()