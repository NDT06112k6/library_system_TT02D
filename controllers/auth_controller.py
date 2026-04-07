from models import user_model
from tkinter import messagebox


class AuthController:
    """
    Controller xử lý xác thực người dùng.
    Bao gồm: đăng nhập, đăng ký.
    """

    def login(self, username: str, password: str) -> bool:
        """
        Kiểm tra thông tin đăng nhập.
        - Trả về True nếu đúng, False nếu sai.
        """
        # Kiểm tra input rỗng
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return False

        # Tìm user trong database
        is_valid = user_model.find_user(username, password)

        if is_valid:
            messagebox.showinfo("Thành công", "Đăng nhập thành công")
            return True
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng")
            return False

    def register(self, username: str, password: str) -> bool:
        """
        Tạo tài khoản mới.
        - Trả về True nếu tạo thành công, False nếu thất bại.
        """
        # Kiểm tra input rỗng
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return False

        # Kiểm tra username đã tồn tại chưa
        if user_model.username_exists(username):
            messagebox.showerror("Lỗi", f"Tên đăng nhập '{username}' đã tồn tại")
            return False

        # Lưu tài khoản mới vào database
        user_model.add_user(username, password)
        messagebox.showinfo("Thành công", "Tạo tài khoản thành công")
        return True