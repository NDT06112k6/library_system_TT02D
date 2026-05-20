import mysql.connector
import pandas as pd
from tkinter import messagebox

class Query:
    def __init__(self, table_name=None, fields=None):
        self.host = "localhost"
        self.user = "root"
        self.password = "root"
        self.database = "library_system"
        self.connection = None
        self.table_name = table_name
        self.fields = fields

    def connect(self) :
        try :
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset="utf8mb4"
            )
            return self.connection
        except mysql.connector.Error as err :
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối cơ sở dữ liệu : {err}")
            return None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query, params=None):
        conn = self.connect()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            conn.commit()
            return result
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi truy vấn", f"Lỗi thực thi lệnh SQL: {err}")
            return None
        finally:
            cursor.close()
            self.close()

    def search(self, column_name, keyword, exact=False):
        if exact:
            query = f"SELECT * FROM {self.table_name} WHERE {column_name} = %s"
            params = (keyword,)
        else:
            query = f"SELECT * FROM {self.table_name} WHERE {column_name} LIKE %s"
            params = (f"%{keyword}%",)
        
        result = self.execute_query(query, params)
        if result is not None:
            return pd.DataFrame(result)
        return pd.DataFrame(columns=self.fields)

    def list_all(self):
        query = f"SELECT * FROM {self.table_name}"
        result = self.execute_query(query)
        if result is not None:
            return [list(row.values()) for row in result]
        return []

    def delete(self, column_name, value):
        query = f"DELETE FROM {self.table_name} WHERE {column_name} = %s"
        conn = self.connect()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(query, (value,))
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi xóa", f"Không thể xóa dữ liệu: {err}")
            return False
        finally:
            cursor.close()
            self.close()

    def create(self, data):
        columns = ", ".join(self.fields[1:])
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        conn = self.connect()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(query, tuple(data))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi thêm", f"Không thể thêm dữ liệu: {err}")
            return False
        finally:
            cursor.close()
            self.close()
        
    def update(self, key_column, key_value, update_data: dict):
        """
        Cập nhật dữ liệu động cho bất kỳ bảng nào.
        update_data: dict dạng {"tên_cột": "giá_trị_mới"}
        """
        if not update_data:
            return False
            
        # Xây dựng mệnh đề SET của câu lệnh SQL (VD: hoten = %s, sdt = %s)
        set_clause = ", ".join([f"{col} = %s" for col in update_data.keys()])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {key_column} = %s"
        
        # Gộp các giá trị cần cập nhật kèm theo điều kiện WHERE ở cuối
        params = list(update_data.values()) + [key_value]
        
        conn = self.connect()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(query, tuple(params))
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi cập nhật", f"Không thể cập nhật cơ sở dữ liệu: {err}")
            return False
        finally:
            cursor.close()
            self.close()