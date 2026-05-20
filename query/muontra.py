from .base import Query
import pandas as pd

class MuonTraData(Query):
    def __init__(self):
        super().__init__("database/muontra.csv", ["ma_phieu", "username", "ma_sach", "ngay_muon", "ngay_tra", "trang_thai"])

    def get_all(self):
        return self.list(1, 9999)["data"].values.tolist()

    def search_muon_tra(self, keyword):
        try:
            import pandas as pd
            by_user = self.search("username", keyword, exact=False)
            by_sach = self.search("ma_sach", keyword, exact=False)
            return pd.concat([by_user, by_sach]).drop_duplicates().values.tolist()
        except Exception as e:
            print(f"Lỗi tìm kiếm mượn trả: {e}")
            return []
    
    def confirm_return(self, ma_phieu, ngay_tra):
        """Cập nhật trạng thái 'đã trả' và ngày trả cho một mã phiếu cụ thể."""
        try:
            phieu = self.search("ma_phieu", ma_phieu, exact=True).iloc[0]
            new_row = [ma_phieu, phieu["username"], phieu["ma_sach"], phieu["ngay_muon"], ngay_tra, "da_tra"]
            self.update("ma_phieu", ma_phieu, new_row)
        except Exception as e:
            print(f"Lỗi xác nhận trả: {e}")

    def generate_new_id(self):
        """Tự động sinh mã phiếu mượn mới theo định dạng MTxxx."""
        try:
            max_val = self.get_max_value("ma_phieu")
            if not max_val or pd.isna(max_val):
                return "MT001"
            so = int(str(max_val)[2:]) + 1
            return f"MT{str(so).zfill(3)}"
        except Exception:
            return "MT001"

    def is_currently_borrowing(self, username, ma_sach):
        """Kiểm tra xem một người dùng có đang mượn một quyển sách cụ thể mà chưa trả hay không."""
        try:
            df = self._read_data()
            mask = (df["username"] == username) & (df["ma_sach"] == ma_sach) & (df["trang_thai"] == "dang_muon")
            return len(df[mask]) > 0
        except Exception:
            return False

    def get_status_counts(self):
        """Thống kê số lượng phiếu theo các trạng thái (đang mượn, đã trả)."""
        try:
            df = self._read_data()
            return df["trang_thai"].value_counts().to_dict()
        except Exception:
            return {}

    def get_top_borrowed_books(self, limit=5):
        """Lấy danh sách các mã sách được mượn nhiều nhất."""
        df = self._read_data()
        if df.empty: return []
        counts = df["ma_sach"].value_counts().head(limit)
        return list(counts.items())