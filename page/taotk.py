import customtkinter as ctk
from tkinter import messagebox
from query.taikhoan import AccountData
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
        self.account_data = AccountData()
        self.config()
        self.view()

    def config(self):
        """
        Cấu hình cửa sổ tạo tài khoản.
        """
        self.master.title("Tạo tài khoản")
        self.master.geometry("420x650")
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
            border_width=2, corner_radius=8
        )
        self.entry_username.pack(pady=(0, 10))

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

        # ----- Họ tên -----
        ctk.CTkLabel(
            form_frame,
            text="HỌ TÊN",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#566573"
        ).pack(anchor="w", padx=10, pady=(0, 4))

        self.entry_hoten = ctk.CTkEntry(
            form_frame, width=280, height=40,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Nhập họ tên...",
            border_color="#ABB2B9", border_width=1, corner_radius=8
        )
        self.entry_hoten.pack(pady=(0, 10))
        self.entry_hoten.bind("<FocusIn>",  lambda e: self.on_focus(self.entry_hoten, True))
        self.entry_hoten.bind("<FocusOut>", lambda e: self.on_focus(self.entry_hoten, False))

        # ----- SĐT -----
        ctk.CTkLabel(
            form_frame,
            text="SỐ ĐIỆN THOẠI",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#566573"
        ).pack(anchor="w", padx=10, pady=(0, 4))

        self.entry_sdt = ctk.CTkEntry(
            form_frame, width=280, height=40,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Nhập SĐT...",
            border_color="#ABB2B9", border_width=1, corner_radius=8
        )
        self.entry_sdt.pack(pady=(0, 10))
        self.entry_sdt.bind("<FocusIn>",  lambda e: self.on_focus(self.entry_sdt, True))
        self.entry_sdt.bind("<FocusOut>", lambda e: self.on_focus(self.entry_sdt, False))

        # ----- Chức vụ -----
        ctk.CTkLabel(
            form_frame,
            text="CHỨC VỤ",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#566573"
        ).pack(anchor="w", padx=10, pady=(0, 4))

        self.entry_chucvu = ctk.CTkEntry(
            form_frame, width=280, height=40,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Nhập chức vụ...",
            border_color="#ABB2B9", border_width=1, corner_radius=8
        )
        self.entry_chucvu.pack(pady=(0, 10))
        self.entry_chucvu.bind("<FocusIn>",  lambda e: self.on_focus(self.entry_chucvu, True))
        self.entry_chucvu.bind("<FocusOut>", lambda e: self.on_focus(self.entry_chucvu, False))

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

    # ── Main action ─────────────────────────────────────────────────────────

    def tao_tk(self):
        """Xử lý logic khi người dùng nhấn nút 'TẠO TÀI KHOẢN'."""
        username = self.entry_username.get().strip()
        gmail    = self.entry_gmail.get().strip()
        hoten    = self.entry_hoten.get().strip()
        sdt      = self.entry_sdt.get().strip()
        chucvu   = self.entry_chucvu.get().strip()
        password = self.entry_password.get().strip()
        confirm  = self.entry_confirm.get().strip()
        
        # 1. Kiểm tra username và sự tồn tại
        valid, msg = Validation.is_valid_username(username)
        if not valid:
            messagebox.showerror("Lỗi", msg)
            return

        if self.account_data.check_exists(username):
            messagebox.showerror("Lỗi", f"Tên đăng nhập '{username}' đã tồn tại!")
            return

        # 2. Kiểm tra Email & SĐT
        valid_email, msg_email = Validation.is_valid_email_simple(gmail)
        if not valid_email:
            messagebox.showerror("Lỗi", msg_email)
            return

        valid_phone, msg_phone = Validation.is_valid_phone(sdt)
        if not valid_phone:
            messagebox.showerror("Lỗi", msg_phone)
            return

        # 3. Kiểm tra các trường khác và mật khẩu
        if not hoten or not chucvu or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return

        if password != confirm:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp")
            return

        try:
            self.account_data.create([username, password, hoten, sdt, chucvu, gmail])
            messagebox.showinfo("Thông báo", "Tạo tài khoản thành công!")
            self.app_manager.show_login_page()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo tài khoản: {str(e)}")
