import customtkinter as ctk
from controllers.auth_controller import AuthController


class registerPage:
    """
    View: Trang đăng ký tài khoản.
    Chỉ xử lý giao diện, không chứa logic nghiệp vụ.
    """

    def __init__(self, master, app_manager):
        self.master      = master
        self.app_manager = app_manager
        self.controller  = AuthController()

        self.config()
        self.view()

    def config(self):
        self.master.title("Tạo tài khoản")
        self.master.geometry("400x300")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def view(self):
        # --- Card chính ---
        frame = ctk.CTkFrame(self.master, corner_radius=12)
        frame.pack(pady=30, padx=30, fill="both", expand=True)

        # Tiêu đề
        ctk.CTkLabel(
            frame,
            text="TẠO TÀI KHOẢN",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(20, 10))

        # Ô nhập username
        self.entry_username = ctk.CTkEntry(
            frame,
            placeholder_text="Nhập username...",
            height=35,
            corner_radius=8
        )
        self.entry_username.pack(pady=10, padx=20, fill="x")

        # Ô nhập password
        self.entry_password = ctk.CTkEntry(
            frame,
            placeholder_text="Nhập password...",
            show="*",
            height=35,
            corner_radius=8
        )
        self.entry_password.pack(pady=10, padx=20, fill="x")

        # --- Khu vực nút bấm ---
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(
            btn_frame,
            text="Quay lại đăng nhập",
            fg_color="#6c757d",
            hover_color="#5a6268",
            corner_radius=10,
            command=self.go_to_login
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            btn_frame,
            text="Tạo tài khoản",
            fg_color="#1A73E8",
            hover_color="#1669c1",
            corner_radius=10,
            command=self.handle_register
        ).grid(row=0, column=1, padx=10)

    def handle_register(self):
        """Lấy input và gửi sang Controller xử lý"""
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        success = self.controller.register(username, password)

        if success:
            self.app_manager.show_login_page()

    def go_to_login(self):
        """Quay lại trang đăng nhập"""
        self.app_manager.show_login_page()