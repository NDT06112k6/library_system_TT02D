import customtkinter as ctk
from tkinter import messagebox, ttk
from common.button import CustomButton
from query import Query


class QuanLyTKPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.Q = Query("database/tk.csv", ["taikhoan", "matkhau", "email"])
        self.config()
        self.view()
        self.load_accounts()

    def config(self):
        self.master.title("👤 Quản lý tài khoản")
        self.master.geometry("900x500")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def view(self):
        # ===== Title =====
        title_label = ctk.CTkLabel(
            self.master,
            text="👤Quản lý tài khoản",
            font=("Segoe UI", 24, "bold")
        )
        title_label.pack(pady=15)

                # ===== Thanh tìm kiếm =====
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

        # Manual placeholder behavior
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

        # Bind Enter key to search
        self.entry_search.bind("<Return>", lambda event: self.search_account())

        # ===== Button Frame =====
        button_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        button_frame.pack(pady=10, padx=20, fill="x")

        left_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        left_frame.pack(side="left")

        right_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        right_frame.pack(side="right")

        CustomButton(left_frame, text="🔄 Làm mới",           command=self.load_accounts,                    style_type="info").pack(side="left", padx=5)
        CustomButton(left_frame, text="🗑️Xóa",              command=self.delete_account,                   style_type="danger").pack(side="left", padx=5)
        CustomButton(left_frame, text="✏️Sửa",              command=self.edit_account,                     style_type="warning").pack(side="left", padx=5)
        CustomButton(left_frame, text="📖Quản lý sách",      command=lambda: self.app_manager.show_quanlysach_page(), style_type="success").pack(side="left", padx=5)
        CustomButton(left_frame, text="📚Mượn/Trả sách",     command=lambda: self.app_manager.show_muontra_page(),    style_type="primary").pack(side="left", padx=5)
        CustomButton(left_frame, text="📊Thống kê",           command=lambda: self.app_manager.show_thongke_page(), style_type="info").pack(side="left", padx=5)

        # Nút Đăng xuất thay cho Quay lại
        CustomButton(right_frame, text="🚪Đăng xuất", command=self.dang_xuat, style_type="secondary").pack(side="right", padx=5)

        # ===== Table Frame =====
        table_frame = ctk.CTkFrame(self.master, corner_radius=10)
        table_frame.pack(expand=True, fill="both", padx=20, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        rowheight=30,
                        font=("Segoe UI", 11),
                        borderwidth=0)
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 12, "bold"))

        # Treeview – thêm cột Gmail
        columns = ("STT", "Username", "Password", "Gmail")
        self.account_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        self.account_tree.heading("STT",      text="STT")
        self.account_tree.heading("Username", text="Tên đăng nhập")
        self.account_tree.heading("Password", text="Mật khẩu")
        self.account_tree.heading("Gmail",    text="Gmail")

        self.account_tree.column("STT",      width=50,  anchor="center")
        self.account_tree.column("Username", width=200, anchor="center")
        self.account_tree.column("Password", width=200, anchor="center")
        self.account_tree.column("Gmail",    width=300, anchor="center")

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

    # ====== LOGIC ======

    def load_accounts(self):
        """Tải toàn bộ tài khoản"""
        self.entry_search.delete(0, "end")
        self.entry_search.insert(0, "Tìm theo tên đăng nhập...")
        self.entry_search.configure(text_color="gray")
        try:
            data = self.Q.list(1, 9999)["data"]
            self._populate_tree(data)
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
                self.Q.delete("taikhoan", username)
                self.load_accounts()
                messagebox.showinfo("Thành công", "Đã xóa tài khoản thành công")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa tài khoản: {str(e)}")

    def edit_account(self):
        selected_item = self.account_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tài khoản cần sửa")
            return

        item_values  = self.account_tree.item(selected_item[0], "values")
        old_username = item_values[1]
        old_password = item_values[2]

        self.app_manager.show_suatk_page(old_username, old_password)

    def dang_xuat(self):
        """Hỏi xác nhận trước khi đăng xuất"""
        if messagebox.askyesno("Xác nhận đăng xuất", "Bạn có chắc chắn muốn đăng xuất không?"):
            self.app_manager.show_login_page()

    def search_account(self):
        """Tìm kiếm tài khoản theo tên đăng nhập"""
        keyword = self.entry_search.get().strip()
        if keyword == "Tìm theo tên đăng nhập...":
            keyword = ""
        try:
            if not keyword:
                # Nếu không có từ khóa, tải tất cả
                self.load_accounts()
            else:
                # Tìm kiếm một phần theo tên đăng nhập
                result = self.Q.search("taikhoan", keyword, exact=False)
                self._populate_tree(result)
                self.status_label.configure(text=f"Tìm thấy {len(result)} tài khoản")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {str(e)}")
            self.status_label.configure(text="Lỗi tìm kiếm")

    def _populate_tree(self, data):
        """Điền dữ liệu vào Treeview"""
        # Xóa dữ liệu cũ
        for item in self.account_tree.get_children():
            self.account_tree.delete(item)
        
        # Thêm dữ liệu mới
        for idx, row in data.iterrows():
            stt = idx + 1
            username = row.get("taikhoan", "")
            password = row.get("matkhau", "")
            email = row.get("email", "")
            self.account_tree.insert("", "end", values=(stt, username, password, email))

    
