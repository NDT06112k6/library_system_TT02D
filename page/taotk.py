import customtkinter as ctk
from tkinter import messagebox
from query.taikhoan import AccountData
from common.validation import Validation


class TaoTKPage:
    """
    Trang tạo tài khoản mới dành cho khách hàng với chức vụ mặc định là Độc giả.
    Hỗ trợ cuộn chuột khi form quá dài.
    """
    def __init__(self, master, app_manager, is_admin=False):
        self.master = master
        self.app_manager = app_manager
        self.is_admin = is_admin
        self.account_data = AccountData()
        self.config()
        self.view()

    def config(self):
        """Cấu hình cửa sổ"""
        self.master.title("Tạo tài khoản")
        self.master.geometry("750x550") 
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def view(self):
        """Vẽ giao diện tạo tài khoản - Chia 2 cột"""
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
        form_frame = ctk.CTkScrollableFrame(self.master, fg_color="transparent")
        form_frame.pack(pady=5, fill="both", expand=True, padx=20)

        # Khung chứa chính (Sử dụng Grid để chia 2 cột)
        inner_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        inner_frame.pack(anchor="center", pady=10, fill="x", expand=True)

        inner_frame.columnconfigure(0, weight=1, uniform="col")
        inner_frame.columnconfigure(1, weight=1, uniform="col")

        # Cột Trái
        left_col = ctk.CTkFrame(inner_frame, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        # Cột Phải
        right_col = ctk.CTkFrame(inner_frame, fg_color="transparent")
        right_col.grid(row=0, column=1, sticky="nsew", padx=(15, 0))

        # Hàm hỗ trợ tạo ô nhập liệu nhanh (tránh lặp code)
        def make_input(parent, label_text, placeholder, is_password=False):
            ctk.CTkLabel(
                parent, text=label_text,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color="#566573"
            ).pack(anchor="w", pady=(0, 4))

            entry = ctk.CTkEntry(
                parent, height=40,
                font=ctk.CTkFont(family="Segoe UI", size=12),
                placeholder_text=placeholder,
                border_color="#ABB2B9", border_width=1, corner_radius=8,
                show="*" if is_password else ""
            )
            entry.pack(fill="x", pady=(0, 15))
            entry.bind("<FocusIn>", lambda e, ent=entry: self.on_focus(ent, True))
            entry.bind("<FocusOut>", lambda e, ent=entry: self.on_focus(ent, False))
            return entry

        # ----- PHÂN BỔ DỮ LIỆU CỘT TRÁI -----
        self.entry_hoten = make_input(left_col, "HỌ TÊN:", "Nhập họ tên...")
        self.entry_username = make_input(left_col, "USERNAME:", "Nhập tên đăng nhập...")
        self.entry_password = make_input(left_col, "PASSWORD:", "Nhập mật khẩu...", is_password=True)
        self.entry_confirm = make_input(left_col, "CONFIRM PASSWORD:", "Nhập lại mật khẩu...", is_password=True)

        # ----- PHÂN BỔ DỮ LIỆU CỘT PHẢI -----
        self.entry_sdt = make_input(right_col, "SỐ ĐIỆN THOẠI:", "Nhập SĐT...")
        self.entry_gmail = make_input(right_col, "GMAIL:", "Nhập Gmail (@gmail.com)...")
        
        # Ô Chức vụ (Đặc biệt vì có màu nền xám và bị khóa)
        ctk.CTkLabel(
            right_col, text="CHỨC VỤ:",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#566573"
        ).pack(anchor="w", pady=(0, 4))
        
        self.entry_chucvu = ctk.CTkEntry(
            right_col, height=40, font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color="#E5E8E8", border_color="#ABB2B9", border_width=1, corner_radius=8
        )
        self.entry_chucvu.pack(fill="x", pady=(0, 15))
        self.entry_chucvu.insert(0, "Độc giả")
        self.entry_chucvu.configure(state="disabled")

        # ========== KHUNG NÚT BẤM (Căn giữa dưới cùng) ==========
        button_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        button_frame.grid(row=1, column=0, columnspan=2, pady=(20, 10))

        ctk.CTkButton(
            button_frame, text="TẠO TÀI KHOẢN", command=self.tao_tk,
            width=280, height=42, fg_color="#2980B9", hover_color="#1A5276",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), corner_radius=8
        ).pack(pady=(0, 10))

        if not self.is_admin:
            ctk.CTkButton(
                button_frame, text="QUAY LẠI ĐĂNG NHẬP", command=self.back_login,
                width=280, height=42, fg_color="#BDC3C7", hover_color="#A6B1B9",
                text_color="#2C3E50", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), corner_radius=8
            ).pack()
        else:
            # Nếu là Admin, chỉ vẽ nút QUAY LẠI (về trang quản lý)
            ctk.CTkButton(
                button_frame, text="QUAY LẠI TRANG QUẢN LÝ", command=self.back_admin,
                width=280, height=42, fg_color="#BDC3C7", hover_color="#A6B1B9",
                text_color="#2C3E50", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), corner_radius=8
            ).pack()
    def on_focus(self, entry, is_focused):
        """Xử lý sự kiện focus cho entry"""
        if is_focused:
            entry.configure(border_color="#2980B9", border_width=2)
        else:
            entry.configure(border_color="#ABB2B9", border_width=1)

    def back_admin(self):
            self.app_manager.show_quanlytk_page()

    def back_login(self):
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