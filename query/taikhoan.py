import email

from .base import Query
import pandas as pd
import re
from page.constants import PATH_ACCOUNTS, COL_ACCOUNTS
from page.exceptions import DuplicateEntryError

class AccountData(Query):
    """Lớp quản lý dữ liệu tài khoản từ MySQL"""
    
    def __init__(self):
        # Khởi tạo với table_name = "taikhoan"
        super().__init__("taikhoan", ["id", "taikhoan", "matkhau", "hoten", "sdt", "chucvu", "email"])

    def authenticate(self, username, password):
        """
        Xác thực đăng nhập người dùng.
        
        Args:
            username (str): Tên đăng nhập
            password (str): Mật khẩu
            
        Returns:
            dict: Thông tin tài khoản nếu thành công, None nếu thất bại
        """
        try:
            res = self.search("taikhoan", username, exact=True)
            if not res.empty and res.iloc[0]["matkhau"] == password:
                return res.iloc[0].to_dict()
        except Exception as e:
            print(f"Lỗi xác thực: {e}")
        return None

    def search_accounts(self, keyword):
        """
        Tìm kiếm tài khoản theo tên đăng nhập hoặc họ tên.
        
        Args:
            keyword (str): Từ khóa tìm kiếm
            
        Returns:
            list: Danh sách tài khoản khớp
        """
        try:
            # Tìm kiếm theo taikhoan
            by_username = self.search("taikhoan", keyword, exact=False)
            # Tìm kiếm theo hoten
            by_hoten = self.search("hoten", keyword, exact=False)
            # Gộp và loại bỏ trùng lặp
            result = pd.concat([by_username, by_hoten]).drop_duplicates()
            return result.values.tolist()
        except Exception as e:
            print(f"Lỗi tìm kiếm tài khoản: {e}")
            return []

    def get_all_accounts(self):
        """Lấy tất cả tài khoản dưới dạng list."""
        try:
            return self.list_all()
        except Exception as e:
            print(f"Lỗi lấy tất cả tài khoản: {e}")
            return []

    def delete_account(self, username):
        """
        Xóa tài khoản theo username.
        
        Args:
            username (str): Tên đăng nhập cần xóa
            
        Returns:
            bool: True nếu xóa thành công
        """
        return self.delete("taikhoan", username)

    def check_exists(self, username):
        """
        Kiểm tra tài khoản có tồn tại không.
        
        Args:
            username (str): Tên đăng nhập
            
        Returns:
            bool: True nếu tồn tại
        """
        try:
            result = self.search("taikhoan", username, exact=True)
            return not result.empty
        except Exception:
            return False

    def is_valid_gmail(self, email: str) -> bool:
        """
        Kiểm tra email có đúng định dạng @gmail.com không.
        
        Args:
            email (str): Email cần kiểm tra
            
        Returns:
            bool: True nếu hợp lệ
        """
        pattern = r'^[a-zA-Z0-9._%+\-]+@gmail\.com$'
        return bool(re.match(pattern, email))

    def validate_and_create(self, data: list):
        """
        Kiểm tra tính hợp lệ trước khi tạo tài khoản.
        
        Args:
            data (list): [taikhoan, matkhau, hoten, sdt, chucvu, email]
            
        Returns:
            bool: True nếu tạo thành công
            
        Raises:
            DuplicateEntryError: Nếu tên đăng nhập đã tồn tại
        """
        username = data[0]
        if self.check_exists(username):
            raise DuplicateEntryError(f"Tên đăng nhập '{username}' đã tồn tại")
        return self.create(data)
    
