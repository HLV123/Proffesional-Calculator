import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🚀 Khởi động Calculator Application...")
    
    try:
        from utils.constants import APP_NAME, APP_VERSION
        from utils.logger import get_logger
        from gui.main_window import CalculatorMainWindow
        
        print(f"✅ Import thành công!")
        print(f"📱 Khởi động {APP_NAME} v{APP_VERSION}")
        
        logger = get_logger("Main")
        logger.info("Calculator starting...")
        
        print("🎮 Tạo giao diện...")
        calculator_app = CalculatorMainWindow()
        
        print("🎯 Bắt đầu GUI loop...")
        calculator_app.run()
        
        print("👋 Calculator đã đóng")
        return 0
        
    except ImportError as e:
        print(f"❌ Lỗi import: {e}")
        print("Đảm bảo bạn đang ở trong thư mục calculator và tất cả file cần thiết đã có")
        return 1
        
    except Exception as e:
        print(f"❌ Lỗi không xác định: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⛔ Ứng dụng bị dừng bởi người dùng")
        sys.exit(1)
    except Exception as e:
        print(f"💥 Lỗi nghiêm trọng: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)