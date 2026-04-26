
import tkinter as tk

class CustomButton(tk.Button):
    """Button tùy chỉnh với style riêng"""
    
    def __init__(self, parent, text="", command=None, style_type="primary", **kwargs):
        self.style_type = style_type
        super().__init__(parent, text=text, command=command, **kwargs)
        self.configure_style()
        
    def configure_style(self):
        """Cấu hình style cho button"""
        if self.style_type == "primary":
            self.configure(bg='#007bff', fg='white', font=('Segoe UI', 10, 'bold'))
        elif self.style_type == "success":
            self.configure(bg='#28a745', fg='white', font=('Segoe UI', 10))
        elif self.style_type == "danger":
            self.configure(bg='#dc3545', fg='white', font=('Segoe UI', 10))
        elif self.style_type == "warning":
            self.configure(bg='#ffc107', fg='black', font=('Segoe UI', 10))
        elif self.style_type == "info":
            self.configure(bg='#17a2b8', fg='white', font=('Segoe UI', 10))
        elif self.style_type == "secondary":
            self.configure(bg='#6c757d', fg='white', font=('Segoe UI', 10))
