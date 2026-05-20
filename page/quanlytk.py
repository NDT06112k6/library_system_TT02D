import customtkinter as ctk
from tkinter import messagebox, ttk
from common.button import CustomButton
from query.taikhoan import AccountData


class QuanLyTKPage:

    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.account_data = AccountData()
        self.config()
        self.view()
        self.load_accounts()

    def config(self):
        self.master.title("👤 Quản lý tài khoản")
        self.master.geometry("1000x600")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def view(self):
        title_label = ctk.CTkLabel(
            self.master,
            text="👤 Quản lý tài khoản",
            font=("Segoe UI", 24, "bold")
        )
        title_label.pack(pady=15)

        search_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        search_frame.pack(pady=5, padx=20, fill="x")

        self.entry_search = ctk.CTkEntry(
            search_frame,
            height=35,
            corner_radius=8
        )
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_search.insert(0, "Tìm theo tên đăng nhập...")
        self.entry_search.configure(text_color="gray")

        def on_focus_in(event):
            if self.entry_search.get() == "Tìm theo tên đăng nhập...":
                self.entry_search.delete(0, "end")
                self.entry_search.configure(text_color="black")

        def on_focus_out(event):
            if self.entry_search.get() == "":
                self.entry_search.insert(0, "Tìm theo tên đăng nhập...")
                self.entry_search.configure(text_color="gray")

        def on_key_press(event):
            if self.entry_search.get() == "Tìm theo tên đăng nhập...":
                self.entry_search.delete(0, "end")
                self.entry_search.configure(text_color="black")

        self.entry_search.bind("<FocusIn>", on_focus_in)
        self.entry_search.bind("<FocusOut>", on_focus_out)
        self.entry_search.bind("<Key>", on_key_press)

        CustomButton(
            search_frame,
            text="Tìm kiếm",
            command=self.search_account,
            style_type="info"
        ).pack(side="left")

        self.entry_search.bind("<Return>", lambda event: self.search_account())

        button_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        button_frame.pack(pady=10, padx=20, fill="x")

        left_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        left_frame.pack(side="left")

        right_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        right_frame.pack(side="right")

        CustomButton(left_frame, text="🔄 Làm mới", command=self.load_accounts, style_type="info").pack(side="left", padx=5)
        CustomButton(left_frame, text="🗑️ Xóa", command=self.delete_account, style_type="danger").pack(side="left", padx=5)
        CustomButton(left_frame, text="✏️ Sửa", command=self.edit_account, style_type="warning").pack(side="left", padx=5)
        CustomButton(left_frame, text="📖 Quản lý sách", command=lambda: self.app_manager.show_quanlysach_page(), style_type="success").pack(side="left", padx=5)
        CustomButton(left_frame, text="📚 Mượn/Trả sách", command=lambda: self.app_manager.show_muontra_page(), style_type="primary").pack(side="left", padx=5)
        CustomButton(left_frame, text="📊 Thống kê", command=lambda: self.app_manager.show_thongke_page(), style_type="info").pack(side="left", padx=5)

        CustomButton(right_frame, text="← Quay Lại", command=self.back, style_type="secondary").pack(side="right", padx=5)

        table_frame = ctk.CTkFrame(self.master, corner_radius=10)
        table_frame.pack(expand=True, fill="both", padx=20, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        rowheight=32,
                        font=("Segoe UI", 11),
                        borderwidth=0)
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 12, "bold"))

        columns = ("STT", "Username", "Password", "HoTen", "SDT", "ChucVu", "Gmail")
        self.account_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.account_tree.heading("STT", text="STT")
        self.account_tree.heading("Username", text="Tên đăng nhập")
        self.account_tree.heading("Password", text="Mật khẩu")
        self.account_tree.heading("HoTen", text="Họ tên")
        self.account_tree.heading("SDT", text="SĐT")
        self.account_tree.heading("ChucVu", text="Chức vụ")
        self.account_tree.heading("Gmail", text="Gmail")

        self.account_tree.column("STT", width=50, anchor="center", stretch=False)
        self.account_tree.column("Username", width=130, anchor="center", stretch=True)
        self.account_tree.column("Password", width=110, anchor="center", stretch=True)
        self.account_tree.column("HoTen", width=180, anchor="center", stretch=True)
        self.account_tree.column("SDT", width=110, anchor="center", stretch=False)
        self.account_tree.column("ChucVu", width=110, anchor="center", stretch=False)
        self.account_tree.column("Gmail", width=200, anchor="center", stretch=True)

        scrollbar = ctk.CTkScrollbar(table_frame, command=self.account_tree.yview)
        self.account_tree.configure(yscrollcommand=scrollbar.set)

        self.account_tree.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        self.status_label = ctk.CTkLabel(
            self.master,
            text="Sẵn sàng",
            anchor="w"
        )
        self.status_label.pack(fill="x", padx=10, pady=5)

    def load_accounts(self):
        self.entry_search.delete(0, "end")
        self.entry_search.insert(0, "Tìm theo tên đăng nhập...")
        self.entry_search.configure(text_color="gray")
        try:
            rows = self.account_data.get_all_accounts()
            self._populate_tree(rows)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")
            self.status_label.configure(text="Lỗi tải dữ liệu")

    def delete_account(self):
        selected_item = self.account_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tài khoản cần xóa")
            return

        username = self.account_tree.item(selected_item[0], "values")[1]

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa tài khoản '{username}'?"):
            try:
                self.account_data.delete_account(username)
                self.load_accounts()
                messagebox.showinfo("Thành công", "Đã xóa tài khoản thành công")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa tài khoản: {str(e)}")

    def edit_account(self):
        selected_item = self.account_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tài khoản cần sửa")
            return

        item_values = self.account_tree.item(selected_item[0], "values")
        old_username = item_values[1]
        old_password = item_values[2]
        old_hoten = item_values[3]
        old_sdt = item_values[4]
        old_chucvu = item_values[5]
        old_email = item_values[6]

        self.app_manager.show_suatk_page(old_username, old_password, old_hoten, old_sdt, old_chucvu, old_email)

    def back(self):
        self.app_manager.show_main_page()

    def search_account(self):
        keyword = self.entry_search.get().strip()
        if keyword == "Tìm theo tên đăng nhập...":
            keyword = ""
        try:
            if not keyword:
                self.load_accounts()
            else:
                rows = self.account_data.search_accounts(keyword)
                self._populate_tree(rows)
                self.status_label.configure(text=f"Tìm thấy {len(rows)} tài khoản")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {str(e)}")
            self.status_label.configure(text="Lỗi tìm kiếm")

    def _populate_tree(self, data):
        for item in self.account_tree.get_children():
            self.account_tree.delete(item)
        
        for idx, row in enumerate(data, 1):
            if len(row) >= 7:
                self.account_tree.insert("", "end", values=(
                    idx, 
                    row[1], 
                    row[2], 
                    row[3], 
                    row[4], 
                    row[5], 
                    row[6]
                ))
        self.status_label.configure(text=f"Tổng số: {len(data)} tài khoản")