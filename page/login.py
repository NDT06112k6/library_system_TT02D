import customtkinter as ctk
from tkinter import messagebox
import os
import json
from query import Query

REMEMBER_FILE = "database/remember.json"


class LoginPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.Q = Query("database/tk.csv", ["taikhoan", "matkhau", "email"])

        self.config()
        self.view()
        self.load_remembered()

    def config(self):
        self.master.title("Đăng nhập")
        self.master.geometry("400x370")

        # Theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def view(self):
        # Frame chính (card)
        frame = ctk.CTkFrame(self.master, corner_radius=12)
        frame.pack(pady=20, padx=30, fill="both", expand=True)

        # Tiêu đề
        label = ctk.CTkLabel(
            frame,
            text="ĐĂNG NHẬP",
            font=("Segoe UI", 24, "bold")
        )
        label.pack(pady=(20, 10))

        # Username
        self.entry_username = ctk.CTkEntry(
            frame,
            placeholder_text="Nhập username...",
            height=35,
            corner_radius=8
        )
        self.entry_username.pack(pady=8, padx=20, fill="x")

        # Password
        self.entry_password = ctk.CTkEntry(
            frame,
            placeholder_text="Nhập password...",
            show="*",
            height=35,
            corner_radius=8
        )
        self.entry_password.pack(pady=8, padx=20, fill="x")

        # Gmail
        self.entry_gmail = ctk.CTkEntry(
            frame,
            placeholder_text="Nhập Gmail...",
            height=35,
            corner_radius=8
        )
        self.entry_gmail.pack(pady=8, padx=20, fill="x")

        # Ghi nhớ tài khoản checkbox
        self.remember_var = ctk.BooleanVar(value=False)
        self.chk_remember = ctk.CTkCheckBox(
            frame,
            text="Ghi nhớ tài khoản",
            variable=self.remember_var,
            font=("Segoe UI", 12),
            checkbox_width=18,
            checkbox_height=18
        )
        self.chk_remember.pack(pady=(4, 0), padx=20, anchor="w")

        # Button frame
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        # Nút tạo tài khoản
        btn_register = ctk.CTkButton(
            btn_frame,
            text="Tạo tài khoản",
            fg_color="#6c757d",
            hover_color="#5a6268",
            corner_radius=10,
            command=self.tao_tk
        )
        btn_register.grid(row=0, column=0, padx=10)

        # Nút đăng nhập
        btn_login = ctk.CTkButton(
            btn_frame,
            text="Đăng nhập",
            fg_color="#1A73E8",
            hover_color="#1669c1",
            corner_radius=10,
            command=self.login
        )
        btn_login.grid(row=0, column=1, padx=10)

    def load_remembered(self):
        """Tự động điền thông tin nếu đã ghi nhớ"""
        try:
            if os.path.exists(REMEMBER_FILE):
                with open(REMEMBER_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("remember"):
                    self.entry_username.insert(0, data.get("username", ""))
                    self.entry_password.insert(0, data.get("password", ""))
                    self.entry_gmail.insert(0, data.get("gmail", ""))
                    self.remember_var.set(True)
        except Exception:
            pass

    def save_remember(self, username, password, gmail):
        """Lưu thông tin đăng nhập"""
        os.makedirs("database", exist_ok=True)
        try:
            with open(REMEMBER_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "remember": True,
                    "username": username,
                    "password": password,
                    "gmail": gmail
                }, f, ensure_ascii=False)
        except Exception:
            pass

    def clear_remember(self):
        """Xóa thông tin đã ghi nhớ"""
        try:
            if os.path.exists(REMEMBER_FILE):
                with open(REMEMBER_FILE, "w", encoding="utf-8") as f:
                    json.dump({"remember": False}, f)
        except Exception:
            pass

    def tao_tk(self):
        self.app_manager.show_taotk_page()

    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        gmail = self.entry_gmail.get().strip()

        try:
            # Tìm kiếm bằng Query
            result = self.Q.search("taikhoan", username, exact=True)
            
            if not result.empty:
                row = result.iloc[0]
                if row["matkhau"] == password and row["email"] == gmail:
                    # Xử lý ghi nhớ tài khoản
                    if self.remember_var.get():
                        self.save_remember(username, password, gmail)
                    else:
                        self.clear_remember()

                    messagebox.showinfo("Thông báo", "Đăng nhập thành công")
                    self.app_manager.show_quanlytk_page()
                    return

            messagebox.showerror("Thông báo", "Đăng nhập thất bại")

        except FileNotFoundError:
            messagebox.showerror("Thông báo", "Chưa có tài khoản nào được tạo")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi đăng nhập: {str(e)}")