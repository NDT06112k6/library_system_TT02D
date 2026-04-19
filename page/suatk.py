import tkinter as tk
from tkinter import messagebox
import os
import re
import customtkinter as ctk
from query import Query


class SuaTKPage:
    def __init__(self, master, app_manager, username=None, password=None):
        self.master = master
        self.app_manager = app_manager
        self.old_username = username or ""
        self.old_password = password or ""
        self.Q = Query("database/tk.csv", ["taikhoan", "matkhau", "email"])
        self.old_email = self.get_current_email(username) or ""
        self.config()
        self.view()

    def get_current_email(self, username):
        """Get current email for the username"""
        try:
            result = self.Q.search("taikhoan", username, exact=True)
            if not result.empty:
                return result.iloc[0]["email"]
            return ""
        except Exception:
            return ""

    def config(self):
        self.master.title("Sửa tài khoản")
        self.master.geometry("500x450")
        self.master.resizable(False, False)

    def view(self):
        # Title
        ctk.CTkLabel(
            self.master, text="Sửa thông tin tài khoản",
            font=("Arial", 24, "bold"), text_color='#0066cc'
        ).pack(pady=20)

        # Main frame
        main_frame = ctk.CTkFrame(self.master, fg_color='white')
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # ─── Thông tin hiện tại ───────────────────────────────────────────
        ctk.CTkLabel(
            main_frame, text="Thông tin hiện tại",
            font=("Arial", 14, "bold"), text_color='#004080'
        ).pack(anchor="w", padx=20, pady=(0, 10))

        old_frame = ctk.CTkFrame(main_frame, fg_color='#cce7ff', border_width=1)
        old_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(old_frame, text=f"Tên đăng nhập: {self.old_username}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=8)
        ctk.CTkLabel(old_frame, text=f"Mật khẩu: {'*' * len(self.old_password)}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=8)
        ctk.CTkLabel(old_frame, text=f"Email: {self.old_email}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=8)

        # ─── Thông tin mới ────────────────────────────────────────────────
        ctk.CTkLabel(
            main_frame, text="Thông tin mới",
            font=("Arial", 14, "bold"), text_color='#004080'
        ).pack(anchor="w", padx=20, pady=(0, 10))

        new_frame = ctk.CTkFrame(main_frame, fg_color='#cce7ff', border_width=1)
        new_frame.pack(fill="both", expand=True)

        def make_row(parent, label_text, show=""):
            row = ctk.CTkFrame(parent, fg_color='transparent')
            row.pack(fill="x", padx=20, pady=8)
            ctk.CTkLabel(row, text=label_text, font=("Arial", 12), width=160, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(row, font=("Arial", 12), show=show)
            entry.pack(side="right", fill="x", expand=True)
            return entry

        self.entry_username = make_row(new_frame, "Tên đăng nhập mới:")
        self.entry_password = make_row(new_frame, "Mật khẩu mới:", show="*")
        self.entry_email    = make_row(new_frame, "Email mới (Gmail):")

        # Điền giá trị cũ
        self.entry_username.insert(0, self.old_username)
        self.entry_password.insert(0, self.old_password)
        self.entry_email.insert(0, self.old_email)

        # Show password checkbox
        self.show_password = tk.BooleanVar()
        tk.Checkbutton(
            new_frame, text="Hiển thị mật khẩu",
            variable=self.show_password, command=self.toggle_password,
            font=("Arial", 12), bg='#cce7ff'
        ).pack(pady=4)

        # Validation info
        ctk.CTkLabel(
            new_frame,
            text="• Tên đăng nhập không được trùng\n• Gmail phải đúng định dạng @gmail.com",
            font=("Arial", 10), text_color="gray"
        ).pack(pady=8)

        # ─── Buttons ──────────────────────────────────────────────────────
        button_frame = ctk.CTkFrame(self.master, fg_color='white')
        button_frame.pack(pady=20)

        ctk.CTkButton(button_frame, text="Lưu thay đổi", fg_color="#28a745", command=self.save_changes).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Hủy bỏ", fg_color="#6c757d", command=self.cancel).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Khôi phục", fg_color="#ffc107", command=self.reset_form).pack(side="left", padx=10)

        self.master.update()
        self.master.deiconify()
        self.master.lift()
        self.master.focus_force()

    # ── Helpers ─────────────────────────────────────────────────────────────

    def toggle_password(self):
        self.entry_password.configure(show="" if self.show_password.get() else "*")

    def reset_form(self):
        for entry, val in [
            (self.entry_username, self.old_username),
            (self.entry_password, self.old_password),
            (self.entry_email, self.old_email),
        ]:
            entry.delete(0, tk.END)
            entry.insert(0, val)

    def is_valid_gmail(self, email: str) -> bool:
        """Kiểm tra định dạng @gmail.com"""
        pattern = r'^[a-zA-Z0-9._%+\-]+@gmail\.com$'
        return bool(re.match(pattern, email))

    def username_exists(self, username: str) -> bool:
        """Kiểm tra tên đăng nhập đã tồn tại (bỏ qua tài khoản hiện tại)"""
        try:
            result = self.Q.search("taikhoan", username, exact=True)
            if result.empty:
                return False
            # Nếu có kết quả, kiểm tra xem có phải tài khoản hiện tại không
            return result.iloc[0]["taikhoan"] != self.old_username
        except Exception:
            return False

    def validate_input(self) -> bool:
        new_username = self.entry_username.get().strip()
        new_email = self.entry_email.get().strip()

        # Tên đăng nhập trùng
        if new_username != self.old_username and self.username_exists(new_username):
            messagebox.showerror("Lỗi", f"Tên đăng nhập '{new_username}' đã tồn tại!")
            return False

        # Định dạng Gmail
        if new_email and not self.is_valid_gmail(new_email):
            messagebox.showerror("Lỗi", "Gmail không hợp lệ!\nĐịnh dạng đúng: example@gmail.com")
            return False

        return True

    def save_changes(self):
        if not self.validate_input():
            return

        new_username = self.entry_username.get().strip()
        new_password = self.entry_password.get().strip()
        new_email = self.entry_email.get().strip()

        if new_username == self.old_username and new_password == self.old_password and new_email == self.old_email:
            messagebox.showinfo("Thông báo", "Không có thay đổi nào được thực hiện")
            return

        try:
            # Xóa tài khoản cũ
            self.Q.delete("taikhoan", self.old_username)
            # Tạo tài khoản mới
            self.Q.create([
                new_username,
                new_password,
                new_email
            ])
            messagebox.showinfo("Thành công", "Đã cập nhật tài khoản thành công")
            self.app_manager.show_quanlytk_page()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật tài khoản: {str(e)}")

    def cancel(self):
        if self.has_unsaved_changes():
            if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn hủy? Các thay đổi sẽ không được lưu."):
                self.app_manager.show_quanlytk_page()
        else:
            self.app_manager.show_quanlytk_page()

    def has_unsaved_changes(self) -> bool:
        return (
            self.entry_username.get().strip() != self.old_username or
            self.entry_password.get().strip() != self.old_password or
            self.entry_email.get().strip() != self.old_email
        )