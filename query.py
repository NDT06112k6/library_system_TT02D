import pandas as pd

class Query:
    """Class xử lý thao tác với file CSV bằng Pandas"""

    def __init__(self, file_path, title=[]):
        # Đường dẫn file CSV
        self.file_path = file_path
        # Danh sách cột cần lấy, nếu rỗng sẽ lấy tất cả
        self.title = title

    def list(self, page, page_size):
        """Đọc dữ liệu từ CSV và phân trang"""
        # Đọc file CSV với dtype=str để tránh lỗi kiểu dữ liệu
        data = pd.read_csv(self.file_path, dtype=str)
        # Chỉ lấy các cột được chỉ định trong title nếu có
        if self.title:
            data = data[self.title]
        # Tính chỉ số bắt đầu và kết thúc cho phân trang
        start = (page - 1) * page_size
        end = start + page_size

        # Trả về dict chứa thông tin phân trang và dữ liệu
        return {
            "page": page,
            "page_size": page_size,
            "total_records": len(data),
            "total_pages": (len(data) + page_size - 1) // page_size,
            "data": data[start:end]
        }

    def search(self, title_keyword, keyword, exact=False):
        """Tìm kiếm dữ liệu theo cột và từ khóa"""
        data = pd.read_csv(self.file_path, dtype=str)
        if self.title:
            data = data[self.title]
        
        # exact=True: khớp chính xác, exact=False: khớp một phần, không phân biệt hoa thường
        if exact:
            # Khớp chính xác, phân biệt hoa thường
            result = data[data[title_keyword].astype(str) == str(keyword)]
        else:
            # Khớp một phần, không phân biệt hoa thường
            result = data[data[title_keyword].astype(str).str.contains(keyword, case=False)]
        return result

    def delete(self, title_keyword, keyword, exact=True):
        """Xóa hàng có giá trị khớp với keyword"""
        data = pd.read_csv(self.file_path, dtype=str)
        if self.title:
            data = data[self.title]

        # Lọc bỏ hàng khớp với keyword
        if exact:
            result = data[data[title_keyword].astype(str) != str(keyword)]
        else:
            result = data[~data[title_keyword].astype(str).str.contains(keyword)]
        
        # Ghi lại file CSV
        result.to_csv(self.file_path, index=False)
        return True

    def update(self, title_keyword, keyword, new_data, exact=True):
        """Cập nhật hàng có giá trị khớp với keyword"""
        data = pd.read_csv(self.file_path, dtype=str)
        if self.title:
            data = data[self.title]

        # Tìm hàng khớp và cập nhật
        if exact:
            mask = data[title_keyword].astype(str) == str(keyword)
        else:
            mask = data[title_keyword].astype(str).str.contains(keyword)
        data.loc[mask, self.title] = new_data
        
        # Ghi lại file CSV
        data.to_csv(self.file_path, index=False)
        return True

    def create(self, new_data):
        """Thêm hàng mới vào CSV"""
        data = pd.read_csv(self.file_path, dtype=str)
        if self.title:
            data = data[self.title]
        
        # Tạo DataFrame từ dữ liệu mới
        new_row = pd.DataFrame([new_data], columns=self.title)
        # Gộp với dữ liệu cũ
        data = pd.concat([data, new_row], ignore_index=True)
        # Ghi lại file CSV
        data.to_csv(self.file_path, index=False)
        return True

    def max(self, title_keyword):
        """Lấy giá trị lớn nhất của cột"""
        data = pd.read_csv(self.file_path, dtype=str)
        if self.title:
            data = data[self.title]

        # Trả về giá trị max của cột, chuyển sang số nếu có thể
        return data[title_keyword].max()