import tkinter as tk
from tkinter import messagebox
import csv
import os
import customtkinter as ctk


class SuaTKPage:
    def __init__(self, master, app_manager, username=None, password=None):
        self.master = master
        self.app_manager = app_manager
        self.old_username = username or ""
        self.old_password = password or ""
        self.old_email = self.get_current_email(username) or ""
        self.config()
        self.view()

    def get_current_email(self, username):
        """Get current email for the username"""
        try:
            database_path = "database/tk.csv"
            if not os.path.exists(database_path):
                return ""
            with open(database_path, "r", encoding="utf-8") as file:
                csv_reader = csv.reader(file)
                next(csv_reader, None)  # Skip header
                for row in csv_reader:
                    if len(row) >= 3 and row[0] == username:
                        return row[2]
            return ""
        except Exception:
            return ""

    def config(self):
        self.master.title("Sửa tài khoản")
        self.master.geometry("500x450")
        self.master.resizable(False, False)

    def view(self):
        # Title
        title_label = ctk.CTkLabel(self.master, text="Sửa thông tin tài khoản", font=("Arial", 24, "bold"), text_color='#0066cc')
        title_label.pack(pady=20)

        # Main frame
        main_frame = ctk.CTkFrame(self.master, fg_color='white')
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Old account info frame
        old_label = ctk.CTkLabel(main_frame, text="Thông tin hiện tại", font=("Arial", 14, "bold"), text_color='#004080')
        old_label.pack(anchor="w", padx=20, pady=(0,10))
        old_frame = ctk.CTkFrame(main_frame, fg_color='#cce7ff', border_width=1)
        old_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(old_frame, text=f"Tên đăng nhập: {self.old_username}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=10)
        ctk.CTkLabel(old_frame, text=f"Mật khẩu: {'*' * len(self.old_password)}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=10)
        ctk.CTkLabel(old_frame, text=f"Email: {self.old_email}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=10)

        # New account info frame
        new_label = ctk.CTkLabel(main_frame, text="Thông tin mới", font=("Arial", 14, "bold"), text_color='#004080')
        new_label.pack(anchor="w", padx=20, pady=(0,10))
        new_frame = ctk.CTkFrame(main_frame, fg_color='#cce7ff', border_width=1)
        new_frame.pack(fill="both", expand=True)

        # Username input
        username_frame = ctk.CTkFrame(new_frame, fg_color='transparent')
        username_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(username_frame, text="Tên đăng nhập mới:", font=("Arial", 12)).pack(side="left")
        self.entry_username = ctk.CTkEntry(username_frame, font=("Arial", 12))
        self.entry_username.pack(side="right", fill="x", expand=True)
        self.entry_username.insert(0, self.old_username)

        # Password input
        password_frame = ctk.CTkFrame(new_frame, fg_color='transparent')
        password_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(password_frame, text="Mật khẩu mới:", font=("Arial", 12)).pack(side="left")
        self.entry_password = ctk.CTkEntry(password_frame, font=("Arial", 12), show="*")
        self.entry_password.pack(side="right", fill="x", expand=True)
        self.entry_password.insert(0, self.old_password)

        # Email input
        email_frame = ctk.CTkFrame(new_frame, fg_color='transparent')
        email_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(email_frame, text="Email mới:", font=("Arial", 12)).pack(side="left")
        self.entry_email = ctk.CTkEntry(email_frame, font=("Arial", 12))
        self.entry_email.pack(side="right", fill="x", expand=True)
        self.entry_email.insert(0, self.old_email)

        # Show password checkbox
        self.show_password = tk.BooleanVar()
        show_pass_check = tk.Checkbutton(new_frame, text="Hiển thị mật khẩu", 
                                       variable=self.show_password, command=self.toggle_password, font=("Arial", 12), bg='#cce7ff')
        show_pass_check.pack(pady=5)

        # Validation info
        info_text = "• Tên đăng nhập và mật khẩu không được để trống\n• Tên đăng nhập không được trùng với tài khoản khác"
        ctk.CTkLabel(new_frame, text=info_text, font=("Arial", 10), text_color="gray").pack(pady=10)

        # Buttons frame
        button_frame = ctk.CTkFrame(self.master, fg_color='white')
        button_frame.pack(pady=20)

        save_btn = ctk.CTkButton(button_frame, text="Lưu thay đổi", fg_color="#28a745", command=self.save_changes)
        save_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(button_frame, text="Hủy bỏ", fg_color="#6c757d", command=self.cancel)
        cancel_btn.pack(side="left", padx=10)

        reset_btn = ctk.CTkButton(button_frame, text="Khôi phục", fg_color="#ffc107", command=self.reset_form)
        reset_btn.pack(side="left", padx=10)

        # Update the window to ensure it displays
        self.master.update()
        self.master.deiconify()
        self.master.lift()
        self.master.focus_force()

    def toggle_password(self):
        """Toggle password visibility"""
        if self.show_password.get():
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")

    def reset_form(self):
        """Reset form to original values"""
        self.entry_username.delete(0, tk.END)
        self.entry_username.insert(0, self.old_username)
        self.entry_password.delete(0, tk.END)
        self.entry_password.insert(0, self.old_password)
        self.entry_email.delete(0, tk.END)
        self.entry_email.insert(0, self.old_email)

    def validate_input(self):
        """Validate user input"""
        new_username = self.entry_username.get().strip()
        new_password = self.entry_password.get().strip()
        new_email = self.entry_email.get().strip()

        # Check if username already exists (excluding current account)
        if new_username != self.old_username and self.username_exists(new_username):
            messagebox.showerror("Lỗi", f"Tên đăng nhập '{new_username}' đã tồn tại")
            return False

        return True

    def username_exists(self, username):
        """Check if username already exists in database"""
        try:
            database_path = "database/tk.csv"
            if not os.path.exists(database_path):
                return False

            with open(database_path, "r", encoding="utf-8") as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if len(row) >= 2 and row[0] == username:
                        return True
            return False
        except Exception:
            return False

    def save_changes(self):
        """Save changes to database"""
        if not self.validate_input():
            return

        new_username = self.entry_username.get().strip()
        new_password = self.entry_password.get().strip()
        new_email = self.entry_email.get().strip()

        # Check if any changes were made
        if new_username == self.old_username and new_password == self.old_password and new_email == self.old_email:
            messagebox.showinfo("Thông báo", "Không có thay đổi nào được thực hiện")
            return

        try:
            self.update_account_in_file(new_username, new_password, new_email)
            messagebox.showinfo("Thành công", "Đã cập nhật tài khoản thành công")
            self.app_manager.show_quanlytk_page()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật tài khoản: {str(e)}")

    def update_account_in_file(self, new_username, new_password, new_email):
        """Update account in CSV file"""
        database_path = "database/tk.csv"
        temp_path = "database/tk_temp.csv"
        
        with open(database_path, "r", encoding="utf-8") as infile, \
             open(temp_path, "w", encoding="utf-8", newline="") as outfile:
            csv_reader = csv.reader(infile)
            csv_writer = csv.writer(outfile)
            
            for row in csv_reader:
                if len(row) >= 2:
                    if row[0] == self.old_username:
                        csv_writer.writerow([new_username, new_password, new_email])
                    else:
                        # Ensure row has 3 columns
                        while len(row) < 3:
                            row.append("")
                        csv_writer.writerow(row)
        
        # Replace original file with temp file
        os.replace(temp_path, database_path)

    def cancel(self):
        """Cancel and return to account management"""
        if self.has_unsaved_changes():
            if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn hủy? Các thay đổi sẽ không được lưu."):
                self.app_manager.show_quanlytk_page()
        else:
            self.app_manager.show_quanlytk_page()

    def has_unsaved_changes(self):
        """Check if there are unsaved changes"""
        current_username = self.entry_username.get().strip()
        current_password = self.entry_password.get().strip()
        current_email = self.entry_email.get().strip()
        return (current_username != self.old_username or current_password != self.old_password or current_email != self.old_email)