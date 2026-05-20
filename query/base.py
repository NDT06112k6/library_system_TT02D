import pandas as pd
import os
from typing import List, Dict, Any, Optional, Union
from abc import ABC

class Query(ABC):
    """Lớp cơ sở xử lý thao tác với file CSV bằng Pandas"""
    
    def __init__(self, file_path: str, columns: List[str]):
        self.file_path = file_path
        self.columns = columns
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Kiểm tra và khởi tạo file CSV cùng thư mục chứa nếu chưa tồn tại."""
        try:
            if not os.path.exists(self.file_path):
                os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
                pd.DataFrame(columns=self.columns).to_csv(self.file_path, index=False)
        except Exception as e:
            print(f"Lỗi khởi tạo file {self.file_path}: {e}")

    def _read_data(self) -> pd.DataFrame:
        """Đọc dữ liệu từ file CSV trả về DataFrame của Pandas."""
        try:
            if not os.path.exists(self.file_path):
                return pd.DataFrame(columns=self.columns)
            return pd.read_csv(self.file_path, dtype=str, encoding="utf-8").fillna("")
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file {self.file_path}")
            return pd.DataFrame(columns=self.columns)
        except Exception as e:
            print(f"Lỗi đọc dữ liệu: {e}")
            return pd.DataFrame(columns=self.columns)

    def list(self, page: int = 1, page_size: int = 9999) -> Dict[str, Any]:
        """
        Đọc dữ liệu và phân trang.
        
        Args:
            page (int): Số trang hiện tại.
            page_size (int): Số lượng bản ghi trên một trang.
            
        Returns:
            dict: Chứa thông tin phân trang và dữ liệu dưới dạng DataFrame slice.
        """
        df = self._read_data()
        start = (page - 1) * page_size
        end = start + page_size
        return {
            "page": page,
            "page_size": page_size,
            "total_records": len(df),
            "data": df[start:end]
        }

    def list_all(self) -> List[List[Any]]:
        """Trả về toàn bộ dữ liệu hiện có dưới dạng list của các list."""
        df = self._read_data()
        return df.values.tolist()

    def search(self, column: str, keyword: str, exact: bool = False) -> pd.DataFrame:
        """
        Tìm kiếm dữ liệu trong một cột cụ thể.
        
        Args:
            column (str): Tên cột cần tìm.
            keyword (str): Từ khóa tìm kiếm.
            exact (bool): Nếu True sẽ tìm khớp hoàn toàn, False sẽ tìm theo cụm từ chứa từ khóa.
            
        Returns:
            pd.DataFrame: Kết quả tìm kiếm.
        """
        df = self._read_data()
        if column not in df.columns:
            return pd.DataFrame(columns=self.columns)
            
        if exact:
            result = df[df[column].astype(str) == str(keyword)]
        else:
            result = df[df[column].astype(str).str.contains(str(keyword), case=False, na=False)]
        return result

    def add(self, new_row_data: List[Any]) -> bool:
        """Thêm một bản ghi mới vào file CSV."""
        df = self._read_data()
        new_row = pd.DataFrame([new_row_data], columns=self.columns)
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.file_path, index=False)
        return True

    def create(self, new_row_data: List[Any]) -> bool:
        """Alias cho phương thức add()."""
        return self.add(new_row_data)

    def update(self, id_column: str, id_value: Any, updated_row_data: List[Any]) -> bool:
        """Cập nhật thông tin một bản ghi dựa trên khóa ID."""
        df = self._read_data()
        mask = df[id_column].astype(str) == str(id_value)
        if not df[mask].empty:
            df.loc[mask, self.columns] = updated_row_data
            df.to_csv(self.file_path, index=False)
            return True
        return False

    def delete(self, id_column: str, id_value: Any) -> bool:
        """Xóa một bản ghi dựa trên khóa ID."""
        df = self._read_data()
        df = df[df[id_column].astype(str) != str(id_value)]
        df.to_csv(self.file_path, index=False)
        return True

    def get_max_value(self, column: str) -> Optional[Any]:
        """Lấy giá trị lớn nhất hiện có trong một cột cụ thể."""
        df = self._read_data()
        return df[column].max() if not df.empty else None