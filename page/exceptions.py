class LibraryDataError(Exception):
    """Lỗi chung cho tầng dữ liệu"""
    pass

class EntityNotFoundError(LibraryDataError):
    """Không tìm thấy bản ghi"""
    pass

class DuplicateEntryError(LibraryDataError):
    """Trùng lặp khóa chính (Username, Mã sách)"""
    pass