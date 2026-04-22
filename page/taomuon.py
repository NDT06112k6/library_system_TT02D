import customtkinter as ctk
from tkinter import messagebox, ttk
import os
from query import Query
import pandas as pd
from datetime import datetime


class TaoMuonPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.Q_sach = Query("database/books.csv", ["ma_sach", "ten_sach", "tac_gia", "the_loai", "so_luong", "gia"])
        self.Q_muontra = Query("database/muontra.csv", ["ma_phieu", "username", "ma_sach", "ngay_muon", "ngay_tra", "trang_thai"])
        self.Q_tk = Query("database/tk.csv", ["taikhoan", "matkhau", "email"])
        self.config()
        self.view()
        self.load_sach_available()

    def config(self):
        self.master.title("Tạo phiếu mượn")
        self.master.geometry("600x550")
        self.master.resizable(True, True)

    def view(self):
        # Tiêu đề
        ctk.CTkLabel(
            self.master,
            text="Tạo phiếu mượn sách",
            font=("Arial", 24, "bold"),
            text_color="#0066cc"
        ).pack(pady=20)

        # Form frame
        form_frame = ctk.CTkFrame(self.master, fg_color="white")
        form_frame.pack(fill="x", padx=20)

        # Mã phiếu (tự sinh, không cho sửa)
        row1 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=8)
        ctk.CTkLabel(row1, text="Mã phiếu:", font=("Arial", 12), width=100, anchor="w").pack(side="left")
        self.entry_maphieu = ctk.CTkEntry(row1, font=("Arial", 12), corner_radius=8, fg_color="#e9ecef")
        self.entry_maphieu.pack(side="right", fill="x", expand=True)
        self.entry_maphieu.insert(0, self._sinh_ma_phieu())
        self.entry_maphieu.configure(state="disabled")

        # Username người mượn
        row2 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=8)
        ctk.CTkLabel(row2, text="Username:", font=("Arial", 12), width=100, anchor="w").pack(side="left")
        self.entry_username = ctk.CTkEntry(row2, font=("Arial", 12), corner_radius=8,
                                           placeholder_text="Nhập username người mượn...")
        self.entry_username.pack(side="right", fill="x", expand=True)

        # Ngày mượn (tự động lấy ngày hiện tại)
        row3 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row3.pack(fill="x", padx=20, pady=8)
        ctk.CTkLabel(row3, text="Ngày mượn:", font=("Arial", 12), width=100, anchor="w").pack(side="left")
        self.entry_ngaymuon = ctk.CTkEntry(row3, font=("Arial", 12), corner_radius=8, fg_color="#e9ecef")
        self.entry_ngaymuon.pack(side="right", fill="x", expand=True)
        self.entry_ngaymuon.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_ngaymuon.configure(state="disabled")

        # Danh sách sách có thể mượn
        ctk.CTkLabel(
            self.master,
            text="Chọn sách (chỉ hiển thị sách còn hàng):",
            font=("Arial", 12, "bold"),
            anchor="w"
        ).pack(padx=20, pady=(15, 5), fill="x")

        table_frame = ctk.CTkFrame(self.master, corner_radius=10)
        table_frame.pack(expand=True, fill="both", padx=20, pady=5)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=28, font=("Arial", 11))
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

        columns = ("Mã sách", "Tên sách", "Tác giả", "Số lượng còn")
        self.sach_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)

        col_configs = {
            "Mã sách":      (80,  "center"),
            "Tên sách":     (220, "w"),
            "Tác giả":      (130, "center"),
            "Số lượng còn": (100, "center"),
        }
        for col, (width, anchor) in col_configs.items():
            self.sach_tree.heading(col, text=col)
            self.sach_tree.column(col, width=width, anchor=anchor)

        scrollbar = ctk.CTkScrollbar(table_frame, command=self.sach_tree.yview)
        self.sach_tree.configure(yscrollcommand=scrollbar.set)
        self.sach_tree.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Nút bấm
        btn_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(
            btn_frame, text="Tạo phiếu mượn",
            fg_color="#28a745", hover_color="#218838",
            command=self.save
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame, text="Hủy bỏ",
            fg_color="#6c757d", hover_color="#5a6268",
            command=self.cancel
        ).pack(side="left", padx=10)

    # ===== LOGIC =====

    def load_sach_available(self):
        """Chỉ hiển thị sách còn số lượng > 0"""
        try:
            data = self.Q_sach.list(1, 9999)["data"]
            for _, row in data.iterrows():
                if int(row["so_luong"]) > 0:
                    self.sach_tree.insert("", "end", values=(row["ma_sach"], row["ten_sach"], row["tac_gia"], row["so_luong"]))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách sách: {str(e)}")

    def save(self):
        """Lưu phiếu mượn vào CSV"""
        username = self.entry_username.get().strip()
        if not username:
            messagebox.showerror("Lỗi", "Vui lòng nhập username người mượn")
            return

        # Kiểm tra username tồn tại trong tk.csv
        if not self._username_exists(username):
            messagebox.showerror("Lỗi", f"Username '{username}' không tồn tại")
            return

        # Kiểm tra đã chọn sách chưa
        selected = self.sach_tree.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn sách cần mượn")
            return
        
        # Kiểm tra user đã mượn sách này chưa (chưa trả)
        ma_sach = self.sach_tree.item(selected[0], "values")[0]
        if self._da_muon_chua_tra(username, ma_sach):
            messagebox.showerror("Lỗi", f"'{username}' đang mượn sách này rồi, chưa trả!")
            return

        ma_sach = self.sach_tree.item(selected[0], "values")[0]
        ma_phieu = self.entry_maphieu.get()
        ngay_muon = self.entry_ngaymuon.get()

        try:
            # Ghi phiếu mượn
            os.makedirs("database", exist_ok=True)
            self.Q_muontra.create([ma_phieu, username, ma_sach, ngay_muon, "", "dang_muon"])

            # Trừ 1 số lượng sách
            self._cap_nhat_so_luong_sach(ma_sach, delta=-1)

            messagebox.showinfo("Thành công", f"Đã tạo phiếu mượn '{ma_phieu}' thành công")
            self.app_manager.show_muontra_page()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo phiếu: {str(e)}")

    def cancel(self):
        self.app_manager.show_muontra_page()

    # ===== HÀM HỖ TRỢ =====

    def _sinh_ma_phieu(self):
        """Tự động sinh mã phiếu tiếp theo"""
        try:
            max_val = self.Q_muontra.max("ma_phieu")
            if pd.isna(max_val):
                return "MT001"
            so = int(str(max_val)[2:]) + 1
            return f"MT{str(so).zfill(3)}"
        except Exception:
            return "MT001"

    def _username_exists(self, username):
        """Kiểm tra username có trong tk.csv không"""
        result = self.Q_tk.search("taikhoan", username, exact=True)
        return len(result) > 0

    def _cap_nhat_so_luong_sach(self, ma_sach, delta):
        """Cộng hoặc trừ số lượng sách"""
        sach = self.Q_sach.search("ma_sach", ma_sach, exact=True).iloc[0]
        so_luong_moi = str(max(0, int(sach["so_luong"]) + delta))
        self.Q_sach.update("ma_sach", ma_sach, [
            ma_sach, sach["ten_sach"], sach["tac_gia"],
            sach["the_loai"], so_luong_moi, sach["gia"]
        ])
    
    def _da_muon_chua_tra(self, username, ma_sach):
        """Kiểm tra user đang mượn sách này chưa trả"""
        try:
            data = self.Q_muontra.list(1, 9999)["data"]
            mask = (
                (data["username"] == username) &
                (data["ma_sach"] == ma_sach) &
                (data["trang_thai"] == "dang_muon")
            )
            return len(data[mask]) > 0
        except Exception:
            return False