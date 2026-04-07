import tkinter as tk
from page.login import loginPage
from page.register import registerPage
from page.account_manager import account_managerPage
from page.edit_account import edit_accountPage


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
        self.current_page = loginPage(self.root, self)

    def show_taotk_page(self):
        """Hiển thị trang tạo tài khoản"""
        self.clear_current_page()
        self.root.geometry("300x200")
        self.current_page = registerPage(self.root, self)

    def show_quanlytk_page(self):
        """Hiển thị trang quản lý tài khoản"""
        self.clear_current_page()
        self.root.geometry("600x400")
        self.current_page = account_managerPage(self.root, self)

    def show_suatk_page(self, username=None, password=None):
        """Hiển thị trang sửa tài khoản"""
        self.clear_current_page()
        self.root.geometry("400x300")
        self.current_page = edit_accountPage(self.root, self, username, password)

    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()