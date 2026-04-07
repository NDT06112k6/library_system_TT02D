import customtkinter as ctk
from tkinter import ttk
from controllers.accout_controller import AccountController


class account_managerPage:
    """
    View: Trang quản lý tài khoản.
    Chỉ xử lý giao diện, không chứa logic nghiệp vụ.
    """

    def __init__(self, master, app_manager):
        self.master      = master
        self.app_manager = app_manager
        self.controller  = AccountController()

        self.config()
        self.view()
        self.load_accounts()

    def config(self):
        self.master.title("Quản lý tài khoản")
        self.master.geometry("600x400")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def view(self):
        # --- Tiêu đề ---
        ctk.CTkLabel(
            self.master,
            text="Quản lý tài khoản",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=10)

        # --- Khu vực nút bấm ---
        btn_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        btn_frame.pack(pady=5)

        ctk.CTkButton(
            btn_frame,
            text="Làm mới",
            fg_color="#17a2b8",
            hover_color="#138496",
            corner_radius=10,
            command=self.load_accounts
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Xóa tài khoản",
            fg_color="#dc3545",
            hover_color="#c82333",
            corner_radius=10,
            command=self.handle_delete
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Sửa tài khoản",
            fg_color="#ffc107",
            hover_color="#e0a800",
            corner_radius=10,
            command=self.handle_edit
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Quay lại",
            fg_color="#6c757d",
            hover_color="#5a6268",
            corner_radius=10,
            command=self.go_to_login
        ).pack(side="left", padx=5)

        # --- Bảng danh sách tài khoản ---
        tree_frame = ctk.CTkFrame(self.master)
        tree_frame.pack(expand=True, fill="both", padx=20, pady=10)

        columns = ("STT", "Username", "Password")
        self.account_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=15
        )

        # Tiêu đề cột
        self.account_tree.heading("STT",      text="STT")
        self.account_tree.heading("Username", text="Tên đăng nhập")
        self.account_tree.heading("Password", text="Mật khẩu")

        # Độ rộng cột
        self.account_tree.column("STT",      width=50,  anchor="center")
        self.account_tree.column("Username", width=200, anchor="center")
        self.account_tree.column("Password", width=200, anchor="center")

        # Thanh cuộn
        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=self.account_tree.yview
        )
        self.account_tree.configure(yscrollcommand=scrollbar.set)

        self.account_tree.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")

        # --- Thanh trạng thái ---
        self.status_label = ctk.CTkLabel(
            self.master,
            text="Sẵn sàng",
            anchor="w"
        )
        self.status_label.pack(side="bottom", fill="x", padx=10, pady=5)

    def load_accounts(self):
        """Tải danh sách tài khoản từ Controller và hiển thị lên bảng"""
        # Xóa dữ liệu cũ trong bảng
        for item in self.account_tree.get_children():
            self.account_tree.delete(item)

        accounts = self.controller.get_all_accounts()

        if not accounts:
            self.status_label.configure(text="Không có tài khoản nào")
            return

        # Hiển thị từng tài khoản lên bảng
        for idx, account in enumerate(accounts, 1):
            self.account_tree.insert("", "end", values=(idx, account[0], account[1]))

        self.status_label.configure(text=f"Đã tải {len(accounts)} tài khoản")

    def get_selected_account(self):
        """
        Lấy tài khoản đang được chọn trong bảng.
        Trả về (username, password) hoặc None nếu chưa chọn.
        """
        selected = self.account_tree.selection()

        if not selected:
            return None

        values = self.account_tree.item(selected[0], "values")
        return values[1], values[2]  # (username, password)

    def handle_delete(self):
        """Xử lý xóa tài khoản được chọn"""
        account = self.get_selected_account()

        if not account:
            from tkinter import messagebox
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tài khoản cần xóa")
            return

        username, _ = account
        success = self.controller.delete_account(username)

        if success:
            self.load_accounts()

    def handle_edit(self):
        """Chuyển sang trang sửa tài khoản được chọn"""
        account = self.get_selected_account()

        if not account:
            from tkinter import messagebox
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tài khoản cần sửa")
            return

        username, password = account
        self.app_manager.show_suatk_page(username, password)

    def go_to_login(self):
        """Quay lại trang đăng nhập"""
        self.app_manager.show_login_page()