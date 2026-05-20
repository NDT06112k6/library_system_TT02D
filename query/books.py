from .base import Query
import pandas as pd

class BookData(Query):
    """Lớp quản lý dữ liệu sách từ MySQL"""
    
    def __init__(self):
        # Khởi tạo với table_name = "books" và danh sách cột
        super().__init__("books", ["id", "ma_sach", "ten_sach", "tac_gia", "the_loai", "so_luong", "gia"])

    def get_all(self):
        """Lấy tất cả sách dưới dạng list."""
        try:
            results = self.list_all()
            return results
        except Exception as e:
            print(f"Lỗi lấy tất cả sách: {e}")
            return []

    def search_books(self, keyword):
        """
        Tìm kiếm sách theo tên hoặc tác giả.
        
        Args:
            keyword (str): Từ khóa tìm kiếm
            
        Returns:
            list: Danh sách sách tìm được
        """
        try:
            by_ten = self.search("ten_sach", keyword, exact=False)
            by_tac_gia = self.search("tac_gia", keyword, exact=False)
            # Gộp kết quả và loại bỏ trùng lặp
            result = pd.concat([by_ten, by_tac_gia]).drop_duplicates()
            return result.values.tolist()
        except Exception as e:
            print(f"Lỗi tìm sách: {e}")
            return []

    def check_exists(self, ma_sach):
        """
        Kiểm tra mã sách có tồn tại không.
        
        Args:
            ma_sach (str): Mã sách
            
        Returns:
            bool: True nếu tồn tại
        """
        try:
            result = self.search("ma_sach", ma_sach, exact=True)
            return len(result) > 0
        except Exception:
            return False

    def update_quantity(self, ma_sach, delta):
        """
        Cập nhật số lượng sách (tăng/giảm).
        
        Args:
            ma_sach (str): Mã sách
            delta (int): Số lượng thay đổi (âm để giảm, dương để tăng)
        """
        try:
            # Lấy thông tin sách hiện tại
            result = self.search("ma_sach", ma_sach, exact=True)
            if not result.empty:
                sach = result.iloc[0]
                # Tính số lượng mới (đảm bảo ≥ 0)
                new_qty = max(0, int(sach["so_luong"]) + delta)
                # Cập nhật toàn bộ cột (theo thứ tự self.columns)
                self.update("ma_sach", ma_sach, [
                    ma_sach,
                    sach["ten_sach"],
                    sach["tac_gia"],
                    sach["the_loai"],
                    new_qty,
                    sach["gia"]
                ])
        except Exception as e:
            print(f"Lỗi cập nhật số lượng: {e}")

    def get_total_count(self):
        """
        Lấy tổng số đầu sách.
        
        Returns:
            int: Số đầu sách
        """
        try:
            results = self.list_all()
            return len(results)
        except Exception:
            return 0