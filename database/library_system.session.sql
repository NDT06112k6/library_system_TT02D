-- Bảng lưu trữ thông tin người dùng
CREATE TABLE taikhoan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    taikhoan VARCHAR(100) UNIQUE NOT NULL,
    matkhau VARCHAR(255) NOT NULL,
    hoten VARCHAR(255),
    sdt VARCHAR(20),
    chucvu VARCHAR(100),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng lưu trữ thông tin sách
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ma_sach VARCHAR(50) UNIQUE NOT NULL,
    ten_sach VARCHAR(255) NOT NULL,
    tac_gia VARCHAR(255),
    the_loai VARCHAR(100),
    so_luong INT DEFAULT 0,
    gia DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng quản lý giao dịch mượn/trả
CREATE TABLE muontra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ma_phieu VARCHAR(50) UNIQUE NOT NULL,
    username VARCHAR(100) NOT NULL,
    ma_sach VARCHAR(50) NOT NULL,
    ngay_muon DATE,
    ngay_tra DATE,
    trang_thai VARCHAR(50) DEFAULT 'dang_muon',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ma_sach) REFERENCES books(ma_sach),
    FOREIGN KEY (username) REFERENCES taikhoan(taikhoan)
);

-- Thêm dữ liệu mẫu cho tài khoản
INSERT INTO taikhoan (taikhoan, matkhau, hoten, sdt, chucvu, email) VALUES
('1', '1', 'Admin', '0999999999', 'Quản lý', '1'),
('NDT6116', '1', 'Nguyễn Đức Trường', '0123456789', 'Độc giả', 'ductruong6116@gmail.com');

-- Thêm dữ liệu mẫu cho sách
INSERT INTO books (ma_sach, ten_sach, tac_gia, the_loai, so_luong, gia) VALUES
('S001', 'Lap Trinh Python Co Ban', 'Nguyen Van A', 'Công nghệ', 8, 120000),

-- Thêm dữ liệu lịch sử mượn trả
INSERT INTO muontra (ma_phieu, username, ma_sach, ngay_muon, ngay_tra, trang_thai) VALUES
('MT003', '1', 'S002', '2026-04-17', '2026-04-20', 'da_tra'),