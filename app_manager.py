import tkinter as tk
from page.login import LoginPage
from page.taotk import TaoTKPage
from page.quanlytk import QuanLyTKPage
from page.suatk import SuaTKPage
from page.quanlysach import QuanLySachPage
from page.themsach import ThemSachPage
from page.suasach import SuaSachPage

class AppManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ứng dụng Đăng nhập")
        self.root.geometry("300x200")
        self.current_page = None
        self.show_login_page()

    def clear_current_page(self):
        """Xóa tất cả widget của page hiện tại"""
        if self.current_page:
            for widget in self.root.winfo_children():
                widget.destroy()

    def show_login_page(self):
        """Hiển thị trang đăng nhập"""
        self.clear_current_page()
        self.root.geometry("300x230")
        self.current_page = LoginPage(self.root, self)

    def show_taotk_page(self):
        """Hiển thị trang tạo tài khoản"""
        self.clear_current_page()
        self.root.geometry("300x200")
        self.current_page = TaoTKPage(self.root, self)

    def show_quanlytk_page(self):
        """Hiển thị trang quản lý tài khoản"""
        self.clear_current_page()
        self.root.geometry("600x400")
        self.current_page = QuanLyTKPage(self.root, self)

    def show_suatk_page(self, username=None, password=None):
        """Hiển thị trang sửa tài khoản"""
        self.clear_current_page()
        self.root.geometry("500x450")
        self.current_page = SuaTKPage(self.root, self, username, password)
    def show_quanlysach_page(self):
        """Hiển thị trang quản lý sách"""
        self.clear_current_page()
        self.root.geometry("800x550")
        self.current_page = QuanLySachPage(self.root, self)

    def show_themsach_page(self):
        """Hiển thị trang thêm sách"""
        self.clear_current_page()
        self.root.geometry("450x480")
        self.current_page = ThemSachPage(self.root, self)

    def show_suasach_page(self, ma_sach):
        """Hiển thị trang sửa sách"""
        self.clear_current_page()
        self.root.geometry("450x500")
        self.current_page = SuaSachPage(self.root, self, ma_sach)
    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()