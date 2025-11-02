# ==================== services/search_service.py ====================
from common.element_finder import ElementFinder
from common.element_actions import ElementActions
from common.browser_actions import BrowserActions
from config import Config
import time

class SearchService:
    """Service xử lý tìm kiếm và tải file"""
    
    def __init__(self, driver):
        self.driver = driver
        self.finder = ElementFinder(driver, Config.DEFAULT_TIMEOUT)
        self.actions = ElementActions(driver)
        self.browser = BrowserActions(driver)
    
    def setup_authentication(self):
        """Setup cookie xác thực"""
        # Mở trang trước để set cookie
        self.browser.navigate_to(Config.BASE_URL)
        time.sleep(2)
        
        # Set cookie
        self.browser.set_cookie(
            Config.AUTH_COOKIE_NAME,
            Config.AUTH_COOKIE_VALUE
        )
        
        # Refresh để cookie có hiệu lực
        self.browser.refresh_page()
        time.sleep(2)


        self.browser.navigate_to(Config.BASE_URL)
        time.sleep(2)
        self.browser.refresh_page()
        time.sleep(2)
    
    def search_keyword(self, keyword: str):
        """Tìm kiếm với keyword"""
        print(f"\n=== Bước 1: Tìm kiếm keyword '{keyword}' ===")
        
        # Tìm textbox và nhập keyword
        textbox = self.finder.find_by_id(Config.SEARCH_TEXTBOX_ID)
        if not textbox:
            raise Exception("Không tìm thấy textbox tìm kiếm")
        
        self.actions.send_text(textbox, keyword)
        
        # Click button tìm kiếm
        search_btn = self.finder.find_clickable_by_id(Config.SEARCH_BUTTON_ID)
        if not search_btn:
            raise Exception("Không tìm thấy button tìm kiếm")
        
        self.actions.click_element(search_btn, wait_after=3)
        print("Đã gửi yêu cầu tìm kiếm")
    
    def open_search_result(self):
        """Mở kết quả tìm kiếm đầu tiên"""
        print("\n=== Bước 2: Mở kết quả tìm kiếm ===")
        
        # Tìm link kết quả
        result_link = self.finder.find_clickable_by_id(Config.RESULT_LINK_ID)
        if not result_link:
            raise Exception("Không tìm thấy kết quả tìm kiếm")
        
        # Click để mở tab mới
        self.actions.click_element(result_link, wait_after=2)
        
        # Chuyển sang tab mới
        self.browser.switch_to_new_tab()
        self.browser.wait_for_page_load()
        
        print("Đã mở kết quả tìm kiếm trong tab mới")
    
    def download_file(self):
        """Tải file PDF"""
        print("\n=== Bước 3: Tải file PDF ===")
        
        # Đợi page load
        time.sleep(Config.DOWNLOAD_WAIT_TIME)
        
        # Tìm link download
        download_link = self.finder.find_clickable_by_id(Config.DOWNLOAD_LINK_ID)
        if not download_link:
            raise Exception("Không tìm thấy link download")
        
        # Click để download
        self.actions.click_element(download_link, wait_after=2)
        print("Đã bắt đầu tải file")
    
    def execute_workflow(self, keyword: str):
        """Thực hiện toàn bộ workflow"""
        try:
            # Setup authentication
            self.setup_authentication()
            
            # Tìm kiếm
            self.search_keyword(keyword)
            
            # Mở kết quả
            self.open_search_result()
            
            # Download file
            self.download_file()
            
            print("\n✓ Hoàn thành workflow!")
            return True
            
        except Exception as e:
            print(f"\n✗ Lỗi: {e}")
            return False


