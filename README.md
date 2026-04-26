# 📚 Hệ Thống Quản Lý Thư Viện Nhà Sách Quang Vinh

## Tổng Quan

Phần mềm quản lý thư viện nhà sách **Quang Vinh** được xây dựng bằng **Python**, sử dụng giao diện đồ họa **CustomTkinter** và lưu trữ dữ liệu bằng **CSV**. Dự án được thiết kế theo mô hình **hướng đối tượng (OOP)**, tách biệt rõ ràng giữa giao diện, logic xử lý và dữ liệu.

---

## Tính Năng

### 👤 Quản lý tài khoản
- Đăng ký tài khoản với xác thực Gmail và mật khẩu
- Đăng nhập với tùy chọn **ghi nhớ tài khoản**
- Xem, tìm kiếm, sửa, xóa tài khoản
- Validate email đúng định dạng `@gmail.com`
- Kiểm tra username không trùng lặp

### 📖 Quản lý sách
- Thêm, sửa, xóa sách trong thư viện
- Tìm kiếm sách theo tên hoặc tác giả
- Hiển thị danh sách với đầy đủ thông tin: mã, tên, tác giả, thể loại, số lượng, giá

### 📋 Quản lý mượn/trả sách
- Tạo phiếu mượn với mã tự sinh (MT001, MT002...)
- Xác nhận trả sách, tự động cập nhật số lượng
- Xóa phiếu mượn (tự động hoàn trả số lượng nếu đang mượn)
- Lọc phiếu theo trạng thái: **Đang mượn** / **Đã trả**
- Tìm kiếm phiếu theo username hoặc mã sách
- Kiểm tra user không mượn 2 lần cùng 1 sách chưa trả

### 📊 Thống kê
- Tổng số đầu sách trong thư viện
- Số phiếu đang mượn / đã trả
- Top 5 sách được mượn nhiều nhất

---

## Công Nghệ Sử Dụng

| Công nghệ | Vai trò |
|-----------|---------|
| Python 3.x | Ngôn ngữ lập trình chính |
| CustomTkinter | Giao diện đồ họa (GUI) |
| Pandas | Xử lý dữ liệu CSV qua class Query |
| CSV | Lưu trữ dữ liệu |
| JSON | Lưu thông tin ghi nhớ đăng nhập |

---

## Cấu Trúc Thư Mục

```
library_system_TT02D/
│
├── Main.py                  # Điểm khởi chạy ứng dụng
├── app_manager.py           # Quản lý điều hướng giữa các trang
├── query.py                 # Class Query - xử lý CSV bằng Pandas
│
├── common/
│   ├── button.py            # CustomButton component
│   └── validation.py        # Class Validation - kiểm tra dữ liệu đầu vào
│
├── page/
│   ├── login.py             # Trang đăng nhập
│   ├── taotk.py             # Trang tạo tài khoản
│   ├── quanlytk.py          # Trang quản lý tài khoản
│   ├── suatk.py             # Trang sửa tài khoản
│   ├── quanlysach.py        # Trang quản lý sách
│   ├── themsach.py          # Trang thêm sách
│   ├── suasach.py           # Trang sửa sách
│   ├── muontra.py           # Trang quản lý mượn/trả
│   ├── taomuon.py           # Trang tạo phiếu mượn
│   └── thongke.py           # Trang thống kê
│
└── database/
    ├── tk.csv               # Dữ liệu tài khoản
    ├── books.csv            # Dữ liệu sách
    ├── muontra.csv          # Dữ liệu phiếu mượn/trả
    └── remember.json        # Lưu thông tin ghi nhớ đăng nhập
```

---

## Hướng Dẫn Cài Đặt

### Yêu cầu
- Python 3.10 trở lên
- pip

### Bước 1: Clone dự án
```bash
git clone https://github.com/NDT06112k6/library_system_TT02D.git
cd library_system_TT02D
```

### Bước 2: Tạo môi trường ảo
```bash
python -m venv .venv
```

### Bước 3: Kích hoạt môi trường ảo
```bash
# Windows
.venv\Scripts\activate
```

### Bước 4: Cài đặt thư viện
```bash
pip install customtkinter pandas
```

### Bước 5: Chạy ứng dụng
```bash
python Main.py
```

---

## Hướng Dẫn Sử Dụng

### Đăng nhập
1. Nhập **username**, **password**, **Gmail**
2. Tick **"Ghi nhớ tài khoản"** nếu muốn tự động điền lần sau
3. Bấm **Đăng nhập**

> Tài khoản mặc định: xem file `database/tk.csv`

### Quản lý sách
1. Từ trang **Quản lý tài khoản** → bấm **Quản lý sách**
2. Dùng thanh tìm kiếm để lọc theo tên sách hoặc tác giả
3. Chọn sách → bấm **Sửa** hoặc **Xóa**
4. Bấm **Thêm sách** để nhập sách mới

### Tạo phiếu mượn
1. Từ **Quản lý tài khoản** → bấm **Mượn/Trả sách**
2. Bấm **Tạo phiếu mượn**
3. Nhập username người mượn
4. Chọn sách từ danh sách (chỉ hiển thị sách còn hàng)
5. Bấm **Tạo phiếu mượn**

### Xác nhận trả sách
1. Vào trang **Mượn/Trả sách**
2. Chọn phiếu có trạng thái **Đang mượn**
3. Bấm **Xác nhận trả**

---

## Sơ Đồ Điều Hướng

```
Đăng nhập
    ├── Tạo tài khoản
    └── Quản lý tài khoản
            ├── Sửa tài khoản
            ├── Quản lý sách
            │       ├── Thêm sách
            │       └── Sửa sách
            ├── Mượn/Trả sách
            │       └── Tạo phiếu mượn
            ├── Thống kê
            └── Đăng xuất
```

---

## Thông Tin Dự Án

- **Môn học:** Lập trình Python
- **Nhóm:** 1 Trường (Nhóm trưởng) - Quang - Vinh
- **Giảng Viên Hướng Dẫn:** Phạm Nguyên Hồng
- **Người Thực Hiện:** Trường (Nhóm trưởng) - Quang - Vinh
- **GitHub:** [library_system_TT02D](https://github.com/NDT06112k6/library_system_TT02D)