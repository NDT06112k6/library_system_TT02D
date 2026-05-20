from .base import Query
import pandas as pd

class MuonTraData(Query):
    """Lớp quản lý dữ liệu mượn/trả từ MySQL"""
    
    def __init__(self):
        # Khởi tạo với table_name = "muontra"
        super().__init__("muontra", ["id", "ma_phieu", "username", "ma_sach", "ngay_muon", "ngay_tra", "trang_thai"])

    def get_all(self):
        """Lấy tất cả phiếu mượn/trả dưới dạng list."""
        try:
            results = self.list_all()
            return results
        except Exception as e:
            print(f"Lỗi lấy tất cả phiếu: {e}")
            return []

    def search_muon_tra(self, keyword):
        """
        Tìm kiếm phiếu mượn/trả theo username hoặc ma_sach.
        
        Args:
            keyword (str): Từ khóa tìm kiếm
            
        Returns:
            list: Danh sách phiếu khớp
        """
        try:
            by_user = self.search("username", keyword, exact=False)
            by_sach = self.search("ma_sach", keyword, exact=False)
            result = pd.concat([by_user, by_sach]).drop_duplicates()
            return result.values.tolist()
        except Exception as e:
            print(f"Lỗi tìm kiếm mượn trả: {e}")
            return []
    
    def confirm_return(self, ma_phieu, ngay_tra):
        """
        Xác nhận trả sách - cập nhật trạng thái và ngày trả.
        
        Args:
            ma_phieu (str): Mã phiếu
            ngay_tra (str): Ngày trả (YYYY-MM-DD)
        """
        try:
            # Lấy thông tin phiếu hiện tại
            phieu_df = self.search("ma_phieu", ma_phieu, exact=True)
            if not phieu_df.empty:
                phieu = phieu_df.iloc[0]
                # Cập nhật với trạng thái "da_tra"
                new_row = [
                    ma_phieu,
                    phieu["username"],
                    phieu["ma_sach"],
                    phieu["ngay_muon"],
                    ngay_tra,
                    "da_tra"
                ]
                self.update("ma_phieu", ma_phieu, new_row)
        except Exception as e:
            print(f"Lỗi xác nhận trả: {e}")

    def generate_new_id(self):
        """
        Sinh mã phiếu mới theo định dạng MT001, MT002, ...
        
        Returns:
            str: Mã phiếu mới
        """
        try:
            max_val = self.get_max_value("ma_phieu")
            if not max_val or pd.isna(max_val):
                return "MT001"
            # Lấy số từ max_val (ví dụ: "MT003" → 3)
            so = int(str(max_val)[2:]) + 1
            return f"MT{str(so).zfill(3)}"
        except Exception:
            return "MT001"

    def is_currently_borrowing(self, username, ma_sach):
        """
        Kiểm tra xem người dùng có đang mượn sách này không.
        
        Args:
            username (str): Tên đăng nhập
            ma_sach (str): Mã sách
            
        Returns:
            bool: True nếu đang mượn
        """
        try:
            # Query để tìm phiếu đang mượn
            query = "SELECT * FROM muontra WHERE username = %s AND ma_sach = %s AND trang_thai = 'dang_muon'"
            results = self.db.fetch_all_as_dict(query, (username, ma_sach))
            return len(results) > 0
        except Exception:
            return False

    def get_status_counts(self):
        """
        Thống kê số lượng phiếu theo trạng thái.
        
        Returns:
            dict: {'da_tra': count, 'dang_muon': count}
        """
        try:
            query = "SELECT trang_thai, COUNT(*) as count FROM muontra GROUP BY trang_thai"
            results = self.db.fetch_all_as_dict(query)
            # Chuyển thành dict {trang_thai: count}
            return {item['trang_thai']: item['count'] for item in results}
        except Exception:
            return {}

    def get_top_borrowed_books(self, limit=5):
        """
        Lấy top N sách được mượn nhiều nhất.
        
        Args:
            limit (int): Số sách top (mặc định 5)
            
        Returns:
            list: [(ma_sach, count), ...] - sorted by count descending
        """
        try:
            query = f"SELECT ma_sach, COUNT(*) as count FROM muontra GROUP BY ma_sach ORDER BY count DESC LIMIT %s"
            results = self.db.fetch_all_as_dict(query, (limit,))
            # Chuyển thành list of tuples (ma_sach, count)
            return [(item['ma_sach'], item['count']) for item in results]
        except Exception:
            return []