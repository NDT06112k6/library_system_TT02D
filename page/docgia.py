"""
page/docgia_page.py
Giao diện chính dành cho Độc giả.

Bố cục:
  ┌─ Header ─────────────────────────────────────┐
  │  Logo | Search bar         | User | Logout   │
  ├─ Sidebar ──┬─ Content ─────────────────────── │
  │  Filters   │  BookGrid / BorrowList           │
  └────────────┴──────────────────────────────────┘
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from datetime import date

from query.docgia import DocGiaQuery, MAX_BORROW, BORROW_DAYS
from page.components import BookCard, BorrowRow, C, FONT_FAMILY


# ═══════════════════════════════════════════════════════════════════
#  DocGiaPage
# ═══════════════════════════════════════════════════════════════════
class DocGiaPage:
    """Trang dành cho độc giả: tìm sách, mượn sách, xem lịch sử."""

    VIEW_BOOKS   = "books"
    VIEW_HISTORY = "history"

    def __init__(self, master: ctk.CTk, app_manager):
        self.master      = master
        self.app_manager = app_manager
        self.query       = DocGiaQuery()
        self.username    = app_manager.current_user
        self.hoten       = getattr(app_manager, "current_hoten", self.username)

        self._current_view    = self.VIEW_BOOKS
        self._search_after_id = None          # debounce ID
        self._all_books       = []            # cache toàn bộ
        self._filtered_books  = []            # cache sau filter/search
        self._card_widgets    = []            # list BookCard hiện tại
        self._cols            = 3             # số cột lưới (tự tính lại)

        # Pagination
        self.BOOKS_PER_PAGE   = 12
        self._current_page    = 1
        self._total_pages     = 1

        self.master.title("📚 Thư Viện Quang Vinh — Độc Giả")
        self.master.geometry("1200x750")
        self.master.minsize(900, 600)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self._build_layout()
        self._load_categories()
        self._refresh_books()

        # Responsive: tính lại cột khi đổi kích thước cửa sổ
        self.master.bind("<Configure>", self._on_resize)
        self._check_overdue_alert()

    # ═══════════════════════════════════════════════════
    #  1. XÂY DỰNG BỐ CỤC
    # ═══════════════════════════════════════════════════
    def _build_layout(self):
        self.master.configure(fg_color=C["bg"])

        # ── Header ─────────────────────────────────────
        header = ctk.CTkFrame(self.master, fg_color="#1E3A5F", height=60, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Logo / tên — click để về trang chủ
        def _go_home():
            if self._current_view != self.VIEW_BOOKS:
                self._current_view = self.VIEW_BOOKS
                # Lấy text tùy theo tình trạng quá hạn
                txt = "⚠️ Sách quá hạn!" if getattr(self, '_has_overdue', False) else "📋 Sách đã mượn"
                self.btn_history.configure(text=txt)
                self._apply_filters()

        home_btn = ctk.CTkButton(
            header, text="📚  Thư Viện Quang Vinh",
            font=(FONT_FAMILY, 18, "bold"), text_color="white",
            fg_color="transparent", hover_color="#2D5A8E",
            cursor="hand2", anchor="w",
            command=_go_home,
        )
        home_btn.pack(side="left", padx=(16, 4))

        # Nút bên phải header
        btn_logout = ctk.CTkButton(
            header, text="⏻ Đăng xuất", width=110, height=32,
            fg_color="#DC2626", hover_color="#B91C1C",
            font=(FONT_FAMILY, 11), corner_radius=8,
            command=self._logout,
        )
        btn_logout.pack(side="right", padx=12, pady=14)

        self.btn_history = ctk.CTkButton(
            header, text="📋 Sách đã mượn", width=130, height=32,
            fg_color="#2563EB", hover_color="#1D4ED8",
            font=(FONT_FAMILY, 11), corner_radius=8,
            command=self._toggle_view,
        )
        self.btn_history.pack(side="right", padx=4)

        # Thông tin user
        ctk.CTkLabel(
            header,
            text=f"👤  {self.hoten}",
            font=(FONT_FAMILY, 11), text_color="#93C5FD",
        ).pack(side="right", padx=12)

        # Search bar trung tâm
        search_wrap = ctk.CTkFrame(header, fg_color="transparent")
        search_wrap.pack(expand=True)

        search_box = ctk.CTkFrame(search_wrap, fg_color="white", corner_radius=20, height=36)
        search_box.pack(ipadx=4)
        search_box.pack_propagate(False)

        ctk.CTkLabel(search_box, text="🔍", font=(FONT_FAMILY, 13),
                     text_color=C["muted"]).pack(side="left", padx=(10, 0))
        self.search_entry = ctk.CTkEntry(
            search_box,
            placeholder_text="Tìm theo tên sách, tác giả hoặc thể loại...",
            placeholder_text_color="#9CA3AF",
            border_width=0, fg_color="white", text_color="#111827",
            font=(FONT_FAMILY, 12), width=340,
        )
        self.search_entry.pack(side="left", padx=(4, 10), pady=4)

        # Bắt sự kiện nhả phím (gõ xong) để gọi hàm tìm kiếm debounce
        self.search_entry.bind("<KeyRelease>", self._on_search_type)

        # ── Body = Sidebar + Content ────────────────────
        body = ctk.CTkFrame(self.master, fg_color="transparent")
        body.pack(fill="both", expand=True)

        self._build_sidebar(body)
        self._build_content(body)

    # ── Sidebar ──────────────────────────────────────────
    def _build_sidebar(self, parent):
        sb = ctk.CTkFrame(parent, fg_color="white", width=210,
                          corner_radius=0, border_width=0)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        ctk.CTkLabel(sb, text="Bộ lọc", font=(FONT_FAMILY, 13, "bold"),
                     text_color=C["text"]).pack(anchor="w", padx=18, pady=(18, 6))

        # Thể loại
        ctk.CTkLabel(sb, text="Thể loại", font=(FONT_FAMILY, 11),
                     text_color=C["muted"]).pack(anchor="w", padx=18)
        self.cat_var = tk.StringVar(value="Tất cả")
        self.cat_menu = ctk.CTkOptionMenu(
            sb, variable=self.cat_var, values=["Tất cả"],
            command=self._apply_filters,
            fg_color="white", button_color=C["primary"],
            text_color=C["text"], font=(FONT_FAMILY, 11),
            width=174, corner_radius=8,
        )
        self.cat_menu.pack(padx=18, pady=(4, 14))

        # Sắp xếp
        ctk.CTkLabel(sb, text="Sắp xếp", font=(FONT_FAMILY, 11),
                     text_color=C["muted"]).pack(anchor="w", padx=18)
        self.sort_var = tk.StringVar(value="A–Z")
        sort_options  = ["A–Z", "Mới nhất", "Phổ biến", "Còn sách"]
        ctk.CTkOptionMenu(
            sb, variable=self.sort_var, values=sort_options,
            command=self._apply_filters,
            fg_color="white", button_color=C["primary"],
            text_color=C["text"], font=(FONT_FAMILY, 11),
            width=174, corner_radius=8,
        ).pack(padx=18, pady=(4, 14))

        # Đường kẻ
        ctk.CTkFrame(sb, fg_color=C["border"], height=1).pack(fill="x", padx=14, pady=6)

        # Thống kê nhanh
        ctk.CTkLabel(sb, text="Hạn mượn", font=(FONT_FAMILY, 11),
                     text_color=C["muted"]).pack(anchor="w", padx=18, pady=(6, 0))
        ctk.CTkLabel(sb, text=f"{BORROW_DAYS} ngày / lượt",
                     font=(FONT_FAMILY, 12, "bold"), text_color=C["primary"]).pack(anchor="w", padx=18)

        ctk.CTkLabel(sb, text="Giới hạn mượn", font=(FONT_FAMILY, 11),
                     text_color=C["muted"]).pack(anchor="w", padx=18, pady=(10, 0))
        self.quota_label = ctk.CTkLabel(sb, text=f"0 / {MAX_BORROW} sách",
                                         font=(FONT_FAMILY, 12, "bold"), text_color=C["success"])
        self.quota_label.pack(anchor="w", padx=18)

        # Nút Làm mới
        ctk.CTkButton(
            sb, text="🔄  Làm mới", height=34, corner_radius=8,
            fg_color=C["primary"], hover_color=C["primary_h"],
            font=(FONT_FAMILY, 11), command=self._refresh_books,
        ).pack(fill="x", padx=18, pady=(24, 0))

    # ── Content ──────────────────────────────────────────
    def _build_content(self, parent):
        self.content_frame = ctk.CTkFrame(parent, fg_color=C["bg"], corner_radius=0)
        self.content_frame.pack(fill="both", expand=True)

        # Thanh trạng thái nhỏ
        self.status_bar = ctk.CTkLabel(
            self.content_frame,
            text="Đang tải…", font=(FONT_FAMILY, 10, "italic"),
            text_color=C["muted"], anchor="w",
        )
        self.status_bar.pack(fill="x", padx=18, pady=(10, 4))

        # Scrollable container
        self.scroll = ctk.CTkScrollableFrame(
            self.content_frame, fg_color=C["bg"], corner_radius=0,
        )
        self.scroll.pack(fill="both", expand=True, padx=10, pady=(0, 4))

        # ── Thanh phân trang ──────────────────────────
        self._pagination_bar = ctk.CTkFrame(
            self.content_frame, fg_color="white",
            height=48, corner_radius=0,
            border_width=1, border_color=C["border"],
        )
        self._pagination_bar.pack(fill="x", side="bottom")
        self._pagination_bar.pack_propagate(False)
        # Các widget bên trong sẽ được dựng lại mỗi lần render
        self._page_btn_container = ctk.CTkFrame(self._pagination_bar, fg_color="transparent")
        self._page_btn_container.place(relx=0.5, rely=0.5, anchor="center")

    # ═══════════════════════════════════════════════════
    #  2. TẢI DỮ LIỆU
    # ═══════════════════════════════════════════════════
    def _load_categories(self):
        cats = ["Tất cả"] + self.query.get_categories()
        self.cat_menu.configure(values=cats)

    def _refresh_books(self):
        self._all_books = self.query.get_all_books()
        self._update_quota_label()
        self._apply_filters()

    def _update_quota_label(self):
        active = self.query.count_active_borrows(self.username)
        color  = C["danger"] if active >= MAX_BORROW else C["success"]
        self.quota_label.configure(text=f"{active} / {MAX_BORROW} sách", text_color=color)

    # ═══════════════════════════════════════════════════
    #  3. TÌM KIẾM & LỌC
    # ═══════════════════════════════════════════════════
    def _on_search_type(self, *_):
        """Debounce: chỉ query sau 300 ms kể từ lần gõ cuối."""
        if self._search_after_id:
            self.master.after_cancel(self._search_after_id)
        self._search_after_id = self.master.after(300, self._apply_filters)

    def _apply_filters(self, *_):
        if self._current_view != self.VIEW_BOOKS:
            return
        kw = self.search_entry.get().strip()
        cat   = self.cat_var.get()
        sort  = {"A–Z": "az", "Mới nhất": "newest",
                 "Phổ biến": "popular", "Còn sách": "available"
                }.get(self.sort_var.get(), "az")

        self._filtered_books = self.query.search_books(kw, cat, sort)
        self._current_page   = 1          # filter → về trang đầu
        self._total_pages    = max(1, -(-len(self._filtered_books) // self.BOOKS_PER_PAGE))
        self.status_bar.configure(
            text=f"Tìm thấy {len(self._filtered_books)} cuốn sách"
        )
        self._render_current_page()

    # ═══════════════════════════════════════════════════
    #  4. RENDER LƯỚI SÁCH + PAGINATION
    # ═══════════════════════════════════════════════════
    def _render_current_page(self):
        """Cắt slice theo trang hiện tại rồi render lưới + thanh trang."""
        start = (self._current_page - 1) * self.BOOKS_PER_PAGE
        end   = start + self.BOOKS_PER_PAGE
        page_books = self._filtered_books[start:end]
        self._render_grid(page_books)
        self._render_pagination()

    def _go_to_page(self, page: int):
        """Chuyển sang trang chỉ định, cuộn lên đầu."""
        self._current_page = max(1, min(page, self._total_pages))
        self._render_current_page()
        # Cuộn về đầu danh sách
        try:
            self.scroll._parent_canvas.yview_moveto(0)
        except Exception:
            pass

    def _render_pagination(self):
        """Vẽ lại thanh số trang bên dưới lưới."""
        for w in self._page_btn_container.winfo_children():
            w.destroy()

        # Ẩn toàn bộ thanh nếu chỉ có 1 trang
        if self._total_pages <= 1:
            self._pagination_bar.pack_forget()
            return
        self._pagination_bar.pack(fill="x", side="bottom")

        cp = self._current_page
        tp = self._total_pages

        def _btn(text, page, active=False, disabled=False):
            fg  = C["primary"]     if active   else ("#E5E7EB" if disabled else "#F3F4F6")
            txt = "white"           if active   else (C["muted"] if disabled else C["text"])
            hov = C["primary_h"]   if active   else ("#E5E7EB" if disabled else "#E5E7EB")
            b = ctk.CTkButton(
                self._page_btn_container,
                text=str(text), width=36, height=32,
                fg_color=fg, hover_color=hov,
                text_color=txt, corner_radius=6,
                font=(FONT_FAMILY, 11, "bold" if active else "normal"),
                state="disabled" if disabled else "normal",
                command=(lambda p=page: self._go_to_page(p)) if not disabled else None,
            )
            b.pack(side="left", padx=2)

        # Nút ◀ Trước
        _btn("◀", cp - 1, disabled=(cp == 1))

        # Dãy số trang — hiển thị tối đa 7 nút, dùng "…" khi cần
        def visible_pages(current, total, window=2):
            """Tính tập hợp số trang cần hiển thị."""
            pages = set()
            pages.add(1)
            pages.add(total)
            for p in range(max(2, current - window), min(total, current + window + 1)):
                pages.add(p)
            return sorted(pages)

        prev = None
        for p in visible_pages(cp, tp):
            if prev is not None and p - prev > 1:
                # Dấu "…"
                ctk.CTkLabel(
                    self._page_btn_container, text="…",
                    font=(FONT_FAMILY, 11), text_color=C["muted"], width=20,
                ).pack(side="left", padx=1)
            _btn(p, p, active=(p == cp))
            prev = p

        # Nút ▶ Tiếp
        _btn("▶", cp + 1, disabled=(cp == tp))

        # Nhãn "Trang X / Y" ở đầu
        ctk.CTkLabel(
            self._pagination_bar,
            text=f"Trang {cp} / {tp}",
            font=(FONT_FAMILY, 10, "italic"),
            text_color=C["muted"],
        ).place(relx=0.02, rely=0.5, anchor="w")

        # Nhãn tổng sách ở cuối
        total_books = len(self._filtered_books)
        ctk.CTkLabel(
            self._pagination_bar,
            text=f"{total_books} cuốn",
            font=(FONT_FAMILY, 10),
            text_color=C["muted"],
        ).place(relx=0.98, rely=0.5, anchor="e")

    def _render_grid(self, books: list):
        # Xóa cũ
        for w in self.scroll.winfo_children():
            w.destroy()
        self._card_widgets.clear()

        if not books:
            ctk.CTkLabel(
                self.scroll, text="😕  Không tìm thấy sách nào",
                font=(FONT_FAMILY, 14), text_color=C["muted"],
            ).pack(pady=60)
            return

        cols = self._calc_cols()
        rows_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        rows_frame.pack(fill="both", expand=True)

        for i, book in enumerate(books):
            card = BookCard(
                rows_frame, book,
                on_borrow=self._confirm_borrow,
                on_detail=self._show_detail,
            )
            card.grid(row=i // cols, column=i % cols,
                      padx=8, pady=8, sticky="nsew")
            self._card_widgets.append(card)

        for c in range(cols):
            rows_frame.columnconfigure(c, weight=1)

    def _calc_cols(self) -> int:
        try:
            if not self.scroll.winfo_exists():
                return self._cols
            w = self.scroll.winfo_width()
        except Exception:
            return self._cols
        if w < 600:  return 2
        if w < 900:  return 3
        return 4

    def _on_resize(self, event):
        if event.widget is not self.master:
            return
        if not hasattr(self, 'scroll') or not self.scroll.winfo_exists():
            return
        new_cols = self._calc_cols()
        if new_cols != self._cols:
            self._cols = new_cols
            if self._current_view == self.VIEW_BOOKS:
                self._render_current_page()

    # ═══════════════════════════════════════════════════
    #  5. MƯỢN SÁCH
    # ═══════════════════════════════════════════════════
    def _confirm_borrow(self, ma_sach: str):
        book = self.query.get_book_detail(ma_sach)
        if not book:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin sách.")
            return

        ten = book.get("ten_sach", ma_sach)

        # ── Xác nhận ──────────────────────────────────
        if not messagebox.askyesno(
            "Xác nhận gửi yêu cầu mượn",
            f"Bạn muốn gửi yêu cầu mượn:\n\n📖  {ten}\n\n"
            f"Yêu cầu sẽ chờ quản lý xét duyệt.\n"
            f"Sau khi duyệt, sách sẽ được tính thời hạn {BORROW_DAYS} ngày.\n\n"
            f"Xác nhận?"
        ):
            return

        # ── Gửi yêu cầu (tạo phiếu cho_duyet) ────────
        ok, msg, _ = self.query.create_borrow(self.username, ma_sach)
        if ok:
            messagebox.showinfo(
                "Gửi yêu cầu thành công ✅",
                f"Đã gửi yêu cầu mượn:\n\n📖  {ten}\n\n"
                f"Trạng thái: ⏳ Chờ quản lý duyệt\n"
                f"Vào \"Sách đã mượn\" để theo dõi."
            )
            self._refresh_books()
        else:
            messagebox.showerror("Không thể gửi yêu cầu ❌", msg)

    # ═══════════════════════════════════════════════════
    #  6. CHI TIẾT SÁCH (popup)
    # ═══════════════════════════════════════════════════
    def _show_detail(self, ma_sach: str):
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

        # Bìa
        cover = ctk.CTkFrame(pop, fg_color=cover_color, height=120, corner_radius=0)
        cover.pack(fill="x")
        cover.pack_propagate(False)
        short = "".join(w[0].upper() for w in book.get("ten_sach","?").split()[:3])
        ctk.CTkLabel(cover, text=short, font=(FONT_FAMILY, 36, "bold"),
                     text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        body = ctk.CTkFrame(pop, fg_color="white", corner_radius=0)
        body.pack(fill="both", expand=True)

        def row(label, value):
            f = ctk.CTkFrame(body, fg_color="transparent")
            f.pack(fill="x", padx=24, pady=3)
            ctk.CTkLabel(f, text=label, font=(FONT_FAMILY, 10), text_color=C["muted"],
                         width=80, anchor="w").pack(side="left")
            ctk.CTkLabel(f, text=str(value), font=(FONT_FAMILY, 11, "bold"),
                         text_color=C["text"], anchor="w").pack(side="left")

        ctk.CTkLabel(body, text=book.get("ten_sach",""),
                     font=(FONT_FAMILY, 14, "bold"), text_color=C["text"],
                     wraplength=340).pack(padx=24, pady=(16, 4), anchor="w")
        row("Tác giả",   book.get("tac_gia","—"))
        row("Thể loại",  book.get("the_loai","—"))
        row("Mã sách",   book.get("ma_sach","—"))
        row("Tồn kho",   f"{book.get('so_luong',0)} cuốn")
        row("Giá bìa",   f"{int(book.get('gia',0)):,} ₫" if book.get("gia") else "—")

        ctk.CTkButton(
            body,
            text="📨  Gửi yêu cầu mượn" if avail else "Hết sách",
            fg_color=C["primary"] if avail else "#D1D5DB",
            hover_color=C["primary_h"] if avail else "#D1D5DB",
            text_color="white" if avail else C["muted"],
            state="normal" if avail else "disabled",
            height=36, corner_radius=8, font=(FONT_FAMILY, 12, "bold"),
            command=lambda: (pop.destroy(), self._confirm_borrow(ma_sach)),
        ).pack(fill="x", padx=24, pady=(12, 6))
        ctk.CTkButton(body, text="Đóng", fg_color="#F3F4F6", hover_color="#E5E7EB",
                      text_color=C["text"], height=32, corner_radius=8,
                      command=pop.destroy).pack(fill="x", padx=24, pady=(0, 16))

    # ═══════════════════════════════════════════════════
    #  7. LỊCH SỬ MƯỢN
    # ═══════════════════════════════════════════════════
    def _toggle_view(self):
        if self._current_view == self.VIEW_BOOKS:
            self._current_view = self.VIEW_HISTORY
            self.btn_history.configure(text="📚 Danh sách sách")
            self._render_history()
        else:
            self._current_view = self.VIEW_BOOKS
            # Trả lại nút đỏ nếu có sách quá hạn
            txt = "⚠️ Sách quá hạn!" if getattr(self, '_has_overdue', False) else "📋 Sách đã mượn"
            self.btn_history.configure(text=txt)
            self._apply_filters()

    def _render_history(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        records = self.query.get_my_borrows(self.username)
        self.status_bar.configure(text=f"Lịch sử mượn: {len(records)} phiếu")

        if not records:
            ctk.CTkLabel(self.scroll, text="📭  Bạn chưa mượn sách nào",
                         font=(FONT_FAMILY, 14), text_color=C["muted"]).pack(pady=60)
            return

        # Header bảng
        header = ctk.CTkFrame(self.scroll, fg_color="#E5E7EB", corner_radius=6, height=36)
        header.pack(fill="x", pady=(0, 2))
        header.pack_propagate(False)
        for txt, w in [("STT", 40), ("Tên sách", 190), ("Tác giả", 120),
                       ("Ngày mượn", 90), ("Hạn trả", 90), ("Trạng thái", 160)]:
            ctk.CTkLabel(header, text=txt, font=(FONT_FAMILY, 10, "bold"),
                         text_color=C["text_sub"], width=w, anchor="w").pack(side="left", padx=4)

        for idx, rec in enumerate(records, 1):
            rec["_idx"] = idx
            BorrowRow(self.scroll, rec, idx).pack(fill="x", pady=1)

    def _check_overdue_alert(self):
        """Kiểm tra và đổi màu nút Header nếu độc giả có sách quá hạn"""
        from datetime import date, datetime
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
            # Nếu có sách quá hạn -> Đổi thành màu Đỏ báo động
            self.btn_history.configure(
                fg_color="#DC2626", hover_color="#B91C1C", text="⚠️ Sách quá hạn!"
            )
        else:
            # Trạng thái bình thường
            self.btn_history.configure(
                fg_color="#2563EB", hover_color="#1D4ED8", text="📋 Sách đã mượn"
            )

    # ═══════════════════════════════════════════════════
    #  8. ĐĂNG XUẤT
    # ═══════════════════════════════════════════════════
    def _logout(self):
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc muốn đăng xuất?"):
            self.app_manager.show_login_page()
        