import customtkinter as ctk
from tkinter import messagebox, ttk
import csv
import os
from datetime import datetime

from common.button import CustomButton


class MuonTraPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.config()
        self.view()
        self.load_phieu()

    def config(self):
        self.master.title("Quản lý mượn/trả sách")
        self.master.geometry("900x550")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def view(self):
        # ===== Tiêu đề =====
        ctk.CTkLabel(
            self.master,
            text="Quản lý mượn/trả sách",
            font=("Arial", 24, "bold")
        ).pack(pady=15)

        # ===== Bộ lọc trạng thái =====
        filter_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        filter_frame.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(filter_frame, text="Lọc:", font=("Arial", 12)).pack(side="left", padx=(0, 10))

        self.filter_var = ctk.StringVar(value="tat_ca")
        options = [("Tất cả", "tat_ca"), ("Đang mượn", "dang_muon"), ("Đã trả", "da_tra")]
        for text, value in options:
            ctk.CTkRadioButton(
                filter_frame, text=text,
                variable=self.filter_var, value=value,
                command=self.load_phieu
            ).pack(side="left", padx=10)

        # ===== Nút chức năng =====
        button_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        button_frame.pack(pady=10, padx=20, fill="x")

        left_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        left_frame.pack(side="left")

        right_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        right_frame.pack(side="right")

        CustomButton(left_frame, text="Làm mới", command=self.load_phieu, style_type="info").pack(side="left", padx=5)
        CustomButton(left_frame, text="Tạo phiếu mượn", command=self.tao_muon, style_type="success").pack(side="left", padx=5)
        CustomButton(left_frame, text="Xác nhận trả", command=self.xac_nhan_tra, style_type="warning").pack(side="left", padx=5)

        CustomButton(right_frame, text="Quay lại", command=self.back, style_type="secondary").pack(side="right", padx=5)

        # ===== Bảng danh sách phiếu =====
        table_frame = ctk.CTkFrame(self.master, corner_radius=10)
        table_frame.pack(expand=True, fill="both", padx=20, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=30, font=("Arial", 11), borderwidth=0)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        columns = ("STT", "Mã phiếu", "Username", "Mã sách", "Ngày mượn", "Ngày trả", "Trạng thái")
        self.phieu_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        col_configs = {
            "STT":        (40,  "center"),
            "Mã phiếu":   (90,  "center"),
            "Username":   (120, "center"),
            "Mã sách":    (90,  "center"),
            "Ngày mượn":  (120, "center"),
            "Ngày trả":   (120, "center"),
            "Trạng thái": (100, "center"),
        }
        for col, (width, anchor) in col_configs.items():
            self.phieu_tree.heading(col, text=col)
            self.phieu_tree.column(col, width=width, anchor=anchor)

        # Màu khác nhau cho 2 trạng thái
        self.phieu_tree.tag_configure("dang_muon", foreground="#e65c00")
        self.phieu_tree.tag_configure("da_tra", foreground="#28a745")

        scrollbar = ctk.CTkScrollbar(table_frame, command=self.phieu_tree.yview)
        self.phieu_tree.configure(yscrollcommand=scrollbar.set)

        self.phieu_tree.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # ===== Thanh trạng thái =====
        self.status_label = ctk.CTkLabel(self.master, text="Sẵn sàng", anchor="w")
        self.status_label.pack(fill="x", padx=10, pady=5)

    # ===== LOGIC =====

    def load_phieu(self):
        """Tải danh sách phiếu, lọc theo trạng thái"""
        all_phieu = self._read_all_phieu()
        filter_val = self.filter_var.get()

        if filter_val == "tat_ca":
            filtered = all_phieu
        else:
            filtered = [p for p in all_phieu if p[5] == filter_val]

        # Xóa dữ liệu cũ
        for item in self.phieu_tree.get_children():
            self.phieu_tree.delete(item)

        for idx, row in enumerate(filtered, 1):
            trang_thai_display = "Đang mượn" if row[5] == "dang_muon" else "Đã trả"
            tag = row[5]  # "dang_muon" hoặc "da_tra"
            self.phieu_tree.insert("", "end",
                values=(idx, row[0], row[1], row[2], row[3], row[4], trang_thai_display),
                tags=(tag,)
            )

        self.status_label.configure(text=f"Tổng: {len(filtered)} phiếu")

    def tao_muon(self):
        self.app_manager.show_taomuon_page()

    def xac_nhan_tra(self):
        """Xác nhận trả sách cho phiếu được chọn"""
        selected = self.phieu_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phiếu cần xác nhận trả")
            return

        values = self.phieu_tree.item(selected[0], "values")
        ma_phieu = values[1]
        trang_thai = values[6]

        if trang_thai == "Đã trả":
            messagebox.showinfo("Thông báo", "Phiếu này đã được trả rồi")
            return

        if not messagebox.askyesno("Xác nhận", f"Xác nhận trả sách cho phiếu '{ma_phieu}'?"):
            return

        try:
            ma_sach = values[3]
            ngay_tra = datetime.now().strftime("%d/%m/%Y")

            self._cap_nhat_tra(ma_phieu, ngay_tra)
            self._cap_nhat_so_luong_sach(ma_sach, delta=+1)  # Trả sách → cộng 1

            self.load_phieu()
            messagebox.showinfo("Thành công", "Đã xác nhận trả sách thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật: {str(e)}")

    def back(self):
        self.app_manager.show_quanlytk_page()

    # ===== HÀM HỖ TRỢ =====

    def _read_all_phieu(self):
        """Đọc toàn bộ phiếu từ CSV"""
        database_path = "database/muontra.csv"
        if not os.path.exists(database_path):
            return []
        try:
            with open(database_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)  # Bỏ header
                return [row for row in reader if len(row) >= 6]
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc dữ liệu: {str(e)}")
            return []

    def _cap_nhat_tra(self, ma_phieu, ngay_tra):
        """Cập nhật ngày trả và trạng thái trong CSV"""
        database_path = "database/muontra.csv"
        temp_path = "database/muontra_temp.csv"

        with open(database_path, "r", encoding="utf-8") as infile, \
             open(temp_path, "w", encoding="utf-8", newline="") as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            writer.writerow(next(reader))  # Giữ header

            for row in reader:
                if row[0] == ma_phieu:
                    row[4] = ngay_tra
                    row[5] = "da_tra"
                writer.writerow(row)

        os.replace(temp_path, database_path)

    def _cap_nhat_so_luong_sach(self, ma_sach, delta):
        """Cộng hoặc trừ số lượng sách (delta = +1 hoặc -1)"""
        database_path = "database/books.csv"
        temp_path = "database/books_temp.csv"

        with open(database_path, "r", encoding="utf-8") as infile, \
             open(temp_path, "w", encoding="utf-8", newline="") as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            writer.writerow(next(reader))  # Giữ header

            for row in reader:
                if row[0] == ma_sach:
                    so_luong = int(row[4]) + delta
                    row[4] = str(max(0, so_luong))  # Không để âm
                writer.writerow(row)

        os.replace(temp_path, database_path)