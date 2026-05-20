import customtkinter as ctk
from tkinter import messagebox
from query.books import BookData
from common.theme import Colors, Fonts, Spacing

class ThemSachPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.book_data = BookData()
        self.config()
        self.view()

    def config(self):
        self.master.title("Thêm sách")
        self.master.geometry("450x480")
        self.master.resizable(True, True)

    def view(self):
        # Master Frame
        main_frame = ctk.CTkFrame(self.master, fg_color=Colors.BG_MAIN)
        main_frame.pack(fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(main_frame, fg_color=Colors.PRIMARY, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(
            header,
            text="📖 THÊM SÁCH MỚI",
            font=Fonts.HEADER,
            text_color=Colors.WHITE
        ).pack(pady=Spacing.MD)

        # Form frame
        form_frame = ctk.CTkFrame(main_frame, fg_color=Colors.BG_SECONDARY)
        form_frame.pack(fill="both", expand=True, padx=Spacing.LG, pady=Spacing.LG)

        def create_form_field(parent, label_text, placeholder=""):
            """Tạo form field chuẩn"""
            label = ctk.CTkLabel(parent, text=label_text, font=Fonts.SMALL_BOLD, text_color=Colors.TEXT_PRIMARY)
            label.pack(anchor="w", padx=Spacing.MD, pady=(Spacing.MD, Spacing.XS))
            
            entry = ctk.CTkEntry(
                parent, height=40, font=Fonts.REGULAR, 
                placeholder_text=placeholder,
                fg_color=Colors.BG_MAIN, border_color=Colors.BORDER, text_color=Colors.TEXT_PRIMARY
            )
            entry.pack(fill="x", padx=Spacing.MD, pady=(0, Spacing.MD))
            return entry

        self.entries = {}
        self.entries["ma_sach"] = create_form_field(form_frame, "📝 Mã Sách (VD: S001)", "Nhập mã sách...")
        self.entries["ten_sach"] = create_form_field(form_frame, "📖 Tên Sách", "Nhập tên sách...")
        self.entries["tac_gia"] = create_form_field(form_frame, "✍️ Tác Giả", "Nhập tên tác giả...")
        self.entries["the_loai"] = create_form_field(form_frame, "📂 Thể Loại", "Nhập thể loại...")

        # Row: số lượng & giá
        row_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row_frame.pack(fill="x", padx=Spacing.MD, pady=Spacing.MD)

        left_col = ctk.CTkFrame(row_frame, fg_color="transparent")
        left_col.pack(side="left", fill="both", expand=True, padx=(0, Spacing.SM))
        ctk.CTkLabel(left_col, text="📚 Số Lượng", font=Fonts.SMALL_BOLD).pack(anchor="w", pady=(0, Spacing.XS))
        self.entries["so_luong"] = ctk.CTkEntry(left_col, height=40, font=Fonts.REGULAR, fg_color=Colors.BG_MAIN, border_color=Colors.BORDER)
        self.entries["so_luong"].pack(fill="x")

        right_col = ctk.CTkFrame(row_frame, fg_color="transparent")
        right_col.pack(side="right", fill="both", expand=True, padx=(Spacing.SM, 0))
        ctk.CTkLabel(right_col, text="💰 Giá (VND)", font=Fonts.SMALL_BOLD).pack(anchor="w", pady=(0, Spacing.XS))
        self.entries["gia"] = ctk.CTkEntry(right_col, height=40, font=Fonts.REGULAR, fg_color=Colors.BG_MAIN, border_color=Colors.BORDER)
        self.entries["gia"].pack(fill="x")

        # Button frame
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=Spacing.MD, pady=Spacing.MD)

        ctk.CTkButton(
            btn_frame, text="💾 Lưu Sách", height=40, font=Fonts.BOLD,
            fg_color=Colors.SUCCESS, hover_color="#1E8449", command=self.save
        ).pack(side="left", fill="x", expand=True, padx=(0, Spacing.SM))

        ctk.CTkButton(
            btn_frame, text="← Quay Lại", height=40, font=Fonts.BOLD,
            fg_color=Colors.BORDER, text_color=Colors.TEXT_PRIMARY, hover_color=Colors.BORDER_DARK, command=self.cancel
        ).pack(side="left", fill="x", expand=True)

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
        if self.book_data.check_exists(data["ma_sach"]):
            messagebox.showerror("Lỗi", f"Mã sách '{data['ma_sach']}' đã tồn tại")
            return None

        return data

    def save(self):
        """Xử lý logic khi người dùng nhấn nút 'Thêm sách'."""
        data = self.validate()
        if data is None:
            return

        try:
            self.book_data.create([
                data["ma_sach"], data["ten_sach"], data["tac_gia"],
                data["the_loai"], data["so_luong"], data["gia"]
            ])

            messagebox.showinfo("Thành công", "Đã thêm sách thành công")
            self.app_manager.show_quanlysach_page()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu: {str(e)}")

    def cancel(self):
        self.app_manager.show_quanlysach_page()