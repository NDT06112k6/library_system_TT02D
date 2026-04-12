import customtkinter as ctk
from tkinter import messagebox, ttk
import csv
import os

from common.button import CustomButton


class QuanLySachPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.config()
        self.view()
        self.load_books()

    def config(self):
        self.master.title("Quản lý sách")
        self.master.geometry("800x550")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def view(self):
        # ===== Tiêu đề =====
        ctk.CTkLabel(
            self.master,
            text="Quản lý sách",
            font=("Arial", 24, "bold")
        ).pack(pady=15)

        # ===== Thanh tìm kiếm =====
        search_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        search_frame.pack(pady=5, padx=20, fill="x")

        self.entry_search = ctk.CTkEntry(
            search_frame,
            placeholder_text="Tìm theo tên sách hoặc tác giả...",
            height=35,
            corner_radius=8
        )
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 10))

        CustomButton(
            search_frame,
            text="Tìm kiếm",
            command=self.search_books,
            style_type="info"
        ).pack(side="left")

        # ===== Khung nút chức năng =====
        button_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        button_frame.pack(pady=10, padx=20, fill="x")

        left_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        left_frame.pack(side="left")

        right_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        right_frame.pack(side="right")

        CustomButton(left_frame, text="Làm mới", command=self.load_books, style_type="info").pack(side="left", padx=5)
        CustomButton(left_frame, text="Thêm sách", command=self.them_sach, style_type="success").pack(side="left", padx=5)
        CustomButton(left_frame, text="Sửa", command=self.sua_sach, style_type="warning").pack(side="left", padx=5)
        CustomButton(left_frame, text="Xóa", command=self.xoa_sach, style_type="danger").pack(side="left", padx=5)

        CustomButton(right_frame, text="Quay lại", command=self.back, style_type="secondary").pack(side="right", padx=5)

        # ===== Bảng danh sách sách =====
        table_frame = ctk.CTkFrame(self.master, corner_radius=10)
        table_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Style cho Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=30, font=("Arial", 11), borderwidth=0)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        columns = ("STT", "Mã sách", "Tên sách", "Tác giả", "Thể loại", "Số lượng", "Giá")
        self.book_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        # Thiết lập heading và độ rộng cột
        col_configs = {
            "STT":      (40,  "center"),
            "Mã sách":  (80,  "center"),
            "Tên sách": (220, "w"),
            "Tác giả":  (130, "center"),
            "Thể loại": (100, "center"),
            "Số lượng": (70,  "center"),
            "Giá":      (90,  "center"),
        }
        for col, (width, anchor) in col_configs.items():
            self.book_tree.heading(col, text=col)
            self.book_tree.column(col, width=width, anchor=anchor)

        # Scrollbar
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.book_tree.yview)
        self.book_tree.configure(yscrollcommand=scrollbar.set)

        self.book_tree.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # ===== Thanh trạng thái =====
        self.status_label = ctk.CTkLabel(self.master, text="Sẵn sàng", anchor="w")
        self.status_label.pack(fill="x", padx=10, pady=5)

    # ===== LOGIC =====

    def load_books(self):
        """Tải toàn bộ danh sách sách từ CSV"""
        self._populate_tree(self._read_all_books())

    def search_books(self):
        """Lọc sách theo tên hoặc tác giả"""
        keyword = self.entry_search.get().strip().lower()
        if not keyword:
            self.load_books()
            return

        all_books = self._read_all_books()
        # Tìm theo tên sách (cột 1) hoặc tác giả (cột 2)
        filtered = [b for b in all_books if keyword in b[1].lower() or keyword in b[2].lower()]
        self._populate_tree(filtered)

    def them_sach(self):
        self.app_manager.show_themsach_page()

    def sua_sach(self):
        selected = self.book_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách cần sửa")
            return

        values = self.book_tree.item(selected[0], "values")
        # values: (STT, ma_sach, ten_sach, tac_gia, the_loai, so_luong, gia)
        self.app_manager.show_suasach_page(values[1])

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
            self._remove_book_from_file(ma_sach)
            self.load_books()
            messagebox.showinfo("Thành công", "Đã xóa sách thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa: {str(e)}")

    def back(self):
        self.app_manager.show_quanlytk_page()

    # ===== HÀM HỖ TRỢ =====

    def _read_all_books(self):
        """Đọc toàn bộ sách từ CSV, trả về list các row (bỏ header)"""
        database_path = "database/books.csv"
        if not os.path.exists(database_path):
            self.status_label.configure(text="Chưa có dữ liệu sách")
            return []

        try:
            with open(database_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)  # Bỏ qua header
                return list(reader)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc dữ liệu: {str(e)}")
            return []

    def _populate_tree(self, rows):
        """Đổ dữ liệu vào Treeview"""
        # Xóa dữ liệu cũ
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)

        for idx, row in enumerate(rows, 1):
            if len(row) >= 6:
                # Format giá: thêm dấu phẩy (VD: 120,000)
                gia = f"{int(row[5]):,}" if row[5].isdigit() else row[5]
                self.book_tree.insert("", "end", values=(idx, row[0], row[1], row[2], row[3], row[4], gia))

        self.status_label.configure(text=f"Tổng: {len(rows)} sách")

    def _remove_book_from_file(self, ma_sach_xoa):
        """Xóa sách khỏi CSV theo mã sách"""
        database_path = "database/books.csv"
        temp_path = "database/books_temp.csv"

        with open(database_path, "r", encoding="utf-8") as infile, \
             open(temp_path, "w", encoding="utf-8", newline="") as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            # Giữ lại header
            writer.writerow(next(reader))

            for row in reader:
                if row[0] != ma_sach_xoa:
                    writer.writerow(row)

        os.replace(temp_path, database_path)