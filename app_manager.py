import tkinter as tk
import customtkinter as ctk
from page.login import LoginPage
from page.taotk import TaoTKPage
from page.quanlytk import QuanLyTKPage
from page.suatk import SuaTKPage
from page.quanlysach import QuanLySachPage
from page.themsach import ThemSachPage
from page.suasach import SuaSachPage
from page.muontra import MuonTraPage
from page.taomuon import TaoMuonPage
from page.thongke import ThongKePage
from page.main_page import MainPage
from page.docgia import DocGiaPage


class AppManager:
    """
    Lớp quản lý ứng dụng chính.
    Quản lý luồng hiển thị, kích thước màn hình và phân quyền tài khoản (Role-based Authorization).
    """
    def __init__(self):
        """
        Khởi tạo AppManager.
        Tạo cửa sổ chính và định nghĩa biến lưu trữ quyền hạn người dùng.
        """
        self.root = ctk.CTk()
        self.root.title("Hệ Thống Quản Lý Thư Viện")
        self.root.geometry("300x200")
        
        # BIẾN PHÂN QUYỀN TOÀN CỤC: Khởi tạo rỗng, sẽ nạp khi login thành công
        self.current_user = None  # Lưu tài khoản đăng nhập (Ví dụ: "1", "Admin")
        self.current_role = None  # Lưu chức vụ (Ví dụ: "Sinh viên", "Thủ thư", "Quản lý")
        
        self.current_page = None
        self.show_login_page()

    def clear_current_page(self):
        """Xóa tất cả widget của page hiện tại để chuẩn bị chuyển giao diện"""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.current_page = None

    def login_success(self, username, chucvu, hoten=None):
        """
        Hàm trung gian bắt buộc gọi từ trang LoginPage khi người dùng đăng nhập đúng.
        Nạp thông tin phiên làm việc và chuyển vào trang Dashboard chính.
        Route theo chức vụ: Độc giả → DocGiaPage, còn lại → MainPage (admin).
        """
        self.current_user  = username
        self.current_role  = chucvu
        self.current_hoten = hoten or username
        if chucvu and chucvu.strip() in ("Độc giả", "Sinh viên", "docgia"):
            self.show_docgia_page()
        else:
            self.show_main_page(username)

    def show_login_page(self):
        """Hiển thị trang đăng nhập"""
        self.clear_current_page()
        self.root.geometry("400x480")
        # Reset lại quyền khi quay về màn hình đăng nhập
        self.current_user = None
        self.current_role = None
        self.current_page = LoginPage(self.root, self)

    def show_main_page(self, username="Admin"):
        """Hiển thị trang Dashboard chính (Menu chính)"""
        self.clear_current_page()
        self.root.geometry("1000x650")
        self.current_page = MainPage(self.root, self, username)

    def show_taotk_page(self):
        """Hiển thị trang tạo tài khoản mới"""
        self.clear_current_page()
        self.root.geometry("420x650")
        self.current_page = TaoTKPage(self.root, self)
    
    def show_register_page(self):
        """Hàm bổ trợ đồng bộ luồng gọi chuyển từ LoginPage sang trang Đăng Ký"""
        self.show_taotk_page()

    def show_quanlytk_page(self):
        """Hiển thị trang quản lý tài khoản"""
        self.clear_current_page()
        self.root.geometry("600x400")
        self.current_page = QuanLyTKPage(self.root, self)

    def show_suatk_page(self, username=None, password=None, hoten=None, sdt=None, chucvu=None, email=None):
        """Hiển thị trang sửa đổi thông tin tài khoản"""
        self.clear_current_page()
        self.root.geometry("550x750")
        self.current_page = SuaTKPage(self.root, self, username, password, hoten, sdt, chucvu, email)
    
    def show_quanlysach_page(self):
        """Hiển thị trang xem/quản lý kho sách"""
        self.clear_current_page()
        self.root.geometry("800x550")
        self.current_page = QuanLySachPage(self.root, self)

    def show_themsach_page(self):
        """Hiển thị trang nhập thêm sách mới"""
        self.clear_current_page()
        self.root.geometry("450x480")
        self.current_page = ThemSachPage(self.root, self)

    def show_suasach_page(self, ma_sach):
        """Hiển thị trang cập nhật thông tin sách"""
        self.clear_current_page()
        self.root.geometry("450x500")
        self.current_page = SuaSachPage(self.root, self, ma_sach)
    
    def show_muontra_page(self):
        """Hiển thị trang tra cứu hoặc xử lý mượn/trả"""
        self.clear_current_page()
        self.root.geometry("900x550")
        self.current_page = MuonTraPage(self.root, self)

    def show_taomuon_page(self):
        """Hiển thị trang thiết lập phiếu mượn mới"""
        self.clear_current_page()
        self.root.geometry("600x550")
        self.current_page = TaoMuonPage(self.root, self)

    def show_thongke_page(self):
        """Hiển thị trang tổng hợp số liệu báo cáo"""
        self.clear_current_page()
        self.root.geometry("900x600")
        self.current_page = ThongKePage(self.root, self)
    
    def show_docgia_page(self):
        """Hiển thị giao diện dành cho Độc giả"""
        self.clear_current_page()
        self.root.geometry("1200x750")
        self.current_page = DocGiaPage(self.root, self)

    

    def run(self):
        """Kích hoạt vòng lặp chạy ứng dụng"""
        self.root.mainloop()