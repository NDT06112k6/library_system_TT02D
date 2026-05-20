from .base import Query
import pandas as pd
import re
from page.constants import PATH_ACCOUNTS, COL_ACCOUNTS
from page.exceptions import DuplicateEntryError

class AccountData(Query):
    def __init__(self):
        super().__init__(PATH_ACCOUNTS, COL_ACCOUNTS)

    def authenticate(self, username, password):
        """
        Xử lý xác thực đăng nhập người dùng.
        
        Args:
            username (str): Tên đăng nhập.
            password (str): Mật khẩu.
            
        Returns:
            dict: Thông tin tài khoản nếu thành công, None nếu thất bại.
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
            keyword (str): Từ khóa tìm kiếm.
            
        Returns:
            list: Danh sách các tài khoản khớp với từ khóa.
        """
        try:
            df = self._read_data()
            mask = (df["taikhoan"].str.contains(keyword, case=False) | 
                    df["hoten"].str.contains(keyword, case=False))
            return df[mask].values.tolist()
        except Exception as e:
            print(f"Lỗi tìm kiếm tài khoản: {e}")
            return []

    def get_all_accounts(self):
        """Lấy toàn bộ danh sách tài khoản dưới dạng list of lists."""
        return self.list_all()

    def delete_account(self, username):
        """Xóa tài khoản theo username."""
        return self.delete("taikhoan", username)

    def check_exists(self, username):
        """Kiểm tra sự tồn tại của username trong hệ thống."""
        try:
            return not self.search("taikhoan", username, exact=True).empty
        except Exception:
            return False

    def is_valid_gmail(self, email: str) -> bool:
        """Kiểm tra xem email có đúng định dạng @gmail.com hay không."""
        pattern = r'^[a-zA-Z0-9._%+\-]+@gmail\.com$'
        return bool(re.match(pattern, email))

    def validate_and_create(self, data: list):
        """Kiểm tra tính hợp lệ (trùng lặp) trước khi tạo tài khoản mới."""
        username = data[0]
        email = data[5]
        if self.check_exists(username):
            raise DuplicateEntryError(f"Tên đăng nhập '{username}' đã tồn tại")
        # Có thể thêm các validate khác ở đây
        return self.create(data)