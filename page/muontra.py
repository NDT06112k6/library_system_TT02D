import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime
import pandas as pd
from query import Query

from common.button import CustomButton


class MuonTraPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.Q_muontra = Query("database/muontra.csv", ["ma_phieu", "username", "ma_sach", "ngay_muon", "ngay_tra", "trang_thai"])
        self.Q_sach = Query("database/books.csv", ["ma_sach", "ten_sach", "tac_gia", "the_loai", "so_luong", "gia"])
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

        # ===== Thanh tìm kiếm =====
        search_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        search_frame.pack(pady=5, padx=20, fill="x")

        self.entry_search = ctk.CTkEntry(
            search_frame,
            placeholder_text="Tìm theo username, mã sách hoặc trạng thái...",
            height=35,
            corner_radius=8
        )
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_search.bind("<Return>", lambda event: self.search_phieu())

        CustomButton(
            search_frame,
            text="Tìm kiếm",
            command=self.search_phieu,
            style_type="info"
        ).pack(side="left")

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
        CustomButton(left_frame, text="Xóa phiếu", command=self.xoa_phieu, style_type="danger").pack(side="left", padx=5)

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
        self.entry_search.delete(0, "end")  # Xóa search
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
            # Xử lý ngày trả: nếu chưa trả thì hiển thị "Chưa trả"
            ngay_tra_display = "Chưa trả" if pd.isna(row[4]) or str(row[4]).strip() == "" else row[4]
            self.phieu_tree.insert("", "end",
                values=(idx, row[0], row[1], row[2], row[3], ngay_tra_display, trang_thai_display),
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

    def search_phieu(self):
        """Tìm kiếm phiếu theo username hoặc mã sách"""
        keyword = self.entry_search.get().strip()
        if not keyword:
            self.load_phieu()
            return

        try:
            by_username = self.Q_muontra.search("username", keyword, exact=False)
            by_masach = self.Q_muontra.search("ma_sach", keyword, exact=False)
            result = pd.concat([by_username, by_masach]).drop_duplicates()

            # Lọc thêm theo trạng thái nếu đang filter
            filter_val = self.filter_var.get()
            if filter_val != "tat_ca":
                result = result[result["trang_thai"] == filter_val]

            # Xóa dữ liệu cũ
            for item in self.phieu_tree.get_children():
                self.phieu_tree.delete(item)

            for idx, row in enumerate(result.values.tolist(), 1):
                trang_thai_display = "Đang mượn" if row[5] == "dang_muon" else "Đã trả"
                tag = row[5]
                # Xử lý ngày trả: nếu chưa trả thì hiển thị "Chưa trả"
                ngay_tra_display = "Chưa trả" if str(row[4]).strip() in ["", "nan"] else row[4]
                self.phieu_tree.insert("", "end",
                    values=(idx, row[0], row[1], row[2], row[3], ngay_tra_display, trang_thai_display),
                    tags=(tag,)
                )
            self.status_label.configure(text=f"Tìm thấy {len(result)} phiếu")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {str(e)}")

    def back(self):
        self.app_manager.show_quanlytk_page()

    # ===== HÀM HỖ TRỢ =====

    def _read_all_phieu(self):
        """Đọc toàn bộ phiếu từ CSV"""
        try:
            data = self.Q_muontra.list(1, 9999)["data"]
            return data.values.tolist()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc dữ liệu: {str(e)}")
            return []

    def _cap_nhat_tra(self, ma_phieu, ngay_tra):
        """Cập nhật ngày trả và trạng thái"""
        # Lấy dữ liệu phiếu hiện tại
        phieu = self.Q_muontra.search("ma_phieu", ma_phieu, exact=True).iloc[0]
        self.Q_muontra.update("ma_phieu", ma_phieu, [
            ma_phieu, phieu["username"], phieu["ma_sach"],
            phieu["ngay_muon"], ngay_tra, "da_tra"
        ])

    def _cap_nhat_so_luong_sach(self, ma_sach, delta):
        """Cộng hoặc trừ số lượng sách"""
        sach = self.Q_sach.search("ma_sach", ma_sach, exact=True).iloc[0]
        so_luong_moi = str(max(0, int(sach["so_luong"]) + delta))
        self.Q_sach.update("ma_sach", ma_sach, [
            ma_sach, sach["ten_sach"], sach["tac_gia"],
            sach["the_loai"], so_luong_moi, sach["gia"]
        ])

    def xoa_phieu(self):
        """Xóa phiếu mượn"""
        selected = self.phieu_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phiếu cần xóa")
            return

        values = self.phieu_tree.item(selected[0], "values")
        ma_phieu = values[1]

        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa phiếu '{ma_phieu}'?"):
            return

        try:
            # Nếu đang mượn thì cộng lại số lượng sách
            if values[6] == "Đang mượn":
                ma_sach = values[3]
                self._cap_nhat_so_luong_sach(ma_sach, delta=+1)

            self.Q_muontra.delete("ma_phieu", ma_phieu)
            self.load_phieu()
            messagebox.showinfo("Thành công", "Đã xóa phiếu thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa: {str(e)}")