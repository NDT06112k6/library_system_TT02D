import re
from datetime import datetime

class Validation:
    """
    Lớp chứa các phương thức kiểm tra dữ liệu.
    """
    @staticmethod
    def validate_email(email):
        """"Kiểm tra email hợp lệ"""
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, email):
            return False, "Email không hợp lệ (ví dụ: user@example.com)"
        return True, ""

    @staticmethod
    def validate_date(date_str):
        """"Kiểm tra ngày tháng hợp lệ (dd/mm/yyyy)"""
        pattern = r'^\d{2}/\d{2}/\d{4}$'
        if not re.match(pattern, date_str):
            return False, "Ngày tháng phải có định dạng dd/mm/yyyy (ví dụ: 20/04/2026)"
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True, ""
        except ValueError:
            return False, "Ngày tháng không hợp lệ (kiểm tra ngày, tháng, năm)"

    @staticmethod
    def validate_required(value, field_name):
        """"Kiểm tra trường bắt buộc"""
        if not value or value.strip() == "":
            return False, f"{field_name} không được để trống"
        return True, ""

    @staticmethod
    def validate_positive_integer(value, field_name):
        """"Kiểm tra số nguyên dương"""
        try:
            num = int(value)
            if num <= 0:
                return False, f"{field_name} phải là số nguyên dương"
            return True, ""
        except ValueError:
            return False, f"{field_name} phải là số nguyên"
