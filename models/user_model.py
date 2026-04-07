import csv
import os

DB_PATH = "database/acc.csv"

def get_all_users():
    """Đọc tất cả tài khoản từ CSV"""
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return [row for row in csv.reader(f) if len(row) >= 2]

def find_user(username, password):
    """Tìm user theo username và password"""
    for row in get_all_users():
        if row[0] == username and row[1] == password:
            return True
    return False

def username_exists(username):
    """Kiểm tra username đã tồn tại chưa"""
    return any(row[0] == username for row in get_all_users())

def add_user(username, password):
    """Thêm tài khoản mới"""
    with open(DB_PATH, "a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow([username, password])

def delete_user(username):
    """Xóa tài khoản theo username"""
    rows = [r for r in get_all_users() if r[0] != username]
    _write_all(rows)

def update_user(old_username, new_username, new_password):
    """Cập nhật tài khoản"""
    rows = []
    for r in get_all_users():
        if r[0] == old_username:
            rows.append([new_username, new_password])
        else:
            rows.append(r)
    _write_all(rows)

def _write_all(rows):
    """Ghi toàn bộ dữ liệu vào CSV"""
    with open(DB_PATH, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)