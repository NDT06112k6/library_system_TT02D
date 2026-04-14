import pandas as pd

class Query:
    def __init__(self, file_path, title=[]):
        self.file_path = file_path
        self.title = title

    def list(self, page, page_size):
        data = pd.read_csv(self.file_path)
        if self.title:
            data = data[self.title]
        start = (page - 1) * page_size
        end = start + page_size

        page = {
            "page": page,
            "page_size": page_size,
            "total_records": len(data),
            "total_pages": (len(data) + page_size - 1) // page_size,
            "data": data[start:end]
        }
        return page
    def search(self, title_keyword, keyword):
        data = pd.read_csv(self.file_path)
        if self.title:
            data = data[self.title]
        result = data[data[title_keyword].astype(str).str.contains(keyword)]
        return result
    def delete(self,title_keyword, keyword):
        data = pd.read_csv(self.file_path)
        if self.title:
            data = data[self.title]
        result = data[~data[title_keyword].astype(str).str.contains(keyword)]
        result.to_csv(self.file_path, index=False)
        return True
    def update(self, title_keyword, keyword, new_data):
        data = pd.read_csv(self.file_path)
        if self.title:
            data = data[self.title]
        data.loc[data[title_keyword].astype(str).str.contains(keyword), self.title] = new_data
        data.to_csv(self.file_path, index=False)
        return True
    def create(self, new_data):
        data = pd.read_csv(self.file_path)
        if self.title:
            data = data[self.title]
        new_row = pd.DataFrame([new_data], columns=self.title)
        data = pd.concat([data, new_row], ignore_index=True)
        data.to_csv(self.file_path, index=False)
        return True
    def max(self, title_keyword):
        data = pd.read_csv(self.file_path)
        if self.title:
            data = data[self.title]
        max_value = data[title_keyword].max()
        return max_value