import customtkinter as ctk
from tkinter import ttk
from query.muontra import MuonTraData
from query.books import BookData
import numpy as np
import pandas as pd


# Bảng màu chuẩn đồng bộ với hệ thống
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
        
        self.Cau_Hinh_Cua_So()
        self.setup_styles()
        self.Hien_Thi_Giao_Dien()

    def Cau_Hinh_Cua_So(self): 
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
    
    def Hien_Thi_Giao_Dien(self): 
        """Xây dựng khung giao diện chính."""

        header = ctk.CTkFrame(self.master, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        
        ctk.CTkLabel(
            header, text="📊 DASHBOARD HOẠT ĐỘNG THƯ VIỆN",
            font=(FONT_FAMILY, 22, "bold"), text_color=C["text"]
        ).pack(side="left")

        ctk.CTkButton(
            header, text="← Quay Lại", font=(FONT_FAMILY, 12, "bold"),
            fg_color="#64748b", hover_color="#475569", width=120, height=35,
            command=self.Quay_Lai_Menu
        ).pack(side="right") 

        # 2. Vùng cuộn chính (Chống tràn UI)
        self.scroll_view = ctk.CTkScrollableFrame(self.master, fg_color="transparent")
        self.scroll_view.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.scroll_view.columnconfigure(0, weight=1)

        # 3. Khu vực Thẻ thống kê (Cards) 
        self._Xay_Dung_The_Thong_Ke()

        # 4. Khu vực Bảng dữ liệu (Tables) 
        self._Xay_Dung_Bang()

    def _Xay_Dung_The_Thong_Ke(self): 
        """Xây dựng lưới thẻ chỉ số (Grid 4 cột)"""
        card_frame = ctk.CTkFrame(self.scroll_view, fg_color="transparent")
        card_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        for i in range(4): 
            card_frame.columnconfigure(i, weight=1, uniform="card")

        # Lấy dữ liệu
        total_books = self.Lay_Tong_So_Sach()
        cho_duyet = self.Lay_Ban_Ghi_Muon_Theo_Trang_Thai("cho_duyet")
        dang_muon = self.Lay_Ban_Ghi_Muon_Theo_Trang_Thai("dang_muon")
        da_tra = self.Lay_Ban_Ghi_Muon_Theo_Trang_Thai("da_tra")
        qua_han = self.Lay_Ban_Ghi_Muon_Theo_Trang_Thai("qua_han")

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
            self.Tao_The_Thong_Ke(card_frame, title, str(val), color, icon).grid(row=row_idx, column=col_idx, padx=8, pady=8, sticky="ew")

        # Tính trung bình số lượng sách
        all_books = self.book_data.list_all()
        #quantities (SoLuong)
        quantities = [book[5] for book in all_books]
        avg_qty = np.mean(quantities) if quantities else 0
        median_qty = np.median(quantities) if quantities else 0
        
        if all_books:
            quantities = [book[5] for book in all_books]
            prices = [book[6] for book in all_books]
            
            stats = {
                'Số sách TB': f"{np.mean(quantities):.0f}",
                'Giá TB': f"{np.mean(prices):,.0f} đ",
                'Sách đắt nhất': f"{np.max(prices):,.0f} đ",
                'Sách rẻ nhất': f"{np.min(prices):,.0f} đ",
                'Tổng giá trị': f"{np.sum(prices):,.0f} đ"
            }

    def _Xay_Dung_Bang(self): 
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
        self._Tao_Widget_Bang(
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
        self._Tao_Widget_Bang(
            table_frame, "🥇 Top Độc Giả Tích Cực", 
            ["Tài khoản Độc giả", "Tổng số phiếu"], query_top_readers
        ).grid(row=0, column=1, padx=8, pady=8, sticky="nsew")

    def Tao_The_Thong_Ke(self, parent, title, value, color, icon):
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

    def _Tao_Widget_Bang(self, parent, title, columns, query): 
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
            data = self.muontra_data.thuc_thi_query(query)
            if not data or len(data) == 0:
                tree.insert("", "end", values=["Trống"] * len(columns))
            else:
                for row in data:
                    tree.insert("", "end", values=tuple(row.values()))
        except Exception as e:
            print(f"Lỗi tải dữ liệu bảng: {e}")
            tree.insert("", "end", values=["Lỗi"] * len(columns))

        return frame

    # CÁC HÀM LOGIC DATABASE (ĐÃ NÂNG CẤP SỬ DỤNG PANDAS VÀ SỬA LỖI CỘT)
    def Lay_Tong_So_Sach(self): 
        """Lấy tổng số lượng đầu sách từ cơ sở dữ liệu bằng Pandas DataFrame"""
        try:
            danh_sach_sach = self.book_data.get_all()
            
            # ĐÃ SỬA: Thêm cột 'created_at' vào cuối để khớp với 8 cột từ CSDL MySQL
            ten_cac_cot = ["id", "ma_sach", "ten_sach", "tac_gia", "the_loai", "so_luong", "gia", "created_at"]
            
            df_sach = pd.DataFrame(danh_sach_sach, columns=ten_cac_cot)
            
            if not df_sach.empty:
                return int(len(df_sach))
            return 0
        except Exception as e:
            print(f"Lỗi khi đếm tổng số sách bằng Pandas: {e}")
            return 0    

    def Lay_Ban_Ghi_Muon_Theo_Trang_Thai(self, status): 
        """Lấy số lượng phiếu mượn theo trạng thái bằng các hàm lọc của Pandas"""
        try:
            danh_sach_phieu = self.muontra_data.get_all()
            
            # ĐÃ SỬA: Thêm cột 'created_at' vào cuối để khớp với 10 cột từ CSDL MySQL
            ten_cac_cot = ["id", "ma_phieu", "username", "ma_sach", "ngay_muon", "han_tra", "ngay_tra", "tien_phat", "trang_thai", "created_at"]
            
            df_phieu = pd.DataFrame(danh_sach_phieu, columns=ten_cac_cot)
            
            if not df_phieu.empty:
                df_loc_nguoi_dung = df_phieu[~df_phieu["username"].isin(["1", "admin"])]
                df_ket_qua = df_loc_nguoi_dung[df_loc_nguoi_dung["trang_thai"] == status]
                return int(len(df_ket_qua))
            return 0
        except Exception as e:
            print(f"Lỗi khi lọc số phiếu mượn bằng Pandas: {e}")
            return 0
        
    def Quay_Lai_Menu(self): 
        """Trở về menu chính.""" 
        self.app_manager.Hien_Thi_Trang_Chinh()