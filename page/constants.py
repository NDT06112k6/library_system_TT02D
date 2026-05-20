import os

DB_DIR = "database"

PATH_BOOKS = os.path.join(DB_DIR, "books.csv")
PATH_ACCOUNTS = os.path.join(DB_DIR, "tk.csv")
PATH_MUONTRA = os.path.join(DB_DIR, "muontra.csv")

COL_BOOKS = ["ma_sach", "ten_sach", "tac_gia", "the_loai", "so_luong", "gia"]
COL_ACCOUNTS = ["taikhoan", "matkhau", "hoten", "sdt", "chucvu", "email"]
COL_MUONTRA = ["ma_phieu", "username", "ma_sach", "ngay_muon", "ngay_tra", "trang_thai"]