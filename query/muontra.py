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
            # 1. Truy vấn lấy mã phiếu của lượt mượn cuối cùng nhất trong database
            query = "SELECT ma_phieu FROM muontra ORDER BY id DESC LIMIT 1"
            result = self.execute_query(query)
            
            # 2. Kiểm tra xem database đã có dữ liệu phiếu nào chưa
            if result != None:
                if len(result) > 0:
                    # Lấy mã phiếu lớn nhất hiện tại (Ví dụ: "MT001")
                    last_id = result[0]['ma_phieu'] 
                    
                    # Cắt bỏ 2 ký tự đầu "MT" để lấy phần số phía sau (Ví dụ: "001")
                    number_part = last_id[2:] 
                    
                    # Chuyển chuỗi số thành số nguyên và cộng thêm 1 đơn vị
                    next_number = int(number_part) + 1 
                    
                    # Định dạng lại thành chuỗi có 3 chữ số (Ví dụ: số 2 thành "002")
                    new_id = "MT" + "{:03d}".format(next_number)
                    return new_id
                else:
                    # Nếu danh sách kết quả bằng 0 (chưa có phiếu nào)
                    return "MT001"
            else:
                # Nếu kết quả trả về rỗng (Database trống)
                return "MT001"
                
        except Exception:
            # Nếu xảy ra lỗi bất kỳ trong quá trình quét dữ liệu
            return "MT001"
    def is_currently_borrowing(self, username, ma_sach):
        """Kiểm tra xem độc giả có đang mượn cuốn sách cụ thể nào đó hay không"""
        try:    
            query = "SELECT * FROM muontra WHERE username = %s AND ma_sach = %s AND trang_thai = 'dang_muon'"
            results = self.db.fetch_all_as_dict(query, (username, ma_sach))
            return len(results) > 0
        except Exception:
            return False

    def get_status_counts(self):
        """Thống kê tổng số lượng phiếu phân loại theo từng trạng thái"""
        try:
            query = "SELECT trang_thai, COUNT(*) as count FROM muontra GROUP BY trang_thai"
            results = self.db.fetch_all_as_dict(query)
            return {item['trang_thai']: item['count'] for item in results}
        except Exception:
            return {}

    def get_top_borrowed_books(self, limit=5):
        """Thống kê danh sách sách được độc giả mượn nhiều nhất"""
        try:
            query = f"SELECT ma_sach, COUNT(*) as count FROM muontra GROUP BY ma_sach ORDER BY count DESC LIMIT %s"
            results = self.db.fetch_all_as_dict(query, (limit,))
            return [(item['ma_sach'], item['count']) for item in results]
        except Exception:
            return []

    def create_borrow_request(self, username, ma_sach):
        """Ghi nhận yêu cầu mượn sách mới từ độc giả với trạng thái chờ duyệt"""
        ma_phieu = self.generate_new_id()
        data = [ma_phieu, username, ma_sach, None, None, None, 0, "cho_duyet"]
        return self.create(data)

    def approve_borrow_request(self, ma_phieu, ngay_muon, han_tra):
        """Cập nhật trạng thái phiếu từ chờ duyệt sang đang mượn kèm thời hạn"""
        data_update = {
            "ngay_muon": ngay_muon,
            "han_tra": han_tra,
            "trang_thai": "dang_muon"
        }
        return self.update("ma_phieu", ma_phieu, data_update)