# ==================== common/element_actions.py ====================
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import time

class ElementActions:
    """Class chứa các actions với element"""
    
    def __init__(self, driver):
        self.driver = driver
    
    def click_element(self, element: WebElement, wait_after: float = 0.5):
        """Click vào element"""
        try:
            element.click()
            print(f"Đã click vào element")
            if wait_after > 0:
                time.sleep(wait_after)
            return True
        except Exception as e:
            print(f"Lỗi khi click element: {e}")
            return False
    
    def click_by_javascript(self, element: WebElement):
        """Click vào element bằng JavaScript (dùng khi click thường không work)"""
        try:
            self.driver.execute_script("arguments[0].click();", element)
            print("Đã click vào element bằng JavaScript")
            return True
        except Exception as e:
            print(f"Lỗi khi click bằng JS: {e}")
            return False
    
    def send_text(self, element: WebElement, text: str, clear_first: bool = True):
        """Nhập text vào element"""
        try:
            if clear_first:
                element.clear()
            element.send_keys(text)
            print(f"Đã nhập text: '{text}'")
            return True
        except Exception as e:
            print(f"Lỗi khi nhập text: {e}")
            return False
    
    def send_keys(self, element: WebElement, key):
        """Send phím đặc biệt (Enter, Tab, ...)"""
        try:
            element.send_keys(key)
            print(f"Đã send key")
            return True
        except Exception as e:
            print(f"Lỗi khi send key: {e}")
            return False
    
    def get_text(self, element: WebElement) -> str:
        """Lấy text của element"""
        try:
            return element.text
        except Exception as e:
            print(f"Lỗi khi lấy text: {e}")
            return ""
    
    def get_attribute(self, element: WebElement, attr_name: str) -> str:
        """Lấy attribute của element"""
        try:
            return element.get_attribute(attr_name)
        except Exception as e:
            print(f"Lỗi khi lấy attribute: {e}")
            return ""
    
    def is_visible(self, element: WebElement) -> bool:
        """Kiểm tra element có hiển thị không"""
        try:
            return element.is_displayed()
        except:
            return False
