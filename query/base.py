import pandas as pd
from tkinter import messagebox
import csv
from datetime import datetime
from database.mysql_handler import MySQLHandler

class Query:
    def __init__(self, table_name=None, fields=None):
        """Khởi tạo cấu hình kết nối thông qua MySQLHandler"""
        self.db_handler = MySQLHandler(host="localhost", user="root", password="root", database="library_system")
        self.table_name = table_name
        self.fields = fields
        self.connection = None

    def connect(self):
        """Thiết lập kết nối tới cơ sở dữ liệu qua MySQLHandler"""
        if self.db_handler.connect():
            self.connection = self.db_handler.connection
            return self.connection
        return None

    def close(self):
        """Đóng kết nối cơ sở dữ liệu một cách an toàn"""
        # Nếu hàm close() tồn tại trong MySQLHandler thì gọi nó
        if hasattr(self.db_handler, 'close'):
            self.db_handler.close()
        # Nếu không, tự động đóng connection của thư viện mysql.connector
        elif self.connection:
            if self.connection.is_connected():
                self.connection.close()
                
        self.connection = None

    def thuc_thi_query(self, query, params=None):
        """Thực thi câu lệnh truy vấn SQL và trả về kết quả dưới dạng danh sách"""
        conn = self.connect()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            conn.commit()
            return result
        except Exception as err:
            messagebox.showerror("Lỗi truy vấn", f"Lỗi thực thi lệnh SQL: {err}")
            return None
        finally:
            cursor.close()
            self.close()

    def search(self, column_name, keyword, exact=False):
        """Tìm kiếm dữ liệu dựa trên cột và từ khóa chỉ định"""
        if exact:
            query = f"SELECT * FROM {self.table_name} WHERE {column_name} = %s"
            params = (keyword,)
        else:
            query = f"SELECT * FROM {self.table_name} WHERE {column_name} LIKE %s"
            params = (f"%{keyword}%",)
        
        result = self.thuc_thi_query(query, params)
        if result is not None:
            return pd.DataFrame(result)
        return pd.DataFrame(columns=self.fields)

    def list_all(self):
        """Truy vấn tất cả dữ liệu từ bảng đang quản lý"""
        query = f"SELECT * FROM {self.table_name}"
        result = self.thuc_thi_query(query)
        if result is not None:
            return [list(row.values()) for row in result]
        return []

    def delete(self, column_name, value):
        """Xóa bản ghi khỏi cơ sở dữ liệu theo điều kiện cột"""
        query = f"DELETE FROM {self.table_name} WHERE {column_name} = %s"
        conn = self.connect()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(query, (value,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as err:
            messagebox.showerror("Lỗi xóa", f"Không thể xóa dữ liệu: {err}")
            return False
        finally:
            cursor.close()
            self.close()

    def create(self, data):
        """Thêm mới một bản ghi dữ liệu vào cơ sở dữ liệu"""
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
        except Exception as err:
            messagebox.showerror("Lỗi thêm", f"Không thể thêm dữ liệu: {err}")
            return False
        finally:
            cursor.close()
            self.close()
    
    def update(self, key_column, key_value, update_data: dict):
        """Cập nhật dữ liệu động theo cặp khóa-giá trị"""
        if not update_data:
            return False
            
        set_clause = ", ".join([f"{col} = %s" for col in update_data.keys()])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {key_column} = %s"
        
        params = list(update_data.values()) + [key_value]
        
        conn = self.connect()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(query, tuple(params))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as err:
            messagebox.showerror("Lỗi cập nhật", f"Không thể cập nhật cơ sở dữ liệu: {err}")
            return False
        finally:
            cursor.close()
            self.close()
        
    def xuat_csv(self):
        try:
            results = self.list_all()
            filename = f"{self.table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(self.fields)
                writer.writerows(results)
            messagebox.showinfo("Thành công", f"Xuất file {filename}")
            return filename
        except Exception as e:
            messagebox.showerror("Lỗi", f"Export failed: {e}")
            return None
    
    def nhap_csv(self, filepath):
        """Nhập dữ liệu từ file CSV vào database"""
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as tep_csv:
                doc_csv = csv.DictReader(tep_csv)
                for dong_du_lieu in doc_csv:
                    danh_sach_gia_tri = []
                    for ten_truong in self.fields[1:]:
                        if ten_truong in dong_du_lieu:
                            gia_tri = dong_du_lieu[ten_truong]
                        else:
                            gia_tri = None
                        danh_sach_gia_tri.append(gia_tri)
                    self.create(danh_sach_gia_tri)
            return True
        except Exception as loi:
            messagebox.showerror("Lỗi", f"Nhập thất bại: {str(loi)}")
            return False