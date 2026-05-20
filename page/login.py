import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import os
import json
from query.taikhoan import AccountData
from common.theme import Colors, Fonts, Spacing

REMEMBER_FILE = "database/remember.json"


class LoginPage:

    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        self.account_data = AccountData()

        self.config()
        self.view()

        self.load_remembered_account()

    def config(self):
        self.master.title("🔐 Đăng Nhập")
        self.master.geometry("400x480")
        self.master.configure(fg_color=Colors.BG_MAIN)
        ctk.set_appearance_mode("light")

    def view(self):
        main_frame = ctk.CTkFrame(
            self.master,
            fg_color=Colors.BG_SECONDARY,
            corner_radius=12,
            border_width=1,
            border_color=Colors.BORDER
        )
        main_frame.pack(padx=Spacing.LG, pady=Spacing.LG, fill="both", expand=True)

        title = ctk.CTkLabel(
            main_frame,
            text="🔐 ĐĂNG NHẬP",
            font=Fonts.HEADER,
            text_color=Colors.PRIMARY
        )
        title.pack(pady=(Spacing.XL, Spacing.LG))

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

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=Spacing.XL, pady=Spacing.XL)

        self.login_button = ctk.CTkButton(
            btn_frame,
            text="🔓 Đăng Nhập",
            command=self.login,
            height=45,
            font=Fonts.BOLD,
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_HOVER,
            text_color=Colors.WHITE
        )
        self.login_button.pack(fill="x", expand=True)

    def load_remembered_account(self):
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
        try:
            if os.path.exists(REMEMBER_FILE):
                with open(REMEMBER_FILE, "w", encoding="utf-8") as f:
                    json.dump({"remember": False}, f)
        except Exception:
            pass

    def login(self):
        """Xử lý đăng nhập, lấy chức vụ từ kết quả MySQL để phân quyền hệ thống"""
        try:
            username = self.entry_username.get().strip()
            password = self.entry_password.get().strip()

            if not username:
                messagebox.showerror("Lỗi", "Vui lòng nhập username")
                return
            if not password:
                messagebox.showerror("Lỗi", "Vui lòng nhập password")
                return

            # Xác thực tài khoản với database MySQL
            user = self.account_data.authenticate(username, password)
            
            if user:
                # 1. Quản lý lưu file ghi nhớ mật khẩu cục bộ
                if self.remember_var.get():
                    self.save_remember(username, password)
                else:
                    self.clear_remember()

                # 2. PHÂN TÍCH QUYỀN HẠN (ROLE CHUCVU)
                chuc_vu = "Sinh viên"  # Vai trò mặc định phòng trường hợp lỗi
                
                if isinstance(user, dict):
                    # Nếu AccountData trả về dạng dữ liệu Từ điển
                    chuc_vu = user.get("chucvu") or user.get("chuc_vu") or "Sinh viên"
                elif isinstance(user, (list, tuple)) and len(user) > 0:
                    # Nếu AccountData trả về hàng dữ liệu dạng List/Tuple (ID=0, TK=1, MK=2, HT=3, SDT=4, CV=5...)
                    # Thông thường nếu câu lệnh SELECT * FROM taikhoan thì cột chucvu nằm ở index 4 hoặc 5
                    chuc_vu = user[4] if len(user) == 6 else user[5]

                messagebox.showinfo("Thông báo", f"Đăng nhập thành công!\nChức vụ: {chuc_vu}")
                
                # 3. ĐỒNG BỘ: Gọi hàm login_success của AppManager để nạp quyền toàn hệ thống
                self.master.after(10, lambda: self.app_manager.login_success(username, str(chuc_vu).strip()))
                return

            messagebox.showerror("Thông báo", "Đăng nhập thất bại! Sai tài khoản hoặc mật khẩu.")

        except FileNotFoundError:
            messagebox.showerror("Thông báo", "Chưa có tài khoản nào được tạo")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi đăng nhập: {str(e)}")