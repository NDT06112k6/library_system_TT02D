import customtkinter as ctk
from controllers.accout_controller import AccountController


class edit_accountPage:
    """
    View: Trang sửa thông tin tài khoản.
    Chỉ xử lý giao diện, không chứa logic nghiệp vụ.
    """

    def __init__(self, master, app_manager, username=None, password=None):
        self.master        = master
        self.app_manager   = app_manager
        self.controller    = AccountController()
        self.old_username  = username or ""
        self.old_password  = password or ""

        self.config()
        self.view()

    def config(self):
        self.master.title("Sửa tài khoản")
        self.master.geometry("400x380")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def view(self):
        # --- Card chính ---
        frame = ctk.CTkFrame(self.master, corner_radius=12)
        frame.pack(pady=20, padx=30, fill="both", expand=True)

        # Tiêu đề
        ctk.CTkLabel(
            frame,
            text="SỬA TÀI KHOẢN",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(20, 10))

        # --- Thông tin hiện tại (chỉ đọc) ---
        info_frame = ctk.CTkFrame(frame, corner_radius=8)
        info_frame.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(
            info_frame,
            text="Thông tin hiện tại",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=10, pady=(8, 0))

        ctk.CTkLabel(
            info_frame,
            text=f"Tên đăng nhập: {self.old_username}",
            font=("Segoe UI", 11)
        ).pack(anchor="w", padx=10, pady=3)

        ctk.CTkLabel(
            info_frame,
            text=f"Mật khẩu: {'*' * len(self.old_password)}",
            font=("Segoe UI", 11)
        ).pack(anchor="w", padx=10, pady=(3, 8))

        # --- Thông tin mới ---
        ctk.CTkLabel(
            frame,
            text="Thông tin mới",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=20)

        # Ô nhập username mới
        self.entry_username = ctk.CTkEntry(
            frame,
            placeholder_text="Tên đăng nhập mới...",
            height=35,
            corner_radius=8
        )
        self.entry_username.pack(pady=8, padx=20, fill="x")
        self.entry_username.insert(0, self.old_username)

        # Ô nhập password mới
        self.entry_password = ctk.CTkEntry(
            frame,
            placeholder_text="Mật khẩu mới...",
            show="*",
            height=35,
            corner_radius=8
        )
        self.entry_password.pack(pady=8, padx=20, fill="x")
        self.entry_password.insert(0, self.old_password)

        # Checkbox hiện/ẩn mật khẩu
        self.show_password_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            frame,
            text="Hiển thị mật khẩu",
            variable=self.show_password_var,
            command=self.toggle_password
        ).pack(anchor="w", padx=20, pady=5)

        # --- Khu vực nút bấm ---
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(
            btn_frame,
            text="Lưu thay đổi",
            fg_color="#28a745",
            hover_color="#218838",
            corner_radius=10,
            command=self.handle_save
        ).grid(row=0, column=0, padx=8)

        ctk.CTkButton(
            btn_frame,
            text="Khôi phục",
            fg_color="#ffc107",
            hover_color="#e0a800",
            corner_radius=10,
            command=self.reset_form
        ).grid(row=0, column=1, padx=8)

        ctk.CTkButton(
            btn_frame,
            text="Hủy bỏ",
            fg_color="#6c757d",
            hover_color="#5a6268",
            corner_radius=10,
            command=self.handle_cancel
        ).grid(row=0, column=2, padx=8)

    def toggle_password(self):
        """Hiện hoặc ẩn mật khẩu"""
        if self.show_password_var.get():
            self.entry_password.configure(show="")
        else:
            self.entry_password.configure(show="*")

    def reset_form(self):
        """Khôi phục lại thông tin ban đầu"""
        self.entry_username.delete(0, "end")
        self.entry_username.insert(0, self.old_username)

        self.entry_password.delete(0, "end")
        self.entry_password.insert(0, self.old_password)

    def handle_save(self):
        """Lấy input và gửi sang Controller xử lý"""
        new_username = self.entry_username.get().strip()
        new_password = self.entry_password.get().strip()

        # Kiểm tra không có thay đổi nào
        if new_username == self.old_username and new_password == self.old_password:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Không có thay đổi nào được thực hiện")
            return

        success = self.controller.update_account(
            self.old_username,
            new_username,
            new_password
        )

        if success:
            self.app_manager.show_quanlytk_page()

    def handle_cancel(self):
        """Hủy bỏ và quay lại trang quản lý"""
        new_username = self.entry_username.get().strip()
        new_password = self.entry_password.get().strip()

        # Nếu có thay đổi chưa lưu thì hỏi xác nhận
        has_changes = (
            new_username != self.old_username or
            new_password != self.old_password
        )

        if has_changes:
            from tkinter import messagebox
            confirmed = messagebox.askyesno(
                "Xác nhận",
                "Bạn có chắc muốn hủy? Các thay đổi sẽ không được lưu."
            )
            if not confirmed:
                return

        self.app_manager.show_quanlytk_page()