
from app_manager import AppManager

def main():
    """ Hàm chính của chương trình. """
    print("Phần mềm đang khởi chạy")
    app = AppManager()
    
    app.run()

if __name__ == "__main__":
    main()
