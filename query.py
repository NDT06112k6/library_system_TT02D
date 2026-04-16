import pandas as pd

class Query:
    def __init__(self, file_path, title=[]):
        self.file_path = file_path
        self.title = title

    def list(self, page, page_size):
        data = pd.read_csv(self.file_path, dtype=str)
        if self.title:
            data = data[self.title]
        start = (page - 1) * page_size
        end = start + page_size
        return {
            "page": page,
            "page_size": page_size,
            "total_records": len(data),
            "total_pages": (len(data) + page_size - 1) // page_size,
            "data": data[start:end]
        }

    def search(self, title_keyword, keyword, exact=False):
        data = pd.read_csv(self.file_path, dtype=str)
        if self.title:
            data = data[self.title]
        if exact:
            # Khớp chính xác
            result = data[data[title_keyword].astype(str) == str(keyword)]
        else:
            # Khớp một phần
            result = data[data[title_keyword].astype(str).str.contains(keyword)]
        return result

    def delete(self, title_keyword, keyword, exact=True):
        data = pd.read_csv(self.file_path, dtype=str)
        if self.title:
            data = data[self.title]
        if exact:
            result = data[data[title_keyword].astype(str) != str(keyword)]
        else:
            result = data[~data[title_keyword].astype(str).str.contains(keyword)]
        result.to_csv(self.file_path, index=False)
        return True

    def update(self, title_keyword, keyword, new_data, exact=True):
        data = pd.read_csv(self.file_path, dtype=str)
        if self.title:
            data = data[self.title]
        if exact:
            mask = data[title_keyword].astype(str) == str(keyword)
        else:
            mask = data[title_keyword].astype(str).str.contains(keyword)
        data.loc[mask, self.title] = new_data
        data.to_csv(self.file_path, index=False)
        return True

    def create(self, new_data):
        data = pd.read_csv(self.file_path, dtype=str)
        if self.title:
            data = data[self.title]
        new_row = pd.DataFrame([new_data], columns=self.title)
        data = pd.concat([data, new_row], ignore_index=True)
        data.to_csv(self.file_path, index=False)
        return True

    def max(self, title_keyword):
        data = pd.read_csv(self.file_path, dtype=str)
        if self.title:
            data = data[self.title]
        return data[title_keyword].max()