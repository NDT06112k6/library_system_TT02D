import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
#Q
# HÀM HIỂN THỊ BẢNG
def show_table(parent, columns, column_configs, height=10):
    """Hiển thị bảng Treeview 
    """
    # Tạo frame chứa bảng
    table_frame = ctk.CTkFrame(parent, 
                               corner_radius=10
                               )
    
    # Tạo bảng Treeview
    tree = ttk.Treeview(table_frame, 
                        columns=columns, 
                        show="headings", 
                        height=height
                        )
    
    # Duyệt từng cột để cấu hình
    for col in columns:
        width, anchor = column_configs.get(col, (100, "center"))
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor=anchor)
        
    # Tạo thanh cuộn dọc
    scrollbar = ctk.CTkScrollbar(table_frame, 
                                 command=tree.yview
                                )
    
    # Liên kết scrollbar với Treeview
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", 
              expand=True, 
              fill="both", 
              padx=5, 
              pady=5
              )

    scrollbar.pack(side="right", 
                   fill="y"
                   )
    
    # Hiển thị frame chứa bảng
    table_frame.pack(expand=True, 
                     fill="both", 
                     padx=20, 
                     pady=10
                     )
    return tree

# HÀM TẠO Ô NHẬP LIỆU
def create_input_field(parent, label_text, placeholder="", show=""):
    """
    Tạo ô nhập liệu gồm:
    - Label
    - Entry
    
    Parameters:
    - parent: frame chứa
    - label_text: text của label
    - placeholder: chữ gợi ý
    - show: ký tự ẩn (vd: "*" cho password)
    """
    row = ctk.CTkFrame(parent, 
                       fg_color="transparent"
                       )
    row.pack(fill="x", padx=20, pady=8)
    
    # Tạo label
    ctk.CTkLabel(row, text=label_text, 
                 font=("Segoe UI", 12), 
                 width=120, 
                 anchor="w"
                 ).pack(side="left")
    
    # Tạo ô nhập liệu
    entry = ctk.CTkEntry(row, 
                         font=("Segoe UI", 12), 
                         corner_radius=8, 
                         placeholder_text=placeholder, 
                         show=show)
    
    # Hiển thị ô nhập
    entry.pack(side="right", 
               fill="x", 
               expand=True
               )
    
    return entry

# HÀM HIỂN THỊ ERROR
def show_error(title, message):
    """Hiển thị hộp thoại lỗi"""
    messagebox.showerror(
        title=f"❌ {title}",
        message=message
    )

# HÀM HIỂN THỊ THÀNH CÔNG
def show_success(title, message):
    """Hiển thị hộp thoại thành công"""
    messagebox.showinfo(
        title=f"✅ {title}",
        message=message
    )

# HÀM HIỂN THỊ CẢNH BÁO
def show_warning(title, message):
    """Hiển thị hộp thoại cảnh báo"""
    messagebox.showwarning(
        title=f"⚠️ {title}",
        message=message
    )
