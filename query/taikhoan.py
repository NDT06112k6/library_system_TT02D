from .base import Query
import pandas as pd
import re
from page.exceptions import Nhap_Lieu_Trung_Lap

class AccountData(Query):
    def __init__(self):
        """Khởi tạo thực thể quản lý dữ liệu tài khoản thư viện"""
        super().__init__("taikhoan", ["id", "taikhoan", "matkhau", "hoten", "sdt", "chucvu", "email"])

    def authenticate(self, username, password):
        """Xác thực thông tin đăng nhập của người dùng"""
        try:
            res = self.search("taikhoan", username, exact=True)
            if not res.empty and res.iloc[0]["matkhau"] == password:
                return res.iloc[0].to_dict()
        except Exception as e:
            print(f"Lỗi xác thực: {e}")
        return None

    def search_accounts(self, keyword):
        """Tìm kiếm danh sách tài khoản theo từ khóa đầu vào"""
        try:
            by_username = self.search("taikhoan", keyword, exact=False)
            by_hoten = self.search("hoten", keyword, exact=False)
            result = pd.concat([by_username, by_hoten]).drop_duplicates()
            return result.values.tolist()
        except Exception as e:
            print(f"Lỗi tìm kiếm tài khoản: {e}")
            return []

    def get_all_accounts(self):
        """Truy vấn toàn bộ danh sách tài khoản hệ thống"""
        try:
            return self.list_all()
        except Exception as e:
            print(f"Lỗi lấy tất cả tài khoản: {e}")
            return []

    def Xoa_Tai_Khoan(self, username):
        """Thực hiện xóa một tài khoản ra khỏi hệ thống"""
        return self.delete("taikhoan", username)

    def check_exists(self, username):
        """Kiểm tra trạng thái tồn tại của một tên đăng nhập"""
        try:
            result = self.search("taikhoan", username, exact=True)
            return not result.empty
        except Exception:
            return False

    def is_valid_gmail(self, email: str) -> bool:
        """Kiểm tra tính hợp lệ định dạng thư điện tử Gmail"""
        pattern = r'^[a-zA-Z0-9._%+\-]+@gmail\.com$'
        return bool(re.match(pattern, email))

    def validate_and_create(self, data: list):
        """Kiểm tra điều kiện ràng buộc dữ liệu trước khi tiến hành tạo tài khoản mới"""
        username = data[0]
        if self.check_exists(username):
            raise Nhap_Lieu_Trung_Lap(f"Tên đăng nhập '{username}' đã tồn tại")
        return self.create(data)