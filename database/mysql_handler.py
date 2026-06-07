import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any, Optional

class MySQLHandler:
    """Lớp quản lý kết nối và thực hiện các thao tác CRUD với MySQL."""
    
    def __init__(self, host: str = "localhost", user: str = "root", 
                 password: str = "root", database: str = "library_system"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self) -> bool:
        """Thiết lập kết nối tới cơ sở dữ liệu với cấu hình UTF-8."""
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
            # Thiết lập session để hỗ trợ ký tự đặc biệt/tiếng Việt 
            cursor = self.connection.cursor()
            cursor.execute("SET NAMES utf8mb4")
            cursor.close()
            if self.connection.is_connected():
                print(f"Kết nối MySQL thành công: {self.database}")
                return True
        except Error as e:
            print(f"Lỗi kết nối MySQL: {e}")
            return False
    
    def disconnect(self) -> None:
        """Đóng kết nối nếu đang mở."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Đóng kết nối MySQL")
    
    def thuc_thi_query(self, query: str, params: tuple = None) -> bool:
        """
        Thực thi các lệnh thay đổi dữ liệu (INSERT, UPDATE, DELETE)
        Tự động thực hiện commit hoặc rollback nếu có lỗi
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
            print(f"Lỗi execute query: {e}")
            self.connection.rollback()
            return False
    
    def Lay_Mot_Ban_Ghi(self, query: str, params: tuple = None) -> Optional[tuple]:
        """Truy vấn lấy bản ghi duy nhất."""
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
            print(f"Lỗi lấy một bản ghi: {e}")
            return None
    
    def lay_all_ban_ghi(self, query: str, params: tuple = None) -> List[tuple]:
        """Truy vấn lấy danh sách tất cả các bản ghi dạng Tuple"""
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
            print(f"Lỗi lay_all_ban_ghi: {e}")
            return []
    
    def Lay_All_Dang_Tu_Dien(self, query: str, params: tuple = None) -> List[Dict]:
        """Truy vấn lấy dữ liệu dạng Dictionary (key là tên cột)"""
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
            print(f"Lỗi lấy tất cả bản ghi dưới dạng từ điển: {e}")
            return []
    
    def Lay_Ten_Cot(self, table: str) -> List[str]:
        """Lấy danh sách tên các cột của một bảng bằng lệnh DESCRIBE"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"DESCRIBE {table}")
            columns = []
            for col in cursor.fetchall():
                columns.append(col[0])
            cursor.close()
            return columns
        except Error as e:
            print(f"Lỗi lấy tên cột: {e}")
            return []
    
    def is_connected(self) -> bool:
        """Kiểm tra trạng thái kết nối."""
        if self.connection is not None:
            if self.connection.is_connected():
                return True
            else:
                return False
        else:
            return False