import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from query.taikhoan import AccountData
from common.validation import Validation
from query.muontra import MuonTraData


class SuaTKPage:
    def __init__(self, master, app_manager, username=None, password=None, hoten=None, sdt=None, chucvu=None, email=None):
        self.master = master
        self.app_manager = app_manager
        self.old_username = username or ""
        self.old_password = password or ""
        self.old_hoten = hoten or ""
        self.old_sdt = sdt or ""
        self.old_chucvu = chucvu or ""
        self.old_email = email or ""
        self.account_data = AccountData()
        self.config()
        self.view()

    def Lay_Email_Hien_Tai(self, username): 
        """Lấy email hiện tại của tài khoản"""
        try:
            result = self.account_data.search("taikhoan", username, exact=True)
            if not result.empty:
                return result.iloc[0]["email"]
            return ""
        except Exception:
            return ""

    def config(self): 
        self.master.title("👤 Cập nhật tài khoản")
        self.master.geometry("580x750")  
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def view(self):
        # Title chính
        ctk.CTkLabel(
            self.master, 
            text="✏️ SỬA THÔNG TIN TÀI KHOẢN",
            font=("Segoe UI", 20, "bold"), 
            text_color='#1E3A8A'
        ).pack(pady=(20, 15))

        canvas = tk.Canvas(self.master, bg='white', highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(self.master, command=canvas.yview)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=(0, 10))
        scrollbar.pack(side="right", fill="y", padx=(0, 10))

        # Khung chứa chính bên trong Canvas
        main_frame = ctk.CTkFrame(canvas, fg_color='white')
        canvas_window = canvas.create_window((0, 0), window=main_frame, anchor="nw")

        def Tren_Cau_Hinh_Khung(event=None): 
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width() - 15)
        
        main_frame.bind("<Configure>", Tren_Cau_Hinh_Khung)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        def Tren_Con_Lan_Chuot(event): 
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except Exception:
                pass
        
        canvas.bind_all("<MouseWheel>", Tren_Con_Lan_Chuot)

        # THÔNG TIN HIỆN TẠI 
        ctk.CTkLabel(
            main_frame, 
            text="📌 Thông tin tài khoản hiện tại",
            font=("Segoe UI", 13, "bold"), 
            text_color='#4B5563'
        ).pack(anchor="w", padx=10, pady=(5, 8))

        old_frame = ctk.CTkFrame(main_frame, fg_color='#F3F4F6', corner_radius=10, border_width=0)
        old_frame.pack(fill="x", padx=5, pady=(0, 20))

        info_labels = [
            (f"Tên đăng nhập: {self.old_username}", f"Mật khẩu: {self.old_password}"),
            (f"Họ tên: {self.old_hoten}", f"SĐT: {self.old_sdt}"),
            (f"Chức vụ: {self.old_chucvu}", f"Email: {self.old_email}")
        ]
        for r_idx, (col1, col2) in enumerate(info_labels):
            ctk.CTkLabel(old_frame, text=col1, font=("Segoe UI", 11), text_color="#374151").grid(row=r_idx, column=0, sticky="w", padx=20, pady=6)
            ctk.CTkLabel(old_frame, text=col2, font=("Segoe UI", 11), text_color="#374151").grid(row=r_idx, column=1, sticky="w", padx=40, pady=6)

        # THÔNG TIN MỚI 
        ctk.CTkLabel(
            main_frame, 
            text="📝 Nhập thông tin chỉnh sửa mới",
            font=("Segoe UI", 13, "bold"), 
            text_color='#1E3A8A'
        ).pack(anchor="w", padx=10, pady=(0, 8))

        # Khung bọc lớn bên ngoài cho phần nhập liệu mới
        new_frame = ctk.CTkFrame(main_frame, fg_color='#F9FAFB', corner_radius=12, border_width=1, border_color="#E5E7EB")
        new_frame.pack(fill="both", expand=True, padx=5, pady=(0, 10))

        # Chia new_frame làm 2 cột chính bên trong bằng cấu hình Grid hệ thống
        new_frame.columnconfigure(0, weight=1, uniform="group1")
        new_frame.columnconfigure(1, weight=1, uniform="group1")

        # Khung cột Trái (Tài khoản & Mật khẩu)
        left_column = ctk.CTkFrame(new_frame, fg_color="transparent")
        left_column.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        # Khung cột Phải (Thông tin liên hệ & chức vụ)
        right_column = ctk.CTkFrame(new_frame, fg_color="transparent")
        right_column.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

        # Hàm dựng ô nhập liệu theo từng hàng độc lập trong mỗi cột
        def make_column_row(parent, label_text, show=""):
            row = ctk.CTkFrame(parent, fg_color='transparent')
            row.pack(fill="both", expand=True, padx=10, pady=12) 
            ctk.CTkLabel(row, text=label_text, font=("Segoe UI", 12, "bold"), text_color="#4B5563").pack(anchor="w", pady=(0, 4))
            entry = ctk.CTkEntry(row, font=("Segoe UI", 12), show=show, height=35, corner_radius=8)
            entry.pack(fill="x")
            return entry

        # Sắp xếp các ô nhập liệu vào 2 cột song song
        self.entry_username = make_column_row(left_column, "Tên đăng nhập mới:")
        self.entry_password = make_column_row(left_column, "Mật khẩu mới:", show="*")
        self.entry_chucvu   = make_column_row(left_column, "Chức vụ:")

        self.entry_hoten    = make_column_row(right_column, "Họ tên mới:")
        self.entry_sdt      = make_column_row(right_column, "Số điện thoại mới:")
        self.entry_email    = make_column_row(right_column, "Email mới (Gmail):")

        # Điền lại giá trị mặc định vào Form 
        self.entry_username.insert(0, self.old_username)
        self.entry_password.insert(0, self.old_password)
        self.entry_hoten.insert(0, self.old_hoten)
        self.entry_sdt.insert(0, self.old_sdt)
        self.entry_chucvu.insert(0, self.old_chucvu)
        self.entry_email.insert(0, self.old_email)

        # --- KHÓA KHÔNG CHO SỬA CHỮ ĐỘC GIẢ ---
        if self.old_chucvu == "Độc giả":
            self.entry_chucvu.configure(
                state="disabled",
                fg_color="#A5AAB1",
                text_color="#D0D8E6"
            )

        self.show_password = tk.BooleanVar()
        chk_pass = ctk.CTkCheckBox(
            new_frame, 
            text="Hiển thị mật khẩu công khai",
            variable=self.show_password, 
            command=self.Bat_Tat_Mat_Khau,
            font=("Segoe UI", 11),
            checkbox_width=18,
            checkbox_height=18,
            corner_radius=4 
        )
        chk_pass.grid(row=1, column=0, sticky="nw", padx=20, pady=(10, 15))

        bottom_info_frame = ctk.CTkFrame(new_frame, fg_color="transparent")
        bottom_info_frame.grid(row=1, column=1, sticky="ew", padx=10, pady=(0, 15))

        hint_frame = ctk.CTkFrame(bottom_info_frame, fg_color="#EFF6FF", corner_radius=6)
        hint_frame.pack(fill="x", expand=True)
        ctk.CTkLabel(
            hint_frame,
            text="⚠️ Tên đăng nhập không được trùng lặp.\n⚠️ Hệ thống chỉ nhận đuôi @gmail.com",
            font=("Segoe UI", 10, "italic"), 
            text_color="#1D4ED8",
            justify="left"
        ).pack(pady=8, padx=10, anchor="w")
        # ---------------------------------------------------------------------

        # CỤM NÚT ĐIỀU KHIỂN 
        button_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        button_frame.pack(pady=(20, 30), fill="x", padx=30) 

        # Chia đều 3 cột với tỷ lệ chuẩn
        button_frame.columnconfigure((0, 1, 2), weight=1, uniform="group")

        ctk.CTkButton(
            button_frame, text="💾 Lưu thay đổi", fg_color="#10B981", hover_color="#059669", 
            font=("Segoe UI", 12, "bold"), height=38, corner_radius=8, command=self.Luu_Thay_Doi
        ).grid(row=0, column=0, padx=6, sticky="ew") 

        ctk.CTkButton(
            button_frame, text="🔄 Khôi phục", fg_color="#F59E0B", hover_color="#D97706", 
            font=("Segoe UI", 12, "bold"), height=38, corner_radius=8, command=self.Dat_Lai_Form
        ).grid(row=0, column=1, padx=6, sticky="ew")

        ctk.CTkButton(
            button_frame, text="❌ Hủy bỏ", fg_color="#EF4444", hover_color="#DC2626", 
            font=("Segoe UI", 12, "bold"), height=38, corner_radius=8, command=self.cancel
        ).grid(row=0, column=2, padx=6, sticky="ew")

    # Chức năng Logic 
    
    def Bat_Tat_Mat_Khau(self):
        self.entry_password.configure(show="" if self.show_password.get() else "*")
        
    def Dat_Lai_Form(self): 

        self.entry_chucvu.configure(state="normal")

        for entry, val in [
            (self.entry_username, self.old_username),
            (self.entry_password, self.old_password),
            (self.entry_hoten, self.old_hoten),
            (self.entry_sdt, self.old_sdt),
            (self.entry_chucvu, self.old_chucvu),
            (self.entry_email, self.old_email),
        ]:
            entry.delete(0, tk.END)
            entry.insert(0, val)

         # Khóa lại nếu là Độc giả
        if self.old_chucvu == "Độc giả":
            self.entry_chucvu.configure(state="disabled")

    def Ten_Dang_Nhap_Ton_Tai(self, username: str) -> bool: 
        """Kiểm tra tên đăng nhập tồn tại duy nhất""" 
        try:
            result = self.account_data.search("taikhoan", username, exact=True)
            if hasattr(result, "empty") and result.empty:
                return False
            if hasattr(result, "iloc") and len(result) > 0:
                return result.iloc[0]["taikhoan"] != self.old_username
            return False
        except Exception:
            return False

    def Xac_Thuc_Dau_Vao(self) -> bool: 
        new_username = self.entry_username.get().strip()
        new_email = self.entry_email.get().strip()

        if new_username != self.old_username and self.Ten_Dang_Nhap_Ton_Tai(new_username):
            messagebox.showerror("Lỗi", f"Tên đăng nhập '{new_username}' đã tồn tại!")
            return False

        valid_email, msg_email = Validation.xac_thuc_email_co_ban(new_email)
        if not valid_email:
            messagebox.showerror("Lỗi", msg_email)
            return False

        new_sdt = self.entry_sdt.get().strip()
        valid_phone, msg_phone = Validation.xac_thuc_sdt(new_sdt)
        if not valid_phone:
            messagebox.showerror("Lỗi", msg_phone)
            return False

        return True

    def Luu_Thay_Doi(self): 
        """Xử lý logic cập nhật dữ liệu tài khoản.""" 
        if not self.Xac_Thuc_Dau_Vao():
            return

        new_username = self.entry_username.get().strip()
        new_password = self.entry_password.get().strip()
        new_hoten = self.entry_hoten.get().strip()
        new_sdt = self.entry_sdt.get().strip()
        new_chucvu = self.entry_chucvu.get().strip()
        new_email = self.entry_email.get().strip()

        if (new_username == self.old_username and new_password == self.old_password and 
                new_hoten == self.old_hoten and new_sdt == self.old_sdt and 
                new_chucvu == self.old_chucvu and new_email == self.old_email):
            messagebox.showinfo("Thông báo", "Không có thay đổi nào được thực hiện")
            return 

        # ─── BỘ LỌC THÔNG MINH: CHẶN TRƯỚC KHI GỌI DATABASE ───
        if new_username != self.old_username:
            try:
                mt_data = MuonTraData()
                # Tìm xem Tên đăng nhập cũ này có phiếu mượn/trả nào không
                phieu_cu = mt_data.search("username", self.old_username, exact=True)
                
                if not phieu_cu.empty:
                    messagebox.showwarning(
                        "Không thể đổi Tên đăng nhập", 
                        "Tài khoản này hiện đang có lịch sử mượn trả sách (chờ duyệt/đang mượn/đã trả).\n\nKhông thể thay đổi 'Tên đăng nhập' để đảm bảo tính toàn vẹn của dữ liệu thư viện!"
                    )
                    # Tự động gõ lại tên cũ vào ô để sửa sai cho người dùng
                    self.entry_username.delete(0, tk.END)
                    self.entry_username.insert(0, self.old_username)
                    return  
            except Exception as e:
                print(f"Lỗi kiểm tra ràng buộc: {e}")
        # ────────────────────────────────────────────────────────

        try:
            thong_tin_sua = {
                "taikhoan": new_username,
                "matkhau": new_password,
                "hoten": new_hoten,
                "sdt": new_sdt,
                "chucvu": new_chucvu,
                "email": new_email
            }
            
            self.account_data.update("taikhoan", self.old_username, thong_tin_sua)
            messagebox.showinfo("Thành công", "Đã cập nhật tài khoản thành công")
            self.app_manager.Hien_Thi_Trang_Quan_Ly_TK()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật tài khoản: {str(e)}")

    def cancel(self):
        if self.Co_Thay_Doi_Chua_Luu():
            if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn hủy? Các thay đổi sẽ không được lưu."):
                self.app_manager.Hien_Thi_Trang_Quan_Ly_TK()
        else:
            self.app_manager.Hien_Thi_Trang_Quan_Ly_TK()

    def Co_Thay_Doi_Chua_Luu(self) -> bool: 
        return (
            self.entry_username.get().strip() != self.old_username or
            self.entry_password.get().strip() != self.old_password or
            self.entry_hoten.get().strip() != self.old_hoten or
            self.entry_sdt.get().strip() != self.old_sdt or
            self.entry_chucvu.get().strip() != self.old_chucvu or
            self.entry_email.get().strip() != self.old_email
        )