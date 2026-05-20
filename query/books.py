from .base import Query

class BookData(Query):
    def __init__(self):
        super().__init__("database/books.csv", ["ma_sach", "ten_sach", "tac_gia", "the_loai", "so_luong", "gia"])

    def get_all(self):
        return self.list(1, 9999)["data"].values.tolist()

    def search_books(self, keyword):
        try:
            import pandas as pd
            by_ten = self.search("ten_sach", keyword, exact=False)
            by_tac_gia = self.search("tac_gia", keyword, exact=False)
            return pd.concat([by_ten, by_tac_gia]).drop_duplicates().values.tolist()
        except Exception as e:
            print(f"Lỗi tìm sách: {e}")
            return []

    def check_exists(self, ma_sach):
        """Kiểm tra mã sách đã tồn tại trong database chưa."""
        try:
            return len(self.search("ma_sach", ma_sach, exact=True)) > 0
        except Exception:
            return False

    def update_quantity(self, ma_sach, delta):
        """Cập nhật số lượng sách (tăng hoặc giảm) dựa trên mã sách."""
        try:
            res = self.search("ma_sach", ma_sach, exact=True)
            if not res.empty:
                sach = res.iloc[0]
                new_qty = str(max(0, int(sach["so_luong"]) + delta))
                self.update("ma_sach", ma_sach, [ma_sach, sach["ten_sach"], sach["tac_gia"], sach["the_loai"], new_qty, sach["gia"]])
        except Exception as e:
            print(f"Lỗi cập nhật số lượng: {e}")

    def get_total_count(self):
        """Trả về tổng số đầu sách có trong thư viện."""
        try:
            return len(self._read_data())
        except Exception:
            return 0