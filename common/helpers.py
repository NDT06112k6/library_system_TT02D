import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

def show_table(parent, columns, column_configs, height=10):
    """Hiển thị bảng Treeview với cấu hình chuẩn"""
    table_frame = ctk.CTkFrame(parent, corner_radius=10)
    
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=height)
    
    for col in columns:
        width, anchor = column_configs.get(col, (100, "center"))
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor=anchor)
        
    scrollbar = ctk.CTkScrollbar(table_frame, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", expand=True, fill="both", padx=5, pady=5)
    scrollbar.pack(side="right", fill="y")
    table_frame.pack(expand=True, fill="both", padx=20, pady=10)
    return tree

def create_input_field(parent, label_text, placeholder="", show=""):
    """Tạo input field (label + entry) chuẩn CTK"""
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", padx=20, pady=8)
    
    ctk.CTkLabel(row, text=label_text, font=("Segoe UI", 12), width=120, anchor="w").pack(side="left")
    entry = ctk.CTkEntry(row, font=("Segoe UI", 12), corner_radius=8, placeholder_text=placeholder, show=show)
    entry.pack(side="right", fill="x", expand=True)
    
    return entry

def show_error(title, message):
    """Hiển thị error với style đẹp kèm Emoji"""
    messagebox.showerror(
        title=f"❌ {title}",
        message=message
    )

def show_success(title, message):
    """Hiển thị success kèm Emoji"""
    messagebox.showinfo(
        title=f"✅ {title}",
        message=message
    )

def show_warning(title, message):
    """Hiển thị warning kèm Emoji"""
    messagebox.showwarning(
        title=f"⚠️ {title}",
        message=message
    )