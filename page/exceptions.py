class Loi_Du_Lieu_Thu_Vien(Exception):
    """Lỗi chung cho tầng dữ liệu"""
    pass

class Khong_Tim_Thay_Du_Lieu(Loi_Du_Lieu_Thu_Vien):
    """Không tìm thấy bản ghi"""
    pass

class Nhap_Lieu_Trung_Lap(Loi_Du_Lieu_Thu_Vien):
    """Trùng lặp khóa chính (Username, Mã sách)"""
    pass
