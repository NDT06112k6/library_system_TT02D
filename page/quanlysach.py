import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk
from query.books import BookData
from query.muontra import MuonTraData  
from common.theme import Colors, Fonts, Spacing
import threading
#Q

class QuanLySachPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.book_data = BookData()
        self.muontra_data = MuonTraData()  
        self._is_active = True
        self.config()
        self.view()
        self.Tai_Sach()

    def _safe_after(self, delay, func):
        """Gửi after chỉ khi page vẫn active và master còn tồn tại"""
        if not self._is_active:
            return None
        try:
            if self.master.winfo_exists():
                return self.master.after(delay, func)
        except Exception:
            pass
        return None

    def config(self):
        self.master.title("📚 Quản Lý Sách")
        self.master.geometry("900x650")
        self.master.configure(fg_color=Colors.BG_MAIN)
        ctk.set_appearance_mode("light")

    def view(self):
        main_frame = ctk.CTkFrame(self.master, fg_color=Colors.BG_MAIN)
        main_frame.pack(fill="both", expand=True)

        header = ctk.CTkFrame(main_frame, fg_color=Colors.PRIMARY, corner_radius=0)
        header.pack(fill="x")
        
        # Đổi tiêu đề động theo vai trò đăng nhập để tăng trải nghiệm người dùng
        if self.app_manager.current_role == "Độc giả":
            page_title = "📚 KHO SÁCH THƯ VIỆN"
        else:
            page_title = "📚 QUẢN LÝ KHO SÁCH"

        ctk.CTkLabel(
            header,
            text=page_title,
            font=Fonts.HEADER,
            text_color=Colors.WHITE
        ).pack(pady=Spacing.MD)

        search_frame = ctk.CTkFrame(main_frame, fg_color=Colors.BG_SECONDARY)
        search_frame.pack(fill="x", padx=Spacing.LG, pady=Spacing.LG)

        left_search = ctk.CTkFrame(search_frame, fg_color="transparent")
        left_search.pack(side="left", fill="x", expand=True, padx=Spacing.MD, pady=Spacing.MD)

        self.entry_search = ctk.CTkEntry(
            left_search,
            placeholder_text="Tìm theo mã sách, tên sách, tác giả, thể loại...",
            height=35,
            font=Fonts.REGULAR,
            fg_color=Colors.BG_MAIN,
            border_color=Colors.BORDER
        )
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Thanh tìm kiếm tự động lọc mỗi khi bạn gõ phím (
        self.entry_search.bind("<KeyRelease>", lambda e: self.Tim_Kiem_Sach())

        ctk.CTkButton(left_search, text="Tìm", width=70, height=35, font=Fonts.SMALL_BOLD, command=self.Tim_Kiem_Sach).pack(side="left", padx=2)
        ctk.CTkButton(left_search, text="Reset", width=70, height=35, font=Fonts.SMALL_BOLD, fg_color=Colors.BORDER, text_color=Colors.TEXT_PRIMARY, hover_color=Colors.BORDER_DARK, command=self.Tai_Sach).pack(side="left", padx=2)

        right_filter = ctk.CTkFrame(search_frame, fg_color="transparent")
        right_filter.pack(side="right", padx=Spacing.MD)

        all_books = self.book_data.get_all()

        temp_categories = []
        for b in all_books:
            if len(b) > 4:  
                temp_categories.append(b[4])  
        
        unique_categories = list(set(temp_categories))
        categories = sorted(unique_categories)
        categories.insert(0, "Tất cả thể loại")

        self.filter_category = ctk.CTkOptionMenu(
            right_filter,
            values=categories,
            command=self.Loc_Theo_The_Loai,
            width=150,
            height=35,
            font=Fonts.SMALL,
            fg_color=Colors.BG_MAIN,
            button_color=Colors.PRIMARY,
            text_color=Colors.TEXT_PRIMARY
        )
        self.filter_category.pack(side="right")
        ctk.CTkLabel(right_filter, text="📂 Thể loại:", font=Fonts.SMALL_BOLD).pack(side="right", padx=5)

        table_frame = ctk.CTkFrame(main_frame, fg_color=Colors.BG_SECONDARY)
        table_frame.pack(expand=True, fill="both", padx=20, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background=Colors.BG_SECONDARY, 
                        foreground=Colors.TEXT_PRIMARY,
                        fieldbackground=Colors.BG_SECONDARY,
                        rowheight=35, 
                        font=Fonts.REGULAR, 
                        borderwidth=0)
        style.configure("Treeview.Heading", 
                        background=Colors.PRIMARY, 
                        foreground=Colors.WHITE, 
                        font=Fonts.SMALL_BOLD, 
                        borderwidth=0)
        style.map("Treeview", background=[('selected', Colors.BG_HOVER)], foreground=[('selected', Colors.PRIMARY)])

        columns = ("STT", "Mã sách", "Tên sách", "Tác giả", "Thể loại", "Số lượng", "Giá")
        self.book_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.book_tree.heading("STT", text="STT")
        self.book_tree.heading("Mã sách", text="Mã Sách")
        self.book_tree.heading("Tên sách", text="Tên Sách")
        self.book_tree.heading("Tác giả", text="Tác Giả")
        self.book_tree.heading("Thể loại", text="Thể Loại")
        self.book_tree.heading("Số lượng", text="Số Lượng")
        self.book_tree.heading("Giá", text="Giá Bán")

        self.book_tree.column("STT", width=50, minwidth=50, anchor="center")
        self.book_tree.column("Mã sách", width=100, minwidth=100, anchor="center")
        self.book_tree.column("Tên sách", width=250, minwidth=200, anchor="w")
        self.book_tree.column("Tác giả", width=150, minwidth=120, anchor="w")
        self.book_tree.column("Thể loại", width=120, minwidth=100, anchor="center")
        self.book_tree.column("Số lượng", width=90, minwidth=80, anchor="center")
        self.book_tree.column("Giá", width=100, minwidth=90, anchor="e")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.book_tree.yview)
        self.book_tree.configure(yscrollcommand=scrollbar.set)

        self.book_tree.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        action_frame = ctk.CTkFrame(main_frame, fg_color=Colors.BG_SECONDARY)
        action_frame.pack(fill="x", padx=Spacing.LG, pady=Spacing.LG)

        self.status_label = ctk.CTkLabel(action_frame, text="Sẵn sàng", font=Fonts.SMALL, text_color=Colors.TEXT_SECONDARY)
        self.status_label.pack(side="left", padx=Spacing.MD)

        btns_container = ctk.CTkFrame(action_frame, fg_color="transparent")
        btns_container.pack(side="right", padx=Spacing.MD, pady=Spacing.SM)

        #  PHÂN QUYỀN NÚT CHỨC NĂNG 
        current_role = str(self.app_manager.current_role).strip()

        if current_role in ["Admin", "Quản lý", "Thủ thư"]:
            # Hiển thị các nút Quản trị nếu là nhân viên quản lý
            ctk.CTkButton(btns_container, text="Thêm Mới", fg_color=Colors.SUCCESS, font=Fonts.SMALL_BOLD, command=self.them_sach).pack(side="left", padx=5)
            ctk.CTkButton(btns_container, text="Sửa", fg_color=Colors.INFO, font=Fonts.SMALL_BOLD, command=self.sua_sach).pack(side="left", padx=5)
            ctk.CTkButton(btns_container, text="Xóa", fg_color=Colors.ERROR, font=Fonts.SMALL_BOLD, command=self.xoa_sach).pack(side="left", padx=5)
            ctk.CTkButton(btns_container, text="Xuất CSV", fg_color="#8B5CF6", font=Fonts.SMALL_BOLD, command=self.xuat_du_lieu_csv).pack(side="left", padx=5)
            ctk.CTkButton(btns_container, text="Nhập CSV", fg_color="#8B5CF6", font=Fonts.SMALL_BOLD, command=self.nhap_du_lieu_csv).pack(side="left", padx=5)
        else:
            # TỰ ĐỘNG THAY THẾ: Nút đăng ký mượn dành riêng cho Độc giả
            ctk.CTkButton(
                btns_container, 
                text="📖 Đăng ký mượn", 
                fg_color="#28a745", 
                hover_color="#218838", 
                font=Fonts.SMALL_BOLD, 
                command=self.gui_yeu_cau_muon
            ).pack(side="left", padx=5)

        # Nút Quay lại dùng chung cho tất cả mọi người
        ctk.CTkButton(btns_container, text="← Quay Lại", fg_color=Colors.BORDER, text_color=Colors.TEXT_PRIMARY, font=Fonts.SMALL_BOLD, command=self.back).pack(side="left", padx=5) 

    # ─── LOGIC YÊU CẦU MƯỢN SÁCH DÀNH CHO ĐỘC GIẢ ─── 
    def gui_yeu_cau_muon(self):
        """Xử lý gửi yêu cầu đặt sách chờ phê duyệt dưới MySQL Docker"""
        selected = self.book_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cuốn sách bạn muốn đăng ký mượn!")
            return
        
        values = self.book_tree.item(selected[0], "values")
        ma_sach = values[1]
        ten_sach = values[2]
        so_luong_con = int(values[5])

        # 1. Kiểm tra tồn kho thời gian thực
        if so_luong_con <= 0:
            messagebox.showerror("Lỗi", f"Sách '{ten_sach}' hiện tại đã hết hàng trong kho!")
            return

        # 2. Kiểm tra xem Độc giả này có đang gửi yêu cầu hoặc đang mượn cuốn này rồi không
        username_hien_tai = self.app_manager.current_user
        if self.muontra_data.Sach_Dang_Muon(username_hien_tai, ma_sach):
            messagebox.showerror("Lỗi", "Bạn đang mượn hoặc có yêu cầu chờ duyệt với cuốn sách này rồi!")
            return

        # 3. Tiến hành gửi yêu cầu phê duyệt lên hệ thống
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn gửi yêu cầu mượn cuốn sách:\n'{ten_sach}'?"):
            try:
                self.muontra_data.Tao_Yeu_Cau_Muon(username_hien_tai, ma_sach)
                messagebox.showinfo("Thành công", "Gửi yêu cầu thành công!\nVui lòng đến quầy thư viện để nhận sách và duyệt phiếu.") 
                self.Tai_Sach()
            except Exception as e:
                messagebox.showerror("Lỗi hệ thống", f"Không thể gửi yêu cầu mượn: {str(e)}") 

    def Tai_Sach(self): 
        self.entry_search.delete(0, "end")
        self.filter_category.set("Tất cả thể loại")
        self._Tong_Tai_Khoan(self._Doc_Tat_Ca_Sach())

    def Loc_Theo_The_Loai(self, category):
        all_books = self._Doc_Tat_Ca_Sach()
        if category == "Tất cả thể loại":
            self._Tong_Tai_Khoan(all_books)
        else:
            filtered = [b for b in all_books if len(b) > 4 and b[4] == category]
            self._Tong_Tai_Khoan(filtered)

    def Tim_Kiem_Sach(self): 
        keyword = self.entry_search.get().strip()
        if not keyword:
            self.Tai_Sach()
            return
        try:
            result = self.book_data.search_books(keyword)
            self._Tong_Tai_Khoan(result)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {str(e)}")

    def them_sach(self):
        self.app_manager.Hien_Thi_Trang_Them_Sach()

    def sua_sach(self):
        selected = self.book_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách cần sửa")
            return
        values = self.book_tree.item(selected[0], "values")
        self.app_manager.Hien_Thi_Trang_Sua_Sach(values[1])

    def xoa_sach(self):
        selected = self.book_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách cần xóa")
            return
        values = self.book_tree.item(selected[0], "values")
        ma_sach = values[1]
        ten_sach = values[2]

        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa sách '{ten_sach}'?"):
            return
        try:
            self._Xoa_Sach_Khoi_File(ma_sach)
            self.Tai_Sach()
            messagebox.showinfo("Thành công", "Đã xóa sách thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa: {str(e)}")

    def back(self):
        self._is_active = False
        self.app_manager.Hien_Thi_Trang_Chinh()

    def _Doc_Tat_Ca_Sach(self): 
        try:
            return self.book_data.get_all() 
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc dữ liệu: {str(e)}")
            return []

    def _Tong_Tai_Khoan(self, rows):
        """Hiển thị dữ liệu sách lên Treeview tự động nhận diện kiểu dữ liệu"""
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        
        for idx, row in enumerate(rows, 1):
            try:
                if isinstance(row, dict):
                    # Xử lý lấy giá trị từ Dictionary một cách an toàn
                    if "gia" in row:
                        gia_raw = row["gia"]
                    elif "giaban" in row:
                        gia_raw = row["giaban"]
                    else:
                        gia_raw = 0
                    
                    # Định dạng tiền tệ
                    gia = "{:,}".format(int(float(gia_raw)))
                    
                    # Lấy mã sách
                    if "ma_sach" in row:
                        ma_sach = row["ma_sach"]
                    else:
                        ma_sach = row.get("masach", "N/A")

                    # Lấy tên sách
                    if "ten_sach" in row:
                        ten_sach = row["ten_sach"]
                    else:
                        ten_sach = row.get("tensach", "N/A")
                    
                    # Các trường còn lại tương tự
                    tac_gia = row.get("tac_gia", "N/A")
                    the_loai = row.get("the_loai", "N/A")
                    so_luong = row.get("so_luong", 0)

                    self.book_tree.insert("", "end", values=(idx, ma_sach, ten_sach, tac_gia, the_loai, so_luong, gia))
                else:
                    if len(row) >= 7:
                        if row[6]:
                            gia = "{:,}".format(int(float(row[6])))
                        else:
                            gia = "0"
                        self.book_tree.insert("", "end", values=(idx, row[1], row[2], row[3], row[4], row[5], gia))
                    else:
                        if row[5]:
                            gia = "{:,}".format(int(float(row[5])))
                        else:
                            gia = "0"
                        self.book_tree.insert("", "end", values=(idx, row[0], row[1], row[2], row[3], row[4], gia))
            except Exception as e:
                print(f"Lỗi hiển thị hàng số {idx}: {e}")
                continue
                
        self.status_label.configure(text=f"Tổng: {len(rows)} sách")

    def _Xoa_Sach_Khoi_File(self, ma_sach_xoa): 
        try:
            from query.muontra import MuonTraData
            muon_tra_data = MuonTraData()
            query = "DELETE FROM muontra WHERE ma_sach = %s"
            muon_tra_data.thuc_thi_query(query, (ma_sach_xoa,))
            self.book_data.delete("ma_sach", ma_sach_xoa)
            return True
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa: {str(e)}")
            return False

    def xuat_du_lieu_csv(self):
        """Hàm xuất dữ liệu sách sang file CSV"""
        def do_export():
            try:
                ten_file = self.book_data.xuat_csv()
                self._safe_after(0, lambda: messagebox.showinfo("Thành công", f"Đã xuất file: {ten_file}"))
            except Exception as loi:
                self._safe_after(0, lambda: messagebox.showerror("Lỗi", f"Không thể xuất file: {str(loi)}"))
        
        thread = threading.Thread(target=do_export)
        thread.daemon = True
        thread.start()

    def nhap_du_lieu_csv(self):
        """Nhập dữ liệu từ file CSV (Sửa lỗi treo giao diện và hoàn thiện luồng Threading)"""
        duong_dan = filedialog.askopenfilename(
            title="Chọn file CSV để nhập",
            filetypes=[("Tệp CSV", "*.csv"), ("Tất cả tệp", "*.*")]
        )
        
        if not duong_dan:
            return
        
        xac_nhan = messagebox.askyesno(
            "Xác nhận",
            "Bạn có muốn xóa toàn bộ sách cũ trước khi nhập CSV mới không?\n(Nếu không -> dữ liệu mới sẽ được thêm nối tiếp vào bảng)"
        )
    
        def do_import(path, clear_old):
            try:
                if clear_old:
                    if self.book_data.connect():
                        con_tro = self.book_data.connection.cursor()
                        con_tro.execute("DELETE FROM books")
                        self.book_data.connection.commit()
                        con_tro.close()
                        self.book_data.close()
                
                # Thực hiện nạp file dữ liệu CSV vào MySQL
                ket_qua_nhap = self.book_data.nhap_csv(path)

                # Gửi lệnh cập nhật giao diện về Main Thread
                if ket_qua_nhap:
                    self._safe_after(0, self.Tai_Sach)
                    self._safe_after(0, lambda: messagebox.showinfo(
                        "Thành công", "Đã nhập dữ liệu sách từ file CSV thành công!"
                    ))
                else:
                    self._safe_after(0, lambda: messagebox.showwarning(
                        "Cảnh báo", "Nhập dữ liệu từ file CSV không thành công"
                    ))
            except Exception as loi:
                error_msg = str(loi)  
                self._safe_after(0, lambda msg=error_msg: messagebox.showerror(
                    "Lỗi", f"Không thể nhập file sách: {msg}"
                ))
        
        # Kích hoạt luồng chạy ngầm (truyền biến vào args để tách biệt phạm vi)
        thread = threading.Thread(target=do_import, args=(duong_dan, xac_nhan))
        thread.daemon = True
        thread.start()

    def cleanup(self):
        """Dọn dẹp tài nguyên: đảm bảo các thread không chạy sau khi page được xóa"""
        self._is_active = False