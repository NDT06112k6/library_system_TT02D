import pandas as pd
from .base import Query

class BookData(Query):
    def __init__(self):
        """Khởi tạo thực thể quản lý kho dữ liệu sách từ cơ sở dữ liệu"""
        super().__init__("books", ["id", "ma_sach", "ten_sach", "tac_gia", "the_loai", "so_luong", "gia"])

    def get_all(self):
        """Truy vấn lấy toàn bộ danh sách sách hiện có trong hệ thống"""
        try:
            return self.list_all()
        except Exception as e:
            print(f"Lỗi lấy tất cả sách: {e}")
            return []

    def search_books(self, keyword):
        """Tìm kiếm thông tin sách dựa theo mã, tên, tác giả, thể loại"""
        try:
            by_ma = self.search("ma_sach", keyword, exact=False)
            by_ten = self.search("ten_sach", keyword, exact=False)
            by_tac_gia = self.search("tac_gia", keyword, exact=False)
            by_the_loai = self.search("the_loai", keyword, exact=False)
            
            # Gom tất cả kết quả lại và loại bỏ các dòng trùng lặp
            result = pd.concat([by_ma, by_ten, by_tac_gia, by_the_loai]).drop_duplicates()
            return result.values.tolist()
        except Exception as e:
            print(f"Lỗi tìm sách: {e}")
            return []
    def check_exists(self, ma_sach):
        """Kiểm tra sự tồn tại của đầu sách thông qua mã sách định danh"""
        try:
            result = self.search("ma_sach", ma_sach, exact=True)
            return len(result) > 0
        except Exception:
            return False

    def update_quantity(self, ma_sach, delta):
        """Cập nhật thay đổi số lượng kho sách (tăng hoặc giảm)"""
        try:
            result = self.search("ma_sach", ma_sach, exact=True)
            if not result.empty:
                sach = result.iloc[0]
                new_qty = max(0, int(sach["so_luong"]) + delta)
                new_data = {
                    "ten_sach": sach["ten_sach"],
                    "tac_gia": sach["tac_gia"],
                    "the_loai": sach["the_loai"],
                    "so_luong": new_qty,
                    "gia": sach["gia"]
                }
                self.update("ma_sach", ma_sach, new_data)
        except Exception as e:
            print(f"Lỗi cập nhật số lượng: {e}")

    def get_total_count(self):
        """Thống kê tổng số lượng đầu sách đang quản lý"""
        try:
            results = self.list_all()
            return len(results)
        except Exception:
            return 0
    
    def delete_all(self):
        """Xóa tất cả sách trong database"""
        try:
            query = "DELETE FROM books"
            self.execute_query(query)
            return True
        except Exception as e:
            print(f"Lỗi xóa dữ liệu: {str(e)}")
            return False