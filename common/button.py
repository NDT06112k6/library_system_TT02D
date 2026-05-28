
import tkinter as tk
#Q
class CustomButton(tk.Button):
    """Button tùy chỉnh với nhiều style khác nhau
    """
    
    def __init__(self, parent, 
                 text="", 
                 command=None, 
                 style_type="primary", 
                 **kwargs
                 ):
        """
        Hàm khởi tạo button
        
        Parameters:
        - parent: widget cha chứa button
        - text: nội dung hiển thị trên button
        - command: hàm được gọi khi click
        - style_type: loại style của button
        - kwargs: tham số mở rộng khác
        """

        # Lưu kiểu style
        self.style_type = style_type

        # Gọi constructor của lớp cha tk.Button
        super().__init__(parent, 
                         text=text, 
                         command=command, 
                         **kwargs
                         )
        
        # Gọi hàm cấu hình style
        self.configure_style()
        
    # HÀM CẤU HÌNH STYLE
    def configure_style(self):
        # BUTTON CHÍNH
        if self.style_type == "primary":
            self.configure(bg='#007bff', fg='white', font=('Segoe UI', 10, 'bold'))
        
        # BUTTON THÀNH CÔNG
        elif self.style_type == "success":
            self.configure(bg='#28a745', fg='white', font=('Segoe UI', 10))
        
        # BUTTON NGUY HIỂM / XÓA
        elif self.style_type == "danger":
            self.configure(bg='#dc3545', fg='white', font=('Segoe UI', 10))
       
        # BUTTON CẢNH BÁO
        elif self.style_type == "warning":
            self.configure(bg='#ffc107', fg='black', font=('Segoe UI', 10))
        
        # BUTTON THÔNG TIN
        elif self.style_type == "info":
            self.configure(bg='#17a2b8', fg='white', font=('Segoe UI', 10))
        
        # BUTTON PHỤ
        elif self.style_type == "secondary":
            self.configure(bg='#6c757d', fg='white', font=('Segoe UI', 10))
