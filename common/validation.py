import re
from datetime import datetime

class Validation:
    """Lớp chứa các phương thức kiểm tra dữ liệu."""
    # Kiểm tra dữ liệu có rỗng hay không
    @staticmethod
    def is_empty(value):
        return not value or not str(value).strip()

# Kiểm tra username hợp lệ
    @staticmethod
    def is_valid_username(username):
        if Validation.is_empty(username):
            return False, "Username không được trống"
        if len(username) < 3:
            return False, "Username phải ≥ 3 ký tự"
        if len(username) > 20:
            return False, "Username phải ≤ 20 ký tự"
        return True, ""

# Kiểm tra email 
    @staticmethod
    def is_valid_email_simple(email):
        if '@' not in email or '.' not in email:
            return False, "Email không hợp lệ"
        return True, ""

# Kiểm tra số điện thoại
    @staticmethod
    def is_valid_phone(phone):
        if not phone.isdigit() or len(phone) != 10:
            return False, "SĐT phải 10 chữ số"
        if not phone.startswith('0'):
            return False, "SĐT phải bắt đầu từ 0"
        return True, ""
    
# Kiểm tra số dương
    @staticmethod
    def is_positive_number(value, field_name="Giá trị"):
        try:
            num = int(value)
            if num <= 0:
                return False, f"{field_name} phải > 0"
            return True, ""
        except:
            return False, f"{field_name} phải là số"

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
        """"Kiểm tra trường bắt buộc nhập"""
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
