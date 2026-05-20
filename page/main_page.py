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
        self.load_dashboard_data()

    def config(self):
        self.master.title("🖥️ Bảng Điều Khiển Quản Trị Thư Viện")
        self.master.geometry("1000x650")
        ctk.set_appearance_mode("light")

    def view(self):
        # CONTAINER CHÍNH CHIA LÀM 2 VÙNG: BANEL TRÁI (SIDEBAR) & PANEL PHẢI (CONTENT)
        main_container = ctk.CTkFrame(self.master, fg_color="transparent")
        main_container.pack(fill="both", expand=True)

        # 1. ─── THANH MENU BÊN TRÁI (SIDEBAR) VỚI CÁC NÚT ĐIỀU HƯỚNG ───
        sidebar = ctk.CTkFrame(main_container, fg_color="#1e293b", width=220, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo / Tên thương hiệu nhỏ trên Sidebar
        ctk.CTkLabel(
            sidebar, text="📚 QUANG VINH\nLIBRARY", 
            font=("Segoe UI", 16, "bold"), text_color="#f1f5f9"
        ).pack(pady=(20, 30))

        # Khối các nút chức năng quản lý
        ctk.CTkButton(
            sidebar, text="📚 Quản Lý Sách", fg_color="transparent", text_color="#cbd5e1",
            hover_color="#334155", font=("Segoe UI", 13, "bold"), anchor="w", height=40,
            command=lambda: self.app_manager.show_quanlysach_page()
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            sidebar, text="🔄 Mượn Trả Sách", fg_color="transparent", text_color="#cbd5e1",
            hover_color="#334155", font=("Segoe UI", 13, "bold"), anchor="w", height=40,
            command=lambda: self.app_manager.show_muontra_page()
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            sidebar, text="📊 Thống Kê Báo Cáo", fg_color="transparent", text_color="#cbd5e1",
            hover_color="#334155", font=("Segoe UI", 13, "bold"), anchor="w", height=40,
            command=lambda: self.app_manager.show_thongke_page()
        ).pack(fill="x", padx=10, pady=5)

        # Nút Đăng xuất ở cuối thanh bên
        ctk.CTkButton(
            sidebar, text="🚪 Đăng Xuất", fg_color="#ef4444", text_color="white",
            hover_color="#dc2626", font=("Segoe UI", 13, "bold"), height=35,
            command=lambda: self.app_manager.show_login_page()
        ).pack(side="bottom", fill="x", padx=15, pady=20)


        # 2. ─── VÙNG KHÔNG GIAN BÊN PHẢI (LẤP ĐẦY KHOẢNG TRỐNG) ───
        content_area = ctk.CTkFrame(main_container, fg_color="#f8fafc", corner_radius=0)
        content_area.pack(side="right", fill="both", expand=True)

        # Tiêu đề Header Chào mừng
        header_banner = ctk.CTkFrame(content_area, fg_color="#ffffff", height=60, corner_radius=0, border_width=1, border_color="#e2e8f0")
        header_banner.pack(fill="x", side="top")
        header_banner.pack_propagate(False)

        ctk.CTkLabel(
            header_banner, text="👑 HỆ THỐNG QUẢN LÝ THƯ VIỆN QUANG VINH", 
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

        # Định dạng nhanh phong cách bảng Treeview cho đẹp và đồng bộ màu
        style = ttk.Style()
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#f1f5f9")

    # ================= LOGIC ĐỌC DỮ LIỆU TỪ MYSQL DOCKER =================
    
    def load_dashboard_data(self):
        """Đổ dữ liệu thời gian thực từ database lên các Card và 2 bảng thông báo nhanh"""
        try:
            # 1. Đếm và cập nhật số liệu lên các khối Card
            query_total_books = "SELECT COUNT(*) as total FROM books"
            res_books = self.book_data.execute_query(query_total_books)
            self.lbl_tong_sach.configure(text=str(res_books[0]['total'] if res_books else 0))

            query_active_borrows = "SELECT COUNT(*) as total FROM muontra WHERE trang_thai = 'dang_muon'"
            res_borrows = self.book_data.execute_query(query_active_borrows)
            self.lbl_dang_muon.configure(text=str(res_borrows[0]['total'] if res_borrows else 0))

            query_pending = "SELECT COUNT(*) as total FROM muontra WHERE trang_thai = 'cho_duyet'"
            res_pending = self.book_data.execute_query(query_pending)
            self.lbl_cho_duyet.configure(text=str(res_pending[0]['total'] if res_pending else 0))

            # 2. Đổ dữ liệu vào bảng "YÊU CẦU CHỜ DUYỆT" (Trạng thái == 'cho_duyet')
            for item in self.tree_new_requests.get_children(): self.tree_new_requests.delete(item)
            query_req_list = "SELECT username, ma_sach FROM muontra WHERE trang_thai = 'cho_duyet' ORDER BY id DESC LIMIT 5"
            req_data = self.book_data.execute_query(query_req_list)
            if req_data:
                for row in req_data:
                    self.tree_new_requests.insert("", "end", values=(row['username'], row['ma_sach']))

            # 3. Đổ dữ liệu vào bảng "CẢNH BÁO QUÁ HẠN" (Đang mượn ngoài và ngày hiện tại lớn hơn hạn trả)
            for item in self.tree_overdue.get_children(): self.tree_overdue.delete(item)
            query_overdue_list = """
                SELECT username, han_tra FROM muontra 
                WHERE trang_thai = 'dang_muon' AND CURDATE() > STR_TO_DATE(han_tra, '%Y-%m-%d')
                ORDER BY han_tra ASC LIMIT 5
            """
            overdue_data = self.book_data.execute_query(query_overdue_list)
            if overdue_data:
                for row in overdue_data:
                    self.tree_overdue.insert("", "end", values=(row['username'], row['han_tra']))

        except Exception as e:
            print(f"Lỗi khi tải dữ liệu cho bảng điều khiển Dashboard: {e}")