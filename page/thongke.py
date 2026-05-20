import customtkinter as ctk
from query.muontra import MuonTraData
from query.books import BookData


class ThongKePage:
    """
    Trang thống kê số liệu tổng quan và trực quan hóa Top sách mượn nhiều nhất
    bằng biểu đồ cột tự vẽ (không dùng thư viện ngoài).
    """
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.muontra_data = MuonTraData()
        self.book_data = BookData()
        
        self.config()
        self.view()

    def config(self):
        self.master.title("📊 Hệ Thống Thống Kê & Báo Cáo")
        self.master.geometry("950x650")
        ctk.set_appearance_mode("light")

    def view(self):
        # ===== TIÊU ĐỀ CHÍNH =====
        ctk.CTkLabel(
            self.master,
            text="📊 THỐNG KÊ HOẠT ĐỘNG THƯ VIỆN",
            font=("Segoe UI", 24, "bold"),
            text_color="#1a365d"
        ).pack(pady=20)

        # ===== KHU VỰC CÁC CARD THỐNG KÊ TỔNG QUAN =====
        card_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        card_frame.pack(pady=10, padx=30, fill="x")

        tong_sach = self._dem_tong_sach()
        self._tao_card(card_frame, "📚 Tổng đầu sách", str(tong_sach), "#3498db")

        so_da_tra = self._dem_phieu_theo_trang_thai("da_tra")
        self._tao_card(card_frame, "✅ Phiếu đã trả", str(so_da_tra), "#27ae60")

        so_dang_muon_phieu = self._dem_phieu_theo_trang_thai("dang_muon")
        self._tao_card(card_frame, "📖 Phiếu đang mượn", str(so_dang_muon_phieu), "#e74c3c")

        # ===== KHU VỰC BIỂU ĐỒ CỘT TRỰC QUAN (VISUAL CHART) =====
        chart_container = ctk.CTkFrame(self.master, fg_color="#f8fafc", border_width=1, border_color="#e2e8f0", corner_radius=15)
        chart_container.pack(fill="both", expand=True, padx=30, pady=(20, 15))

        ctk.CTkLabel(
            chart_container,
            text="📈 TOP 5 SÁCH ĐƯỢC MƯỢN NHIỀU NHẤT (Biểu đồ số lần mượn)",
            font=("Segoe UI", 14, "bold"),
            text_color="#475569",
            anchor="w"
        ).pack(padx=20, pady=(15, 10), fill="x")

        # Khung chứa các thanh biểu đồ cột nằm ngang
        self.chart_body = ctk.CTkFrame(chart_container, fg_color="transparent")
        self.chart_body.pack(fill="both", expand=True, padx=20, pady=10)

        # Tiến hành nạp dữ liệu và vẽ biểu đồ cột lên màn hình
        self._ve_bieu_do_dong()

        # ===== NÚT QUAY LẠI =====
        btn_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(
            btn_frame,
            text="← Quay Lại Menu Chính",
            font=("Segoe UI", 13, "bold"),
            fg_color="#64748b",
            hover_color="#475569",
            width=180,
            height=40,
            command=self.back
        ).pack()

    # ===== HÀM DESIGN CARD ĐỒ HỌA =====
    def _tao_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, fg_color=color, corner_radius=12)
        card.pack(side="left", padx=10, fill="both", expand=True)

        ctk.CTkLabel(
            card, text=title,
            font=("Segoe UI", 13, "bold"),
            text_color="white"
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            card, text=value,
            font=("Segoe UI", 32, "bold"),
            text_color="white"
        ).pack(pady=(5, 15))

    # ===== BIỂU DIỄN VẼ BIỂU ĐỒ ĐỘNG BẰNG CODE thuần =====
    def _ve_bieu_do_dong(self):
        """Vẽ biểu đồ cột dọc 3D giả lập kèm bảng xếp hạng chi tiết siêu trực quan"""
        try:
            # 1. Truy vấn lấy top 5 sách mượn từ MySQL Docker
            query = """
                SELECT m.ma_sach, b.ten_sach, COUNT(m.ma_sach) as lan_muon
                FROM muontra m
                JOIN books b ON m.ma_sach = b.ma_sach
                GROUP BY m.ma_sach, b.ten_sach
                ORDER BY lan_muon DESC
                LIMIT 5
            """
            top_list = self.muontra_data.execute_query(query)

            if not top_list:
                ctk.CTkLabel(self.chart_body, text="❌ Chưa có dữ liệu mượn trả để phân tích đồ thị.", font=("Segoe UI", 13, "italic"), text_color="gray").pack(pady=80)
                return

            # Thiết lập khung chia đôi: Bên trái vẽ biểu đồ cột dọc, Bên phải làm bảng số liệu vinh danh
            split_frame = ctk.CTkFrame(self.chart_body, fg_color="transparent")
            split_frame.pack(fill="both", expand=True, padx=10, pady=10)

            # ================= VÙNG BÊN TRÁI: BIỂU ĐỒ CỘT DỌC (VERTICAL BARS) =================
            visual_frame = ctk.CTkFrame(split_frame, fg_color="#ffffff", border_width=1, border_color="#f1f5f9", corner_radius=12)
            visual_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))

            # Khung chứa các cột (Xếp cạnh nhau từ dưới lên)
            bars_area = ctk.CTkFrame(visual_frame, fg_color="transparent", height=230)
            bars_area.pack(fill="x", side="top", padx=20, pady=(30, 5))
            bars_area.pack_propagate(False)

            # Mốc số lần mượn cao nhất để tính chiều cao tỷ lệ cột (Tối đa 180 pixel chiều cao)
            max_lan_muon = int(top_list[0].get("lan_muon", 1))
            if max_lan_muon == 0: max_lan_muon = 1

            # Mảng màu sắc Gradient giả lập cho từng Top (Tạo sự tương phản mạnh)
            color_palette = ["#3b82f6", "#10b981", "#f59e0b", "#ec4899", "#8b5cf6"]

            for idx, row in enumerate(top_list):
                lan_muon = int(row.get("lan_muon", 0))
                color = color_palette[idx] if idx < len(color_palette) else "#64748b"

                # Tính toán chiều cao cột động
                ty_le_chieu_cao = lan_muon / max_lan_muon
                chieu_cao_cot = int(ty_le_chieu_cao * 160)
                if chieu_cao_cot < 15: chieu_cao_cot = 15 # Chiều cao tối thiểu để hiện khối màu

                # Tạo container cho một cột (Gồm: Số lần mượn ở đầu -> Khối màu -> Tên Top ở chân)
                column_wrapper = ctk.CTkFrame(bars_area, fg_color="transparent", width=70)
                column_wrapper.pack(side="left", fill="y", expand=True, padx=5)

                # Số lần mượn hiển thị trên đầu cột
                ctk.CTkLabel(column_wrapper, text=f"{lan_muon} lượt", font=("Segoe UI", 11, "bold"), text_color=color).pack(side="top", pady=(0, 2))

                # Đáy neo giữ cột mọc ngược lên trên
                bar_base = ctk.CTkFrame(column_wrapper, fg_color="transparent")
                bar_base.pack(side="top", fill="both", expand=True)

                # Khối cột màu đồ họa phẳng
                chart_bar = ctk.CTkFrame(bar_base, fg_color=color, corner_radius=6, width=32, height=chieu_cao_cot)
                chart_bar.pack(side="bottom")

            # Đường kẻ chân đế biểu đồ và nhãn Top bên dưới chân cột
            axis_line = ctk.CTkFrame(visual_frame, fg_color="#cbd5e1", height=2, corner_radius=0)
            axis_line.pack(fill="x", padx=30, pady=0)

            labels_area = ctk.CTkFrame(visual_frame, fg_color="transparent", height=30)
            labels_area.pack(fill="x", padx=20, pady=(5, 10))
            labels_area.pack_propagate(False)

            for idx in range(len(top_list)):
                lbl_wrapper = ctk.CTkFrame(labels_area, fg_color="transparent", width=70)
                lbl_wrapper.pack(side="left", fill="both", expand=True, padx=5)
                ctk.CTkLabel(lbl_wrapper, text=f"Top {idx+1}", font=("Segoe UI", 11, "bold"), text_color="#64748b").pack()


            # ================= VÙNG BÊN PHẢI: BẢNG VINH DANH SÁCH CHI TIẾT =================
            leaderboard_frame = ctk.CTkFrame(split_frame, fg_color="#ffffff", border_width=1, border_color="#f1f5f9", corner_radius=12, width=420)
            leaderboard_frame.pack(side="right", fill="both")
            leaderboard_frame.pack_propagate(False)

            ctk.CTkLabel(
                leaderboard_frame, text="🏆 THÔNG TIN CHI TIẾT ĐẦU SÁCH", 
                font=("Segoe UI", 12, "bold"), text_color="#1e293b"
            ).pack(anchor="w", padx=15, pady=15)

            # Tính tổng số lượt mượn của cả top để tính tỷ lệ % đóng góp thị phần
            tong_luot_top = sum([int(r.get("lan_muon", 0)) for r in top_list])
            if tong_luot_top == 0: tong_luot_top = 1

            for idx, row in enumerate(top_list):
                ten_sach = row.get("ten_sach", "N/A")
                lan_muon = int(row.get("lan_muon", 0))
                color = color_palette[idx] if idx < len(color_palette) else "#64748b"
                
                phan_tram = (lan_muon / tong_luot_top) * 180 # Quy đổi ra chiều dài thanh mini bar tối đa 180px

                # Cắt ngắn tên sách nếu quá dài
                if len(ten_sach) > 30: ten_sach = ten_sach[:28] + "..."

                # Tạo hàng thông tin
                item_row = ctk.CTkFrame(leaderboard_frame, fg_color="transparent")
                item_row.pack(fill="x", padx=15, pady=5)

                # Số huy hiệu thứ hạng tròn
                badge = ctk.CTkFrame(item_row, fg_color=color, width=22, height=22, corner_radius=11)
                badge.pack(side="left", padx=(0, 8))
                badge.pack_propagate(False)
                ctk.CTkLabel(badge, text=str(idx+1), font=("Segoe UI", 10, "bold"), text_color="white").pack(expand=True)

                # Tên sách hiển thị
                ctk.CTkLabel(item_row, text=ten_sach, font=("Segoe UI", 12, "semibold"), text_color="#334155", width=160, anchor="w").pack(side="left")

                # Thanh đo tỷ lệ mini-chart lồng vào trong bảng dữ liệu
                mini_bar_bg = ctk.CTkFrame(item_row, fg_color="#f1f5f9", width=180, height=12, corner_radius=6)
                mini_bar_bg.pack(side="left", padx=5)
                mini_bar_bg.pack_propagate(False)

                mini_bar_fill = ctk.CTkFrame(mini_bar_bg, fg_color=color, width=int(phan_tram), height=12, corner_radius=6)
                mini_bar_fill.pack(side="left")

        except Exception as e:
            print(f"Lỗi kết xuất giao diện đồ họa nâng cao: {e}")

    # ===== CÁC HÀM TRUY VẤN SQL KẾT NỐI ĐỒNG BỘ =====
    def _dem_tong_sach(self):
        try:
            query = "SELECT COUNT(*) as total FROM books"
            result = self.book_data.execute_query(query)
            return result[0]['total'] if result else 0
        except Exception:
            return 0    

    def _dem_phieu_theo_trang_thai(self, trang_thai):
        try:
            query = "SELECT COUNT(*) as total FROM muontra WHERE trang_thai = %s"
            result = self.muontra_data.execute_query(query, (trang_thai,))
            return result[0]['total'] if result else 0
        except Exception:
            return 0

    def back(self):
        self.app_manager.show_main_page()