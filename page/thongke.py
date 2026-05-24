import customtkinter as ctk
from tkinter import ttk
from query.muontra import MuonTraData
from query.books import BookData

# --- Bảng màu chuẩn đồng bộ với hệ thống ---
C = {
    "bg": "#F0F4F8",
    "card": "#FFFFFF",
    "primary": "#2563EB",
    "success": "#16A34A",
    "warning": "#D97706",
    "danger": "#DC2626",
    "info": "#06B6D4",
    "purple": "#8B5CF6",
    "text": "#111827",
    "text_sub": "#4B5563",
    "border": "#E5E7EB"
}
FONT_FAMILY = "Segoe UI"

class ThongKePage:
    def __init__(self, master, app_manager):
        """Khởi tạo giao diện thống kê."""
        self.master = master
        self.app_manager = app_manager
        self.muontra_data = MuonTraData()
        self.book_data = BookData()
        
        self.config_window()
        self.setup_styles()
        self.render_view()

    def config_window(self):
        """Thiết lập cấu hình cửa sổ hiển thị."""
        self.master.title("📊 Dashboard Thống Kê & Báo Cáo")
        self.master.geometry("1050x700")
        self.master.configure(fg_color=C["bg"])
        ctk.set_appearance_mode("light")

    def setup_styles(self):
        """Cấu hình style chuẩn cho Treeview (Bảng)."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=(FONT_FAMILY, 11, "bold"), background=C["primary"], foreground="white", borderwidth=0, padding=8)
        style.configure("Treeview", font=(FONT_FAMILY, 11), rowheight=35, borderwidth=0, background=C["card"], fieldbackground=C["card"])
        style.map("Treeview", background=[("selected", "#EBF4FF")], foreground=[("selected", C["primary"])])

    def render_view(self):
        """Xây dựng khung giao diện chính."""
        # 1. Header
        header = ctk.CTkFrame(self.master, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        
        ctk.CTkLabel(
            header, text="📊 DASHBOARD HOẠT ĐỘNG THƯ VIỆN",
            font=(FONT_FAMILY, 22, "bold"), text_color=C["text"]
        ).pack(side="left")

        ctk.CTkButton(
            header, text="← Quay Lại", font=(FONT_FAMILY, 12, "bold"),
            fg_color="#64748b", hover_color="#475569", width=120, height=35,
            command=self.back_to_menu
        ).pack(side="right")

        # 2. Vùng cuộn chính (Chống tràn UI)
        self.scroll_view = ctk.CTkScrollableFrame(self.master, fg_color="transparent")
        self.scroll_view.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.scroll_view.columnconfigure(0, weight=1)

        # 3. Khu vực Thẻ thống kê (Cards)
        self._build_stat_cards()

        # 4. Khu vực Bảng dữ liệu (Tables)
        self._build_tables()

    def _build_stat_cards(self):
        """Xây dựng lưới thẻ chỉ số (Grid 4 cột)"""
        card_frame = ctk.CTkFrame(self.scroll_view, fg_color="transparent")
        card_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        for i in range(4): 
            card_frame.columnconfigure(i, weight=1, uniform="card")

        # Lấy dữ liệu
        total_books = self.get_total_books_count()
        cho_duyet = self.get_borrow_records_by_status("cho_duyet")
        dang_muon = self.get_borrow_records_by_status("dang_muon")
        da_tra = self.get_borrow_records_by_status("da_tra")
        qua_han = self.get_borrow_records_by_status("qua_han")
        
        total_phieu = cho_duyet + dang_muon + da_tra + qua_han

        # Cấu trúc: (Tiêu đề, Giá trị, Màu sắc, Icon)
        stats = [
            ("Tổng Đầu Sách", total_books, C["info"], "📚"),
            ("Tổng Lượt Mượn", total_phieu, C["purple"], "📈"),
            ("Chờ Duyệt", cho_duyet, C["warning"], "⏳"),
            ("Đang Mượn", dang_muon, C["primary"], "📖"),
            ("Đã Trả", da_tra, C["success"], "✅"),
            ("Quá Hạn", qua_han, C["danger"], "🚨")
        ]

        # Đổ dữ liệu vào giao diện lưới
        for i, (title, val, color, icon) in enumerate(stats):
            row_idx = i // 4
            col_idx = i % 4
            self.create_statistic_card(card_frame, title, str(val), color, icon).grid(row=row_idx, column=col_idx, padx=8, pady=8, sticky="ew")

    def _build_tables(self):
        """Xây dựng 2 bảng thống kê bên dưới và LOẠI BỎ tài khoản quản lý (username = '1')."""
        table_frame = ctk.CTkFrame(self.scroll_view, fg_color="transparent")
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.columnconfigure((0, 1), weight=1, uniform="table_col")

        # --- Bảng 1: Top Sách Mượn Nhiều Nhất (Loại username '1' và 'admin') ---
        query_top_books = """
            SELECT b.ten_sach, b.tac_gia, COUNT(m.ma_sach) as sl 
            FROM muontra m 
            JOIN books b ON m.ma_sach = b.ma_sach 
            WHERE m.username NOT IN ('1', 'admin')
            GROUP BY m.ma_sach, b.ten_sach, b.tac_gia
            ORDER BY sl DESC LIMIT 5
        """
        self._create_table_widget(
            table_frame, "🏆 Top 5 Sách Mượn Nhiều Nhất", 
            ["Tên sách", "Tác giả", "Lượt mượn"], query_top_books
        ).grid(row=0, column=0, padx=8, pady=8, sticky="nsew")

        # --- Bảng 2: Top Độc Giả Tích Cực (Loại username '1' và 'admin') ---
        query_top_readers = """
            SELECT username, COUNT(*) as sl 
            FROM muontra 
            WHERE username NOT IN ('1', 'admin')
            GROUP BY username 
            ORDER BY sl DESC LIMIT 5
        """
        self._create_table_widget(
            table_frame, "🥇 Top Độc Giả Tích Cực", 
            ["Tài khoản Độc giả", "Tổng số phiếu"], query_top_readers
        ).grid(row=0, column=1, padx=8, pady=8, sticky="nsew")

    def create_statistic_card(self, parent, title, value, color, icon):
        """Hàm con hỗ trợ tạo UI cho 1 thẻ thống kê."""
        card = ctk.CTkFrame(parent, fg_color=C["card"], corner_radius=12, border_width=1, border_color=C["border"])
        
        indicator = ctk.CTkFrame(card, fg_color=color, width=8, corner_radius=12)
        indicator.pack(side="left", fill="y", pady=12, padx=(12, 0))
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=15, pady=15)

        header_row = ctk.CTkFrame(content, fg_color="transparent")
        header_row.pack(fill="x")
        ctk.CTkLabel(header_row, text=title, font=(FONT_FAMILY, 13, "bold"), text_color=C["text_sub"]).pack(side="left")
        ctk.CTkLabel(header_row, text=icon, font=(FONT_FAMILY, 16)).pack(side="right")
        
        ctk.CTkLabel(content, text=value, font=(FONT_FAMILY, 30, "bold"), text_color=C["text"]).pack(anchor="w", pady=(5, 0))
        
        return card

    def _create_table_widget(self, parent, title, columns, query):
        """Hàm con hỗ trợ tạo UI bảng và tự động đổ dữ liệu."""
        frame = ctk.CTkFrame(parent, fg_color=C["card"], corner_radius=12, border_width=1, border_color=C["border"])
        ctk.CTkLabel(frame, text=title, font=(FONT_FAMILY, 15, "bold"), text_color=C["text"]).pack(anchor="w", padx=20, pady=(15, 5))

        tree_frame = ctk.CTkFrame(frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=6)
        
        for col in columns:
            tree.heading(col, text=col)
            if "lượt" in col.lower() or "tổng số" in col.lower():
                tree.column(col, width=100, anchor="center")
            else:
                tree.column(col, width=220, anchor="w")
            
        tree.pack(fill="both", expand=True)

        try:
            data = self.muontra_data.execute_query(query)
            if not data or len(data) == 0:
                tree.insert("", "end", values=["Trống"] * len(columns))
            else:
                for row in data:
                    tree.insert("", "end", values=tuple(row.values()))
        except Exception as e:
            print(f"Lỗi tải dữ liệu bảng: {e}")
            tree.insert("", "end", values=["Lỗi"] * len(columns))

        return frame

    # ========================================================
    # CÁC HÀM LOGIC DB (ĐÃ THÊM LỌC SẠCH TÀI KHOẢN ADMIN)
    # ========================================================
    def get_total_books_count(self):
        """Lấy tổng số lượng sách từ cơ sở dữ liệu."""
        try:
            result = self.book_data.execute_query("SELECT COUNT(*) as total_count FROM books")
            if result is not None and len(result) > 0:
                return result[0]['total_count']
            return 0
        except Exception as e:
            print(f"Lỗi khi đếm tổng số sách: {e}")
            return 0    

    def get_borrow_records_by_status(self, status):
        """Lấy số lượng phiếu mượn theo trạng thái (LOẠI BỎ HOÀN TOÀN TÀI KHOẢN QUẢN LÝ)."""
        try:
            # Thêm điều kiện NOT IN ('1', 'admin')
            result = self.muontra_data.execute_query(
                "SELECT COUNT(*) as total_records FROM muontra WHERE trang_thai = %s AND username NOT IN ('1', 'admin')", (status,)
            )
            if result is not None and len(result) > 0:
                return result[0]['total_records']
            return 0
        except Exception as e:
            print(f"Lỗi khi đếm số phiếu mượn: {e}")
            return 0

    def back_to_menu(self):
        """Trở về menu chính."""
        self.app_manager.show_main_page()