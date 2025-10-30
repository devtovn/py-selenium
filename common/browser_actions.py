# ==================== common/browser_actions.py ====================
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
import time

class BrowserActions:
    """Class chứa các actions cơ bản với browser"""
    
    def __init__(self, driver):
        self.driver = driver
    
    def set_cookie(self, name: str, value: str, domain: str = None):
        """Set cookie cho page"""
        cookie = {
            'name': name,
            'value': value
        }
        if domain:
            cookie['domain'] = domain
        
        self.driver.add_cookie(cookie)
        print(f"Đã set cookie '{name}'")
    
    def navigate_to(self, url: str):
        """Điều hướng đến URL"""
        self.driver.get(url)
        print(f"Đã mở: {url}")
    
    def refresh_page(self):
        """Refresh trang hiện tại"""
        self.driver.refresh()
        print("Đã refresh trang")
    
    def switch_to_new_tab(self, tab_index: int = -1):
        """Chuyển sang tab mới (mặc định là tab cuối cùng)"""
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[tab_index])
        print(f"Đã chuyển sang tab {tab_index}")
    
    def switch_to_main_tab(self):
        """Chuyển về tab đầu tiên"""
        self.driver.switch_to.window(self.driver.window_handles[0])
        print("Đã chuyển về tab chính")
    
    def close_current_tab(self):
        """Đóng tab hiện tại"""
        self.driver.close()
        print("Đã đóng tab hiện tại")
    
    def wait_for_page_load(self, timeout: int = 10):
        """Đợi page load xong"""
        try:
            time.sleep(1)  # Đợi cơ bản
            # Có thể thêm logic đợi document.readyState == 'complete'
            self.driver.execute_script("return document.readyState") == "complete"
            print("Trang đã load xong")
        except Exception as e:
            print(f"Lỗi khi đợi page load: {e}")

