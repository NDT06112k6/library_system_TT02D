import customtkinter as ctk
from tkinter import messagebox
import csv
import os


class ThemSachPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.config()
        self.view()

    def config(self):
        self.master.title("Thêm sách")
        self.master.geometry("450x480")
        self.master.resizable(True, True)

    def view(self):
        # Tiêu đề
        ctk.CTkLabel(
            self.master,
            text="Thêm sách mới",
            font=("Arial", 24, "bold"),
            text_color="#0066cc"
        ).pack(pady=20)

        # Form frame
        form_frame = ctk.CTkFrame(self.master, fg_color="white")
        form_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Các trường nhập liệu
        self.entries = {}
        fields = [
            ("ma_sach",   "Mã sách"),
            ("ten_sach",  "Tên sách"),
            ("tac_gia",   "Tác giả"),
            ("the_loai",  "Thể loại"),
            ("so_luong",  "Số lượng"),
            ("gia",       "Giá (VNĐ)"),
        ]

        for key, label in fields:
            row = ctk.CTkFrame(form_frame, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=8)

            ctk.CTkLabel(row, text=label, font=("Arial", 12), width=100, anchor="w").pack(side="left")

            entry = ctk.CTkEntry(row, font=("Arial", 12), corner_radius=8)
            entry.pack(side="right", fill="x", expand=True)

            self.entries[key] = entry

        # Ghi chú validation
        ctk.CTkLabel(
            form_frame,
            text="• Mã sách không được trùng\n• Số lượng và giá phải là số nguyên dương",
            font=("Arial", 10),
            text_color="gray"
        ).pack(pady=10)

        # Nút bấm
        btn_frame = ctk.CTkFrame(self.master, fg_color="white")
        btn_frame.pack(pady=15)

        ctk.CTkButton(
            btn_frame, text="Thêm sách",
            fg_color="#28a745", hover_color="#218838",
            command=self.save
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame, text="Hủy bỏ",
            fg_color="#6c757d", hover_color="#5a6268",
            command=self.cancel
        ).pack(side="left", padx=10)

    def validate(self):
        """Kiểm tra dữ liệu đầu vào"""
        data = {k: v.get().strip() for k, v in self.entries.items()}

        # Kiểm tra trống
        for key, val in data.items():
            if not val:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
                return None

        # Kiểm tra số lượng và giá là số nguyên dương
        for field in ("so_luong", "gia"):
            if not data[field].isdigit() or int(data[field]) <= 0:
                messagebox.showerror("Lỗi", f"'{field.replace('_', ' ').title()}' phải là số nguyên dương")
                return None

        # Kiểm tra mã sách trùng
        if self._ma_sach_exists(data["ma_sach"]):
            messagebox.showerror("Lỗi", f"Mã sách '{data['ma_sach']}' đã tồn tại")
            return None

        return data

    def save(self):
        """Lưu sách mới vào CSV"""
        data = self.validate()
        if data is None:
            return

        try:
            os.makedirs("database", exist_ok=True)
            database_path = "database/books.csv"

            # Tạo header nếu file chưa tồn tại
            if not os.path.exists(database_path):
                with open(database_path, "w", encoding="utf-8", newline="") as f:
                    csv.writer(f).writerow(["ma_sach", "ten_sach", "tac_gia", "the_loai", "so_luong", "gia"])

            with open(database_path, "a", encoding="utf-8", newline="") as f:
                csv.writer(f).writerow([
                    data["ma_sach"], data["ten_sach"], data["tac_gia"],
                    data["the_loai"], data["so_luong"], data["gia"]
                ])

            messagebox.showinfo("Thành công", "Đã thêm sách thành công")
            self.app_manager.show_quanlysach_page()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu: {str(e)}")

    def cancel(self):
        self.app_manager.show_quanlysach_page()

    def _ma_sach_exists(self, ma_sach):
        """Kiểm tra mã sách đã tồn tại chưa"""
        database_path = "database/books.csv"
        if not os.path.exists(database_path):
            return False

        with open(database_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # Bỏ header
            return any(row[0] == ma_sach for row in reader if row)