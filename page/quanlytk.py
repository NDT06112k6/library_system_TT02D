import customtkinter as ctk
from tkinter import messagebox, ttk
import csv
import os

from common.button import CustomButton


class QuanLyTKPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.config()
        self.view()
        self.load_accounts()

    def config(self):
        self.master.title("Quản lý tài khoản")
        self.master.geometry("700x500")

        ctk.set_appearance_mode("light")  # hoặc "dark"
        ctk.set_default_color_theme("blue")

    def view(self):
        # ===== Title =====
        title_label = ctk.CTkLabel(
            self.master,
            text="Quản lý tài khoản",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=15)

        # ===== Button Frame =====
        button_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        button_frame.pack(pady=10, padx=20, fill="x")

        left_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        left_frame.pack(side="left")

        right_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        right_frame.pack(side="right")

        # Buttons (giữ nguyên logic)
        CustomButton(left_frame, text="Làm mới", command=self.load_accounts, style_type="info").pack(side="left", padx=5)
        CustomButton(left_frame, text="Quản lý sách", command=lambda: self.app_manager.show_quanlysach_page(), style_type="success").pack(side="left", padx=5)
        CustomButton(left_frame, text="Mượn/Trả sách", command=lambda: self.app_manager.show_muontra_page(), style_type="primary").pack(side="left", padx=5)
        CustomButton(left_frame, text="Xóa", command=self.delete_account, style_type="danger").pack(side="left", padx=5)
        CustomButton(left_frame, text="Sửa", command=self.edit_account, style_type="warning").pack(side="left", padx=5)

        CustomButton(right_frame, text="Quay lại", command=self.back_to_login, style_type="secondary").pack(side="right", padx=5)

        # ===== Table Frame =====
        table_frame = ctk.CTkFrame(self.master, corner_radius=10)
        table_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Style Treeview (đẹp hơn)
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        rowheight=30,
                        font=("Arial", 11),
                        borderwidth=0)

        style.configure("Treeview.Heading",
                        font=("Arial", 12, "bold"))

        # Treeview
        columns = ("STT", "Username", "Password")
        self.account_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        self.account_tree.heading("STT", text="STT")
        self.account_tree.heading("Username", text="Tên đăng nhập")
        self.account_tree.heading("Password", text="Mật khẩu")

        self.account_tree.column("STT", width=50, anchor="center")
        self.account_tree.column("Username", width=200, anchor="center")
        self.account_tree.column("Password", width=200, anchor="center")

        # Scrollbar đẹp hơn
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.account_tree.yview)
        self.account_tree.configure(yscrollcommand=scrollbar.set)

        self.account_tree.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # ===== Status Bar =====
        self.status_label = ctk.CTkLabel(
            self.master,
            text="Sẵn sàng",
            anchor="w"
        )
        self.status_label.pack(fill="x", padx=10, pady=5)

    # ====== GIỮ NGUYÊN LOGIC ======
    def load_accounts(self):
        for item in self.account_tree.get_children():
            self.account_tree.delete(item)

        try:
            database_path = "database/tk.csv"
            if not os.path.exists(database_path):
                self.status_label.configure(text="Chưa có dữ liệu tài khoản")
                return

            with open(database_path, "r", encoding="utf-8") as file:
                csv_reader = csv.reader(file)
                accounts = list(csv_reader)

                if not accounts:
                    self.status_label.configure(text="Không có tài khoản nào")
                    return

                for idx, account in enumerate(accounts, 1):
                    if len(account) >= 2:
                        self.account_tree.insert("", "end", values=(idx, account[0], account[1]))

                self.status_label.configure(text=f"Đã tải {len(accounts)} tài khoản")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")
            self.status_label.configure(text="Lỗi tải dữ liệu")

    def delete_account(self):
        selected_item = self.account_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tài khoản cần xóa")
            return

        item_values = self.account_tree.item(selected_item[0], "values")
        username = item_values[1]

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa tài khoản '{username}'?"):
            try:
                self.remove_account_from_file(username)
                self.load_accounts()
                messagebox.showinfo("Thành công", "Đã xóa tài khoản thành công")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa tài khoản: {str(e)}")

    def remove_account_from_file(self, username_to_remove):
        database_path = "database/tk.csv"
        temp_path = "database/tk_temp.csv"

        with open(database_path, "r", encoding="utf-8") as infile, \
             open(temp_path, "w", encoding="utf-8", newline="") as outfile:
            csv_reader = csv.reader(infile)
            csv_writer = csv.writer(outfile)

            for row in csv_reader:
                if len(row) >= 2 and row[0] != username_to_remove:
                    csv_writer.writerow(row)

        os.replace(temp_path, database_path)

    def edit_account(self):
        selected_item = self.account_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tài khoản cần sửa")
            return

        item_values = self.account_tree.item(selected_item[0], "values")
        old_username = item_values[1]
        old_password = item_values[2]

        self.app_manager.show_suatk_page(old_username, old_password)

    def back_to_login(self):
        self.app_manager.show_login_page()