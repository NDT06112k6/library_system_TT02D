from models import user_model
from tkinter import messagebox


class AccountController:
    """
    Controller xử lý quản lý tài khoản.
    Bao gồm: lấy danh sách, xóa, sửa tài khoản.
    """

    def get_all_accounts(self) -> list:
        """
        Lấy toàn bộ danh sách tài khoản từ database.
        - Trả về list các [username, password].
        """
        return user_model.get_all_users()

    def delete_account(self, username: str) -> bool:
        """
        Xóa tài khoản theo username.
        - Trả về True nếu xóa thành công.
        """
        confirmed = messagebox.askyesno(
            "Xác nhận",
            f"Bạn có chắc muốn xóa tài khoản '{username}'?"
        )

        if not confirmed:
            return False

        user_model.delete_user(username)
        messagebox.showinfo("Thành công", "Đã xóa tài khoản thành công")
        return True

    def update_account(
        self,
        old_username: str,
        new_username: str,
        new_password: str
    ) -> bool:
        """
        Cập nhật thông tin tài khoản.
        - Trả về True nếu cập nhật thành công.
        """
        # Kiểm tra input rỗng
        if not new_username or not new_password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return False

        # Nếu đổi username, kiểm tra username mới có bị trùng không
        if new_username != old_username and user_model.username_exists(new_username):
            messagebox.showerror("Lỗi", f"Tên đăng nhập '{new_username}' đã tồn tại")
            return False

        # Lưu thay đổi vào database
        user_model.update_user(old_username, new_username, new_password)
        messagebox.showinfo("Thành công", "Cập nhật tài khoản thành công")
        return True