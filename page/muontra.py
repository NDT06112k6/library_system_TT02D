import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from query.muontra import MuonTraData
from query.books import BookData
from common.theme import Colors, Fonts, Spacing
#Vinh
#Q

class MuonTraPage:
    """Quản lý hiển thị, duyệt mượn và xác nhận trả sách."""
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.muontra_data = MuonTraData()
        self.book_data = BookData()
        self.config()
        self.view()
        self.Tai_Phieu()

    def config(self): 
        """Thiết lập cấu hình giao diện cơ bản."""
        self.master.title("Quản Lý Mượn Trả Sách")
        self.master.geometry("1000x650")
        self.master.configure(fg_color=Colors.BG_MAIN)
        ctk.set_appearance_mode("light")

    def view(self):
        """Khởi tạo các thành phần giao diện (UI Components)."""
        main_frame = ctk.CTkFrame(self.master, fg_color=Colors.BG_MAIN)
        main_frame.pack(fill="both", expand=True)

        # Header - Tiêu đề rẽ nhánh tường minh theo quyền hạn người dùng
        header = ctk.CTkFrame(main_frame, fg_color=Colors.PRIMARY, corner_radius=0)
        header.pack(fill="x")
        
        if self.app_manager.current_role == "Độc giả":
            title = "LỊCH SỬ MƯỢN TRẢ SÁCH"
        else:
            title = "QUẢN LÝ MƯỢN TRẢ SÁCH"
            
        ctk.CTkLabel(header, text=title, font=Fonts.HEADER, text_color=Colors.WHITE).pack(pady=Spacing.MD)

        # Bảng dữ liệu (Treeview)
        table_frame = ctk.CTkFrame(main_frame, fg_color=Colors.BG_SECONDARY)
        table_frame.pack(expand=True, fill="both", padx=20, pady=15)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=Colors.BG_SECONDARY, foreground=Colors.TEXT_PRIMARY,
                        fieldbackground=Colors.BG_SECONDARY, rowheight=35, font=Fonts.REGULAR, borderwidth=0)
        style.configure("Treeview.Heading", background=Colors.PRIMARY, foreground=Colors.WHITE, font=Fonts.SMALL_BOLD, borderwidth=0)
        style.map("Treeview", background=[('selected', Colors.BG_HOVER)], foreground=[('selected', Colors.PRIMARY)])

        columns = ("STT", "Mã Phiếu", "Người Mượn", "Mã Sách", "Ngày Mượn", "Hạn Trả", "Tiền Phạt", "Trạng Thái")
        self.phieu_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Vòng lặp tính toán độ rộng cột tường minh
        for col in columns:
            self.phieu_tree.heading(col, text=col)
            
            # Phân tách logic gán độ rộng và căn lề
            if col == "Tiền Phạt":
                width = 100
                anchor_style = "center"
            else:
                if col == "Người Mượn":
                    width = 140
                    anchor_style = "w"
                else:
                    width = 110
                    anchor_style = "center"
                    
            self.phieu_tree.column(col, width=width, anchor=anchor_style)

        self.phieu_tree.tag_configure("cho_duyet", foreground="#e67e22", font=Fonts.REGULAR)
        self.phieu_tree.tag_configure("dang_muon", foreground="#2980b9", font=Fonts.REGULAR)
        self.phieu_tree.tag_configure("da_tra", foreground="#27ae60", font=Fonts.REGULAR)
        self.phieu_tree.tag_configure("qua_han", foreground="#DC2626", font=Fonts.REGULAR, background="#FEE2E2")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.phieu_tree.yview)
        self.phieu_tree.configure(yscrollcommand=scrollbar.set)
        self.phieu_tree.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # RÀNG BUỘC SỰ KIỆN CLICK CHUỘT TRÊN BẢNG TREEVIEW
        self.phieu_tree.bind("<ButtonRelease-1>", self._on_tree_item_clicked)

        # Khung điều khiển hành động
        action_frame = ctk.CTkFrame(main_frame, fg_color=Colors.BG_SECONDARY)
        action_frame.pack(fill="x", padx=Spacing.LG, pady=Spacing.LG)
        self.status_label = ctk.CTkLabel(action_frame, text="Sẵn sàng", font=Fonts.SMALL, text_color=Colors.TEXT_SECONDARY)
        self.status_label.pack(side="left", padx=Spacing.MD)

        self.btns_container = ctk.CTkFrame(action_frame, fg_color="transparent")
        self.btns_container.pack(side="right", padx=Spacing.MD, pady=Spacing.SM)

        # Phân quyền hiển thị nút bấm chức năng ban đầu
        if self.app_manager.current_role in ["Admin", "Quản lý", "Thủ thư"]:
            self.btn_duyet = ctk.CTkButton(self.btns_container, text="✅ Duyệt Mượn", fg_color=Colors.SUCCESS, font=Fonts.SMALL_BOLD, command=self.duyet_yeu_cau)
            self.btn_duyet.pack(side="left", padx=5)
            
            self.btn_tao = ctk.CTkButton(self.btns_container, text="➕ Tạo Phiếu", fg_color=Colors.PRIMARY, font=Fonts.SMALL_BOLD, command=self.tao_phieu)
            self.btn_tao.pack(side="left", padx=5)
            
            self.btn_tra = ctk.CTkButton(self.btns_container, text="🔄 Xác Nhận Trả", fg_color=Colors.INFO, font=Fonts.SMALL_BOLD, command=self.xac_nhan_tra)
            self.btn_tra.pack(side="left", padx=5)

            self.btn_xoa = ctk.CTkButton(self.btns_container, text="🗑️ Xóa Phiếu", fg_color="#DC2626", hover_color="#B91C1C", font=Fonts.SMALL_BOLD, command=self.xoa_phieu)
            self.btn_xoa.pack(side="left", padx=5)
        else:
            ctk.CTkLabel(self.btns_container, text="📌 Hãy mang theo thẻ Độc giả khi đến nhận sách.", font=Fonts.SMALL, text_color="gray").pack(side="left", padx=10)

        ctk.CTkButton(self.btns_container, text="← Quay Lại", fg_color=Colors.BORDER, text_color=Colors.TEXT_PRIMARY, font=Fonts.SMALL_BOLD, command=self.back).pack(side="left", padx=5) 

    def _on_tree_item_clicked(self, event):
        """Xử lý sự kiện tương tác khi người dùng bấm vào một dòng dữ liệu trên bảng."""
        # Xác định vùng click chuột trên Treeview
        clicked_region = self.phieu_tree.identify_region(event.x, event.y)
        
        # Chỉ xử lý nếu click chính xác vào ô dữ liệu (cell)
        if clicked_region == "cell":
            selected_row_id = self.phieu_tree.identify_row(event.y)
            row_data = self.phieu_tree.item(selected_row_id)
            values = row_data['values']
            
            ticket_id = values[1]
            borrower_name = values[2]
            current_status = values[7]
            
            
            # ĐỒNG BỘ TRẢI NGHIỆM GIAO DIỆN (BẬT/TẮT NÚT CHỨC NĂNG THÔNG MINH)
            if self.app_manager.current_role in ["Admin", "Quản lý", "Thủ thư"]:
                if "Đã Trả" in current_status:
                    self.status_label.configure(text=f"Phiếu {ticket_id} đã hoàn thành.")
                    self.btn_duyet.configure(state="disabled")
                    self.btn_tra.configure(state="disabled")
                    
                # Thêm điều kiện nhận diện chữ "Quá Hạn" 
                elif "Đang Mượn" in current_status or "Quá Hạn" in current_status:
                    self.status_label.configure(text=f"Phiếu {ticket_id} đang có sách chưa trả (Hạn trả: {values[5]})")
                    self.btn_duyet.configure(state="disabled")
                    self.btn_tra.configure(state="normal") 
                    
                elif "Chờ Duyệt" in current_status:
                    self.status_label.configure(text=f"Phiếu {ticket_id} đang chờ phê duyệt cấp sách.")
                    self.btn_duyet.configure(state="normal")
                    self.btn_tra.configure(state="disabled")
            else:
                self.status_label.configure(text=f"Đang xem phiếu: {ticket_id} ({current_status})")

    def Tai_Phieu(self):  
        """Tải dữ liệu phiếu mượn từ DB và hiển thị lên bảng."""
        for item in self.phieu_tree.get_children():
            self.phieu_tree.delete(item)

        try:
            all_phieu = self.muontra_data.get_all()
            count = 0
            
            for row in all_phieu:
                # Kiểm tra lọc dữ liệu riêng của sinh viên
                if self.app_manager.current_role == "Sinh viên":
                    if row[2] != self.app_manager.current_user:
                        continue

                count += 1
                
                # 1. Logic ánh xạ trạng thái hiển thị 
                db_status = row[8]
                han_tra_str = row[5] 

                if db_status == "cho_duyet":
                    t_display = "⏳ Chờ Duyệt"
                    tag = "cho_duyet"
                    
                elif db_status == "dang_muon":
                    t_display = "📖 Đang Mượn"
                    tag = "dang_muon"
                    
                    # --- TỰ ĐỘNG PHÁT HIỆN TRỄ HẠN ĐỂ ĐỔI GIAO DIỆN ---
                    if han_tra_str:
                        try:
                            # So sánh Ngày hôm nay với Hạn trả
                            today = datetime.now().date()
                            # Nếu han_tra_str là kiểu date thì dùng luôn, nếu là chuỗi thì ép kiểu
                            if isinstance(han_tra_str, str):
                                han_tra_date = datetime.strptime(han_tra_str, "%Y-%m-%d").date()
                            else:
                                han_tra_date = han_tra_str
                                
                            if today > han_tra_date:
                                t_display = "⚠️ Quá Hạn"
                                tag = "qua_han" 
                        except Exception:
                            pass
                    
                elif db_status == "da_tra":
                    t_display = "✅ Đã Trả"
                    tag = "da_tra"
                else:
                    t_display = "Unknown"
                    tag = ""
                
                # 2. KIỂM TRA VÀ ĐỊNH DẠNG TIỀN PHẠT 
                val_tien_phat = row[7]
                
                # Kiểm tra xem dữ liệu có tồn tại và có phải là kiểu số/chuỗi số không
                if val_tien_phat is not None and not isinstance(val_tien_phat, (datetime, tk.Variable)):
                    try:
                        # Chỉ ép kiểu int khi dữ liệu không phải là đối tượng ngày tháng
                        tien_phat = "{:,}".format(int(val_tien_phat))
                    except (ValueError, TypeError):
                        # Phòng hờ nếu cột bị lệch sang kiểu ngày tháng hoặc chuỗi lạ
                        tien_phat = "0"
                else:
                    tien_phat = "0"
                    
                # 3. Định dạng ngày mượn và hạn trả tường minh
                if row[4]:
                    ngay_muon_display = str(row[4])
                else:
                    ngay_muon_display = "Đang chờ..."
                    
                if row[5]:
                    han_tra_display = str(row[5])
                else:
                    han_tra_display = "Chờ phê duyệt"
                
                self.phieu_tree.insert(
                    "", "end", 
                    values=(count, 
                            row[1], 
                            row[2], 
                            row[3], 
                            ngay_muon_display, 
                            han_tra_display, 
                            tien_phat, 
                            t_display), 
                    tags=(tag,)
                )
            
            self.status_label.configure(text=f"Tổng số: {count} bản ghi")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")

    def duyet_yeu_cau(self):
        """Xử lý nghiệp vụ phê duyệt mượn sách."""
        selected = self.phieu_tree.selection()
        if len(selected) == 0:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn yêu cầu cần duyệt!")
            return

        values = self.phieu_tree.item(selected[0], "values")
        if "Chờ Duyệt" not in values[7]:
            messagebox.showerror("Lỗi", "Phiếu này đã được xử lý!")
            return

        conf = messagebox.askyesno("Xác nhận", f"Phê duyệt phiếu {values[1]}?")
        if conf == True:
            try:
                now = datetime.now()
                ngay_muon_str = now.strftime("%Y-%m-%d")
                
                han_tra_date = now + timedelta(days=14)
                han_tra_str = han_tra_date.strftime("%Y-%m-%d")
                
                self.muontra_data.Yeu_Cau_Phe_Duyet(values[1], ngay_muon_str, han_tra_str)
                self.book_data.update_quantity(values[3], delta=-1)
                
                messagebox.showinfo("Thành công", "Đã duyệt phiếu mượn.")
                self.Tai_Phieu()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def xac_nhan_tra(self):
        """Xử lý nghiệp vụ nhận lại sách và tự động tính tiền phạt."""
        selected = self.phieu_tree.selection()
        if len(selected) == 0:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phiếu cần xác nhận trả!")
            return

        values = self.phieu_tree.item(selected[0], "values")
        
        # Chặn lỗi logic 
        if "Chờ Duyệt" in values[7] or "Chờ phê duyệt" in values[7]:
            messagebox.showerror("Lỗi nghiệp vụ", "Phiếu này chưa được duyệt mượn!\nBạn phải bấm 'Duyệt Mượn' trước, hoặc bấm 'Xóa Phiếu' nếu muốn hủy yêu cầu.")
            return

        if "Đã Trả" in values[7]:
            messagebox.showinfo("Thông báo", "Phiếu đã trả!")
            return

        conf = messagebox.askyesno("Xác nhận", "Xác nhận nhận lại sách?")
        if conf == True:
            try:
                now = datetime.now()
                ngay_tra_str = now.strftime("%Y-%m-%d")
                
                # ─── LOGIC TÍNH TIỀN PHẠT TỰ ĐỘNG ───
                tien_phat = 0
                # han_tra_str = "2026-5-19" 
                han_tra_str = values[5]
                
                han_tra_date = datetime.strptime(han_tra_str, "%Y-%m-%d")
                today_date = datetime.strptime(ngay_tra_str, "%Y-%m-%d")
                
                # Nếu ngày hôm nay > Hạn trả -> Bắt đầu tính phạt
                if today_date > han_tra_date:
                    so_ngay_tre = (today_date - han_tra_date).days
                    muc_phat_mot_ngay = 5000  
                    tien_phat = so_ngay_tre * muc_phat_mot_ngay
                    
                    # Bật thông báo riêng cảnh báo thủ thư thu tiền
                    messagebox.showwarning(
                        "Cảnh báo Quá Hạn", 
                        f"Độc giả đã trả trễ {so_ngay_tre} ngày!\n\nVui lòng thu số tiền phạt: {tien_phat:,} VNĐ"
                    )
                # ────────────────────────────────────

                # Cập nhật thông tin trả sách vào DB
                self.muontra_data.update(
                    "ma_phieu", 
                    values[1], 
                    {"ngay_tra": ngay_tra_str, "tien_phat": tien_phat, "trang_thai": "da_tra"}
                )
                
                # Cộng trả lại sách vào kho
                self.book_data.update_quantity(values[3], delta=1)
                
                # Nếu không bị phạt thì báo thành công bình thường
                if tien_phat == 0:
                    messagebox.showinfo("Thành công", "Đã nhận sách hoàn trả (Đúng hạn).")
                
                self.Tai_Phieu() 
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lý do: {str(e)}")
    def tao_phieu(self):
        self.app_manager.Hien_Thi_Trang_Tao_Muon()

    def xoa_phieu(self):
        """Xóa phiếu mượn và hoàn trả số lượng sách nếu cần."""
        selected = self.phieu_tree.selection()
        if len(selected) == 0:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phiếu cần xóa!")
            return

        values = self.phieu_tree.item(selected[0], "values")
        ma_phieu = values[1]
        ma_sach = values[3]
        trang_thai = values[7]

        conf = messagebox.askyesno(
            "Xác nhận xóa", 
            f"Bạn có chắc chắn muốn xóa vĩnh viễn phiếu {ma_phieu}?\nHành động này không thể hoàn tác!"
        )
        
        if conf:
            try:
                # Nếu phiếu đang giữ sách thực tế (Đang mượn) thì trả lại 1 cuốn vào kho
                if "Đang Mượn" in trang_thai:
                    self.book_data.update_quantity(ma_sach, delta=1)

                # Tiến hành xóa phiếu
                ok, msg = self.muontra_data.delete_phieu(ma_phieu)
                if ok:
                    messagebox.showinfo("Thành công", f"Đã xóa phiếu {ma_phieu}.")
                    self.Tai_Phieu()
                else:
                    messagebox.showerror("Lỗi", msg)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa phiếu: {str(e)}")

    def Lay_Hian_Thi_TrenghTha__Thai(self, db_status): 
        """Helper chuyển đổi trạng thái DB sang hiển thị UI"""
        mapping = {
            "cho_duyet": ("⏳ Chờ Duyệt", "cho_duyet"),
            "dang_muon": ("📖 Đang Mượn", "dang_muon"),
            "da_tra": ("✅ Đã Trả", "da_tra")
        }
        return mapping.get(db_status, ("Unknown", ""))

    def back(self): 
        self.app_manager.Hien_Thi_Trang_Chinh()