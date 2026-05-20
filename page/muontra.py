import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from query.muontra import MuonTraData
from query.books import BookData  # Cần import để cập nhật số lượng sách khi duyệt
from common.theme import Colors, Fonts, Spacing


class MuonTraPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.muontra_data = MuonTraData()
        self.book_data = BookData()  # Khởi tạo lớp dữ liệu sách
        self.config()
        self.view()
        self.load_phieu()

    def config(self):
        self.master.title("🔄 Quản Lý Mượn Trả Sách")
        self.master.geometry("1000x650")
        self.master.configure(fg_color=Colors.BG_MAIN)
        ctk.set_appearance_mode("light")

    def view(self):
        main_frame = ctk.CTkFrame(self.master, fg_color=Colors.BG_MAIN)
        main_frame.pack(fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(main_frame, fg_color=Colors.PRIMARY, corner_radius=0)
        header.pack(fill="x")
        
        title_text = "🔄 LỊCH SỬ MƯỢN TRẢ SÁCH" if self.app_manager.current_role == "Sinh viên" else "🔄 QUẢN LÝ MƯỢN TRẢ SÁCH"
        ctk.CTkLabel(header, text=title_text, font=Fonts.HEADER, text_color=Colors.WHITE).pack(pady=Spacing.MD)

        # Table Frame
        table_frame = ctk.CTkFrame(main_frame, fg_color=Colors.BG_SECONDARY)
        table_frame.pack(expand=True, fill="both", padx=20, pady=15)

        # Style Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background=Colors.BG_SECONDARY, 
                        foreground=Colors.TEXT_PRIMARY,
                        fieldbackground=Colors.BG_SECONDARY,
                        rowheight=35, 
                        font=Fonts.REGULAR, 
                        borderwidth=0)
        style.configure("Treeview.Heading", background=Colors.PRIMARY, foreground=Colors.WHITE, font=Fonts.SMALL_BOLD, borderwidth=0)
        style.map("Treeview", background=[('selected', Colors.BG_HOVER)], foreground=[('selected', Colors.PRIMARY)])

        # Định nghĩa các cột
        columns = ("STT", "Mã Phiếu", "Người Mượn", "Mã Sách", "Ngày Mượn", "Hạn Trả", "Tiền Phạt", "Trạng Thái")
        self.phieu_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.phieu_tree.heading(col, text=col)
            if col in ["STT", "Mã Phiếu", "Mã Sách", "Ngày Mượn", "Hạn Trả", "Trạng Thái"]:
                self.phieu_tree.column(col, width=110, anchor="center")
            elif col == "Tiền Phạt":
                self.phieu_tree.column(col, width=100, anchor="e")
            else:
                self.phieu_tree.column(col, width=140, anchor="w")

        # Cấu hình màu sắc nhãn trạng thái (Tags)
        self.phieu_tree.tag_configure("cho_duyet", foreground="#e67e22", font=Fonts.REGULAR) # Màu cam chờ duyệt
        self.phieu_tree.tag_configure("dang_muon", foreground="#2980b9", font=Fonts.REGULAR) # Màu xanh đang mượn
        self.phieu_tree.tag_configure("da_tra", foreground="#27ae60", font=Fonts.REGULAR)   # Màu xanh lá đã trả

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.phieu_tree.yview)
        self.phieu_tree.configure(yscrollcommand=scrollbar.set)
        self.phieu_tree.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Action Frame Buttons
        action_frame = ctk.CTkFrame(main_frame, fg_color=Colors.BG_SECONDARY)
        action_frame.pack(fill="x", padx=Spacing.LG, pady=Spacing.LG)

        self.status_label = ctk.CTkLabel(action_frame, text="Sẵn sàng", font=Fonts.SMALL, text_color=Colors.TEXT_SECONDARY)
        self.status_label.pack(side="left", padx=Spacing.MD)

        btns_container = ctk.CTkFrame(action_frame, fg_color="transparent")
        btns_container.pack(side="right", padx=Spacing.MD, pady=Spacing.SM)

        current_role = str(self.app_manager.current_role).strip()

        # Phân quyền hiển thị nút bấm điều khiển
        if current_role in ["Admin", "Quản lý", "Thủ thư"]:
            # Nút Phê duyệt yêu cầu mượn sách từ sinh viên gửi lên
            ctk.CTkButton(btns_container, text="✅ Duyệt Mượn", fg_color=Colors.SUCCESS, font=Fonts.SMALL_BOLD, command=self.duyet_yeu_cau).pack(side="left", padx=5)
            # Nút Tạo phiếu trực tiếp (Cho trường hợp mượn trực tiếp tại quầy)
            ctk.CTkButton(btns_container, text="➕ Tạo Phiếu", fg_color=Colors.PRIMARY, font=Fonts.SMALL_BOLD, command=self.tao_phieu).pack(side="left", padx=5)
            # Nút Nhận sách trả
            ctk.CTkButton(btns_container, text="🔄 Xác Nhận Trả", fg_color=Colors.INFO, font=Fonts.SMALL_BOLD, command=self.xac_nhan_tra).pack(side="left", padx=5)
        else:
            # Nếu là Sinh viên thì không hiện các nút xử lý trên, có thể thêm nhãn ghi chú nhỏ
            ctk.CTkLabel(btns_container, text="📌 Hãy mang theo thẻ Sinh viên khi đến nhận sách mang về.", font=Fonts.SMALL, text_color="gray").pack(side="left", padx=10)

        # Nút Quay lại
        ctk.CTkButton(btns_container, text="← Quay Lại", fg_color=Colors.BORDER, text_color=Colors.TEXT_PRIMARY, font=Fonts.SMALL_BOLD, command=self.back).pack(side="left", padx=5)

    def load_phieu(self):
        """Tải danh sách phiếu mượn có áp dụng bộ lọc phân quyền người dùng"""
        for item in self.phieu_tree.get_children():
            self.phieu_tree.delete(item)

        try:
            all_phieu = self.muontra_data.get_all()
            current_user = self.app_manager.current_user
            current_role = self.app_manager.current_role

            count = 0
            for row in all_phieu:
                # Ép dạng cấu trúc dữ liệu tuple/list từ DB MySQL
                ma_phieu = row[1]
                username = row[2]
                ma_sach = row[3]
                ngay_muon = row[4] if row[4] else "Đang chờ..."
                han_tra = row[5] if row[5] else "Chờ phê duyệt"
                tien_phat = f"{int(row[6]):,}" if row[6] else "0"
                trang_thai_raw = row[7]

                # ─── BỘ LỌC BẢO MẬT: Sinh viên chỉ xem được phiếu của chính mình ───
                if current_role == "Sinh viên" and username != current_user:
                    continue

                count += 1
                # Định dạng chuỗi hiển thị trạng thái thân thiện hơn
                if trang_thai_raw == "cho_duyet":
                    trang_thai_display = "⏳ Chờ Duyệt"
                    tag = "cho_duyet"
                elif trang_thai_raw == "dang_muon":
                    trang_thai_display = "📖 Đang Mượn"
                    tag = "dang_muon"
                else:
                    trang_thai_display = "✅ Đã Trả"
                    tag = "da_tra"

                self.phieu_tree.insert("", "end", values=(count, ma_phieu, username, ma_sach, ngay_muon, han_tra, tien_phat, trang_thai_display), tags=(tag,))
            
            self.status_label.configure(text=f"Tổng số: {count} bản ghi")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu phiếu mượn: {str(e)}")

    def duyet_yeu_cau(self):
        """Thủ thư phê duyệt yêu cầu của sinh viên"""
        selected = self.phieu_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một yêu cầu mượn cần duyệt từ bảng!")
            return

        values = self.phieu_tree.item(selected[0], "values")
        ma_phieu = values[1]
        trang_thai_hien_tai = values[7]
        ma_sach = values[3]

        if "Chờ Duyệt" not in trang_thai_hien_tai:
            messagebox.showerror("Lỗi", "Phiếu này đã được duyệt hoặc đã trả xong, không thể duyệt lại!")
            return

        if messagebox.askyesno("Xác nhận phê duyệt", f"Phê duyệt cấp sách cho mã phiếu {ma_phieu}?"):
            try:
                # Tính toán thời gian thực: Mượn hôm nay, hạn trả mặc định sau 14 ngày
                now = datetime.now()
                ngay_muon_str = now.strftime("%Y-%m-%d")
                han_tra_str = (now + timedelta(days=14)).strftime("%Y-%m-%d")

                # 1. Gọi hàm cập nhật MySQL đổi trạng thái sang 'dang_muon'
                self.muontra_data.approve_borrow_request(ma_phieu, ngay_muon_str, han_tra_str)

                # 2. Khấu trừ tự động bớt 1 cuốn sách trong kho dữ liệu sách
                self.book_data.update_quantity(ma_sach, delta=-1)

                messagebox.showinfo("Thành công", f"Đã duyệt thành công phiếu {ma_phieu}!\nSách đã chính thức xuất kho.")
                self.load_phieu()
            except Exception as e:
                messagebox.showerror("Lỗi hệ thống", f"Không thể duyệt phiếu: {str(e)}")

    def tao_phieu(self):
        """Chuyển hướng sang giao diện tạo phiếu mượn (Dành cho Thủ thư làm việc trực tiếp tại quầy)"""
        self.app_manager.show_taomuon_page()

    def xac_nhan_tra(self):
        """Thủ thư xác nhận sinh viên trả sách, tự động cập nhật ngày trả và trả số lượng về kho"""
        selected = self.phieu_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phiếu mượn cần xác nhận trả từ danh sách!")
            return

        # Lấy thông tin dòng được chọn
        values = self.phieu_tree.item(selected[0], "values")
        ma_phieu = values[1]
        ma_sach = values[3]
        trang_thai_hien_tai = values[7]

        # Kiểm tra xem sách đã được trả từ trước chưa
        if "Đã Trả" in trang_thai_hien_tai:
            messagebox.showinfo("Thông báo", f"Phiếu mượn '{ma_phieu}' này đã được xác nhận trả từ trước!")
            return
            
        if "Chờ Duyệt" in trang_thai_hien_tai:
            messagebox.showwarning("Cảnh báo", "Phiếu này chưa được duyệt cấp sách, không thể thực hiện chức năng trả sách!")
            return

        if messagebox.askyesno("Xác nhận nhận sách", f"Xác nhận nhận lại sách cho mã phiếu '{ma_phieu}'?"):
            try:
                now = datetime.now()
                ngay_tra_str = now.strftime("%Y-%m-%d")
                
                # 1. Đọc thông tin phiếu từ database để kiểm tra trễ hạn và tính tiền phạt
                query_check = "SELECT han_tra FROM muontra WHERE ma_phieu = %s"
                res = self.muontra_data.execute_query(query_check, (ma_phieu,))
                
                tien_phat_chuan = 0
                if res and len(res) > 0:
                    han_tra_dt = res[0].get("han_tra")
                    
                    # Nếu có hạn trả và ngày trả thực tế vượt quá hạn trả
                    if han_tra_dt:
                        if type(han_tra_dt).__name__ == "str":
                            han_tra_dt = datetime.strptime(han_tra_dt[:10], "%Y-%m-%d").date()
                        elif type(han_tra_dt).__name__ == "datetime":
                            han_tra_dt = han_tra_dt.date()
                            
                        if now.date() > han_tra_dt:
                            so_ngay_tre = (now.date() - han_tra_dt).days
                            tien_phat_chuan = so_ngay_tre * 2000 # Phạt 2,000đ/ngày trễ

                # 2. Cập nhật trạng thái phiếu mượn thành 'da_tra' trong MySQL
                data_update = {
                    "ngay_tra": ngay_tra_str,
                    "tien_phat": tien_phat_chuan,
                    "trang_thai": "da_tra"
                }
                self.muontra_data.update("ma_phieu", ma_phieu, data_update)

                # 3. Hoàn trả số lượng sách tồn kho (+1 cuốn lại vào kho sách)
                self.book_data.update_quantity(ma_sach, delta=1)

                # Hiển thị thông báo kết quả trả sách
                if tien_phat_chuan > 0:
                    messagebox.showwarning("Thành công (Có phạt)", f"Đã nhận lại sách thành công cho phiếu {ma_phieu}!\n⚠️ Sinh viên trả trễ hạn, số tiền phạt cần thu: {tien_phat_chuan:,}đ")
                else:
                    messagebox.showinfo("Thành công", f"Đã xác nhận trả sách thành công cho phiếu {ma_phieu}.\nSách đã được hoàn trả về kho!")
                
                # Tải lại bảng dữ liệu
                self.load_phieu()
                
            except Exception as e:
                messagebox.showerror("Lỗi hệ thống", f"Không thể xử lý trả sách: {str(e)}")

    def back(self):
        self.app_manager.show_main_page()