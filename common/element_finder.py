# ==================== common/element_finder.py ====================
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from typing import Optional

class ElementFinder:
    """Class chứa các phương thức tìm element"""
    
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def find_by_id(self, element_id: str) -> Optional[WebElement]:
        """Tìm element theo ID"""
        try:
            return self.wait.until(
                EC.presence_of_element_located((By.ID, element_id))
            )
        except Exception as e:
            print(f"Không tìm thấy element với ID '{element_id}': {e}")
            return None
    
    def find_by_xpath(self, xpath: str) -> Optional[WebElement]:
        """Tìm element theo XPath"""
        try:
            return self.wait.until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except Exception as e:
            print(f"Không tìm thấy element với XPath '{xpath}': {e}")
            return None
    
    def find_by_css(self, css_selector: str) -> Optional[WebElement]:
        """Tìm element theo CSS Selector"""
        try:
            return self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
        except Exception as e:
            print(f"Không tìm thấy element với CSS '{css_selector}': {e}")
            return None
    
    def find_clickable_by_id(self, element_id: str) -> Optional[WebElement]:
        """Tìm element có thể click được theo ID"""
        try:
            return self.wait.until(
                EC.element_to_be_clickable((By.ID, element_id))
            )
        except Exception as e:
            print(f"Element với ID '{element_id}' không thể click: {e}")
            return None
    
    def find_all_by_xpath(self, xpath: str) -> list:
        """Tìm tất cả elements theo XPath"""
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return self.driver.find_elements(By.XPATH, xpath)
        except Exception as e:
            print(f"Không tìm thấy elements với XPath '{xpath}': {e}")
            return []
