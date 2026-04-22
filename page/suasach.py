import customtkinter as ctk
from tkinter import messagebox
from query import Query

class SuaSachPage:
    def __init__(self, master, app_manager, ma_sach):
        self.master = master
        self.app_manager = app_manager
        self.Q = Query("database/books.csv", ["ma_sach", "ten_sach", "tac_gia", "the_loai", "so_luong", "gia"])
        self.ma_sach = ma_sach
        self.old_data = self._load_book_data(ma_sach)
        self.config()
        self.view()

    def config(self):
        self.master.title("Sửa sách")
        self.master.geometry("450x500")
        self.master.resizable(True, True)

    def view(self):
        # Tiêu đề
        ctk.CTkLabel(
            self.master,
            text="Sửa thông tin sách",
            font=("Arial", 24, "bold"),
            text_color="#0066cc"
        ).pack(pady=20)

        # Form frame
        form_frame = ctk.CTkFrame(self.master, fg_color="white")
        form_frame.pack(expand=True, fill="both", padx=20, pady=10)

        self.entries = {}
        fields = [
            ("ma_sach",  "Mã sách"),
            ("ten_sach", "Tên sách"),
            ("tac_gia",  "Tác giả"),
            ("the_loai", "Thể loại"),
            ("so_luong", "Số lượng"),
            ("gia",      "Giá (VNĐ)"),
        ]

        for key, label in fields:
            row = ctk.CTkFrame(form_frame, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=8)

            ctk.CTkLabel(row, text=label, font=("Arial", 12), width=100, anchor="w").pack(side="left")

            entry = ctk.CTkEntry(row, font=("Arial", 12), corner_radius=8)
            entry.pack(side="right", fill="x", expand=True)

            # Điền dữ liệu cũ vào form
            if self.old_data and key in self.old_data:
                entry.insert(0, self.old_data[key])

            # Mã sách không cho sửa
            if key == "ma_sach":
                entry.configure(state="disabled", fg_color="#e9ecef")

            self.entries[key] = entry

        # Nút bấm
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
        """Kiểm tra dữ liệu đầu vào"""
        data = {k: v.get().strip() for k, v in self.entries.items()}

        # Kiểm tra trống (bỏ qua ma_sach vì disabled)
        for key in ("ten_sach", "tac_gia", "the_loai", "so_luong", "gia"):
            if not data[key]:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
                return None

        # Kiểm tra số lượng và giá là số nguyên dương
        for field in ("so_luong", "gia"):
            if not data[field].isdigit() or int(data[field]) <= 0:
                messagebox.showerror("Lỗi", f"'{field.replace('_', ' ').title()}' phải là số nguyên dương")
                return None

        return data

    def save(self):
        """Lưu thay đổi vào CSV"""
        data = self.validate()
        if data is None:
            return

        # Kiểm tra có thay đổi không
        if all(data[k] == self.old_data.get(k, "") for k in data if k != "ma_sach"):
            messagebox.showinfo("Thông báo", "Không có thay đổi nào")
            return

        try:
            self._update_book_in_file(data)
            messagebox.showinfo("Thành công", "Đã cập nhật sách thành công")
            self.app_manager.show_quanlysach_page()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật: {str(e)}")

    def reset(self):
        """Khôi phục về dữ liệu ban đầu"""
        for key, entry in self.entries.items():
            if key == "ma_sach":
                continue
            entry.delete(0, "end")
            entry.insert(0, self.old_data.get(key, ""))

    def cancel(self):
        self.app_manager.show_quanlysach_page()

    # ===== HÀM HỖ TRỢ =====

    def _load_book_data(self, ma_sach):
        """Đọc dữ liệu sách theo mã sách"""
        result = self.Q.search("ma_sach", ma_sach, exact=True)
        if result.empty:
            return {}
        return result.iloc[0].to_dict()

    def _update_book_in_file(self, new_data):
        """Ghi dữ liệu mới vào CSV"""
        self.Q.update("ma_sach", self.ma_sach, [
            self.ma_sach,
            new_data["ten_sach"],
            new_data["tac_gia"],
            new_data["the_loai"],
            new_data["so_luong"],
            new_data["gia"]
        ])