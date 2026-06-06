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
        self.Tai_Tai_Khoan()

    def config(self): 
        self.master.title("👤 Quản lý tài khoản")
        self.master.geometry("1100x650")  
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def view(self):
        # KHUNG PANEL BÊN TRÁI
        sidebar_frame = ctk.CTkFrame(self.master, width=280, corner_radius=15, fg_color="#F2F4F7")
        sidebar_frame.pack(side="left", fill="y", padx=15, pady=15)
        sidebar_frame.pack_propagate(False)  

        # Tiêu đề trang quản lý
        title_label = ctk.CTkLabel(
            sidebar_frame,
            text="👤 QUẢN LÝ\nTÀI KHOẢN",
            font=("Segoe UI", 20, "bold"),
            text_color="#1A2530",
            justify="center"
        )
        title_label.pack(pady=(25, 20))

        # Khung Tìm kiếm tích hợp trong Sidebar
        search_group = ctk.CTkFrame(sidebar_frame, fg_color="transparent")
        search_group.pack(fill="x", padx=15, pady=10)

        self.entry_search = ctk.CTkEntry(
            search_group,
            height=35,
            corner_radius=8
        )
        self.entry_search.pack(fill="x", pady=(0, 8))
        self.entry_search.insert(0, "Tìm theo tên đăng nhập...")
        self.entry_search.configure(text_color="gray")

        # Logic sự kiện Focus của Entry  
        def Tren_Tieu_Diem_Vao(event): 
            if self.entry_search.get() == "Tìm theo tên đăng nhập...":
                self.entry_search.delete(0, "end")
                self.entry_search.configure(text_color="black")

        def Tren_Tieu_Diem_Ra(event): 
            if self.entry_search.get() == "":
                self.entry_search.insert(0, "Tìm theo tên đăng nhập...")
                self.entry_search.configure(text_color="gray")

        def Tren_Nut_An(event):
            if self.entry_search.get() == "Tìm theo tên đăng nhập...":
                self.entry_search.delete(0, "end")
                self.entry_search.configure(text_color="black")

        self.entry_search.bind("<FocusIn>", Tren_Tieu_Diem_Vao)
        self.entry_search.bind("<FocusOut>", Tren_Tieu_Diem_Ra)
        self.entry_search.bind("<Key>", Tren_Nut_An)
        self.entry_search.bind("<Return>", lambda event: self.search_account())

        # Nút Tìm kiếm
        CustomButton(
            search_group,
            text="🔍 Tìm kiếm",
            command=self.search_account,
            style_type="info" 
        ) .pack(fill="x")

        # Đường phân cách trang trí
        separator = ctk.CTkFrame(sidebar_frame, height=2, fg_color="#D1D5DB")
        separator.pack(fill="x", padx=15, pady=15)

        # Cụm nút bấm chức năng chính xếp dọc
        CustomButton(sidebar_frame, text="🔄 Làm mới dữ liệu", command=self.Tai_Tai_Khoan, style_type="info").pack(fill="x", padx=15, pady=5)
        CustomButton(sidebar_frame, text="➕ Thêm tài khoản mới", command=self.Them_Tai_Khoan, style_type="success").pack(fill="x", padx=15, pady=5)
        CustomButton(sidebar_frame, text="✏️ Chỉnh sửa tài khoản", command=self.edit_account, style_type="warning").pack(fill="x", padx=15, pady=5)
        CustomButton(sidebar_frame, text="🗑️ Xóa tài khoản", command=self.Xoa_Tai_Khoan, style_type="danger").pack(fill="x", padx=15, pady=5)
        
        # Nút Quay lại đặt cố định dưới đáy thanh công cụ
        CustomButton(sidebar_frame, text="← Quay Lại Hệ Thống", command=self.back, style_type="secondary").pack(side="bottom", fill="x", padx=15, pady=20)

        # KHUNG HIỂN THỊ BẢNG BÊN PHẢI
        main_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        main_frame.pack(side="right", expand=True, fill="both", padx=(0, 15), pady=15)

        table_frame = ctk.CTkFrame(main_frame, corner_radius=12, fg_color="white")
        table_frame.pack(expand=True, fill="both")

        # Cấu hình phong cách bảng Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        rowheight=35,
                        font=("Segoe UI", 11),
                        background="white",
                        fieldbackground="white",
                        borderwidth=0)
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 12, "bold"),
                        background="#E5E7EB",
                        foreground="#1F2937")
        style.map("Treeview", background=[("selected", "#3B82F6")], foreground=[("selected", "white")])

        # Tạo bảng và các cột dữ liệu
        columns = ("STT", "Username", "Password", "HoTen", "SDT", "ChucVu", "Gmail")
        self.account_tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.account_tree.heading("STT", text="STT")
        self.account_tree.heading("Username", text="Tên đăng nhập")
        self.account_tree.heading("Password", text="Mật khẩu")
        self.account_tree.heading("HoTen", text="Họ tên")
        self.account_tree.heading("SDT", text="SĐT")
        self.account_tree.heading("ChucVu", text="Chức vụ")
        self.account_tree.heading("Gmail", text="Gmail")

        self.account_tree.column("STT", width=50, anchor="center", stretch=False)
        self.account_tree.column("Username", width=120, anchor="center", stretch=True)
        self.account_tree.column("Password", width=110, anchor="center", stretch=True)
        self.account_tree.column("HoTen", width=160, anchor="w", stretch=True)
        self.account_tree.column("SDT", width=100, anchor="center", stretch=False)
        self.account_tree.column("ChucVu", width=100, anchor="center", stretch=False)
        self.account_tree.column("Gmail", width=180, anchor="w", stretch=True)

        # Thanh cuộn
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.account_tree.yview)
        self.account_tree.configure(yscrollcommand=scrollbar.set)

        self.account_tree.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 5), pady=10)

        # Nhãn hiển thị trạng thái dưới đáy bảng
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Sẵn sàng",
            font=("Segoe UI", 10, "italic"),
            text_color="gray",
            anchor="w"
        )
        self.status_label.pack(fill="x", padx=10, pady=(5, 0))

    def Tai_Tai_Khoan(self): 
        self.entry_search.delete(0, "end")
        self.entry_search.insert(0, "Tìm theo tên đăng nhập...")
        self.entry_search.configure(text_color="gray")
        try:
            rows = self.account_data.lay_tat_ca_tai_khoan()
            self._Tong_Tai_Khoan(rows)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")
            self.status_label.configure(text="Lỗi tải dữ liệu")

    def Xoa_Tai_Khoan(self): 
        selected_item = self.account_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tài khoản cần xóa")
            return

        username = self.account_tree.item(selected_item[0], "values")[1]

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa tài khoản '{username}'?"):
            try:
                self.account_data.Xoa_Tai_Khoan(username)
                self.Tai_Tai_Khoan()
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

        self.app_manager.Hien_Thi_Trang_Sua_TK(old_username, old_password, old_hoten, old_sdt, old_chucvu, old_email)

    def back(self):
        self.app_manager.Hien_Thi_Trang_Chinh()

    def search_account(self):
        keyword = self.entry_search.get().strip()
        if keyword == "Tìm theo tên đăng nhập...":
            keyword = ""
        try: 
            if not keyword:
                self.Tai_Tai_Khoan()
            else:
                rows = self.account_data.search_accounts(keyword)
                self._Tong_Tai_Khoan(rows)
                self.status_label.configure(text=f"Tìm thấy {len(rows)} tài khoản")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {str(e)}")
            self.status_label.configure(text="Lỗi tìm kiếm")
    
    def _Tong_Tai_Khoan(self, data):
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
    
    def Them_Tai_Khoan(self): 
        self.app_manager.Hien_Thi_Trang_Tao_TK(is_admin=True)