# ==================== main.py ====================
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from services.search_service import SearchService
import time

def setup_driver():
    """Khởi tạo WebDriver với các options"""
    chrome_options = Options()
    
    # Các options hữu ích
    # chrome_options.add_argument('--headless')  # Chạy ẩn browser
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Set download directory (tùy chọn)
    prefs = {
        "download.default_directory": "./downloads",
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    
    return driver

def main():
    """Hàm main"""
    driver = None
    
    try:
        print("=== BẮT ĐẦU CHƯƠNG TRÌNH ===\n")
        
        # Khởi tạo driver
        driver = setup_driver()
        
        # Khởi tạo service
        search_service = SearchService(driver)
        
        # Thực hiện workflow với keyword
        keyword = "test search"
        search_service.execute_workflow(keyword)
        
        # Giữ browser mở một chút để xem kết quả
        time.sleep(5)
        
    except Exception as e:
        print(f"\nLỗi không xử lý được: {e}")
        
    finally:
        if driver:
            print("\n=== ĐÓNG BROWSER ===")
            driver.quit()

if __name__ == "__main__":
    main()