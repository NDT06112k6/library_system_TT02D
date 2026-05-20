import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from query.taikhoan import AccountData
from common.validation import Validation


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

    def get_current_email(self, username):
        """Lấy email hiện tại của tài khoản"""
        try:
            result = self.account_data.search("taikhoan", username, exact=True)
            if not result.empty:
                return result.iloc[0]["email"]
            return ""
        except Exception:
            return ""

    def config(self):
        self.master.title("Sửa tài khoản")
        self.master.geometry("550x750")
        self.master.resizable(True, True)

    def view(self):
        # Title
        ctk.CTkLabel(
            self.master, text="Sửa thông tin tài khoản",
            font=("Segoe UI", 24, "bold"), text_color='#0066cc'
        ).pack(pady=15)

        # Canvas + Scrollbar di chuyển
        canvas = tk.Canvas(self.master, bg='white', highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(self.master, command=canvas.yview)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=(0, 10))
        scrollbar.pack(side="right", fill="y")

        # Tạo frame bên trong canvas
        main_frame = ctk.CTkFrame(canvas, fg_color='white')
        canvas_window = canvas.create_window((0, 0), window=main_frame, anchor="nw")

        def on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())
        
        main_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # ─── Thông tin hiện tại ───────────────────────────────────────────
        ctk.CTkLabel(
            main_frame, text="Thông tin hiện tại",
            font=("Segoe UI", 14, "bold"), text_color='#004080'
        ).pack(anchor="w", padx=20, pady=(0, 10))

        old_frame = ctk.CTkFrame(main_frame, fg_color='#cce7ff', border_width=1)
        old_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(old_frame, text=f"Tên đăng nhập: {self.old_username}", font=("Segoe UI", 12)).pack(anchor="w", padx=20, pady=8)
        ctk.CTkLabel(old_frame, text=f"Mật khẩu: {self.old_password}", font=("Segoe UI", 12)).pack(anchor="w", padx=20, pady=8)
        ctk.CTkLabel(old_frame, text=f"Họ tên: {self.old_hoten}", font=("Segoe UI", 12)).pack(anchor="w", padx=20, pady=8)
        ctk.CTkLabel(old_frame, text=f"SĐT: {self.old_sdt}", font=("Segoe UI", 12)).pack(anchor="w", padx=20, pady=8)
        ctk.CTkLabel(old_frame, text=f"Chức vụ: {self.old_chucvu}", font=("Segoe UI", 12)).pack(anchor="w", padx=20, pady=8)
        ctk.CTkLabel(old_frame, text=f"Email: {self.old_email}", font=("Segoe UI", 12)).pack(anchor="w", padx=20, pady=8)

        # ─── Thông tin mới ────────────────────────────────────────────────
        ctk.CTkLabel(
            main_frame, text="Thông tin mới",
            font=("Segoe UI", 14, "bold"), text_color='#004080'
        ).pack(anchor="w", padx=20, pady=(0, 10))

        new_frame = ctk.CTkFrame(main_frame, fg_color='#cce7ff', border_width=1)
        new_frame.pack(fill="x", padx=0, pady=10)

        def make_row(parent, label_text, show=""):
            row = ctk.CTkFrame(parent, fg_color='transparent')
            row.pack(fill="x", padx=20, pady=8)
            ctk.CTkLabel(row, text=label_text, font=("Segoe UI", 12), width=160, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(row, font=("Segoe UI", 12), show=show)
            entry.pack(side="right", fill="x", expand=True)
            return entry

        self.entry_username = make_row(new_frame, "Tên đăng nhập mới:")
        self.entry_password = make_row(new_frame, "Mật khẩu mới:", show="*")
        self.entry_hoten    = make_row(new_frame, "Họ tên mới:")
        self.entry_sdt      = make_row(new_frame, "SĐT mới:")
        self.entry_chucvu   = make_row(new_frame, "Chức vụ mới:")
        self.entry_email    = make_row(new_frame, "Email mới (Gmail):")

        # Điền giá trị ban đầu vào form
        self.entry_username.insert(0, self.old_username)
        self.entry_password.insert(0, self.old_password)
        self.entry_hoten.insert(0, self.old_hoten)
        self.entry_sdt.insert(0, self.old_sdt)
        self.entry_chucvu.insert(0, self.old_chucvu)
        self.entry_email.insert(0, self.old_email)

        # Hộp kiểm hiển thị mật khẩu
        self.show_password = tk.BooleanVar()
        tk.Checkbutton(
            new_frame, text="Hiển thị mật khẩu",
            variable=self.show_password, command=self.toggle_password,
            font=("Segoe UI", 12), bg='#cce7ff'
        ).pack(pady=4)

        ctk.CTkLabel(
            new_frame,
            text="• Tên đăng nhập không được trùng\n• Gmail phải đúng định dạng @gmail.com",
            font=("Segoe UI", 10), text_color="gray"
        ).pack(pady=8)

        # ─── Nút chức năng ────────────────────────────────────────────────
        button_frame = ctk.CTkFrame(self.master, fg_color='transparent')
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Lưu thay đổi", fg_color="#28a745", command=self.save_changes).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Hủy bỏ", fg_color="#6c757d", command=self.cancel).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Khôi phục", fg_color="#ffc107", command=self.reset_form).pack(side="left", padx=10)

    # ── Chức năng Logic ──────────────────────────────────────────────────────

    def toggle_password(self):
        self.entry_password.configure(show="" if self.show_password.get() else "*")

    def reset_form(self):
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

    def username_exists(self, username: str) -> bool:
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

    def validate_input(self) -> bool:
        new_username = self.entry_username.get().strip()
        new_email = self.entry_email.get().strip()

        if new_username != self.old_username and self.username_exists(new_username):
            messagebox.showerror("Lỗi", f"Tên đăng nhập '{new_username}' đã tồn tại!")
            return False

        valid_email, msg_email = Validation.is_valid_email_simple(new_email)
        if not valid_email:
            messagebox.showerror("Lỗi", msg_email)
            return False

        new_sdt = self.entry_sdt.get().strip()
        valid_phone, msg_phone = Validation.is_valid_phone(new_sdt)
        if not valid_phone:
            messagebox.showerror("Lỗi", msg_phone)
            return False

        return True

    def save_changes(self):
        """Xử lý logic cập nhật dữ liệu tài khoản."""
        if not self.validate_input():
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

        try:
            # SỬA TẠI ĐÂY: Đóng gói thành Dictionary thay vì mảng List để hết lỗi .keys()
            thong_tin_sua = {
                "taikhoan": new_username,
                "matkhau": new_password,
                "hoten": new_hoten,
                "sdt": new_sdt,
                "chucvu": new_chucvu,
                "email": new_email
            }
            
            # Thực thi cập nhật dựa trên tên cột khóa chính 'taikhoan' và giá trị cũ self.old_username
            self.account_data.update("taikhoan", self.old_username, thong_tin_sua)
            messagebox.showinfo("Thành công", "Đã cập nhật tài khoản thành công")
            self.app_manager.show_quanlytk_page()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật tài khoản: {str(e)}")

    def cancel(self):
        if self.has_unsaved_changes():
            if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn hủy? Các thay đổi sẽ không được lưu."):
                self.app_manager.show_quanlytk_page()
        else:
            self.app_manager.show_quanlytk_page()

    def has_unsaved_changes(self) -> bool:
        return (
            self.entry_username.get().strip() != self.old_username or
            self.entry_password.get().strip() != self.old_password or
            self.entry_hoten.get().strip() != self.old_hoten or
            self.entry_sdt.get().strip() != self.old_sdt or
            self.entry_chucvu.get().strip() != self.old_chucvu or
            self.entry_email.get().strip() != self.old_email
        )