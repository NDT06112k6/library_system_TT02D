import customtkinter as ctk
from tkinter import messagebox
from query.books import BookData
from common.theme import Colors, Fonts, Spacing
import threading
import requests

class ThemSachPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.book_data = BookData()
        self.config()
        self.view()

    def config(self): 
        self.master.title("Thêm sách")
        # Tăng chiều cao lên một chút để chứa thêm ô nhập ISBN
        self.master.geometry("450x550")
        self.master.resizable(True, True)

    def view(self):
        # Khung chính
        main_frame = ctk.CTkFrame(self.master, fg_color=Colors.BG_MAIN)
        main_frame.pack(fill="both", expand=True)

        # Tiêu đề
        header = ctk.CTkFrame(main_frame, fg_color=Colors.PRIMARY, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(
            header,
            text="📖 THÊM SÁCH MỚI",
            font=Fonts.HEADER,
            text_color=Colors.WHITE
        ).pack(pady=Spacing.MD)

        # Khung Form
        form_frame = ctk.CTkFrame(main_frame, fg_color=Colors.BG_SECONDARY)
        form_frame.pack(fill="both", expand=True, padx=Spacing.LG, pady=Spacing.LG)

        # Hàm hỗ trợ tạo ô nhập liệu 
        def Tao_Truong_Form(parent, label_text, placeholder=""): # Đổi tên hàm
            label = ctk.CTkLabel(parent, text=label_text, font=Fonts.SMALL_BOLD, text_color=Colors.TEXT_PRIMARY)
            label.pack(anchor="w", padx=Spacing.MD, pady=(Spacing.MD, Spacing.XS))
            
            entry = ctk.CTkEntry(
                parent, height=40, font=Fonts.REGULAR, 
                placeholder_text=placeholder,
                fg_color=Colors.BG_MAIN, border_color=Colors.BORDER, text_color=Colors.TEXT_PRIMARY
            )
            entry.pack(fill="x", padx=Spacing.MD, pady=(0, Spacing.MD))
            return entry

        # Khởi tạo các ô nhập liệu
        self.entries = {} 
        self.entries["ma_sach"] = Tao_Truong_Form(form_frame, "📝 Mã Sách (VD: S001)", "Nhập mã sách...")

        # CHỖ CHÈN GIAO DIỆN API (Dưới Mã sách, Trên Tên sách)
        api_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        api_frame.pack(fill="x", padx=Spacing.MD, pady=(Spacing.SM, 0))

        ctk.CTkLabel(api_frame, text="🌐 Tra cứu Internet (Nhập mã ISBN):", font=Fonts.SMALL_BOLD, text_color=Colors.TEXT_PRIMARY).pack(anchor="w", pady=(0, Spacing.XS))
        
        api_input_frame = ctk.CTkFrame(api_frame, fg_color="transparent")
        api_input_frame.pack(fill="x")
        
        self.entry_isbn = ctk.CTkEntry(api_input_frame, height=35, font=Fonts.REGULAR, placeholder_text="VD: 9780140328721", fg_color=Colors.BG_MAIN, border_color=Colors.BORDER)
        self.entry_isbn.pack(side="left", fill="x", expand=True, padx=(0, Spacing.SM))
        
        ctk.CTkButton(api_input_frame, text="🔍 Điền tự động", width=110, height=35, font=Fonts.BOLD, fg_color=Colors.INFO, hover_color="#138496", command=self.Lay_Du_Lieu_Api).pack(side="right")

        self.entries["ten_sach"] = Tao_Truong_Form(form_frame, "📖 Tên Sách", "Nhập tên sách...")
        self.entries["tac_gia"] = Tao_Truong_Form(form_frame, "✍️ Tác Giả", "Nhập tên tác giả...")
        self.entries["the_loai"] = Tao_Truong_Form(form_frame, "📂 Thể Loại", "Nhập thể loại...")

        # Hàng chứa Số lượng & Giá
        row_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row_frame.pack(fill="x", padx=Spacing.MD, pady=Spacing.MD)

        left_col = ctk.CTkFrame(row_frame, fg_color="transparent")
        left_col.pack(side="left", fill="both", expand=True, padx=(0, Spacing.SM))
        ctk.CTkLabel(left_col, text="📚 Số Lượng", font=Fonts.SMALL_BOLD).pack(anchor="w", pady=(0, Spacing.XS))
        self.entries["so_luong"] = ctk.CTkEntry(left_col, height=40, font=Fonts.REGULAR, fg_color=Colors.BG_MAIN, border_color=Colors.BORDER)
        self.entries["so_luong"].pack(fill="x")

        right_col = ctk.CTkFrame(row_frame, fg_color="transparent")
        right_col.pack(side="right", fill="both", expand=True, padx=(Spacing.SM, 0))
        ctk.CTkLabel(right_col, text="💰 Giá (VND)", font=Fonts.SMALL_BOLD).pack(anchor="w", pady=(0, Spacing.XS))
        self.entries["gia"] = ctk.CTkEntry(right_col, height=40, font=Fonts.REGULAR, fg_color=Colors.BG_MAIN, border_color=Colors.BORDER)
        self.entries["gia"].pack(fill="x")

        # Nút chức năng
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=Spacing.MD, pady=Spacing.MD)

        ctk.CTkButton(
            btn_frame, text="💾 Lưu Sách", height=40, font=Fonts.BOLD,
            fg_color=Colors.SUCCESS, hover_color="#1E8449", command=self.save
        ).pack(side="left", fill="x", expand=True, padx=(0, Spacing.SM))

        ctk.CTkButton(
            btn_frame, text="← Quay Lại", height=40, font=Fonts.BOLD,
            fg_color=Colors.BORDER, text_color=Colors.TEXT_PRIMARY, hover_color=Colors.BORDER_DARK, command=self.cancel
        ).pack(side="left", fill="x", expand=True)

    def validate(self): 
        # Thu thập dữ liệu
        data = {}
        for k, v in self.entries.items():
            data[k] = v.get().strip()

        # Kiểm tra trống
        for key, val in data.items():
            if val == "":
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
                return None

        # Kiểm tra số lượng
        try:
            so_luong = int(data["so_luong"])
            if so_luong <= 0:
                messagebox.showerror("Lỗi", "Số lượng phải là số nguyên dương")
                return None
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng phải là số nguyên")
            return None

        # Kiểm tra giá
        try:
            gia = float(data["gia"])
            if gia <= 0:
                messagebox.showerror("Lỗi", "Giá tiền phải lớn hơn 0")
                return None
            if gia > 999999999:
                messagebox.showerror("Lỗi", "Giá tiền quá lớn (max 999,999,999)")
                return None
        except ValueError:
            messagebox.showerror("Lỗi", "Giá tiền phải là số")
            return None

        # Kiểm tra mã trùng
        if self.book_data.check_exists(data["ma_sach"]) == True:
            messagebox.showerror("Lỗi", f"Mã sách '{data['ma_sach']}' đã tồn tại")
            return None

        return data

    def save(self): 
        data = self.validate()
        if data == None:
            return
        
        try:
            self.book_data.create([
                data["ma_sach"], data["ten_sach"], data["tac_gia"],
                data["the_loai"], data["so_luong"], data["gia"]
            ])
            messagebox.showinfo("Thành công", "Đã thêm sách thành công")
            self.app_manager.show_quanlysach_page()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu: {str(e)}")

    def cancel(self): 
        self.app_manager.show_quanlysach_page()

    # CHỖ CHÈN LOGIC XỬ LÝ API (Nằm ở cuối cùng của Class) 
    def Lay_Du_Lieu_Api(self): # Đổi tên hàm
        """Gọi Open Library API để lấy thông tin sách dựa trên mã ISBN"""
        isbn = self.entry_isbn.get().strip()
        
        if not isbn:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã ISBN để tra cứu (VD: 9780140328721)")
            return

        def chay_ngam_api():
            try:
                url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    key = f"ISBN:{isbn}"
                    
                    if key in data:
                        book_info = data[key]
                        ten_sach_api = book_info.get("title", "")
                        
                        authors = book_info.get("authors", [])
                        tac_gia_api = ", ".join([author["name"] for author in authors]) if authors else "Chưa rõ"
                        
                        self.master.after(0, lambda: self.dien_du_lieu_api(ten_sach_api, tac_gia_api))
                    else:
                        self.master.after(0, lambda: messagebox.showinfo("Thông báo", "Không tìm thấy dữ liệu sách với mã ISBN này!"))
                else:
                    self.master.after(0, lambda: messagebox.showerror("Lỗi", "Máy chủ API từ chối kết nối."))
            
            except requests.exceptions.RequestException:
                self.master.after(0, lambda: messagebox.showerror("Lỗi Mạng", "Vui lòng kiểm tra lại kết nối Internet của bạn!"))
            except Exception as e:
                self.master.after(0, lambda msg=str(e): messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {msg}"))

        luong_api = threading.Thread(target=chay_ngam_api)
        luong_api.daemon = True
        luong_api.start()

    def dien_du_lieu_api(self, ten, tac_gia):
        """Điền dữ liệu lấy được từ Internet vào thẳng các ô nhập liệu"""
        self.entries["ten_sach"].delete(0, 'end')
        self.entries["tac_gia"].delete(0, 'end')

        self.entries["ten_sach"].insert(0, ten)
        self.entries["tac_gia"].insert(0, tac_gia)
        
        messagebox.showinfo("Thành công", "Đã lấy thông tin sách từ Internet thành công!")