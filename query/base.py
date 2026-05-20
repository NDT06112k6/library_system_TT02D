import pandas as pd
from typing import List, Dict, Any, Optional
from abc import ABC
from database.mysql_handler import MySQLHandler

class Query(ABC):
    """Lớp cơ sở xử lý thao tác với MySQL Database"""
    
    def __init__(self, table_name: str, columns: List[str]):
        """
        Khởi tạo Query.
        
        Args:
            table_name (str): Tên bảng MySQL
            columns (list): Danh sách tên cột
        """
        self.table_name = table_name
        self.columns = columns
        self.db = MySQLHandler()
        self.db.connect()

    def list(self, page: int = 1, page_size: int = 9999) -> Dict[str, Any]:
        """
        Lấy dữ liệu với phân trang.
        
        Args:
            page (int): Số trang hiện tại
            page_size (int): Số bản ghi trên 1 trang
            
        Returns:
            dict: {'page', 'page_size', 'total_records', 'data'}
        """
        # Lấy tổng số bản ghi
        total_query = f"SELECT COUNT(*) as count FROM {self.table_name}"
        result = self.db.fetch_one(total_query)
        total_records = result[0] if result else 0
        
        # Lấy dữ liệu với LIMIT
        offset = (page - 1) * page_size
        query = f"SELECT * FROM {self.table_name} LIMIT %s OFFSET %s"
        data = self.db.fetch_all_as_dict(query, (page_size, offset))
        
        return {
            "page": page,
            "page_size": page_size,
            "total_records": total_records,
            "data": data
        }

    def list_all(self) -> List[List[Any]]:
        """Lấy toàn bộ dữ liệu dưới dạng list."""
        query = f"SELECT * FROM {self.table_name}"
        results = self.db.fetch_all(query)
        return results

    def search(self, column: str, keyword: str, exact: bool = False) -> pd.DataFrame:
        """
        Tìm kiếm dữ liệu.
        
        Args:
            column (str): Tên cột tìm kiếm
            keyword (str): Từ khóa tìm kiếm
            exact (bool): Tìm khớp hoàn toàn hay chứa từ khóa
            
        Returns:
            pd.DataFrame: Kết quả tìm kiếm
        """
        if exact:
            query = f"SELECT * FROM {self.table_name} WHERE {column} = %s"
            results = self.db.fetch_all_as_dict(query, (keyword,))
        else:
            query = f"SELECT * FROM {self.table_name} WHERE {column} LIKE %s"
            results = self.db.fetch_all_as_dict(query, (f"%{keyword}%",))
        
        # Chuyển thành DataFrame để tương thích với code cũ
        return pd.DataFrame(results)

    def add(self, new_row_data: List[Any]) -> bool:
        """
        Thêm bản ghi mới.
        
        Args:
            new_row_data (list): Dữ liệu mới [col1, col2, ...]
            
        Returns:
            bool: True nếu thành công
        """
        placeholders = ", ".join(["%s"] * len(self.columns))
        query = f"INSERT INTO {self.table_name} ({', '.join(self.columns)}) VALUES ({placeholders})"
        return self.db.execute_query(query, tuple(new_row_data))

    def create(self, new_row_data: List[Any]) -> bool:
        """Alias cho add()."""
        return self.add(new_row_data)

    def update(self, id_column: str, id_value: Any, updated_row_data: List[Any]) -> bool:
        """
        Cập nhật bản ghi.
        
        Args:
            id_column (str): Tên cột ID (khóa chính)
            id_value (any): Giá trị ID cần update
            updated_row_data (list): Dữ liệu mới [col1, col2, ...]
            
        Returns:
            bool: True nếu thành công
        """
        set_clause = ", ".join([f"{col} = %s" for col in self.columns])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {id_column} = %s"
        params = tuple(updated_row_data) + (id_value,)
        return self.db.execute_query(query, params)

    def delete(self, id_column: str, id_value: Any) -> bool:
        """
        Xóa bản ghi.
        
        Args:
            id_column (str): Tên cột ID
            id_value (any): Giá trị ID cần xóa
            
        Returns:
            bool: True nếu thành công
        """
        query = f"DELETE FROM {self.table_name} WHERE {id_column} = %s"
        return self.db.execute_query(query, (id_value,))

    def get_max_value(self, column: str) -> Optional[Any]:
        """
        Lấy giá trị lớn nhất của cột.
        
        Args:
            column (str): Tên cột
            
        Returns:
            any: Giá trị max hoặc None
        """
        query = f"SELECT MAX({column}) as max_value FROM {self.table_name}"
        result = self.db.fetch_one(query)
        return result[0] if result else None