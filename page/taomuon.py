import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from query.books import BookData
from query.muontra import MuonTraData
from query.taikhoan import AccountData


class TaoMuonPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        
        # Sử dụng các lớp dữ liệu kết nối MySQL
        self.book_data = BookData()
        self.muontra_data = MuonTraData()
        self.account_data = AccountData()

        self.config()
        self.view()
        self.load_sach_available()

    def config(self):
        self.master.title("Tạo phiếu mượn")
        self.master.geometry("600x550")
        self.master.resizable(True, True)

    def view(self):
        # Tiêu đề
        ctk.CTkLabel(
            self.master,
            text="Tạo phiếu mượn sách",
            font=("Segoe UI", 24, "bold"),
            text_color="#0066cc"
        ).pack(pady=20)

        # Form frame
        form_frame = ctk.CTkFrame(self.master, fg_color="white")
        form_frame.pack(fill="x", padx=20)

        # Mã phiếu (Tự động sinh mã)
        row1 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=8)
        ctk.CTkLabel(row1, text="Mã phiếu:", font=("Segoe UI", 12), width=100, anchor="w").pack(side="left")
        self.entry_maphieu = ctk.CTkEntry(row1, font=("Segoe UI", 12), corner_radius=8, fg_color="#e9ecef")
        self.entry_maphieu.pack(side="right", fill="x", expand=True)
        self.entry_maphieu.insert(0, self.muontra_data.generate_new_id())
        self.entry_maphieu.configure(state="disabled")

        # Username người mượn
        row2 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=8)
        ctk.CTkLabel(row2, text="Username:", font=("Segoe UI", 12), width=100, anchor="w").pack(side="left")
        self.entry_username = ctk.CTkEntry(row2, font=("Segoe UI", 12), corner_radius=8,
                                           placeholder_text="Nhập username người mượn...")
        self.entry_username.pack(side="right", fill="x", expand=True)

        # Ngày mượn (Mặc định lấy ngày hiện tại định dạng Việt Nam để hiển thị)
        row3 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row3.pack(fill="x", padx=20, pady=8)
        ctk.CTkLabel(row3, text="Ngày mượn:", font=("Segoe UI", 12), width=100, anchor="w").pack(side="left")
        self.entry_ngaymuon = ctk.CTkEntry(row3, font=("Segoe UI", 12), corner_radius=8, fg_color="#e9ecef")
        self.entry_ngaymuon.pack(side="right", fill="x", expand=True)
        self.entry_ngaymuon.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_ngaymuon.configure(state="disabled")

        # Danh sách sách có thể mượn
        ctk.CTkLabel(
            self.master,
            text="Chọn sách (chỉ hiển thị sách còn hàng):",
            font=("Segoe UI", 12, "bold"),
            anchor="w"
        ).pack(padx=20, pady=(15, 5), fill="x")

        table_frame = ctk.CTkFrame(self.master, corner_radius=10)
        table_frame.pack(expand=True, fill="both", padx=20, pady=5)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

        columns = ("ID", "Mã sách", "Tên sách", "Tác giả", "Số lượng còn")
        self.sach_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)

        col_configs = {
            "ID":           (50,  "center"),
            "Mã sách":      (100, "center"),
            "Tên sách":     (200, "w"),
            "Tác giả":      (120, "center"),
            "Số lượng còn": (100, "center"),
        }
        for col, (width, anchor) in col_configs.items():
            self.sach_tree.heading(col, text=col)
            self.sach_tree.column(col, width=width, anchor=anchor)

        scrollbar = ctk.CTkScrollbar(table_frame, command=self.sach_tree.yview)
        self.sach_tree.configure(yscrollcommand=scrollbar.set)
        self.sach_tree.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Nút bấm chức năng
        btn_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(
            btn_frame, text="Tạo phiếu mượn",
            fg_color="#28a745", hover_color="#218838",
            command=self.save
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame, text="Hủy bỏ",
            fg_color="#6c757d", hover_color="#5a6268",
            command=self.cancel
        ).pack(side="left", padx=10)

    # ===== LOGIC XỬ LÝ =====

    def load_sach_available(self):
        """Chỉ hiển thị những đầu sách có số lượng lớn hơn 0"""
        try:
            books = self.book_data.get_all()
            for row in books:
                so_luong_ton = int(row[5])
                if so_luong_ton > 0:
                    self.sach_tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[5]))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách sách: {str(e)}")

    def save(self):
        """Xử lý tạo phiếu mượn sách và chuẩn hóa ngày tháng lưu vào MySQL"""
        username = self.entry_username.get().strip()
        
        # Kiểm tra trống tường minh
        if username == "":
            messagebox.showerror("Lỗi", "Vui lòng nhập username người mượn")
            return

        # Kiểm tra sự tồn tại của tài khoản
        exists_account = self.account_data.check_exists(username)
        if exists_account == False:
            messagebox.showerror("Lỗi", f"Username '{username}' không tồn tại")
            return

        # Kiểm tra xem đã chọn dòng sách nào trên bảng chưa
        selected = self.sach_tree.selection()
        if len(selected) == 0:
            messagebox.showerror("Lỗi", "Vui lòng chọn sách cần mượn")
            return
        
        values = self.sach_tree.item(selected[0], "values")
        ma_sach = values[1]
        
        # Kiểm tra xem tài khoản này có đang mượn cuốn sách này mà chưa trả không
        is_borrowing = self.muontra_data.Sach_Dang_Muon(username, ma_sach)
        if is_borrowing == True:
            messagebox.showerror("Lỗi", f"'{username}' đang mượn sách này rồi, chưa trả!")
            return

        ma_phieu = self.entry_maphieu.get()
        
        # CƠ CHẾ CHẶN LỖI 1062 DUPLICATE ENTRY TRƯỚC KHI INSERT
        query_check_id = "SELECT COUNT(*) as total FROM muontra WHERE ma_phieu = %s"
        check_result = self.muontra_data.thuc_thi_query(query_check_id, (ma_phieu,))
        
        if check_result:
            total_matches = check_result[0]['total']
            if total_matches > 0:
                messagebox.showerror("Lỗi thêm", f"Mã phiếu '{ma_phieu}' đã tồn tại dưới Database! Vui lòng kiểm tra lại bộ sinh mã.")
                return

        ngay_muon_raw = self.entry_ngaymuon.get()

        try:
            # 1. Chuẩn hóa ngày mượn cho MySQL (YYYY-MM-DD)
            ngay_muon_date = datetime.strptime(ngay_muon_raw, "%d/%m/%Y")
            ngay_muon_chuan_mysql = ngay_muon_date.strftime("%Y-%m-%d")

            # 2. TỰ ĐỘNG TÍNH HẠN TRẢ: Cộng thêm 14 ngày
            han_tra_date = ngay_muon_date + timedelta(days=14)
            han_tra_chuan_mysql = han_tra_date.strftime("%Y-%m-%d")

            # 3. Ghi phiếu mượn xuống database bao gồm cả han_tra và tien_phat mặc định bằng 0
            self.muontra_data.create([
                ma_phieu, 
                username, 
                ma_sach, 
                ngay_muon_chuan_mysql, 
                han_tra_chuan_mysql, 
                None,  
                0,     
                "dang_muon"
            ])

            # Khấu trừ số lượng tồn kho của sách đi 1 đơn vị
            self.book_data.update_quantity(ma_sach, delta=-1)

            messagebox.showinfo("Thành công", f"Đã tạo phiếu mượn '{ma_phieu}' với hạn trả là {han_tra_date.strftime('%d/%m/%Y')}")
            self.app_manager.show_muontra_page()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo phiếu: {str(e)}")

    def cancel(self):
        self.app_manager.show_muontra_page()