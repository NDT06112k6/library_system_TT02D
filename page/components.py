import customtkinter as ctk

# Màu
C = {
    "bg":          "#F0F4F8",
    "card":        "#FFFFFF",
    "card_hover":  "#EBF4FF",
    "primary":     "#2563EB",
    "primary_h":   "#1D4ED8",
    "success":     "#16A34A",
    "danger":      "#DC2626",
    "warning":     "#D97706",
    "muted":       "#6B7280",
    "border":      "#E5E7EB",
    "text":        "#111827",
    "text_sub":    "#4B5563",
    "badge_avail": "#DCFCE7",
    "badge_out":   "#FEE2E2",
    "badge_pend":  "#FEF3C7",
    "sidebar":     "#1E3A5F",
    "sidebar_btn": "#2563EB",
}

FONT_FAMILY = "Segoe UI"

class BookCard(ctk.CTkFrame):
    """
    Card hiển thị thông tin 1 cuốn sách trong lưới
    """
    COVER_COLORS = [
        "#3B82F6","#8B5CF6","#EC4899","#F59E0B",
        "#10B981","#EF4444","#6366F1","#14B8A6",
    ]

    def __init__(self, master, book: dict, on_borrow, on_detail, **kwargs):
        super().__init__(
            master,
            fg_color=C["card"],
            corner_radius=12,
            border_width=1,
            border_color=C["border"],
            **kwargs,
        )
        self.book      = book
        self.on_borrow = on_borrow
        self.on_detail = on_detail
        self._build()
        self._Gan_Hieu_Ung_Di_Chuot()

    # Vẽ nội dung 
    def _build(self):
        b = self.book
        ma   = b.get("ma_sach", "")
        ten  = b.get("ten_sach", "Không có tên")
        tac  = b.get("tac_gia",  "Không rõ")
        loai = b.get("the_loai", "—")
        sl   = int(b.get("so_luong", 0))
        avail = sl > 0

        #Bìa sách giả 
        cover_color = self.COVER_COLORS[hash(ma) % len(self.COVER_COLORS)]
        cover = ctk.CTkFrame(self, fg_color=cover_color, corner_radius=8, height=110)
        cover.pack(fill="x", padx=10, pady=(10, 0))
        cover.pack_propagate(False)

        # Chữ tắt tên sách lên bìa
        short = "".join(w[0].upper() for w in ten.split()[:3]) or "?"
        ctk.CTkLabel(
            cover, text=short,
            font=(FONT_FAMILY, 28, "bold"), text_color="white",
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Badge còn/hết góc bìa
        badge_txt   = f"Còn {sl}" if avail else "Hết sách"
        badge_fg    = C["badge_avail"] if avail else C["badge_out"]
        badge_color = C["success"]    if avail else C["danger"]
        badge = ctk.CTkFrame(cover, fg_color=badge_fg, corner_radius=5, height=22)
        badge.place(relx=1.0, rely=0.0, anchor="ne", x=-6, y=6)
        ctk.CTkLabel(
            badge, text=badge_txt,
            font=(FONT_FAMILY, 9, "bold"), text_color=badge_color,
            padx=6,
        ).pack()

        # Thông tin 
        info = ctk.CTkFrame(self, fg_color="transparent")
        info.pack(fill="x", padx=10, pady=(8, 0))

        ctk.CTkLabel(
            info, text=ten, font=(FONT_FAMILY, 12, "bold"),
            text_color=C["text"], wraplength=160, justify="left", anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            info, text=f"✍  {tac}", font=(FONT_FAMILY, 10),
            text_color=C["text_sub"], anchor="w",
        ).pack(fill="x", pady=(1, 0))

        # Badge thể loại
        badge_loai = ctk.CTkFrame(info, fg_color="#EFF6FF", corner_radius=4, height=20)
        badge_loai.pack(anchor="w", pady=(4, 0))
        ctk.CTkLabel(
            badge_loai, text=loai, font=(FONT_FAMILY, 9),
            text_color=C["primary"], padx=6,
        ).pack()

        # Nút
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(fill="x", padx=10, pady=(8, 10))
        btn_row.columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            btn_row, text="Chi tiết",
            fg_color="#F3F4F6", hover_color="#E5E7EB",
            text_color=C["text"], font=(FONT_FAMILY, 10),
            height=28, corner_radius=6,
            command=lambda: self.on_detail(ma),
        ).grid(row=0, column=0, padx=(0, 4), sticky="ew")

        ctk.CTkButton(
            btn_row, text="Gửi yêu cầu",
            fg_color=C["primary"] if avail else "#D1D5DB",
            hover_color=C["primary_h"] if avail else "#D1D5DB",
            text_color="white" if avail else C["muted"],
            font=(FONT_FAMILY, 10, "bold"),
            height=28, corner_radius=6,
            state="normal" if avail else "disabled",
            command=lambda: self.on_borrow(ma),
        ).grid(row=0, column=1, padx=(4, 0), sticky="ew")

    #  Hiệu ứng hover 
    def _Gan_Hieu_Ung_Di_Chuot(self): 
        def enter(_): self.configure(fg_color=C["card_hover"])
        def leave(_): self.configure(fg_color=C["card"])
        for w in self.winfo_children():
            w.bind("<Enter>", enter)
            w.bind("<Leave>", leave)
        self.bind("<Enter>", enter)
        self.bind("<Leave>", leave)


#  Hàng trong bảng "Sách đã mượn"
class BorrowRow(ctk.CTkFrame):
    STATUS_MAP = {
        "dang_muon":  ("✅ Đã duyệt – Đang mượn", "#DCFCE7", "#16A34A"),
        "cho_duyet":  ("⏳ Chờ duyệt",             "#FEF3C7", "#D97706"),
        "da_tra":     ("↩ Đã trả",                 "#F3F4F6", "#6B7280"),
        "qua_han":    ("🚨 Quá hạn",               "#FEE2E2", "#DC2626"),
    }

    def __init__(self, master, row_data: dict, idx: int, **kwargs):
        bg = "#FAFAFA" if idx % 2 == 0 else "#FFFFFF"
        super().__init__(master, fg_color=bg, corner_radius=0, **kwargs)
        self._build(row_data)

    def _build(self, d):
        from datetime import date, datetime
        cols_w = [40, 190, 120, 90, 90, 160]
        
        cols = [
            str(d.get("_idx", "")),
            d.get("ten_sach", "")[:32],
            d.get("tac_gia",  "")[:18],
            str(d.get("ngay_muon", "—")),
            str(d.get("han_tra",  "—")),  
            d.get("trang_thai", ""),
        ]

        # Kiểm tra quá hạn và tính số ngày
        status_key = d.get("trang_thai", "")
        dynamic_label = None 

        if status_key == "dang_muon":
            han_tra_str = d.get("han_tra")
            if han_tra_str and han_tra_str != "—":
                try:
                    today = date.today()
                    # Xử lý an toàn kiểu dữ liệu ngày tháng
                    if isinstance(han_tra_str, str):
                        han_tra_date = datetime.strptime(str(han_tra_str), "%Y-%m-%d").date()
                    else:
                        han_tra_date = han_tra_str

                    if today > han_tra_date:
                        status_key = "qua_han"
                        so_ngay_tre = (today - han_tra_date).days
                        dynamic_label = f"🚨 Quá hạn ({so_ngay_tre} ngày)" 
                except Exception:
                    pass

        for i, (text, w) in enumerate(zip(cols, cols_w)):
            if i == 5:
                label_txt, bg_color, fg_color = self.STATUS_MAP.get(
                    status_key, (text, "#F3F4F6", "#6B7280")
                )
                
                # Nút ghi đè lại dòng chữ nếu bị trễ hạn
                if status_key == "qua_han" and dynamic_label:
                    label_txt = dynamic_label

                f = ctk.CTkFrame(self, fg_color=bg_color, corner_radius=5, height=22, width=155)
                f.pack(side="left", padx=4, pady=6)
                f.pack_propagate(False)
                ctk.CTkLabel(f, text=label_txt, font=(FONT_FAMILY, 9, "bold"),
                             text_color=fg_color).pack(expand=True)
            else:
                ctk.CTkLabel(
                    self, text=text, font=(FONT_FAMILY, 10),
                    text_color=C["text"], width=w, anchor="w",
                ).pack(side="left", padx=4, pady=6)