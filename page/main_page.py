import customtkinter as ctk
from common.theme import Colors, Fonts, Spacing

class MainPage:
    """Trang chính (Dashboard) sau khi đăng nhập"""
    
    def __init__(self, master, app_manager, username):
        self.master = master
        self.app_manager = app_manager
        self.username = username
        self.config()
        self.view()
    
    def config(self):
        self.master.title("Hệ Thống Quản Lý Thư Viện")
        self.master.geometry("1000x650")
        self.master.configure(fg_color=Colors.BG_MAIN)
    
    def view(self):
        # Master frame
        main = ctk.CTkFrame(self.master, fg_color=Colors.BG_MAIN)
        main.pack(fill="both", expand=True)
        
        # ===== SIDEBAR =====
        sidebar = ctk.CTkFrame(main, fg_color=Colors.PRIMARY, width=220, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Logo/Title
        logo = ctk.CTkLabel(
            sidebar,
            text="📚\nLIB-SYSTEM\nQUANG VINH",
            font=("Segoe UI", 20, "bold"),
            text_color=Colors.WHITE,
            justify="center"
        )
        logo.pack(pady=Spacing.XXL)
        
        # User info
        ctk.CTkLabel(
            sidebar,
            text=f"👤 {self.username}",
            font=Fonts.SMALL_BOLD,
            text_color=Colors.WHITE
        ).pack(pady=Spacing.MD)
        
        # Divider
        ctk.CTkFrame(sidebar, fg_color=Colors.PRIMARY_HOVER, height=1).pack(fill="x", padx=Spacing.LG, pady=Spacing.MD)
        
        # Menu buttons
        menu_buttons = [
            ("🏠 Dashboard", self.app_manager.show_main_page),
            ("👤 Quản Lý TK", self.app_manager.show_quanlytk_page),
            ("📚 Quản Lý Sách", self.app_manager.show_quanlysach_page),
            ("📤 Mượn/Trả", self.app_manager.show_muontra_page),
            ("📊 Thống Kê", self.app_manager.show_thongke_page),
            ("🚪 Đăng Xuất", self.app_manager.show_login_page),
        ]
        
        for label, command in menu_buttons:
            btn = ctk.CTkButton(
                sidebar, text=label, font=Fonts.SMALL_BOLD,
                fg_color="transparent", hover_color=Colors.PRIMARY_HOVER,
                text_color=Colors.WHITE, anchor="w",
                command=lambda cmd=command: cmd(self.username) if label == "🏠 Dashboard" else cmd()
            )
            btn.pack(fill="x", padx=Spacing.SM, pady=Spacing.XS)
        
        # ===== MAIN CONTENT =====
        content = ctk.CTkFrame(main, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True)
        
        # Header Section
        header = ctk.CTkFrame(content, fg_color=Colors.BG_SECONDARY, corner_radius=10)
        header.pack(fill="x", padx=Spacing.LG, pady=Spacing.LG)
        
        ctk.CTkLabel(
            header, text=f"👋 Xin chào, {self.username}!",
            font=Fonts.HEADER, text_color=Colors.PRIMARY
        ).pack(anchor="w", padx=Spacing.LG, pady=(Spacing.LG, 5))
        
        ctk.CTkLabel(
            header, text="Hôm nay bạn muốn quản lý nội dung nào?",
            font=Fonts.REGULAR, text_color=Colors.TEXT_SECONDARY
        ).pack(anchor="w", padx=Spacing.LG, pady=(0, Spacing.LG))
        
        # Dashboard Cards Grid
        grid = ctk.CTkFrame(content, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=Spacing.LG)

        self.create_stat_card(grid, "📚 Tổng Đầu Sách", "150", Colors.INFO).pack(side="left", fill="both", expand=True, padx=Spacing.SM)
        self.create_stat_card(grid, "👥 Thành Viên", "25", Colors.SUCCESS).pack(side="left", fill="both", expand=True, padx=Spacing.SM)
        self.create_stat_card(grid, "📤 Đang Mượn", "12", Colors.WARNING).pack(side="left", fill="both", expand=True, padx=Spacing.SM)
        self.create_stat_card(grid, "⚠️ Quá Hạn", "3", Colors.ERROR).pack(side="left", fill="both", expand=True, padx=Spacing.SM)

    def create_stat_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, fg_color=Colors.BG_SECONDARY, corner_radius=12, border_width=1, border_color=Colors.BORDER)
        
        ctk.CTkLabel(card, text=title, font=Fonts.SMALL_BOLD, text_color=Colors.TEXT_SECONDARY).pack(pady=(Spacing.LG, 5))
        ctk.CTkLabel(
            card, text=value,
            font=("Segoe UI", 32, "bold"),
            text_color=color
        ).pack(pady=(0, Spacing.LG))
        
        return card