import customtkinter as ctk
from tkinter import ttk
from query import Query

class ThongKePage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.Q_muontra = Query("database/muontra.csv", ["ma_phieu", "username", "ma_sach", "ngay_muon", "ngay_tra", "trang_thai"])
        self.Q_sach = Query("database/books.csv", ["ma_sach", "ten_sach", "tac_gia", "the_loai", "so_luong", "gia"])
        
        self.config()
        self.view()

    def config(self):
        self.master.title("Thống kê")
        self.master.geometry("900x600")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def view(self):
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
            data = self.Q_sach.list(1, 9999)["data"]
            return len(data)
        except Exception:
            return 0    

    def _dem_phieu_da_tra(self):
        """Đếm số phiếu đã trả"""
        try:
            data = self.Q_muontra.list(1, 9999)["data"]
            count = len(data[data["trang_thai"] == "da_tra"])
            return count
        except Exception:
            return 0

    def _dem_phieu_dang_muon(self):
        """Đếm số phiếu đang mượn"""
        try:
            data = self.Q_muontra.list(1, 9999)["data"]
            count = len(data[data["trang_thai"] == "dang_muon"])
            return count
        except Exception:
            return 0

    def _load_top_sach(self):
        """Tải top 5 sách mượn nhiều nhất"""
        try:
            # Đọc toàn bộ phiếu mượn
            muontra_data = self.Q_muontra.list(1, 9999)["data"]
            
            # Đếm số lần mượn mỗi sách
            so_muon = muontra_data["ma_sach"].value_counts().head(5)
            
            # Đếm STT
            for idx, (ma_sach, count) in enumerate(so_muon.items(), 1):
                # Lấy tên sách từ books.csv
                sach_data = self.Q_sach.search("ma_sach", str(ma_sach), exact=True)
                if not sach_data.empty:
                    ten_sach = sach_data.iloc[0]["ten_sach"]
                else:
                    ten_sach = "N/A"
                
                self.top_tree.insert("", "end", values=(idx, ma_sach, ten_sach, int(count)))

        except Exception as e:
            print(f"Lỗi load top sách: {str(e)}")

    def back(self):
        self.app_manager.show_quanlytk_page()
