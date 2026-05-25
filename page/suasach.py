import customtkinter as ctk
from tkinter import messagebox
from query.books import BookData


class SuaSachPage:

    def __init__(self, master, app_manager, ma_sach):
        self.master = master
        self.app_manager = app_manager
        self.book_data = BookData()
        self.ma_sach = ma_sach
        self.old_data = self._Tai_Du_Lieu_Sach(ma_sach)
        self.config()
        self.view()

    def config(self): 
        self.master.title("Sửa sách")
        self.master.geometry("450x550")
        self.master.resizable(True, True)

    def view(self):
        ctk.CTkLabel(
            self.master,
            text="Sửa thông tin sách",
            font=("Segoe UI", 24, "bold"),
            text_color="#0066cc"
        ).pack(pady=20)

        form_frame = ctk.CTkFrame(self.master, fg_color="white")
        form_frame.pack(expand=True, fill="both", padx=20, pady=10)

        self.entries = {}
        fields = [
            ("ma_sach", "Mã sách"),
            ("ten_sach", "Tên sách"),
            ("tac_gia", "Tác giả"),
            ("the_loai", "Thể loại"),
            ("so_luong", "Số lượng"),
            ("gia", "Giá (VNĐ)"),
        ]

        for key, label in fields:
            row = ctk.CTkFrame(form_frame, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=8)

            ctk.CTkLabel(row, text=label, font=("Segoe UI", 13, "bold"), width=120, anchor="w").pack(side="left")

            entry = ctk.CTkEntry(row, font=("Segoe UI", 12), corner_radius=8)
            entry.pack(side="right", fill="x", expand=True)

            if self.old_data and key in self.old_data:
                entry.insert(0, str(self.old_data[key]))

            if key == "ma_sach":
                entry.configure(state="disabled", fg_color="#e9ecef")

            self.entries[key] = entry

        btn_frame = ctk.CTkFrame(self.master, fg_color="white")
        btn_frame.pack(pady=15)

        ctk.CTkButton(
            btn_frame, text="Lưu thay đổi",
            fg_color="#28a745", hover_color="#218838",
            command=self.save
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame, text="Khôi phục",
            fg_color="#ffc107", hover_color="#e0a800", text_color="black",
            command=self.reset
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame, text="Hủy bỏ",
            fg_color="#6c757d", hover_color="#5a6268",
            command=self.cancel
        ).pack(side="left", padx=10)

    def validate(self): 
        data = {k: v.get().strip() for k, v in self.entries.items()}

        for key in ("ten_sach", "tac_gia", "the_loai", "so_luong", "gia"):
            if not data[key]:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
                return None

        for field in ("so_luong", "gia"):
            if not data[field].isdigit() or int(data[field]) <= 0:
                messagebox.showerror("Lỗi", f"'{field.replace('_', ' ').title()}' phải là số nguyên dương")
                return None

        return data

    def save(self): 
        data = self.validate()
        if data is None:
            return

        # So sánh kiểm tra xem người dùng có thực sự chỉnh sửa gì không
        if all(str(data[k]) == str(self.old_data.get(k, "")) for k in data if k != "ma_sach"):
            messagebox.showinfo("Thông báo", "Không có thay đổi nào")
            return

        try: 
            self._Cap_Nhat_Sach_Trong_File(data)
            messagebox.showinfo("Thành công", "Đã cập nhật sách thành công")
            self.app_manager.Hien_Thi_Trang_Quan_Ly_Sach()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật: {str(e)}")

    def reset(self):  
        for key, entry in self.entries.items():
            if key == "ma_sach":
                continue
            entry.delete(0, "end") 
            entry.insert(0, str(self.old_data.get(key, "")))

    def cancel(self):
        self.app_manager.Hien_Thi_Trang_Quan_Ly_Sach()

    # ===== HÀM HỖ TRỢ DỮ LIỆU ===== 
    def _Tai_Du_Lieu_Sach(self, ma_sach): 
        """Đọc dữ liệu sách theo mã sách và xử lý an toàn dù kết quả trả về dạng Dict hay DataFrame"""
        result = self.book_data.search("ma_sach", ma_sach, exact=True)
        
        # Nếu kết quả trả về là một Pandas DataFrame trống
        if hasattr(result, "empty") and result.empty:
            return {}
        
        # Nếu kết quả trả về dạng DataFrame có dữ liệu, bốc hàng đầu tiên thành dict
        if hasattr(result, "iloc"):
            return result.iloc[0].to_dict()
            
        # Nếu kết quả truy vấn SQL trả trực tiếp về danh sách Dictionary/List
        if isinstance(result, list) and len(result) > 0:
            return result[0] if isinstance(result[0], dict) else {}
            
        return {}

    def _Cap_Nhat_Sach_Trong_File(self, new_data): 
        """Đóng gói dữ liệu thành dạng Dictionary để truyền xuống hàm update động của lớp cha"""
        thong_tin_sua = {
            "ten_sach": new_data["ten_sach"],
            "tac_gia": new_data["tac_gia"],
            "the_loai": new_data["the_loai"],
            "so_luong": int(new_data["so_luong"]),
            "gia": float(new_data["gia"])
        }
        # Gọi trực tiếp hàm update tổng quát dựa trên tên cột khóa chính 'ma_sach'
        self.book_data.update("ma_sach", self.ma_sach, thong_tin_sua)