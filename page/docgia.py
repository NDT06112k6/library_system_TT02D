import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from query.docgia import DocGiaQuery, MAX_BORROW, BORROW_DAYS
from page.components import BookCard, BorrowRow, C, FONT_FAMILY
from datetime import date, datetime
import os
import webbrowser
import threading

class DocGiaPage:
    """Trang dành cho độc giả: tìm sách, mượn sách, xem lịch sử."""

    VIEW_BOOKS = "books"
    VIEW_HISTORY = "history"

    def __init__(self, master: ctk.CTk, app_manager):
        self.master = master
        self.app_manager = app_manager
        self._is_active = True
        self.query = DocGiaQuery()
        self.username = app_manager.current_user
        self.hoten = getattr(app_manager, "current_hoten", self.username)

        self._current_view = self.VIEW_BOOKS
        self._search_after_id = None
        self._all_books = []
        self._filtered_books = []
        self._card_widgets = []
        self._cols = 3

        # Đánh số trang
        self.BOOKS_PER_PAGE = 12
        self._current_page = 1
        self._total_pages = 1

        self.master.title("📚 Thư Viện Quang Vinh — Độc Giả")
        self.master.geometry("1200x750")
        self.master.minsize(900, 600)

        ctk.set_appearance_mode("light") 
        ctk.set_default_color_theme("blue")

        self._Xay_Dung_Bo_Cuc()
        self._Tai_The_Loai()
        self._Lam_Moi_Sach()

        # Tính lại cột khi đổi kích thước cửa sổ 
        self.master.bind("<Configure>", self._Xu_Ly_Doi_Kich_Thuoc) 
        self._Canh_Bao_Qua_Han()

    # 1. XÂY DỰNG BỐ CỤC
    def _Xay_Dung_Bo_Cuc(self):
        self.master.configure(fg_color=C["bg"])

        # HEADER
        header = ctk.CTkFrame(
            self.master,
            fg_color="#1E3A5F",
            height=60,
            corner_radius=0
        )
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Click để về trang chủ
        def _Ve_Trang_Chu():
            if self._current_view != self.VIEW_BOOKS:
                self._current_view = self.VIEW_BOOKS
                txt = (
                    "⚠️ Sách quá hạn!"
                    if getattr(self, "_has_overdue", False)
                    else "📋 Sách đã mượn"
                )
                self.btn_history.configure(text=txt)
                self._Ap_Dung_Bo_Loc()

        home_btn = ctk.CTkButton(
            header,
            text="📚   Thư Viện Quang Vinh",
            font=(FONT_FAMILY, 18, "bold"),
            text_color="white",
            fg_color="transparent",
            hover_color="#2D5A8E",
            cursor="hand2",
            anchor="w",
            command=_Ve_Trang_Chu, 
        )
        home_btn.pack(side="left", padx=(16, 4))

        btn_logout = ctk.CTkButton(
            header,
            text="⏻ Đăng xuất",
            width=110,
            height=32,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            font=(FONT_FAMILY, 11),
            corner_radius=8,
            command=self._Dang_Xuat,
        ) 
        btn_logout.pack(side="right", padx=12, pady=14)

        self.btn_history = ctk.CTkButton(
            header,
            text="📋 Sách đã mượn",
            width=130,
            height=32,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=(FONT_FAMILY, 11),
            corner_radius=8,
            command=self._Chuyen_View,
        )
        self.btn_history.pack(side="right", padx=4)

        # Thông tin user
        ctk.CTkLabel(
            header,
            text=f"👤   {self.hoten}",
            font=(FONT_FAMILY, 11),
            text_color="#93C5FD",
        ).pack(side="right", padx=12)

        # Thanh tìm kiếm trung tâm
        search_wrap = ctk.CTkFrame(header, fg_color="transparent")
        search_wrap.pack(expand=True)

        search_box = ctk.CTkFrame(
            search_wrap,
            fg_color="white",
            corner_radius=20,
            height=36
        )
        search_box.pack(ipadx=4)
        search_box.pack_propagate(False)

        ctk.CTkLabel(
            search_box,
            text="🔍",
            font=(FONT_FAMILY, 13),
            text_color=C["muted"]
        ).pack(side="left", padx=(10, 0))

        self.search_entry = ctk.CTkEntry(
            search_box,
            placeholder_text="Tìm theo tên sách, tác giả hoặc thể loại...",
            placeholder_text_color="#9CA3AF",
            border_width=0,
            fg_color="white",
            text_color="#111827",
            font=(FONT_FAMILY, 12),
            width=340,
        )
        self.search_entry.pack(side="left", padx=(4, 10), pady=4)
        self.search_entry.bind("<KeyRelease>", self._Tim_Kiem)

        # BODY
        body = ctk.CTkFrame(self.master, fg_color="transparent")
        body.pack(fill="both", expand=True)

        self._Xay_Dung_Thanh_Ben(body)
        self._Xay_Dung_Noi_Dung(body)

    def _Xay_Dung_Thanh_Ben(self, parent):
        sb = ctk.CTkFrame(
            parent,
            fg_color="white",
            width=210,
            corner_radius=0,
            border_width=0
        )
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        ctk.CTkLabel(
            sb,
            text="Bộ lọc",
            font=(FONT_FAMILY, 13, "bold"),
            text_color=C["text"]
        ).pack(anchor="w", padx=18, pady=(18, 6))

        # Thể loại
        ctk.CTkLabel(
            sb,
            text="Thể loại",
            font=(FONT_FAMILY, 11),
            text_color=C["muted"]
        ).pack(anchor="w", padx=18)

        self.cat_var = tk.StringVar(value="Tất cả")

        self.cat_menu = ctk.CTkOptionMenu(
            sb,
            variable=self.cat_var,
            values=["Tất cả"], 
            command=self._Ap_Dung_Bo_Loc,
            fg_color="white",
            button_color=C["primary"],
            text_color=C["text"],
            font=(FONT_FAMILY, 11),
            width=174,
            corner_radius=8,
        )
        self.cat_menu.pack(padx=18, pady=(4, 14))

        # Sắp xếp
        ctk.CTkLabel(
            sb,
            text="Sắp xếp",
            font=(FONT_FAMILY, 11),
            text_color=C["muted"]
        ).pack(anchor="w", padx=18)

        self.sort_var = tk.StringVar(value="A–Z")
        sort_options = ["A–Z", "Mới nhất", "Phổ biến", "Còn sách"]

        ctk.CTkOptionMenu(
            sb,
            variable=self.sort_var,
            values=sort_options,
            command=self._Ap_Dung_Bo_Loc, 
            fg_color="white",
            button_color=C["primary"],
            text_color=C["text"],
            font=(FONT_FAMILY, 11),
            width=174,
            corner_radius=8,
        ).pack(padx=18, pady=(4, 14))

        ctk.CTkFrame(
            sb,
            fg_color=C["border"],
            height=1
        ).pack(fill="x", padx=14, pady=6)

        # Thống kê nhanh
        ctk.CTkLabel(
            sb,
            text="Hạn mượn",
            font=(FONT_FAMILY, 11),
            text_color=C["muted"]
        ).pack(anchor="w", padx=18, pady=(6, 0))

        ctk.CTkLabel(
            sb,
            text=f"{BORROW_DAYS} ngày / lượt",
            font=(FONT_FAMILY, 12, "bold"),
            text_color=C["primary"]
        ).pack(anchor="w", padx=18)

        ctk.CTkLabel(
            sb,
            text="Giới hạn mượn",
            font=(FONT_FAMILY, 11),
            text_color=C["muted"]
        ).pack(anchor="w", padx=18, pady=(10, 0))

        self.quota_label = ctk.CTkLabel(
            sb,
            text=f"0 / {MAX_BORROW} sách",
            font=(FONT_FAMILY, 12, "bold"),
            text_color=C["success"]
        )
        self.quota_label.pack(anchor="w", padx=18)

        # Nút Làm mới
        ctk.CTkButton(
            sb,
            text="🔄   Làm mới",
            height=34,
            corner_radius=8,
            fg_color=C["primary"],
            hover_color=C["primary_h"],
            font=(FONT_FAMILY, 11),
            command=self._Lam_Moi_Sach,
        ).pack(fill="x", padx=18, pady=(24, 0))

        # Nút Mở tài liệu HDSD PDF (Đạt điểm tối đa theo biểu điểm)
        ctk.CTkButton(
            sb,
            text="📄 Hướng Dẫn Sử Dụng",
            height=34,
            corner_radius=8,
            fg_color="#10B981", 
            hover_color="#059669",
            text_color="white",
            font=(FONT_FAMILY, 11, "bold"),
            command=self._Mo_File_PDF_HDSD,
        ).pack(fill="x", padx=18, pady=(10, 0))
    
        # Nút Tổng quan chương trình (About)
        ctk.CTkButton(
            sb, 
            text="ℹ️ Tổng Quan Chương Trình",
            height=34,
            corner_radius=8,
            fg_color="#17a2b8",
            hover_color="#138496",
            text_color="white",
            font=(FONT_FAMILY, 11, "bold"),
            command=self.hien_thi_about,
        ).pack(fill="x", padx=18, pady=(10, 0))

    # Nội dung
    def _Xay_Dung_Noi_Dung(self, parent):
        self.content_frame = ctk.CTkFrame(
            parent,
            fg_color=C["bg"],
            corner_radius=0
        )
        self.content_frame.pack(fill="both", expand=True)

        # Thanh trạng thái nhỏ
        self.status_bar = ctk.CTkLabel(
            self.content_frame,
            text="Đang tải…",
            font=(FONT_FAMILY, 10, "italic"),
            text_color=C["muted"],
            anchor="w",
        )
        self.status_bar.pack(fill="x", padx=18, pady=(10, 4))

        # Vùng chứa có thể cuộn
        self.scroll = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color=C["bg"],
            corner_radius=0,
        )
        self.scroll.pack(fill="both", expand=True, padx=10, pady=(0, 4))

        # Thanh phân trang
        self._pagination_bar = ctk.CTkFrame(
            self.content_frame,
            fg_color="white",
            height=48,
            corner_radius=0,
            border_width=1,
            border_color=C["border"],
        )
        self._pagination_bar.pack(fill="x", side="bottom")
        self._pagination_bar.pack_propagate(False)

        self._page_btn_container = ctk.CTkFrame(self._pagination_bar, fg_color="transparent")
        self._page_btn_container.place(relx=0.5, rely=0.5, anchor="center")

    # 2. TẢI DỮ LIỆU
    def _Tai_The_Loai(self):
        try:
            cats = ["Tất cả"] + self.query.get_categories()
            self.cat_menu.configure(values=cats)
        except Exception:
            pass

    def _Lam_Moi_Sach(self):
        self.status_bar.configure(text="⏳ Đang đồng bộ kho sách từ Database...")
        
        def run_load():
            try:
                self._all_books = self.query.get_all_books()
                if self._is_active and self.master.winfo_exists():
                    self.master.after(0, self._Cap_Nhat_Sau_Khi_Tai)
            except Exception as e:
                print(f"Lỗi tải dữ liệu: {e}")

        threading.Thread(target=run_load, daemon=True).start()

    def _Cap_Nhat_Sau_Khi_Tai(self):
        self._Cap_Nhat_Han_Muon()
        self._Ap_Dung_Bo_Loc()

    def _Cap_Nhat_Han_Muon(self):
        active = self.query.count_active_borrows(self.username)
        color = C["danger"] if active >= MAX_BORROW else C["success"]
        self.quota_label.configure(
            text=f"{active} / {MAX_BORROW} sách",
            text_color=color
        )

    # 3. TÌM KIẾM & LỌC
    def _Tim_Kiem(self, *_):
        """Debounce: chỉ truy vấn sau 300 ms kể từ lần gõ cuối."""
        if not self._is_active:
            return

        if self._search_after_id:
            try:
                if self.master.winfo_exists():
                    self.master.after_cancel(self._search_after_id)
            except Exception:
                pass

        try:
            if self._is_active and self.master.winfo_exists():
                self._search_after_id = self.master.after(300, self._Ap_Dung_Bo_Loc)
        except Exception:
            pass

    def _Ap_Dung_Bo_Loc(self, *_):
        if self._current_view != self.VIEW_BOOKS:
            return

        kw = self.search_entry.get().strip()
        cat = self.cat_var.get()

        sort = {
            "A–Z": "az",
            "Mới nhất": "newest",
            "Phổ biến": "popular",
            "Còn sách": "available"
        }.get(self.sort_var.get(), "az")

        self._filtered_books = self.query.search_books(kw, cat, sort)
        self._current_page = 1
        self._total_pages = max(1, -(-len(self._filtered_books) // self.BOOKS_PER_PAGE))
        
        self.status_bar.configure(text=f"Tìm thấy {len(self._filtered_books)} cuốn sách")
        self._Hien_Thi_Sach()

    # 4. RENDER LƯỚI SÁCH + PAGINATION
    def _Hien_Thi_Sach(self):
        start = (self._current_page - 1) * self.BOOKS_PER_PAGE
        end = start + self.BOOKS_PER_PAGE

        page_books = self._filtered_books[start:end]
        self._Render_Luoi(page_books)
        self._Render_Phan_Trang()

    def _Chuyen_Trang(self, page: int):
        self._current_page = max(1, min(page, self._total_pages))
        self._Hien_Thi_Sach()
        try:
            self.scroll._parent_canvas.yview_moveto(0)
        except Exception:
            pass

    def _Render_Phan_Trang(self):
        for w in self._page_btn_container.winfo_children():
            w.destroy()

        if self._total_pages <= 1:
            self._pagination_bar.pack_forget()
            return

        self._pagination_bar.pack(fill="x", side="bottom")

        cp = self._current_page
        tp = self._total_pages

        def _Tao_Nut(text, page, active=False, disabled=False):
            fg = C["primary"] if active else ("#E5E7EB" if disabled else "#F3F4F6")
            txt = "white" if active else (C["muted"] if disabled else C["text"])
            hov = C["primary_h"] if active else "#E5E7EB"

            b = ctk.CTkButton(
                self._page_btn_container,
                text=str(text),
                width=36,
                height=32,
                fg_color=fg,
                hover_color=hov,
                text_color=txt,
                corner_radius=6,
                font=(FONT_FAMILY, 11, "bold" if active else "normal"),
                state="disabled" if disabled else "normal",
                command=(lambda p=page: self._Chuyen_Trang(p)) if not disabled else None,
            )
            b.pack(side="left", padx=2)

        _Tao_Nut("◀", cp - 1, disabled=(cp == 1))

        def _Lay_Trang_Hien_Thi(current, total, window=2):
            pages = set([1, total])
            for p in range(max(2, current - window), min(total, current + window + 1)):
                pages.add(p)
            return sorted(pages)

        prev = None
        for p in _Lay_Trang_Hien_Thi(cp, tp):
            if prev is not None and p - prev > 1:
                ctk.CTkLabel(
                    self._page_btn_container,
                    text="…",
                    font=(FONT_FAMILY, 11),
                    text_color=C["muted"],
                    width=20,
                ).pack(side="left", padx=1)

            _Tao_Nut(p, p, active=(p == cp))
            prev = p

        _Tao_Nut("▶", cp + 1, disabled=(cp == tp))

        ctk.CTkLabel(
            self._pagination_bar,
            text=f"Trang {cp} / {tp}",
            font=(FONT_FAMILY, 10, "italic"),
            text_color=C["muted"],
        ).place(relx=0.02, rely=0.5, anchor="w")

        ctk.CTkLabel(
            self._pagination_bar,
            text=f"{len(self._filtered_books)} cuốn",
            font=(FONT_FAMILY, 10),
            text_color=C["muted"],
        ).place(relx=0.98, rely=0.5, anchor="e")

    def _Render_Luoi(self, books: list):
        for w in self.scroll.winfo_children():
            w.destroy()

        self._card_widgets.clear()

        if not books:
            ctk.CTkLabel(
                self.scroll,
                text="😕   Không tìm thấy sách nào",
                font=(FONT_FAMILY, 14),
                text_color=C["muted"],
            ).pack(pady=60)
            return

        cols = self._Tinh_So_Cot()
        rows_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        rows_frame.pack(fill="both", expand=True)

        for i, book in enumerate(books):
            card = BookCard(
                rows_frame,
                book,
                on_borrow=self._Xac_Nhan_Muon,
                on_detail=self._Hien_Thi_Chi_Tiet,
            )
            card.grid(row=i // cols, column=i % cols, padx=8, pady=8, sticky="nsew")
            self._card_widgets.append(card)

        for c in range(cols):
            rows_frame.columnconfigure(c, weight=1)

    def _Tinh_So_Cot(self) -> int:
        try:
            if not self.scroll.winfo_exists():
                return self._cols
            w = self.scroll.winfo_width()
        except Exception:
            return self._cols

        if w < 600: return 2
        if w < 900: return 3
        return 4

    def _Xu_Ly_Doi_Kich_Thuoc(self, event):
        if event.widget is not self.master:
            return

        if not hasattr(self, "scroll") or not self.scroll.winfo_exists():
            return
        new_cols = self._Tinh_So_Cot()

        if new_cols != self._cols:
            self._cols = new_cols
            if self._current_view == self.VIEW_BOOKS:
                self._Hien_Thi_Sach()

    # 5. MƯỢN SÁCH
    def _Xac_Nhan_Muon(self, ma_sach: str):
        book = self.query.get_book_detail(ma_sach)
        if not book:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin sách.")
            return

        ten = book.get("ten_sach", ma_sach)
        if not messagebox.askyesno(
            "Xác nhận gửi yêu cầu mượn",
            f"Bạn muốn gửi yêu cầu mượn:\n\n📖   {ten}\n\n"
            f"Yêu cầu sẽ chờ quản lý xét duyệt.\n"
            f"Sau khi duyệt, sách sẽ được tính thời hạn {BORROW_DAYS} ngày.\n\n"
            f"Xác nhận?"
        ):
            return

        ok, msg, _ = self.query.create_borrow(self.username, ma_sach)

        if ok:
            messagebox.showinfo(
                "Gửi yêu cầu thành công ✅",
                f"Đã gửi yêu cầu mượn:\n\n📖   {ten}\n\n"
                f"Trạng thái: ⏳ Chờ quản lý duyệt\n"
                f"Vào \"Sách đã mượn\" để theo dõi."
            )
            self._Lam_Moi_Sach()
        else:
            messagebox.showerror("Không thể gửi yêu cầu ❌", msg)

    # 6. CHI TIẾT SÁCH
    def _Hien_Thi_Chi_Tiet(self, ma_sach: str):
        book = self.query.get_book_detail(ma_sach)
        if not book:
            return
            
        pop = ctk.CTkToplevel(self.master)
        pop.title("Chi tiết sách")
        pop.geometry("400x380")
        pop.resizable(False, False)
        pop.grab_set()

        avail = int(book.get("so_luong", 0)) > 0
        cover_color = BookCard.COVER_COLORS[hash(ma_sach) % len(BookCard.COVER_COLORS)]

        cover = ctk.CTkFrame(pop, fg_color=cover_color, height=120, corner_radius=0)
        cover.pack(fill="x")
        cover.pack_propagate(False)

        short = "".join(w[0].upper() for w in book.get("ten_sach", "?").split()[:3])

        ctk.CTkLabel(
            cover, text=short, font=(FONT_FAMILY, 36, "bold"), text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")

        body = ctk.CTkFrame(pop, fg_color="white", corner_radius=0)
        body.pack(fill="both", expand=True)

        def _Dong_Thong_Tin(label, value):
            f = ctk.CTkFrame(body, fg_color="transparent")
            f.pack(fill="x", padx=24, pady=3)

            ctk.CTkLabel(
                f, text=label, font=(FONT_FAMILY, 10), text_color=C["muted"], width=80, anchor="w"
            ).pack(side="left")

            ctk.CTkLabel(
                f, text=str(value), font=(FONT_FAMILY, 11, "bold"), text_color=C["text"], anchor="w"
            ).pack(side="left")

        ctk.CTkLabel(
            body, text=book.get("ten_sach", ""), font=(FONT_FAMILY, 14, "bold"), text_color=C["text"], wraplength=340
        ).pack(padx=24, pady=(16, 4), anchor="w")

        _Dong_Thong_Tin("Tác giả", book.get("tac_gia", "—"))
        _Dong_Thong_Tin("Thể loại", book.get("the_loai", "—"))
        _Dong_Thong_Tin("Mã sách", book.get("ma_sach", "—"))
        _Dong_Thong_Tin("Tồn kho", f"{book.get('so_luong', 0)} cuốn")
        _Dong_Thong_Tin("Giá bìa", f"{int(book.get('gia', 0)):,} ₫" if book.get("gia") else "—")

        ctk.CTkButton(
            body,
            text="📨   Gửi yêu cầu mượn" if avail else "Hết sách",
            fg_color=C["primary"] if avail else "#D1D5DB",
            hover_color=C["primary_h"] if avail else "#D1D5DB",
            text_color="white" if avail else C["muted"],
            state="normal" if avail else "disabled",
            height=36,
            corner_radius=8,
            font=(FONT_FAMILY, 12, "bold"),
            command=lambda: (pop.destroy(), self._Xac_Nhan_Muon(ma_sach)),
        ).pack(fill="x", padx=24, pady=(12, 6))

        ctk.CTkButton(
            body, text="Đóng", fg_color="#F3F4F6", hover_color="#E5E7EB", text_color=C["text"], height=32, corner_radius=8, command=pop.destroy
        ).pack(fill="x", padx=24, pady=(0, 16))

    # 7. LỊCH SỬ MƯỢN
    def _Chuyen_View(self):
        if self._current_view == self.VIEW_BOOKS:
            self._current_view = self.VIEW_HISTORY
            self.btn_history.configure(text="📚 Danh sách sách")
            self._Hien_Thi_Lich_Su()
        else:
            self._current_view = self.VIEW_BOOKS
            txt = "⚠️ Sách quá hạn!" if getattr(self, "_has_overdue", False) else "📋 Sách đã mượn"
            self.btn_history.configure(text=txt)
            self._Ap_Dung_Bo_Loc()

    def _Hien_Thi_Lich_Su(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        records = self.query.get_my_borrows(self.username)
        self.status_bar.configure(text=f"Lịch sử mượn: {len(records)} phiếu")

        if not records:
            ctk.CTkLabel(
                self.scroll, text="📭   Bạn chưa mượn sách nào", font=(FONT_FAMILY, 14), text_color=C["muted"]
            ).pack(pady=60)
            return

        header = ctk.CTkFrame(self.scroll, fg_color="#E5E7EB", corner_radius=6, height=36)
        header.pack(fill="x", pady=(0, 2))
        header.pack_propagate(False)

        for txt, w in [
            ("STT", 40), ("Tên sách", 190), ("Tác giả", 120),
            ("Ngày mượn", 90), ("Hạn trả", 90), ("Trạng thái", 160)
        ]:
            ctk.CTkLabel(
                header, text=txt, font=(FONT_FAMILY, 10, "bold"), text_color=C["text_sub"], width=w, anchor="w"
            ).pack(side="left", padx=4)

        for idx, rec in enumerate(records, 1):
            rec["_idx"] = idx
            BorrowRow(self.scroll, rec, idx).pack(fill="x", pady=1)

    def _Canh_Bao_Qua_Han(self):
        records = self.query.get_my_borrows(self.username)
        has_overdue = False
        today = date.today()

        for rec in records:
            if rec.get("trang_thai") == "dang_muon" and rec.get("han_tra"):
                try:
                    ht = rec["han_tra"]
                    if isinstance(ht, str):
                        ht = datetime.strptime(ht, "%Y-%m-%d").date()
                    if today > ht:
                        has_overdue = True
                        break
                except Exception:
                    pass

        self._has_overdue = has_overdue
        if has_overdue:
            self.btn_history.configure(fg_color="#DC2626", hover_color="#B91C1C", text="⚠️ Sách quá hạn!")
        else:
            self.btn_history.configure(fg_color="#2563EB", hover_color="#1D4ED8", text="📋 Sách đã mượn")

    # 8. ĐĂNG XUẤT
    def _Dang_Xuat(self):
        self._is_active = False
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc muốn đăng xuất?"):
            self.app_manager.Hien_Thi_Trang_Dang_Nhap()

    # HÀM MỞ FILE PDF HDSD
    def _Mo_File_PDF_HDSD(self):     
        file_name = "HDSD.pdf" 
        if os.path.exists(file_name):
            try:
                duong_dan = os.path.abspath(file_name)
                messagebox.showinfo("Thông báo", "Hệ thống đang mở tệp PDF Hướng dẫn sử dụng!")
                webbrowser.open(duong_dan)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể mở PDF: {str(e)}")
        else:
            messagebox.showwarning("Thông báo", f"Tệp tin '{file_name}' không tồn tại trong thư mục gốc của dự án!")

    # HÀM HIỂN THỊ THÔNG TIN ABOUT NHÓM
    def hien_thi_about(self):
        """Hiển thị cửa sổ thông tin về chương trình"""
        thong_tin_about = """
  📚 HỆ THỐNG QUẢN LÝ THƯ VIỆN        
       QUANG VINH LIBRARY             

📋 Thông Tin Chương Trình:
- Phiên bản: 1.0
- Năm phát triển: 2026
- Mô tả: Ứng dụng quản lý kho sách,
  mượn trả sách, thống kê báo cáo

👥 Nhóm Thực Hiện: 1
- Thành viên 1: Nguyễn Đức Trường (Nhóm trưởng)
- Thành viên 2: Kiều Xuân Vinh
- Thành viên 3: Chu Việt Quang

🎓 Lớp: Lập Trình Python
👨‍🏫 Giảng Viên: Phạm Nguyên Hồng
🏫 Trường: Đại Học Hạ Long

💻 Công Nghệ Sử Dụng:
- CustomTkinter (GUI)
- MySQL (Database)
- Pandas & NumPy (Xử lý dữ liệu)

📧 Liên Hệ: ductruong6116@gmail.com
"""
        messagebox.showinfo("Tổng Quan Về Chương Trình", thong_tin_about)

    def cleanup(self):
        """Dọn dẹp tài nguyên: huỷ after callbacks"""
        self._is_active = False
        try:
            if self._search_after_id:
                try:
                    self.master.after_cancel(self._search_after_id)
                except Exception:
                    pass
                self._search_after_id = None
        except Exception as e:
            print(f"Lỗi dọn dẹp: {e}")