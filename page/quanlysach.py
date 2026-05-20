import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
from query.books import BookData
from common.button import CustomButton
from common.theme import Colors, Fonts, Spacing


class QuanLySachPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        # Khởi tạo Query cho file quản lý sách
        self.book_data = BookData()
        self.config()
        self.view()
        self.load_books()

    def config(self):
        self.master.title("📚 Quản Lý Sách")
        self.master.geometry("900x650")
        self.master.configure(fg_color=Colors.BG_MAIN)
        ctk.set_appearance_mode("light")

    def view(self):
        # Master frame lấp đầy window
        main_frame = ctk.CTkFrame(self.master, fg_color=Colors.BG_MAIN)
        main_frame.pack(fill="both", expand=True)

        # ===== HEADER =====
        header = ctk.CTkFrame(main_frame, fg_color=Colors.PRIMARY, corner_radius=0)
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="📚 QUẢN LÝ KHO SÁCH",
            font=Fonts.HEADER,
            text_color=Colors.WHITE
        ).pack(pady=Spacing.MD)

        # ===== SEARCH & FILTER SECTION =====
        search_frame = ctk.CTkFrame(main_frame, fg_color=Colors.BG_SECONDARY)
        search_frame.pack(fill="x", padx=Spacing.LG, pady=Spacing.LG)

        # Search box bên trái
        left_search = ctk.CTkFrame(search_frame, fg_color="transparent")
        left_search.pack(side="left", fill="x", expand=True, padx=Spacing.MD, pady=Spacing.MD)

        ctk.CTkLabel(left_search, text="🔍 Tìm:", font=Fonts.SMALL_BOLD).pack(side="left", padx=(0, 5))
        self.entry_search = ctk.CTkEntry(
            left_search,
            placeholder_text="Tìm theo tên sách hoặc tác giả...",
            height=35,
            font=Fonts.REGULAR,
            fg_color=Colors.BG_MAIN,
            border_color=Colors.BORDER
        )
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(left_search, text="Tìm", width=70, height=35, font=Fonts.SMALL_BOLD, command=self.search_books).pack(side="left", padx=2)
        ctk.CTkButton(left_search, text="Reset", width=70, height=35, font=Fonts.SMALL_BOLD, fg_color=Colors.BORDER, text_color=Colors.TEXT_PRIMARY, hover_color=Colors.BORDER_DARK, command=self.load_books).pack(side="left", padx=2)

        # Filter bên phải
        right_filter = ctk.CTkFrame(search_frame, fg_color="transparent")
        right_filter.pack(side="right", padx=Spacing.MD)

        all_books = self.book_data.get_all()
        categories = sorted(list(set([b[3] for b in all_books])))
        categories.insert(0, "Tất cả thể loại")

        self.filter_category = ctk.CTkOptionMenu(
            right_filter,
            values=categories,
            command=self.filter_by_category,
            width=150,
            height=35,
            font=Fonts.SMALL,
            fg_color=Colors.BG_MAIN,
            button_color=Colors.PRIMARY,
            text_color=Colors.TEXT_PRIMARY
        )
        self.filter_category.pack(side="right")
        ctk.CTkLabel(right_filter, text="📂 Thể loại:", font=Fonts.SMALL_BOLD).pack(side="right", padx=5)

        # ===== TABLE SECTION =====
        table_frame = ctk.CTkFrame(main_frame, fg_color=Colors.BG_SECONDARY)
        table_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Styling Treeview to match the theme
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background=Colors.BG_SECONDARY, 
                        foreground=Colors.TEXT_PRIMARY,
                        fieldbackground=Colors.BG_SECONDARY,
                        rowheight=35, 
                        font=Fonts.REGULAR, 
                        borderwidth=0)
        style.configure("Treeview.Heading", 
                        background=Colors.PRIMARY, 
                        foreground=Colors.WHITE, 
                        font=Fonts.SMALL_BOLD, 
                        borderwidth=0)
        style.map("Treeview", background=[('selected', Colors.BG_HOVER)], foreground=[('selected', Colors.PRIMARY)])

        columns = ("STT", "Mã sách", "Tên sách", "Tác giả", "Thể loại", "Số lượng", "Giá")
        self.book_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Config columns... (như cũ)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.book_tree.yview)
        self.book_tree.configure(yscrollcommand=scrollbar.set)

        self.book_tree.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # ===== ACTION BUTTONS SECTION =====
        action_frame = ctk.CTkFrame(main_frame, fg_color=Colors.BG_SECONDARY)
        action_frame.pack(fill="x", padx=Spacing.LG, pady=Spacing.LG)

        self.status_label = ctk.CTkLabel(action_frame, text="Sẵn sàng", font=Fonts.SMALL, text_color=Colors.TEXT_SECONDARY)
        self.status_label.pack(side="left", padx=Spacing.MD)

        btns_container = ctk.CTkFrame(action_frame, fg_color="transparent")
        btns_container.pack(side="right", padx=Spacing.MD, pady=Spacing.SM)

        ctk.CTkButton(btns_container, text="➕ Thêm Mới", fg_color=Colors.SUCCESS, font=Fonts.SMALL_BOLD, command=self.them_sach).pack(side="left", padx=5)
        ctk.CTkButton(btns_container, text="✏️ Sửa", fg_color=Colors.INFO, font=Fonts.SMALL_BOLD, command=self.sua_sach).pack(side="left", padx=5)
        ctk.CTkButton(btns_container, text="🗑️ Xóa", fg_color=Colors.ERROR, font=Fonts.SMALL_BOLD, command=self.xoa_sach).pack(side="left", padx=5)
        ctk.CTkButton(btns_container, text="← Quay Lại", fg_color=Colors.BORDER, text_color=Colors.TEXT_PRIMARY, font=Fonts.SMALL_BOLD, command=self.back).pack(side="left", padx=5)

    # ===== LOGIC =====

    def load_books(self):
        """Tải toàn bộ danh sách sách từ CSV"""
        self.entry_search.delete(0, "end")
        self.filter_category.set("Tất cả thể loại")
        self._populate_tree(self._read_all_books())

    def filter_by_category(self, category):
        """Lọc sách theo thể loại"""
        all_books = self._read_all_books()
        if category == "Tất cả thể loại":
            self._populate_tree(all_books)
        else:
            filtered = [b for b in all_books if b[3] == category]
            self._populate_tree(filtered)

    def search_books(self):
        """Thực hiện tìm kiếm sách theo từ khóa từ ô nhập liệu."""
        """Lọc sách theo tên hoặc tác giả"""
        keyword = self.entry_search.get().strip()
        if not keyword:
            self.load_books()
            return

        try:
            result = self.book_data.search_books(keyword)
            self._populate_tree(result)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {str(e)}")

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
        """Đọc toàn bộ sách từ CSV"""
        try:
            return self.book_data.get_all()
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
                gia = f"{int(row[5]):,}"
                self.book_tree.insert("", "end", values=(idx, row[0], row[1], row[2], row[3], row[4], gia))

        self.status_label.configure(text=f"Tổng: {len(rows)} sách")

    def _remove_book_from_file(self, ma_sach_xoa):
        """Xóa sách khỏi CSV theo mã sách"""
        self.book_data.delete("ma_sach", ma_sach_xoa)