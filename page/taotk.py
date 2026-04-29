import customtkinter as ctk
from tkinter import messagebox
import os
import re
from query import Query
from common.validation import Validation
from common.validation import Validation


class TaoTKPage:
    """
    Trang tạo tài khoản mới.

    Cho phép người dùng nhập thông tin để tạo tài khoản.
    """
    def __init__(self, master, app_manager):
        """
        Khởi tạo TaoTKPage.

        Args:
            master: Cửa sổ chính
            app_manager: Quản lý ứng dụng
        """
        self.master = master
        self.app_manager = app_manager
        self.Q = Query("database/tk.csv", ["taikhoan", "matkhau", "email"])
        self.config()
        self.view()

    def config(self):
        """
        Cấu hình cửa sổ tạo tài khoản.
        """
        self.master.title("Tạo tài khoản")
        self.master.geometry("420x420")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def view(self):
        """
        Vẽ giao diện tạo tài khoản.
        """
        for widget in self.master.winfo_children():
            widget.destroy()

        # ========== TIÊU ĐỀ ==========
        label_title = ctk.CTkLabel(
            self.master,
            text="TẠO TÀI KHOẢN",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color="#212F3D"
        )
        label_title.pack(pady=(25, 15))

        # ========== FORM FRAME ==========
        form_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        form_frame.pack(pady=5)

        # ----- Username -----
        ctk.CTkLabel(
            form_frame,
            text="USERNAME",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#566573"
        ).pack(anchor="w", padx=10, pady=(0, 4))

        self.entry_username = ctk.CTkEntry(
            form_frame, width=280, height=40,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Nhập tên đăng nhập...",
            border_color="#ABB2B9", border_width=1, corner_radius=8
        )
        self.entry_username.pack(pady=(0, 10))
        self.entry_username.bind("<FocusIn>",  lambda e: self.on_focus(self.entry_username, True))
        self.entry_username.bind("<FocusOut>", lambda e: self.on_focus(self.entry_username, False))

        # ----- Gmail -----
        ctk.CTkLabel(
            form_frame,
            text="GMAIL",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#566573"
        ).pack(anchor="w", padx=10, pady=(0, 4))

        self.entry_gmail = ctk.CTkEntry(
            form_frame, width=280, height=40,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Nhập Gmail (@gmail.com)...",
            border_color="#ABB2B9", border_width=1, corner_radius=8
        )
        self.entry_gmail.pack(pady=(0, 10))
        self.entry_gmail.bind("<FocusIn>",  lambda e: self.on_focus(self.entry_gmail, True))
        self.entry_gmail.bind("<FocusOut>", lambda e: self.on_focus(self.entry_gmail, False))

        # ----- Password -----
        ctk.CTkLabel(
            form_frame,
            text="PASSWORD",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#566573"
        ).pack(anchor="w", padx=10, pady=(0, 4))

        self.entry_password = ctk.CTkEntry(
            form_frame, width=280, height=40,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Nhập mật khẩu...",
            border_color="#ABB2B9", border_width=1, corner_radius=8, show="*"
        )
        self.entry_password.pack(pady=(0, 10))
        self.entry_password.bind("<FocusIn>",  lambda e: self.on_focus(self.entry_password, True))
        self.entry_password.bind("<FocusOut>", lambda e: self.on_focus(self.entry_password, False))

        # ----- Confirm Password -----
        ctk.CTkLabel(
            form_frame,
            text="CONFIRM PASSWORD",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#566573"
        ).pack(anchor="w", padx=10, pady=(0, 4))

        self.entry_confirm = ctk.CTkEntry(
            form_frame, width=280, height=40,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Nhập lại mật khẩu...",
            border_color="#ABB2B9", border_width=1, corner_radius=8, show="*"
        )
        self.entry_confirm.pack(pady=(0, 5))
        self.entry_confirm.bind("<FocusIn>",  lambda e: self.on_focus(self.entry_confirm, True))
        self.entry_confirm.bind("<FocusOut>", lambda e: self.on_focus(self.entry_confirm, False))

        # ========== BUTTON FRAME ==========
        button_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        button_frame.pack(pady=15)

        ctk.CTkButton(
            button_frame,
            text="TẠO TÀI KHOẢN",
            command=self.tao_tk,
            width=280, height=45,
            fg_color="#2980B9", hover_color="#1A5276",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            corner_radius=8
        ).pack(pady=(0, 10))

        ctk.CTkButton(
            button_frame,
            text="QUAY LẠI ĐĂNG NHẬP",
            command=self.back_login,
            width=280, height=45,
            fg_color="#BDC3C7", hover_color="#A6B1B9",
            text_color="#2C3E50",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            corner_radius=8
        ).pack()

    def on_focus(self, entry, is_focused):
        """
        Xử lý sự kiện focus cho entry.

        Args:
            entry: Ô nhập liệu
            is_focused: Trạng thái focus
        """
        if is_focused:
            entry.configure(border_color="#2980B9", border_width=2)
        else:
            entry.configure(border_color="#ABB2B9", border_width=1)

    def back_login(self):
        """
        Quay lại trang đăng nhập.
        """
        self.app_manager.show_login_page()

    # ── Validation helpers ──────────────────────────────────────────────────

    def is_valid_gmail(self, email: str) -> bool:
        """Kiểm tra định dạng @gmail.com"""
        pattern = r'^[a-zA-Z0-9._%+\-]+@gmail\.com$'
        return bool(re.match(pattern, email))

    def username_exists(self, username: str) -> bool:
        """Kiểm tra tên đăng nhập đã tồn tại"""
        try:
            result = self.Q.search("taikhoan", username, exact=True)
            return not result.empty
        except Exception:
            return False

    # ── Main action ─────────────────────────────────────────────────────────

    def tao_tk(self):
        username = self.entry_username.get().strip()
        gmail    = self.entry_gmail.get().strip()
        password = self.entry_password.get().strip()
        confirm  = self.entry_confirm.get().strip()
        
        # 1. Kiểm tra bỏ trống
        if not username or not password or not gmail:
            messagebox.showerror("Thông báo", "Vui lòng nhập đầy đủ thông tin")
            return

        # 2. Mật khẩu khớp
        if password != confirm:
            messagebox.showerror("Thông báo", "Mật khẩu xác nhận không khớp")
            return

        # 3. Định dạng Gmail
        if not self.is_valid_gmail(gmail):
            messagebox.showerror("Thông báo", "Gmail không hợp lệ!\nĐịnh dạng đúng: example@gmail.com")
            return

        # 4. Tên đăng nhập trùng
        if self.username_exists(username):
            messagebox.showerror("Thông báo", f"Tên đăng nhập '{username}' đã tồn tại!\nVui lòng chọn tên khác.")
            return

        # 5. Tạo tài khoản bằng Query
        try:
            os.makedirs("database", exist_ok=True)
            self.Q.create([username, password, gmail])
            messagebox.showinfo("Thông báo", "Tạo tài khoản thành công!")
            self.app_manager.show_login_page()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo tài khoản: {str(e)}")
