"""
query/docgia.py
Lớp truy vấn dành riêng cho nghiệp vụ độc giả:
  - Tìm/lọc sách
  - Kiểm tra điều kiện mượn
  - Tạo phiếu mượn
  - Xem lịch sử mượn cá nhân
"""
from .base import Query
MAX_BORROW = 5          # Giới hạn số sách mượn đồng thời
BORROW_DAYS = 14        # Số ngày cho phép mượn
#V

class DocGiaQuery(Query):
    """Xử lý toàn bộ truy vấn cho giao diện độc giả."""

    #  SÁCH 

    def get_all_books(self):
        """Lấy toàn bộ sách cùng thông tin cần thiết cho card"""
        query = """
            SELECT ma_sach, ten_sach, tac_gia, the_loai, so_luong, gia
            FROM books
            ORDER BY ten_sach
        """
        return self.thuc_thi_query(query) or []

    def search_books(self, keyword: str, the_loai: str = None, sort: str = "az"):
        """
        Tìm sách theo từ khoá (tên / tác giả / thể loại) + filter + sắp xếp
        """
        conditions = []
        params = []

        if keyword:
            conditions.append(
                "(ten_sach LIKE %s OR tac_gia LIKE %s OR the_loai LIKE %s)"
            )
            kw = f"%{keyword}%"
            params += [kw, kw, kw]

        if the_loai and the_loai != "Tất cả":
            conditions.append("the_loai = %s")
            params.append(the_loai)

        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

        order = {
            "az":        "ten_sach ASC",
            "popular":   "(SELECT COUNT(*) FROM muontra m WHERE m.ma_sach = b.ma_sach) DESC",
            "available": "so_luong DESC",
            "newest":    "b.id DESC",
        }.get(sort, "ten_sach ASC")

        query = f"""
            SELECT b.ma_sach, b.ten_sach, b.tac_gia, b.the_loai, b.so_luong, b.gia
            FROM books b
            {where}
            ORDER BY {order}
        """
        return self.thuc_thi_query(query, params or None) or []

    def lay_danh_muc(self):
        """Lấy danh sách thể loại để fill vào filter."""
        result = self.thuc_thi_query("SELECT DISTINCT the_loai FROM books ORDER BY the_loai")
        return [r["the_loai"] for r in result if r["the_loai"]] if result else []

    def lay_chi_tiet_sach(self, ma_sach: str):
        """Lấy thông tin chi tiết 1 cuốn sách."""
        result = self.thuc_thi_query(
            "SELECT * FROM books WHERE ma_sach = %s", (ma_sach,)
        )
        return result[0] if result else None

    def lay_so_luong_muon(self, ma_sach: str) -> int:
        """Đếm tổng số lần sách được mượn (dùng cho badge 'Phổ biến')."""
        result = self.thuc_thi_query(
            "SELECT COUNT(*) as cnt FROM muontra WHERE ma_sach = %s", (ma_sach,)
        )
        return result[0]["cnt"] if result else 0

    # MƯỢN SÁCH 
    def dem_so_luot_muon(self, username: str) -> int:
        """Đếm số phiếu đang mượn (chưa trả + chờ duyệt) của user."""
        result = self.thuc_thi_query(
            """SELECT COUNT(*) as cnt FROM muontra
               WHERE username = %s AND trang_thai IN ('dang_muon', 'cho_duyet')""",
            (username,)
        )
        return result[0]["cnt"] if result else 0

    def sach_dang_muon(self, username: str, ma_sach: str) -> bool:
        """Kiểm tra user có đang giữ cuốn sách này không."""
        result = self.thuc_thi_query(
            """SELECT COUNT(*) as cnt FROM muontra
               WHERE username = %s AND ma_sach = %s
                 AND trang_thai IN ('dang_muon', 'cho_duyet')""",
            (username, ma_sach)
        )
        return (result[0]["cnt"] if result else 0) > 0

    def lay_so_luong_sach(self, ma_sach: str) -> int:
        """Lấy số lượng tồn kho."""
        result = self.thuc_thi_query(
            "SELECT so_luong FROM books WHERE ma_sach = %s", (ma_sach,)
        )
        return result[0]["so_luong"] if result else 0

    def _next_ma_phieu(self) -> str:
        """Sinh mã phiếu tăng dần, ví dụ MT001 → MT002."""
        result = self.thuc_thi_query(
            "SELECT ma_phieu FROM muontra ORDER BY id DESC LIMIT 1"
        )
        if result:
            try:
                return "MT" + "{:03d}".format(int(result[0]["ma_phieu"][2:]) + 1)
            except Exception:
                pass
        return "MT001"

    def tao_phieu_muon(self, username: str, ma_sach: str):
        """
        Tạo phiếu mượn với trạng thái 'cho_duyet'.
        Tồn kho KHÔNG giảm ở đây — chỉ giảm khi quản lý duyệt.
        Trả về (True, ma_phieu, None) hoặc (False, error_message, None).
        """
        # --- Kiểm tra điều kiện ---
        so_luong = self.lay_so_luong_sach(ma_sach)
        if so_luong <= 0:
            return False, "Sách đã hết, không thể gửi yêu cầu mượn.", None

        if self.sach_dang_muon(username, ma_sach):
            return False, "Bạn đã có yêu cầu hoặc đang mượn cuốn sách này rồi.", None

        active = self.dem_so_luot_muon(username)
        if active >= MAX_BORROW:
            return False, f"Bạn đang có {active}/{MAX_BORROW} yêu cầu/phiếu mượn. Hãy trả bớt trước.", None

        # --- Tạo phiếu chờ duyệt ---
        ma_phieu = self._next_ma_phieu()

        conn = self.connect()
        if not conn:
            return False, "Không kết nối được cơ sở dữ liệu.", None

        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO muontra (ma_phieu, username, ma_sach, trang_thai)
                   VALUES (%s, %s, %s, 'cho_duyet')""",
                (ma_phieu, username, ma_sach)
            )
            conn.commit()
            return True, ma_phieu, None
        except Exception as e:
            conn.rollback()
            return False, f"Lỗi tạo phiếu: {e}", None
        finally:
            cursor.close()
            self.close()

    # LỊCH SỬ 

    def lay_lich_su_muon(self, username: str):
        """
        Lấy lịch sử mượn của user kèm tên sách, tác giả, thể loại
        """
        return self.thuc_thi_query(
            """SELECT m.ma_phieu, m.ma_sach, b.ten_sach, b.tac_gia, b.the_loai,
                      m.ngay_muon, m.ngay_tra, m.trang_thai
               FROM muontra m
               JOIN books b ON m.ma_sach = b.ma_sach
               WHERE m.username = %s
               ORDER BY m.id DESC""",
            (username,)
        ) or []