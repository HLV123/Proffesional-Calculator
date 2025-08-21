# Proffesional-Calculator
Máy tính giao diện GUI có ghi nhớ lịch sử và xuất data lịch sử tính toán về dạng json

<img width="1918" height="1022" alt="Image" src="https://github.com/user-attachments/assets/7b0f903a-d560-489b-88f9-04a9f7090e27" />

<img width="1918" height="1017" alt="Image" src="https://github.com/user-attachments/assets/f2b64cc2-4f36-40a5-ae8f-d83ebd99ebc5" />

# 🧮 Máy Tính Chuyên Nghiệp

Ứng dụng máy tính hiện đại, đầy đủ tính năng được xây dựng bằng Python và Tkinter, cung cấp giao diện GUI đẹp mắt với các phép toán nâng cao và chức năng toàn diện.

## ✨ Tính Năng

### 🔢 Chức Năng Máy Tính Cơ Bản
- **Phép toán cơ bản**: Cộng (+), trừ (-), nhân (*), chia (/)
- **Phép toán nâng cao**: Tính phần trăm (%), đổi dấu (±)
- **Ngoặc đơn**: Hỗ trợ ngoặc đơn để ưu tiên phép toán
- **Thao tác bộ nhớ**: Lưu (MS), Gọi (MR), Xóa (MC), Cộng (M+), Trừ (M-)

### 🎨 Giao Diện Người Dùng
- **GUI hiện đại**: Giao diện sạch sẽ, trực quan được xây dựng với Tkinter
- **Nhiều chủ đề**: Chủ đề Sáng, Tối, Xanh Dương và Xanh Lá
- **Thiết kế responsive**: Tự động điều chỉnh theo kích thước cửa sổ
- **Hiệu ứng tương tác**: Hover effects và press animations

### 📚 Quản Lý Lịch Sử
- **Lưu trữ tính toán**: Tự động lưu tất cả phép tính đã thực hiện
- **Xuất/Nhập lịch sử**: Lưu và tải lịch sử dưới định dạng JSON
- **Sao chép nhanh**: Click đúp để sao chép biểu thức vào clipboard
- **Hiển thị thời gian**: Mỗi phép tính có timestamp chi tiết

### ⌨️ Phím Tắt
- **Số**: 0-9, dấu thập phân (.)
- **Phép toán**: +, -, *, /, %
- **Tính toán**: Enter hoặc =
- **Xóa**: Escape (C), Backspace (CE)
- **Điều khiển**: Ctrl+Q (Thoát), Ctrl+R (Reset)

## 🚀 Cài Đặt và Chạy

### Yêu Cầu Hệ Thống
- Python 3.7 trở lên
- Tkinter (thường có sẵn với Python)
- Hệ điều hành: Windows, macOS, Linux

### Cách Chạy

2. **Chạy ứng dụng**
   ```bash
   cd "D:\Github\New folder\calculator"
   python main.py
   ```

### Cấu Trúc Thư Mục
```
calculator/
├── __init__.py          # Package initialization
├── main.py              # File chạy chính
├── core/                # Logic tính toán chính
│   ├── __init__.py
│   ├── calculator.py    # Engine máy tính
│   ├── parser.py        # Phân tích biểu thức
│   └── validator.py     # Xác thực input
├── gui/                 # Giao diện người dùng
│   ├── __init__.py
│   ├── main_window.py   # Cửa sổ chính
│   ├── components.py    # Các component UI
│   └── styles.py        # Quản lý theme và style
└── utils/               # Tiện ích và cấu hình
    ├── __init__.py
    ├── constants.py     # Hằng số ứng dụng
    ├── exceptions.py    # Xử lý lỗi
    └── logger.py        # Hệ thống logging
```

## 🎯 Cách Sử Dụng

### Tính Toán Cơ Bản
1. Click các nút số và phép toán để nhập biểu thức
2. Nhấn `=` hoặc `Enter` để tính toán
3. Sử dụng `C` để xóa toàn bộ, `CE` để xóa từng ký tự

### Chức Năng Nâng Cao
- **Bộ nhớ**: Sử dụng MS/MR/MC/M+/M- để thao tác với bộ nhớ
- **Lịch sử**: Bật sidebar để xem lịch sử tính toán
- **Themes**: Chọn theme từ menu View → Theme
- **Xuất dữ liệu**: File → Xuất lịch sử để lưu ra JSON

### Biểu Thức Hỗ Trợ
```
Số đơn giản: 123, 45.67, -89
Phép toán cơ bản: 2+3, 10-5, 4*6, 8/2
Ngoặc đơn: (2+3)*4, 10/(5-3)
Phần trăm: 100*15%, 200+10%
Đổi dấu: ±5, ±(3+2)
```

## 🛠️ Tính Năng Kỹ Thuật

### Xử Lý Toán Học An Toàn
- **Shunting Yard Algorithm**: Phân tích biểu thức infix thành postfix
- **Decimal Precision**: Sử dụng Python Decimal cho độ chính xác cao
- **Error Handling**: Xử lý lỗi chi tiết (chia cho 0, overflow, syntax error)

### Kiến Trúc Modular
- **Separation of Concerns**: Tách biệt logic, GUI và utilities
- **Plugin-like Themes**: Dễ dàng thêm theme mới
- **Extensible Design**: Có thể mở rộng thêm chức năng

### Logging và Debug
- **Comprehensive Logging**: Ghi log chi tiết mọi hoạt động
- **File Rotation**: Tự động xoay log files
- **Color Console**: Console output có màu sắc (nếu có colorlog)

## 🎨 Screenshots

### Light Theme
*Giao diện sáng, phù hợp sử dụng ban ngày*

### Dark Theme
*Giao diện tối, bảo vệ mắt khi sử dụng ban đêm*

### Sidebar với Lịch Sử và Bộ Nhớ
*Panel bên phải hiển thị lịch sử tính toán và thao tác bộ nhớ*

### Version 1.0.0
- ✅ Phép toán cơ bản (+, -, *, /) và nâng cao (%, ±)
- ✅ Hỗ trợ ngoặc đơn và ưu tiên phép toán
- ✅ Giao diện GUI hiện đại với 4 themes (Light, Dark, Blue, Green)
- ✅ Quản lý lịch sử tính toán với timestamp
- ✅ Chức năng bộ nhớ đầy đủ (MS/MR/MC/M+/M-)
- ✅ Hệ thống logging và error handling
- ✅ Phím tắt keyboard tiện lợi
- ✅ Xuất/nhập lịch sử dưới định dạng JSON


**⭐ Nếu project này hữu ích, hãy star repository để ủng hộ chúng tôi!**
