"""
Theme & Color Constants cho toàn ứng dụng
Thay đổi 1 chỗ → toàn ứng dụng đổi theo
"""
#Q
# ===== COLOR SCHEME =====
class Colors:
    # Primary
    PRIMARY = "#0066CC"          # Xanh dương (button chính)
    PRIMARY_HOVER = "#0052A3"    # Xanh dương đậm (hover)
    
    # Backgrounds
    BG_MAIN = "#F8FAFB"          # Xanh nhạt (background chính)
    BG_SECONDARY = "#FFFFFF"     # Trắng (card, frame)
    BG_HOVER = "#E8F0FF"         # Xanh rất nhạt (hover row)
    
    # Text
    TEXT_PRIMARY = "#1A1A1A"     # Đen (chữ chính)
    TEXT_SECONDARY = "#666666"   # Xám (chữ phụ)
    TEXT_LIGHT = "#999999"       # Xám nhạt (placeholder)
    
    # Status
    SUCCESS = "#28A745"          # Xanh lá
    WARNING = "#FFC107"          # Vàng
    ERROR = "#DC3545"            # Đỏ
    INFO = "#17A2B8"             # Xanh lơ
    
    # Borders & Dividers
    BORDER = "#E0E0E0"           # Xám nhạt
    BORDER_DARK = "#D0D0D0"      # Xám
    
    # Special
    WHITE = "#FFFFFF"
    BLACK = "#000000"


# ===== FONT SIZES =====
class FontSizes:
    XS = 10
    SM = 11
    BASE = 12
    LG = 13
    XL = 14
    XXL = 16
    TITLE = 20
    HEADER = 24


# ===== FONTS =====
class Fonts:
    # Regular text
    REGULAR = ("Segoe UI", FontSizes.BASE)
    
    # Bold text
    BOLD = ("Segoe UI", FontSizes.BASE, "bold")
    
    # Titles
    TITLE = ("Segoe UI", FontSizes.TITLE, "bold")
    HEADER = ("Segoe UI", FontSizes.HEADER, "bold")
    
    # Small
    SMALL = ("Segoe UI", FontSizes.SM)
    SMALL_BOLD = ("Segoe UI", FontSizes.SM, "bold")


# ===== PADDING/SPACING =====
class Spacing:
    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 20
    XXL = 24


# ===== SHADOWS (cho Treeview) =====
TREEVIEW_STYLE = """
    Treeview:
        background: #FFFFFF
        foreground: #1A1A1A
        fieldbackground: #FFFFFF
        bordercolor: #E0E0E0
"""