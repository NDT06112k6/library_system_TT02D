import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import os
import json
from query.taikhoan import AccountData
from common.theme import Colors, Fonts, Spacing

REMEMBER_FILE = "database/remember.json"


class LoginPage:
    """Trang đăng nhập - xác thực người dùng"""

    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        # Sử dụng class chuyên biệt
        self.account_data = AccountData()

        self.config()
        self.view()
        # Tự động điền thông tin ghi nhớ nếu có
        self.load_remembered_account()

    def config(self):
        """Cấu hình cửa sổ đăng nhập"""
        self.master.title("🔐 Đăng Nhập")
        self.master.geometry("400x480")
        self.master.configure(fg_color=Colors.BG_MAIN)

        # Theme
        ctk.set_appearance_mode("light")

    def view(self):
        """Vẽ giao diện đăng nhập"""
        main_frame = ctk.CTkFrame(
            self.master,
            fg_color=Colors.BG_SECONDARY,
            corner_radius=12,
            border_width=1,
            border_color=Colors.BORDER
        )
        main_frame.pack(padx=Spacing.LG, pady=Spacing.LG, fill="both", expand=True)

        # Tiêu đề
        title = ctk.CTkLabel(
            main_frame,
            text="🔐 ĐĂNG NHẬP",
            font=Fonts.HEADER,
            text_color=Colors.PRIMARY
        )
        title.pack(pady=(Spacing.XL, Spacing.LG))

        # Input Fields
        ctk.CTkLabel(
            main_frame,
            text="Username",
            font=Fonts.SMALL_BOLD,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w", padx=Spacing.XL, pady=(Spacing.MD, Spacing.XS))

        self.entry_username = ctk.CTkEntry(
            main_frame,
            placeholder_text="Nhập username...",
            height=40,
            font=Fonts.REGULAR,
            fg_color=Colors.BG_MAIN,
            border_color=Colors.BORDER,
            text_color=Colors.TEXT_PRIMARY
        )
        self.entry_username.pack(fill="x", padx=Spacing.XL, pady=(0, Spacing.MD))

        ctk.CTkLabel(
            main_frame,
            text="Password",
            font=Fonts.SMALL_BOLD,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w", padx=Spacing.XL, pady=(Spacing.MD, Spacing.XS))

        self.entry_password = ctk.CTkEntry(
            main_frame,
            placeholder_text="Nhập password...",
            show="*",
            height=40,
            font=Fonts.REGULAR,
            fg_color=Colors.BG_MAIN,
            border_color=Colors.BORDER,
            text_color=Colors.TEXT_PRIMARY
        )
        self.entry_password.pack(fill="x", padx=Spacing.XL, pady=(0, Spacing.MD))

        self.remember_var = tk.BooleanVar(value=False)
        checkbox = ctk.CTkCheckBox(
            main_frame,
            text="Ghi nhớ mật khẩu",
            font=Fonts.SMALL,
            text_color=Colors.TEXT_SECONDARY,
            variable=self.remember_var,
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_HOVER
        )
        checkbox.pack(anchor="w", padx=Spacing.XL, pady=Spacing.MD)

        # Buttons Frame
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=Spacing.XL, pady=Spacing.XL)

        ctk.CTkButton(
            btn_frame,
            text="🔓 Đăng Nhập",
            command=self.login,
            height=45,
            font=Fonts.BOLD,
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_HOVER,
            text_color=Colors.WHITE
        ).pack(side="left", fill="x", expand=True, padx=(0, Spacing.SM))

        ctk.CTkButton(
            btn_frame,
            text="📝 Tạo TK",
            command=self.tao_tk,
            height=45,
            font=Fonts.BOLD,
            fg_color=Colors.BORDER,
            hover_color=Colors.BORDER_DARK,
            text_color=Colors.TEXT_PRIMARY
        ).pack(side="left", fill="x", expand=True)

    def load_remembered_account(self):
        """Tự động điền tài khoản ghi nhớ nếu có"""
        try:
            if os.path.exists(REMEMBER_FILE):
                with open(REMEMBER_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("remember"):
                    self.entry_username.insert(0, data.get("username", ""))
                    self.entry_password.insert(0, data.get("password", ""))
                    self.remember_var.set(True)
        except Exception:
            pass

    def save_remember(self, username, password):
        """Lưu username và mật khẩu vào file remember.json"""
        os.makedirs("database", exist_ok=True)
        try:
            with open(REMEMBER_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "remember": True,
                    "username": username,
                    "password": password
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
        """Chuyển đến trang tạo tài khoản"""
        self.app_manager.show_taotk_page()

    def login(self):
        """Xử lý logic khi người dùng nhấn nút 'Đăng nhập'."""
        try:
            username = self.entry_username.get().strip()
            password = self.entry_password.get().strip()

            if not username:
                messagebox.showerror("Lỗi", "Vui lòng nhập username")
                return
            if not password:
                messagebox.showerror("Lỗi", "Vui lòng nhập password")
                return

            # Sử dụng phương thức authenticate đã đóng gói logic
            user = self.account_data.authenticate(username, password)
            
            if user:
                if self.remember_var.get():
                    self.save_remember(username, password)
                else:
                    self.clear_remember()

                messagebox.showinfo("Thông báo", "Đăng nhập thành công")
                # Sử dụng after để tránh lỗi 'invalid command name' khi chuyển trang
                self.master.after(10, lambda: self.app_manager.show_main_page(username))
                return

            messagebox.showerror("Thông báo", "Đăng nhập thất bại")

        except FileNotFoundError:
            messagebox.showerror("Thông báo", "Chưa có tài khoản nào được tạo")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi đăng nhập: {str(e)}")