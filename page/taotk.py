import customtkinter as ctk
from tkinter import messagebox
import os

class TaoTKPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.config()
        self.view()

    def config(self):
        self.master.title("Tạo tài khoản")
        self.master.geometry("420x380")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def view(self):
        # Xóa widget cũ
        for widget in self.master.winfo_children():
            widget.destroy()

        # ========== TIÊU ĐỀ ==========
        label_title = ctk.CTkLabel(
            self.master,
            text="TẠO TÀI KHOẢN",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color="#212F3D"
        )
        label_title.pack(pady=(30, 20))

        # ========== FORM FRAME ==========
        form_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        form_frame.pack(pady=10)

        # ----- Username -----
        lb_user = ctk.CTkLabel(
            form_frame,
            text="USERNAME",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#566573"
        )
        lb_user.pack(anchor="w", padx=10, pady=(0, 5))

        self.entry_username = ctk.CTkEntry(
            form_frame,
            width=280,
            height=40,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Nhập tên đăng nhập...",
            placeholder_text_color="#ABB2B9",
            border_color="#ABB2B9",
            border_width=1,
            corner_radius=8
        )
        self.entry_username.pack(pady=(0, 15))
        # Hiệu ứng focus cho username
        self.entry_username.bind("<FocusIn>", lambda e: self.on_focus(self.entry_username, True))
        self.entry_username.bind("<FocusOut>", lambda e: self.on_focus(self.entry_username, False))

        # ----- Gmail -----
        lb_gmail = ctk.CTkLabel(
            form_frame,
            text="GMAIL",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#566573"
        )
        lb_gmail.pack(anchor="w", padx=10, pady=(0, 5))

        self.entry_gmail = ctk.CTkEntry(
            form_frame,
            width=280,
            height=40,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Nhập Gmail...",
            border_color="#ABB2B9",
            border_width=1,
            corner_radius=8
        )
        self.entry_gmail.pack(pady=(0, 15))

        self.entry_gmail.bind("<FocusIn>", lambda e: self.on_focus(self.entry_gmail, True))
        self.entry_gmail.bind("<FocusOut>", lambda e: self.on_focus(self.entry_gmail, False))

        # ----- Password -----
        lb_pass = ctk.CTkLabel(
            form_frame,
            text="PASSWORD",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#566573"
        )
        lb_pass.pack(anchor="w", padx=10, pady=(0, 5))

        self.entry_password = ctk.CTkEntry(
            form_frame,
            width=280,
            height=40,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Nhập mật khẩu...",
            placeholder_text_color="#ABB2B9",
            border_color="#ABB2B9",
            border_width=1,
            corner_radius=8,
            show="*"
        )
        self.entry_password.pack(pady=(0, 10))

        # ----- Confirm Password -----
        lb_confirm = ctk.CTkLabel(
            form_frame,
            text="CONFIRM PASSWORD",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#566573"
        )
        lb_confirm.pack(anchor="w", padx=10, pady=(0, 5))

        self.entry_confirm = ctk.CTkEntry(
            form_frame,
            width=280,
            height=40,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Nhập lại mật khẩu...",
            border_color="#ABB2B9",
            border_width=1,
            corner_radius=8,
            show="*"
        )
        self.entry_confirm.pack(pady=(0, 10))

        self.entry_confirm.bind("<FocusIn>", lambda e: self.on_focus(self.entry_confirm, True))
        self.entry_confirm.bind("<FocusOut>", lambda e: self.on_focus(self.entry_confirm, False))

        # Hiệu ứng focus cho password
        self.entry_password.bind("<FocusIn>", lambda e: self.on_focus(self.entry_password, True))
        self.entry_password.bind("<FocusOut>", lambda e: self.on_focus(self.entry_password, False))

        # ========== BUTTON FRAME ==========
        button_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        button_frame.pack(pady=20)

        # Nút Tạo tài khoản (Primary - Xanh đại dương đậm)
        btn_create = ctk.CTkButton(
            button_frame,
            text="TẠO TÀI KHOẢN",
            command=self.tao_tk,
            width=280,
            height=45,
            fg_color="#2980B9",
            hover_color="#1A5276",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            corner_radius=8
        )
        btn_create.pack(pady=(0, 12))

        # Nút Quay lại (Secondary - Xám bạc)
        btn_back = ctk.CTkButton(
            button_frame,
            text="QUAY LẠI ĐĂNG NHẬP",
            command=self.back_login,
            width=280,
            height=45,
            fg_color="#BDC3C7",
            hover_color="#A6B1B9",
            text_color="#2C3E50",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            corner_radius=8
        )
        btn_back.pack()

    def on_focus(self, entry, is_focused):
        """Hiệu ứng đổi màu viền khi focus"""
        if is_focused:
            entry.configure(border_color="#2980B9", border_width=2)
        else:
            entry.configure(border_color="#ABB2B9", border_width=1)

    def back_login(self):
        print("Quay lại trang đăng nhập")
        self.app_manager.show_login_page()

    def tao_tk(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username.strip() == "" or password.strip() == "":
            messagebox.showerror("Thông báo", "Vui lòng nhập đầy đủ thông tin")
            return

        os.makedirs("database", exist_ok=True)
        with open("database/tk.csv", "a", encoding="utf-8") as f:
            f.write(username + "," + password + "\n")

        messagebox.showinfo("Thông báo", "Tạo tài khoản thành công")
        self.app_manager.show_login_page()