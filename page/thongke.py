import customtkinter as ctk
from tkinter import ttk
from query.muontra import MuonTraData
from query.books import BookData

class ThongKePage:
    """
    Trang thống kê.

    Hiển thị các thống kê về sách và mượn trả.
    """
    def __init__(self, master, app_manager):
        """
        Khởi tạo ThongKePage.

        Args:
            master: Cửa sổ chính
            app_manager: Quản lý ứng dụng
        """
        self.master = master
        self.app_manager = app_manager
        self.muontra_data = MuonTraData()
        self.book_data = BookData()
        
        self.config()
        self.view()

    def config(self):
        """
        Cấu hình cửa sổ thống kê.
        """
        self.master.title("Thống kê")
        self.master.geometry("900x600")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def view(self):
        """
        Vẽ giao diện thống kê.
        """
        # ===== Tiêu đề =====
        ctk.CTkLabel(
            self.master,
            text="Thống kê mượn sách",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=15)

        # ===== Khung card thống kê =====
        card_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        card_frame.pack(pady=10, padx=20, fill="x")

        # Card 1: Tổng số sách trong thư viện
        tong_sach = self._dem_tong_sach()
        self._tao_card(card_frame, "Tổng số sách", str(tong_sach), "#3498db")

        # Card 2: Số phiếu đã trả
        so_da_tra = self._dem_phieu_da_tra()
        self._tao_card(card_frame, "Số phiếu đã trả", str(so_da_tra), "#27ae60")

        # Card 3: Số phiếu đang mượn
        so_dang_muon_phieu = self._dem_phieu_dang_muon()
        self._tao_card(card_frame, "Số phiếu đang mượn", str(so_dang_muon_phieu), "#e74c3c")

        # ===== Top sách mượn nhiều nhất =====
        ctk.CTkLabel(
            self.master,
            text="Top 5 sách mượn nhiều nhất:",
            font=("Segoe UI", 14, "bold"),
            anchor="w"
        ).pack(padx=20, pady=(15, 5), fill="x")

        table_frame = ctk.CTkFrame(self.master, corner_radius=10)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=25, font=("Segoe UI", 11), borderwidth=0)
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

        columns = ("STT", "Mã sách", "Tên sách", "Lần mượn")
        self.top_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=7)

        col_configs = {
            "STT":      (40,  "center"),
            "Mã sách":  (100, "center"),
            "Tên sách": (500, "w"),
            "Lần mượn": (100, "center"),
        }
        for col, (width, anchor) in col_configs.items():
            self.top_tree.heading(col, text=col)
            self.top_tree.column(col, width=width, anchor=anchor)

        scrollbar = ctk.CTkScrollbar(table_frame, command=self.top_tree.yview)
        self.top_tree.configure(yscrollcommand=scrollbar.set)

        self.top_tree.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # ===== Điền dữ liệu vào bảng =====
        self._load_top_sach()

        # ===== Nút quay lại =====
        btn_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Quay lại",
            fg_color="#6c757d",
            hover_color="#5a6268",
            command=self.back
        ).pack()

    # ===== HÀM HỖ TRỢ =====

    def _tao_card(self, parent, title, value, color):
        """Tạo card thống kê"""
        card = ctk.CTkFrame(parent, fg_color=color, corner_radius=10)
        card.pack(side="left", padx=10, fill="both", expand=True)

        ctk.CTkLabel(
            card, text=title,
            font=("Segoe UI", 12),
            text_color="white"
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            card, text=value,
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        ).pack(pady=(5, 10))

    def _dem_tong_sach(self):
        """Đếm tổng số đầu sách trong thư viện"""
        try:
            return self.book_data.get_total_count()
        except Exception:
            return 0    

    def _dem_phieu_da_tra(self):
        """Đếm số phiếu đã trả"""
        try:
            counts = self.muontra_data.get_status_counts()
            return counts.get("da_tra", 0)
        except Exception:
            return 0

    def _dem_phieu_dang_muon(self):
        """Đếm số phiếu đang mượn"""
        try:
            counts = self.muontra_data.get_status_counts()
            return counts.get("dang_muon", 0)
        except Exception:
            return 0

    def _load_top_sach(self):
        """Tải top 5 sách mượn nhiều nhất"""
        try:
            # Lấy top sách từ data layer
            top_list = self.muontra_data.get_top_borrowed_books(5)
            
            for idx, (ma_sach, count) in enumerate(top_list, 1):
                # Lấy tên sách từ books.csv
                sach_data = self.book_data.search("ma_sach", str(ma_sach), exact=True)
                if not sach_data.empty:
                    ten_sach = sach_data.iloc[0]["ten_sach"]
                else:
                    ten_sach = "N/A"
                
                self.top_tree.insert("", "end", values=(idx, ma_sach, ten_sach, int(count)))

        except Exception as e:
            print(f"Lỗi load top sách: {str(e)}")

    def back(self):
        """
        Quay lại trang quản lý tài khoản.
        """
        self.app_manager.show_quanlytk_page()
