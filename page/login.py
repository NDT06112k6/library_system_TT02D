import customtkinter as ctk
from tkinter import messagebox


class LoginPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        self.config()
        self.view()

    def config(self):
        self.master.title("Đăng nhập")
        self.master.geometry("400x300")

        # Theme
        ctk.set_appearance_mode("light")  # hoặc "dark"
        ctk.set_default_color_theme("blue")

    def view(self):
        # Frame chính (card)
        frame = ctk.CTkFrame(self.master, corner_radius=12)
        frame.pack(pady=30, padx=30, fill="both", expand=True)

        # Tiêu đề
        label = ctk.CTkLabel(
            frame,
            text="ĐĂNG NHẬP",
            font=("Segoe UI", 24, "bold")
        )
        label.pack(pady=(20, 10))

        # Username
        self.entry_username = ctk.CTkEntry(
            frame,
            placeholder_text="Nhập username...",
            height=35,
            corner_radius=8
        )
        self.entry_username.pack(pady=10, padx=20, fill="x")

        # Password
        self.entry_password = ctk.CTkEntry(
            frame,
            placeholder_text="Nhập password...",
            show="*",
            height=35,
            corner_radius=8
        )
        self.entry_password.pack(pady=10, padx=20, fill="x")

        # Gmail
        self.entry_gmail = ctk.CTkEntry(
            frame,
            placeholder_text="Nhập Gmail...",
            height=35,
            corner_radius=8
        )
        self.entry_gmail.pack(pady=10, padx=20, fill="x")

        # Button frame
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        # Nút tạo tài khoản
        btn_register = ctk.CTkButton(
            btn_frame,
            text="Tạo tài khoản",
            fg_color="#6c757d",  # xám
            hover_color="#5a6268",
            corner_radius=10,
            command=self.tao_tk
        )
        btn_register.grid(row=0, column=0, padx=10)

        # Nút đăng nhập
        btn_login = ctk.CTkButton(
            btn_frame,
            text="Đăng nhập",
            fg_color="#1A73E8",  # xanh chủ đạo
            hover_color="#1669c1",
            corner_radius=10,
            command=self.login
        )
        btn_login.grid(row=0, column=1, padx=10)

    def tao_tk(self):
        self.app_manager.show_taotk_page()

    def login(self):
        try:
            with open("database/tk.csv", "r") as file:
                for line in file:
                    tk_info = line.strip().split(",")

                    if (
                        len(tk_info) >= 3
                        and self.entry_username.get() == tk_info[0]
                        and self.entry_password.get() == tk_info[1]
                        and self.entry_gmail.get() == tk_info[2]
                    ):
                        messagebox.showinfo("Thông báo", "Đăng nhập thành công")
                        self.app_manager.show_quanlytk_page()
                        return

                messagebox.showerror("Thông báo", "Đăng nhập thất bại")

        except FileNotFoundError:
            messagebox.showerror("Thông báo", "Chưa có tài khoản nào được tạo")