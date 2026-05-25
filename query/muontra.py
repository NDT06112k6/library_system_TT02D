import pandas as pd
from .base import Query

class MuonTraData(Query):
    def __init__(self):
        """Khởi tạo thực thể quản lý dữ liệu phiếu mượn/trả thư viện"""
        super().__init__("muontra", [
            "id", "ma_phieu", "username", "ma_sach", 
            "ngay_muon", "han_tra", "ngay_tra", "tien_phat", "trang_thai"
        ])

    def get_all(self):
        """Truy vấn tất cả các bản ghi phiếu mượn trả từ cơ sở dữ liệu"""
        try:
            return self.list_all()
        except Exception as e:
            print(f"Lỗi lấy tất cả phiếu: {e}")
            return []

    def search_muon_tra(self, keyword):
        """Tìm kiếm thông tin phiếu mượn trả theo tên người dùng hoặc mã sách"""
        try:
            by_user = self.search("username", keyword, exact=False)
            by_sach = self.search("ma_sach", keyword, exact=False)
            result = pd.concat([by_user, by_sach]).drop_duplicates()
            return result.values.tolist()
        except Exception as e:
            print(f"Lỗi tìm kiếm mượn trả: {e}")
            return []

    def confirm_return(self, ma_phieu, ngay_tra):
        """Xác nhận hoàn trả sách và cập nhật ngày trả cho phiếu mượn"""
        try:
            phieu_df = self.search("ma_phieu", ma_phieu, exact=True)
            if not phieu_df.empty:
                phieu = phieu_df.iloc[0]
                new_data = {
                    "username": phieu["username"],
                    "ma_sach": phieu["ma_sach"],
                    "ngay_muon": phieu["ngay_muon"],
                    "ngay_tra": ngay_tra,
                    "trang_thai": "da_tra"
                }
                self.update("ma_phieu", ma_phieu, new_data)
        except Exception as e:
            print(f"Lỗi xác nhận trả: {e}")

    def generate_new_id(self):
        """Hàm sinh mã phiếu mượn mới tăng dần tường minh"""
        try:
            query = "SELECT ma_phieu FROM muontra ORDER BY id DESC LIMIT 1"
            result = self.thuc_thi_query(query)
            if result is not None and len(result) > 0:
                last_id = result[0]['ma_phieu']
                next_number = int(last_id[2:]) + 1
                return "MT" + "{:03d}".format(next_number)
            return "MT001"
        except Exception:
            return "MT001"

    def Sach_Dang_Muon(self, username, ma_sach):
        """Kiểm tra xem độc giả có đang mượn cuốn sách cụ thể nào đó hay không"""
        try:
            result = self.thuc_thi_query(
                "SELECT COUNT(*) as cnt FROM muontra WHERE username = %s AND ma_sach = %s AND trang_thai = 'dang_muon'",
                (username, ma_sach)
            )
            return result[0]["cnt"] > 0 if result else False
        except Exception:
            return False

    def get_status_counts(self):
        """Thống kê tổng số lượng phiếu phân loại theo từng trạng thái"""
        try:
            result = self.thuc_thi_query(
                "SELECT trang_thai, COUNT(*) as count FROM muontra GROUP BY trang_thai"
            )
            return {item['trang_thai']: item['count'] for item in result} if result else {}
        except Exception:
            return {}

    def get_top_borrowed_books(self, limit=5):
        """Thống kê danh sách sách được độc giả mượn nhiều nhất"""
        try:
            result = self.thuc_thi_query(
                "SELECT ma_sach, COUNT(*) as count FROM muontra GROUP BY ma_sach ORDER BY count DESC LIMIT %s",
                (limit,)
            )
            return [(r['ma_sach'], r['count']) for r in result] if result else []
        except Exception:
            return []

    def Tao_Yeu_Cau_Muon(self, username, ma_sach):
        """Ghi nhận yêu cầu mượn sách mới từ độc giả với trạng thái chờ duyệt"""
        ma_phieu = self.generate_new_id()
        data = [ma_phieu, username, ma_sach, None, None, None, 0, "cho_duyet"]
        return self.create(data)

    def Yeu_Cau_Phe_Duyet(self, ma_phieu, ngay_muon, han_tra):
        """Cập nhật trạng thái phiếu từ chờ duyệt sang đang mượn kèm thời hạn"""
        data_update = {
            "ngay_muon": ngay_muon,
            "han_tra": han_tra,
            "trang_thai": "dang_muon"
        }
        return self.update("ma_phieu", ma_phieu, data_update)

    def delete_phieu(self, ma_phieu):
        """Xóa vĩnh viễn một phiếu mượn khỏi cơ sở dữ liệu."""
        conn = self.connect()
        if not conn:
            return False, "Không thể kết nối CSDL."
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM muontra WHERE ma_phieu = %s", (ma_phieu,))
            conn.commit()
            if cursor.rowcount > 0:
                return True, "Đã xóa thành công."
            return False, "Không tìm thấy phiếu cần xóa."
        except Exception as e:
            conn.rollback()
            return False, f"Lỗi SQL: {e}"
        finally:
            cursor.close()
            self.close()