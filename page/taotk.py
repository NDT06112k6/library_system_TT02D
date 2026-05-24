import customtkinter as ctk
from tkinter import messagebox
from query.taikhoan import AccountData
from common.validation import Validation


class TaoTKPage:
    """
    Trang tạo tài khoản mới dành cho khách hàng với chức vụ mặc định là Độc giả.
    Hỗ trợ cuộn chuột khi form quá dài.
    """
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.account_data = AccountData()
        self.config()
        self.view()

    def config(self):
        """Cấu hình cửa sổ"""
        self.master.title("Tạo tài khoản")
        self.master.geometry("420x650")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def view(self):
        """Vẽ giao diện tạo tài khoản"""
        for widget in self.master.winfo_children():
            widget.destroy()

        # ========== TIÊU ĐỀ ==========
        label_title = ctk.CTkLabel(
            self.master,
            text="TẠO TÀI KHOẢN",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color="#212F3D"
        )
        label_title.pack(pady=(20, 10))

        # ========== FORM KHUNG CUỘN ==========
        form_frame = ctk.CTkScrollableFrame(
            self.master, 
            fg_color="transparent",
            width=320,
            height=400
        )
        form_frame.pack(pady=5, padx=20, fill="both", expand=True)

        # ----- HỌ TÊN -----
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

        # ----- USERNAME -----
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

        # ----- SỐ ĐIỆN THOẠI -----
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

        # ----- CHỨC VỤ -----
        ctk.CTkLabel(
            form_frame,
            text="CHỨC VỤ",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#566573"
        ).pack(anchor="w", padx=10, pady=(0, 4))

        self.entry_chucvu = ctk.CTkEntry(
            form_frame, width=280, height=40,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color="#E5E8E8", border_color="#ABB2B9", border_width=1, corner_radius=8
        )
        self.entry_chucvu.pack(pady=(0, 10))
        self.entry_chucvu.insert(0, "Độc giả")
        self.entry_chucvu.configure(state="disabled")

        # ----- PASSWORD -----
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

        # ----- CONFIRM PASSWORD -----
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
        self.entry_confirm.pack(pady=(0, 10))
        self.entry_confirm.bind("<FocusIn>",  lambda e: self.on_focus(self.entry_confirm, True))
        self.entry_confirm.bind("<FocusOut>", lambda e: self.on_focus(self.entry_confirm, False))

        # ----- GMAIL -----
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

        # ========== KHUNG NÚT BẤM ==========
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=(10, 15))

        ctk.CTkButton(
            button_frame,
            text="TẠO TÀI KHOẢN",
            command=self.tao_tk,
            width=280, height=42,
            fg_color="#2980B9", hover_color="#1A5276",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            corner_radius=8
        ).pack(pady=(0, 10))

        ctk.CTkButton(
            button_frame,
            text="QUAY LẠI ĐĂNG NHẬP",
            command=self.back_login,
            width=280, height=42,
            fg_color="#BDC3C7", hover_color="#A6B1B9",
            text_color="#2C3E50",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            corner_radius=8
        ).pack()

    def on_focus(self, entry, is_focused):
        """Xử lý sự kiện focus cho entry"""
        if is_focused:
            entry.configure(border_color="#2980B9", border_width=2)
        else:
            entry.configure(border_color="#ABB2B9", border_width=1)

    def back_login(self):
        """Quay lại trang đăng nhập"""
        self.app_manager.show_login_page()

    def tao_tk(self):
        """Tạo tài khoản mới"""
        username = self.entry_username.get().strip()
        gmail    = self.entry_gmail.get().strip()
        hoten    = self.entry_hoten.get().strip()
        sdt      = self.entry_sdt.get().strip()
        chucvu   = "Độc giả"
        password = self.entry_password.get().strip()
        confirm  = self.entry_confirm.get().strip()
        
        # Kiểm tra username
        valid, msg = Validation.is_valid_username(username)
        if valid == False:
            messagebox.showerror("Lỗi", msg)
            return

        if self.account_data.check_exists(username) == True:
            messagebox.showerror("Lỗi", f"Tên đăng nhập '{username}' đã tồn tại!")
            return

        # Kiểm tra email
        valid_email, msg_email = Validation.is_valid_email_simple(gmail)
        if valid_email == False:
            messagebox.showerror("Lỗi", msg_email)
            return

        # Kiểm tra SĐT
        valid_phone, msg_phone = Validation.is_valid_phone(sdt)
        if valid_phone == False:
            messagebox.showerror("Lỗi", msg_phone)
            return

        # Kiểm tra họ tên
        if hoten == "":
            messagebox.showerror("Lỗi", "Vui lòng nhập họ tên")
            return

        # Kiểm tra mật khẩu
        if password == "":
            messagebox.showerror("Lỗi", "Vui lòng nhập mật khẩu")
            return

        # Kiểm tra xác nhận mật khẩu
        if password != confirm:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp")
            return

        # Tạo tài khoản
        try:
            self.account_data.create([username, password, hoten, sdt, chucvu, gmail])
            messagebox.showinfo("Thông báo", "Tạo tài khoản thành công!")
            self.app_manager.show_login_page()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo tài khoản: {str(e)}")