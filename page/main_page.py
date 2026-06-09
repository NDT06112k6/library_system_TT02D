import customtkinter as ctk
from tkinter import ttk
from query.muontra import MuonTraData
from query.books import BookData


class MainPage:
    def __init__(self, master, app_manager, username="Admin"):
        self.master = master
        self.app_manager = app_manager
        self.username = username
        self.muontra_data = MuonTraData()
        self.book_data = BookData()

        self.config()
        self.view()
        self.Tai_Du_Lieu_Bang_Dieu_Khien()

    def config(self): 
        self.master.title("Bảng Điều Khiển Quản Trị Thư Viện")
        self.master.geometry("1000x650")
        ctk.set_appearance_mode("light")

    def view(self):
        # VÙNG CHỨA CHÍNH CHIA LÀM 2 VÙNG: PANEL TRÁI (SIDEBAR) & PANEL PHẢI (CONTENT)
        main_container = ctk.CTkFrame(self.master, fg_color="transparent")
        main_container.pack(fill="both", expand=True)

        # 1. ─── THANH MENU BÊN TRÁI (SIDEBAR) VỚI CÁC NÚT ĐIỀU HƯỚNG ───
        sidebar = ctk.CTkFrame(main_container, fg_color="#1e293b", width=220, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo / Tên thương hiệu 
        ctk.CTkLabel(
            sidebar, text="📚 QUANG VINH\nLIBRARY", 
            font=("Segoe UI", 16, "bold"), text_color="#f1f5f9"
        ).pack(pady=(20, 30))

        # Khối các nút chức năng quản lý
        ctk.CTkButton(
            sidebar, text="📚 Quản Lý Sách", fg_color="transparent", text_color="#cbd5e1",
            hover_color="#334155", font=("Segoe UI", 13, "bold"), anchor="w", height=40,
            command=lambda: self.app_manager.Hien_Thi_Trang_Quan_Ly_Sach()
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            sidebar, text="🔄 Mượn Trả Sách", fg_color="transparent", text_color="#cbd5e1",
            hover_color="#334155", font=("Segoe UI", 13, "bold"), anchor="w", height=40,
            command=lambda: self.app_manager.show_muontra_page()
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            sidebar, text="📊 Thống Kê Báo Cáo", fg_color="transparent", text_color="#cbd5e1",
            hover_color="#334155", font=("Segoe UI", 13, "bold"), anchor="w", height=40,
            command=lambda: self.app_manager.Hien_Thi_Trang_Thong_Ke()
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            sidebar, text="👤 Quản Lý Tài Khoản", fg_color="transparent", text_color="#cbd5e1",
            hover_color="#334155", font=("Segoe UI", 13, "bold"), anchor="w", height=40,
            command=lambda: self.app_manager.Hien_Thi_Trang_Quan_Ly_TK()
        ).pack(fill="x", padx=10, pady=5)

        # Footer frame - chứa các nút ở cuối sidebar
        footer_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        # Nút Hướng Dẫn Sử Dụng
        ctk.CTkButton(
            footer_frame, text="📄 Hướng Dẫn Sử Dụng", fg_color="#10b981", text_color="white",
            hover_color="#059669", font=("Segoe UI", 11, "bold"), height=36,
            command=self._Mo_File_PDF_HDSD
        ).pack(fill="x", pady=5)

        # Nút Tổng Quan Chương Trình
        ctk.CTkButton(
            footer_frame, text="ℹ️ Tổng Quan Về Chương Trình", fg_color="#17a2b8", text_color="white",
            hover_color="#138496", font=("Segoe UI", 11, "bold"), height=36,
            command=self.hien_thi_about
        ).pack(fill="x", pady=5)

        # Nút Đăng xuất ở cuối thanh bên
        ctk.CTkButton(
            footer_frame, text="Đăng Xuất", fg_color="#ef4444", text_color="white",
            hover_color="#dc2626", font=("Segoe UI", 13, "bold"), height=35,
            command=self.xac_nhan_dang_xuat
        ).pack(fill="x", pady=(5, 0))

        # 2. ─── VÙNG KHÔNG GIAN BÊN PHẢI  ───
        content_area = ctk.CTkFrame(main_container, fg_color="#f8fafc", corner_radius=0)
        content_area.pack(side="right", fill="both", expand=True)

        # Tiêu đề Header Chào mừng
        header_banner = ctk.CTkFrame(content_area, fg_color="#ffffff", height=60, corner_radius=0, border_width=1, border_color="#e2e8f0")
        header_banner.pack(fill="x", side="top")
        header_banner.pack_propagate(False)

        ctk.CTkLabel(
            header_banner, text="HỆ THỐNG QUẢN LÝ THƯ VIỆN QUANG VINH", 
            font=("Segoe UI", 16, "bold"), text_color="#0f172a"
        ).pack(side="left", padx=20)

        ctk.CTkLabel(
            header_banner, text=f"Xin chào, {self.username} (Quản lý) 🟢", 
            font=("Segoe UI", 12, "italic"), text_color="#64748b"
        ).pack(side="right", padx=20)

        # Vùng chứa dữ liệu Dashboard
        dashboard_body = ctk.CTkFrame(content_area, fg_color="transparent")
        dashboard_body.pack(fill="both", expand=True, padx=20, pady=20)

        # ----- PHẦN 2.1: KHỐI 3 CÁC HỘP ĐỒ HỌA SỐ LIỆU (CARDS) -----
        cards_container = ctk.CTkFrame(dashboard_body, fg_color="transparent")
        cards_container.pack(fill="x", pady=(0, 20))

        # Hộp 1: Tổng sách
        self.card_sach = ctk.CTkFrame(cards_container, fg_color="#3b82f6", corner_radius=12, height=100)
        self.card_sach.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.card_sach.pack_propagate(False)
        ctk.CTkLabel(self.card_sach, text="📚 Tổng Đầu Sách", font=("Segoe UI", 13, "bold"), text_color="white").pack(pady=(15, 2))
        self.lbl_tong_sach = ctk.CTkLabel(self.card_sach, text="0", font=("Segoe UI", 26, "bold"), text_color="white")
        self.lbl_tong_sach.pack()

        # Hộp 2: Đang mượn ngoài
        self.card_muon = ctk.CTkFrame(cards_container, fg_color="#10b981", corner_radius=12, height=100)
        self.card_muon.pack(side="left", fill="x", expand=True, padx=5)
        self.card_muon.pack_propagate(False)
        ctk.CTkLabel(self.card_muon, text="📖 Đang Mượn Ngoài", font=("Segoe UI", 13, "bold"), text_color="white").pack(pady=(15, 2))
        self.lbl_dang_muon = ctk.CTkLabel(self.card_muon, text="0", font=("Segoe UI", 26, "bold"), text_color="white")
        self.lbl_dang_muon.pack()

        # Hộp 3: Đang chờ duyệt cấp sách
        self.card_duyet = ctk.CTkFrame(cards_container, fg_color="#f59e0b", corner_radius=12, height=100)
        self.card_duyet.pack(side="left", fill="x", expand=True, padx=(10, 0))
        self.card_duyet.pack_propagate(False)
        ctk.CTkLabel(self.card_duyet, text="⏳ Yêu Cầu Chờ Duyệt", font=("Segoe UI", 13, "bold"), text_color="white").pack(pady=(15, 2))
        self.lbl_cho_duyet = ctk.CTkLabel(self.card_duyet, text="0", font=("Segoe UI", 26, "bold"), text_color="white")
        self.lbl_cho_duyet.pack()


        # ----- PHẦN 2.2: HAI BẢNG DANH SÁCH NHẮC VIỆC (CHỜ DUYỆT & QUÁ HẠN) -----
        tables_container = ctk.CTkFrame(dashboard_body, fg_color="transparent")
        tables_container.pack(fill="both", expand=True)

        # Bảng bên trái: 🔔 Danh sách yêu cầu chờ duyệt mới nhất
        left_table_box = ctk.CTkFrame(tables_container, fg_color="#ffffff", border_width=1, border_color="#e2e8f0", corner_radius=12)
        left_table_box.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(left_table_box, text="🔔 YÊU CẦU CHỜ DUYỆT MỚI NHẤT", font=("Segoe UI", 13, "bold"), text_color="#b45309").pack(pady=10, padx=15, anchor="w")
        
        self.tree_new_requests = ttk.Treeview(left_table_box, columns=("Độc giả", "Mã sách"), show="headings", height=8)
        self.tree_new_requests.heading("Độc giả", text="Tên Độc Giả")
        self.tree_new_requests.heading("Mã sách", text="Mã Sách Đăng Ký")
        self.tree_new_requests.column("Độc giả", width=120, anchor="w")
        self.tree_new_requests.column("Mã sách", width=100, anchor="center")
        self.tree_new_requests.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Bảng bên phải: ⚠️ Danh sách độc giả quá hạn trả sách
        right_table_box = ctk.CTkFrame(tables_container, fg_color="#ffffff", border_width=1, border_color="#e2e8f0", corner_radius=12)
        right_table_box.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(right_table_box, text="⚠️ CẢNH BÁO QUÁ HẠN (HÔM NAY)", font=("Segoe UI", 13, "bold"), text_color="#b91c1c").pack(pady=10, padx=15, anchor="w")
        
        self.tree_overdue = ttk.Treeview(right_table_box, columns=("Độc giả", "Hạn trả"), show="headings", height=8)
        self.tree_overdue.heading("Độc giả", text="Độc Giả Trễ")
        self.tree_overdue.heading("Hạn trả", text="Hạn Trả Đúng")
        self.tree_overdue.column("Độc giả", width=120, anchor="w")
        self.tree_overdue.column("Hạn trả", width=100, anchor="center")
        self.tree_overdue.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        style = ttk.Style()
        style.theme_use("clam")
        
        # Cấu hình màu gốc cho Header
        style.configure("Treeview.Heading", 
                        background="#1E3A5F", 
                        foreground="white", 
                        font=("Segoe UI", 11, "bold"), 
                        borderwidth=0)
        
        # ÉP MÀU BẰNG MAP 
        style.map("Treeview.Heading",
                  background=[('active', '#2D5A8E'), ('!active', '#1E3A5F')],
                  foreground=[('active', 'white'), ('!active', 'white')])
        
        # Chỉnh nền các dòng dữ liệu bên dưới
        style.configure("Treeview", 
                        background="#FFFFFF", 
                        fieldbackground="#FFFFFF", 
                        foreground="#111827", 
                        rowheight=35, 
                        font=("Segoe UI", 11), 
                        borderwidth=0)
        
        # Chỉnh màu khi click chọn 1 dòng
        style.map("Treeview", 
                  background=[('selected', '#EBF4FF')], 
                  foreground=[('selected', '#2563EB')])
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#f1f5f9")

    def xac_nhan_dang_xuat(self):
        """Hiển thị hộp thoại yêu cầu xác nhận trước khi đăng xuất hệ thống."""
        from tkinter import messagebox
        ans = messagebox.askyesno("Xác nhận đăng xuất", "Bạn có chắc chắn muốn đăng xuất khỏi hệ thống không?")
        if ans == True:
            self.app_manager.Hien_Thi_Trang_Dang_Nhap()

    def _Mo_File_PDF_HDSD(self):     
        """Mở file PDF hướng dẫn sử dụng"""
        import os
        import webbrowser
        from tkinter import messagebox
        
        file_name = "HDSD.pdf" 
        if os.path.exists(file_name):
            try:
                duong_dan = os.path.abspath(file_name)
                messagebox.showinfo("Thông báo", "Hệ thống đang mở tệp PDF Hướng dẫn sử dụng!")
                webbrowser.open(duong_dan)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể mở PDF: {str(e)}")
        else:
            messagebox.showwarning("Thông báo", f"Tệp tin '{file_name}' không tồn tại trong thư mục gốc của dự án!")

    def hien_thi_about(self):
        """Hiển thị cửa sổ thông tin về chương trình"""
        from tkinter import messagebox
        
        thong_tin_about = """
  📚 HỆ THỐNG QUẢN LÝ THƯ VIỆN        
       QUANG VINH LIBRARY             

📋 Thông Tin Chương Trình:
- Phiên bản: 1.0
- Năm phát triển: 2026
- Mô tả: Ứng dụng quản lý kho sách,
  mượn trả sách, thống kê báo cáo

👥 Nhóm Thực Hiện: 1
- Thành viên 1: Nguyễn Đức Trường (Nhóm trưởng)
- Thành viên 2: Kiều Xuân Vinh
- Thành viên 3: Chu Việt Quang

🎓 Lớp: Lập Trình Python
👨‍🏫 Giảng Viên: Phạm Nguyên Hồng
🏫 Trường: Đại Học Hạ Long

💻 Công Nghệ Sử Dụng:
- CustomTkinter (GUI)
- MySQL (Database)
- Pandas & NumPy (Xử lý dữ liệu)
- Matplotlib (Biểu đồ thống kê)
📧 Liên Hệ: Nhom1@gmail.com
"""
        messagebox.showinfo("Tổng Quan Về Chương Trình", thong_tin_about)


    def Tai_Du_Lieu_Bang_Dieu_Khien(self): 
        """Đổ dữ liệu thời gian thực từ database lên các Card và 2 bảng thông báo nhanh"""
        try:
            # 1. Đếm và cập nhật số liệu lên khối Card Tổng Sách
            query_total_books = "SELECT COUNT(*) as total FROM books"
            res_books = self.book_data.thuc_thi_query(query_total_books)
            tong_s = 0
            if res_books and len(res_books) > 0:
                row = res_books[0]
                tong_s = row.get('total', 0) if isinstance(row, dict) else row[0]
            self.lbl_tong_sach.configure(text=str(tong_s))

            # 2. Đếm và cập nhật số liệu lên khối Card Đang Mượn Ngoài
            query_active_borrows = "SELECT COUNT(*) as total FROM muontra WHERE trang_thai = 'dang_muon'"
            res_borrows = self.book_data.thuc_thi_query(query_active_borrows)
            dang_m = 0
            if res_borrows and len(res_borrows) > 0:
                row = res_borrows[0]
                dang_m = row.get('total', 0) if isinstance(row, dict) else row[0]
            self.lbl_dang_muon.configure(text=str(dang_m))

            # 3. Đếm và cập nhật số liệu lên khối Card Yêu Cầu Chờ Duyệt
            query_pending = "SELECT COUNT(*) as total FROM muontra WHERE trang_thai = 'cho_duyet'"
            res_pending = self.book_data.thuc_thi_query(query_pending)
            cho_d = 0
            if res_pending and len(res_pending) > 0:
                row = res_pending[0]
                cho_d = row.get('total', 0) if isinstance(row, dict) else row[0]
            self.lbl_cho_duyet.configure(text=str(cho_d))

            # 4. Làm mới dữ liệu bảng "YÊU CẦU CHỜ DUYỆT"
            for item in self.tree_new_requests.get_children():
                self.tree_new_requests.delete(item)

            query_req_list = "SELECT username, ma_sach FROM muontra WHERE trang_thai = 'cho_duyet' ORDER BY id DESC LIMIT 5"
            req_data = self.book_data.thuc_thi_query(query_req_list)
            
            if req_data:
                for row in req_data:
                    u = row.get('username') if isinstance(row, dict) else row[0]
                    m = row.get('ma_sach') if isinstance(row, dict) else row[1]
                    self.tree_new_requests.insert("", "end", values=(u, m))

            # 5. Làm mới dữ liệu bảng "CẢNH BÁO QUÁ HẠN"
            for item in self.tree_overdue.get_children():
                self.tree_overdue.delete(item)

            query_overdue_list = """
                SELECT username, han_tra FROM muontra 
                WHERE trang_thai = 'dang_muon' AND CURDATE() > STR_TO_DATE(han_tra, '%Y-%m-%d')
                ORDER BY han_tra ASC LIMIT 5
            """
            overdue_data = self.book_data.thuc_thi_query(query_overdue_list)
            
            if overdue_data:
                for row in overdue_data:
                    u = row.get('username') if isinstance(row, dict) else row[0]
                    h = row.get('han_tra') if isinstance(row, dict) else row[1]
                    self.tree_overdue.insert("", "end", values=(u, h))

        except Exception as e:
            print(f"Lỗi khi tải dữ liệu cho bảng điều khiển Dashboard: {e}")
            try:
                self.master.update_idletasks()
            except:
                pass
        
    
    
    