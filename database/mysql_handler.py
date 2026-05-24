import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any, Optional

class MySQLHandler:
    """
    Lớp xử lý kết nối và thao tác với MySQL Database.
    """
    
    def __init__(self, host: str = "localhost", user: str = "root", 
                 password: str = "root", database: str = "library_system"):
        """
        Khởi tạo MySQL Handler.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self) -> bool:
        """
        Kết nối tới MySQL database.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci',
                use_unicode=True
            )
            # Đảm bảo session sử dụng utf8mb4 để tránh lỗi hiển thị ???
            cursor = self.connection.cursor()
            cursor.execute("SET NAMES utf8mb4")
            cursor.close()
            if self.connection.is_connected():
                print(f"✓ Kết nối MySQL thành công: {self.database}")
                return True
        except Error as e:
            print(f"✗ Lỗi kết nối MySQL: {e}")
            return False
    
    def disconnect(self) -> None:
        """Ngắt kết nối MySQL."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Đóng kết nối MySQL")
    
    def execute_query(self, query: str, params: tuple = None) -> bool:
        """
        Thực thi query INSERT, UPDATE, DELETE.
        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"✗ Lỗi execute query: {e}")
            self.connection.rollback()
            return False
    
    def fetch_one(self, query: str, params: tuple = None) -> Optional[tuple]:
        """
        Lấy 1 bản ghi.
        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"✗ Lỗi fetch_one: {e}")
            return None
    
    def fetch_all(self, query: str, params: tuple = None) -> List[tuple]:
        """
        Lấy tất cả bản ghi.
        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"✗ Lỗi fetch_all: {e}")
            return []
    
    def fetch_all_as_dict(self, query: str, params: tuple = None) -> List[Dict]:
        """
        Lấy tất cả bản ghi dạng dictionary.
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"✗ Lỗi fetch_all_as_dict: {e}")
            return []
    
    def get_column_names(self, table: str) -> List[str]:
        """
        Lấy danh sách tên cột của bảng.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"DESCRIBE {table}")
            columns = [col[0] for col in cursor.fetchall()]
            cursor.close()
            return columns
        except Error as e:
            print(f"✗ Lỗi get_column_names: {e}")
            return []
    
    def is_connected(self) -> bool:
        """Kiểm tra xem có kết nối MySQL không."""
        return self.connection is not None and self.connection.is_connected()