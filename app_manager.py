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
    """Lớp quản lý toàn bộ ứng dụng"""

    # HÀM KHỞI TẠO
    def __init__(self):
        """Khởi tạo ứng dụng"""

        self.root = ctk.CTk()
        self.root.title("Hệ Thống Quản Lý Thư Viện")
        self.root.geometry("300x200")
        self.current_user = None  
        self.current_role = None  
        self.current_page = None
        self.Hien_Thi_Trang_Dang_Nhap()  

    # XÓA PAGE HIỆN TẠI 
    def Xoa_Trang_Hien_Tai(self): 
        """Xóa tất cả widget của page hiện tại để chuẩn bị chuyển giao diện"""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.current_page = None


    # XỬ LÝ ĐĂNG NHẬP THÀNH CÔNG
    def Dang_Nhap_Thanh_Cong(self, username, chucvu, hoten=None): 
        """Hàm được gọi sau khi login thành công"""
        self.current_user  = username
        self.current_role  = chucvu
        self.current_hoten = hoten or username

        # PHÂN QUYỀN GIAO DIỆN
        if chucvu and chucvu.strip() in ("Độc giả", "docgia"):
            self.Hien_Thi_Trang_Doc_Gia()
        else:
            self.Hien_Thi_Trang_Chinh(username)

    # TRANG ĐĂNG NHẬP
    def Hien_Thi_Trang_Dang_Nhap(self): 
        """Hiển thị trang đăng nhập"""
        self.Xoa_Trang_Hien_Tai()
        self.root.geometry("400x480")
        # Reset lại quyền khi quay về màn hình đăng nhập
        self.current_user = None
        self.current_role = None
        self.current_page = LoginPage(self.root, self)

    # TRANG CHÍNH ĐỘC GIẢ # Giữ nguyên comment
    def Hien_Thi_Trang_Chinh(self, username="Admin"): 
        """Hiển thị trang Dashboard chính (Menu chính)"""
        self.Xoa_Trang_Hien_Tai()
        self.root.geometry("1000x650")
        self.current_page = MainPage(self.root, self, username)

    # TRANG TẠO TÀI KHOẢN
    def Hien_Thi_Trang_Tao_TK(self, is_admin=False): 
        """Hiển thị trang tạo tài khoản mới"""
        self.Xoa_Trang_Hien_Tai()
        self.root.geometry("420x650")
        self.current_page = TaoTKPage(self.root, self, is_admin=is_admin)
    
    # TRANG ĐĂNG KÝ
    def Hien_Thi_Trang_Dang_Ky(self):
        """Hàm bổ trợ đồng bộ luồng gọi chuyển từ LoginPage sang trang Đăng Ký"""
        self.Hien_Thi_Trang_Tao_TK()

    # TRANG QUẢN LÝ TÀI KHOẢN
    def Hien_Thi_Trang_Quan_Ly_TK(self): 
        """Hiển thị trang quản lý tài khoản"""
        self.Xoa_Trang_Hien_Tai()
        self.root.geometry("600x400")
        self.current_page = QuanLyTKPage(self.root, self)

    # TRANG SỬA TÀI KHOẢN
    def Hien_Thi_Trang_Sua_TK(self, username=None, password=None, hoten=None, sdt=None, chucvu=None, email=None): 
        """Hiển thị trang sửa đổi thông tin tài khoản"""
        self.Xoa_Trang_Hien_Tai()
        self.root.geometry("550x750")
        self.current_page = SuaTKPage(self.root, self, username, password, hoten, sdt, chucvu, email)
    
    # TRANG QUẢN LÝ SÁCH
    def Hien_Thi_Trang_Quan_Ly_Sach(self): 
        """Hiển thị trang xem/quản lý kho sách"""
        self.Xoa_Trang_Hien_Tai()
        self.root.geometry("800x550")
        self.current_page = QuanLySachPage(self.root, self)

    # TRANG THÊM SÁCH
    def Hien_Thi_Trang_Them_Sach(self): 
        """Hiển thị trang nhập thêm sách mới"""
        self.Xoa_Trang_Hien_Tai()
        self.root.geometry("450x480")
        self.current_page = ThemSachPage(self.root, self)

    # TRANG SỬA SÁCH
    def Hien_Thi_Trang_Sua_Sach(self, ma_sach): 
        """Hiển thị trang cập nhật thông tin sách"""
        self.Xoa_Trang_Hien_Tai()
        self.root.geometry("450x500")
        self.current_page = SuaSachPage(self.root, self, ma_sach)
    
    # TRANG MƯỢN/TRẢ
    def show_muontra_page(self):
        """Hiển thị trang tra cứu hoặc xử lý mượn/trả"""
        self.Xoa_Trang_Hien_Tai()
        self.root.geometry("900x550")
        self.current_page = MuonTraPage(self.root, self)

    # TRANG TẠO PHIẾU MƯỢN   
    def Hien_Thi_Trang_Tao_Muon(self): 
        """Hiển thị trang thiết lập phiếu mượn mới"""
        self.Xoa_Trang_Hien_Tai()
        self.root.geometry("600x550")
        self.current_page = TaoMuonPage(self.root, self)

    # TRANG THỐNG KÊ
    def Hien_Thi_Trang_Thong_Ke(self):
        """Hiển thị trang tổng hợp số liệu báo cáo"""
        self.Xoa_Trang_Hien_Tai()
        self.root.geometry("900x600")
        self.current_page = ThongKePage(self.root, self)
    
    # TRANG ĐỘC GIẢ
    def Hien_Thi_Trang_Doc_Gia(self): 
        """Hiển thị giao diện dành cho Độc giả"""
        self.Xoa_Trang_Hien_Tai()
        self.root.geometry("1200x750")
        self.current_page = DocGiaPage(self.root, self)

    def run(self):
        """Kích hoạt vòng lặp chạy ứng dụng"""
        self.root.mainloop()