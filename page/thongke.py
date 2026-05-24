import customtkinter as ctk
from query.muontra import MuonTraData
from query.books import BookData

class ThongKePage:
    def __init__(self, master, app_manager):
        """Khởi tạo giao diện thống kê."""
        self.master = master
        self.app_manager = app_manager
        self.muontra_data = MuonTraData()
        self.book_data = BookData()
        
        self.config_window()
        self.render_view()

    def config_window(self):
        """Thiết lập cấu hình cửa sổ hiển thị."""
        self.master.title("📊 Hệ Thống Thống Kê & Báo Cáo")
        self.master.geometry("950x650")
        ctk.set_appearance_mode("light")

    def render_view(self):
        """Xây dựng khung giao diện chính."""
        # 1. Tiêu đề trang
        ctk.CTkLabel(
            self.master,
            text="📊 THỐNG KÊ HOẠT ĐỘNG THƯ VIỆN",
            font=("Segoe UI", 24, "bold"),
            text_color="#1a365d"
        ).pack(pady=20)

        # 2. Khung chứa các thẻ số liệu
        card_container = ctk.CTkFrame(self.master, fg_color="transparent")
        card_container.pack(pady=10, padx=30, fill="x")

        # 3. Lấy dữ liệu và tạo thẻ hiển thị
        total_books = self.get_total_books_count()
        self.create_statistic_card(card_container, "📚 Tổng đầu sách", str(total_books), "#3498db")

        returned_books = self.get_borrow_records_by_status("da_tra")
        self.create_statistic_card(card_container, "✅ Phiếu đã trả", str(returned_books), "#27ae60")

        borrowing_books = self.get_borrow_records_by_status("dang_muon")
        self.create_statistic_card(card_container, "📖 Phiếu đang mượn", str(borrowing_books), "#e74c3c")

        # 4. Khung chứa biểu đồ
        chart_section = ctk.CTkFrame(self.master, fg_color="#f8fafc", border_width=1, border_color="#e2e8f0", corner_radius=15)
        chart_section.pack(fill="both", expand=True, padx=30, pady=(20, 15))

        self.chart_body = ctk.CTkFrame(chart_section, fg_color="transparent")
        self.chart_body.pack(fill="both", expand=True, padx=20, pady=10)

        self.draw_statistics_chart()

        # 5. Nút điều hướng
        ctk.CTkButton(
            self.master,
            text="← Quay Lại Menu Chính",
            font=("Segoe UI", 13, "bold"),
            fg_color="#64748b",
            hover_color="#475569",
            width=180,
            height=40,
            command=self.back_to_menu
        ).pack(pady=15)

    def create_statistic_card(self, parent, title, value, color):
        """Tạo thẻ hiển thị thông số thống kê."""
        card = ctk.CTkFrame(parent, fg_color=color, corner_radius=12)
        card.pack(side="left", padx=10, fill="both", expand=True)

        ctk.CTkLabel(card, text=title, font=("Segoe UI", 13, "bold"), text_color="white").pack(pady=(15, 5))
        ctk.CTkLabel(card, text=value, font=("Segoe UI", 32, "bold"), text_color="white").pack(pady=(5, 15))

    def draw_statistics_chart(self):
        """Vẽ biểu đồ top sách mượn nhiều nhất."""
        try:
            query = """
                SELECT m.ma_sach, b.ten_sach, COUNT(m.ma_sach) as borrow_frequency
                FROM muontra m
                JOIN books b ON m.ma_sach = b.ma_sach
                GROUP BY m.ma_sach, b.ten_sach
                ORDER BY borrow_frequency DESC
                LIMIT 5
            """
            top_books_data = self.muontra_data.execute_query(query)

            # Kiểm tra dữ liệu trả về
            if top_books_data == None or len(top_books_data) == 0:
                ctk.CTkLabel(self.chart_body, text="❌ Chưa có dữ liệu mượn trả.", font=("Segoe UI", 13, "italic"), text_color="gray").pack(pady=80)
                return

            max_frequency = int(top_books_data[0].get("borrow_frequency", 1))
            if max_frequency == 0:
                max_frequency = 1
            
        except Exception as error:
            print(f"Lỗi hiển thị biểu đồ thống kê: {error}")

    def get_total_books_count(self):
        """Lấy tổng số lượng sách từ cơ sở dữ liệu."""
        try:
            result = self.book_data.execute_query("SELECT COUNT(*) as total_count FROM books")
            
            if result is not None and len(result) > 0:
                row = result[0]
                total = row['total_count']
                return total
            else:
                return 0
                
        except Exception as error:
            print(f"Lỗi khi đếm tổng số sách: {error}")
            return 0    

    def get_borrow_records_by_status(self, status):
        """Lấy số lượng phiếu mượn theo trạng thái."""
        try:
            result = self.muontra_data.execute_query(
                "SELECT COUNT(*) as total_records FROM muontra WHERE trang_thai = %s", (status,)
            )
            
            if result is not None and len(result) > 0:
                row = result[0]
                total = row['total_records']
                return total
            else:
                return 0
                
        except Exception as error:
            print(f"Lỗi khi đếm số phiếu mượn: {error}")
            return 0

    def back_to_menu(self):
        """Trở về menu chính."""
        self.app_manager.show_main_page()