# ==================== services/search_service.py ====================
from common.element_finder import ElementFinder
from common.element_actions import ElementActions
from common.browser_actions import BrowserActions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
import time
import os

class SearchService:
    """Service xử lý tìm kiếm và tải file"""
    
    def __init__(self, driver):
        self.driver = driver
        self.finder = ElementFinder(driver, Config.DEFAULT_TIMEOUT)
        self.actions = ElementActions(driver)
        self.browser = BrowserActions(driver)
        self.wait = WebDriverWait(driver, 10)
    
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
        
        # # Refresh để cookie có hiệu lực
        # self.browser.refresh_page()
        # time.sleep(2)


        self.browser.navigate_to(Config.BASE_URL)
        time.sleep(2)
        # self.browser.refresh_page()
        # time.sleep(2)
        
    
    def search_keyword(self, keyword: str):
        """Tìm kiếm với keyword"""
        print(f"\n=== Bước 1: Tìm kiếm keyword '{keyword}' ===")
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-dialog")))
            print("Trang chính đã load sau login.")
        except Exception:
            print("Không tìm thấy phần tử trang chính sau login, vẫn tiếp tục...")


        # Kiêm tra nếu bị overlay modal
        prevent_btn = self.finder.find_clickable_by_id("btnNO")
        if prevent_btn:
            print("Tìm thấy nút đóng overlay (btnNO) — đang click...")
            self.actions.click_element(prevent_btn, wait_after=3)
        else:
            print("Không tìm thấy nút btnNO — bỏ qua và tiếp tục.")
        
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

    def search_from_file(self, file_path: str):
        """Đọc file .txt và tìm kiếm từng dòng"""
        print(f"\n=== Bắt đầu đọc file: {file_path} ===")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "keywords.txt")

        print(f"\n=== Bắt đầu đọc file: {file_path} ===")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, start=1):
                    keyword = line.strip()
                    if not keyword:
                        continue  # bỏ qua dòng trống
                    print(f"\n[{line_num}] Đang xử lý keyword: {keyword}")

                    try:
                        self.search_keyword(keyword)
                    except Exception as e:
                        print(f"Lỗi khi tìm kiếm '{keyword}': {e}")

                    print("Đợi 10 giây trước khi tìm tiếp...")
                    time.sleep(10)

            print("\n=== Đã xử lý hết các keyword trong file ===")
        except FileNotFoundError:
            print(f"Không tìm thấy file: {file_path}")
    
    def open_search_result(self):
        """Mở kết quả tìm kiếm đầu tiên"""
        print("\n=== Bước 2: Mở kết quả tìm kiếm ===")
        
        # # Tìm link kết quả
        # result_link = self.finder.find_clickable_by_id(Config.RESULT_LINK_ID)
        # if not result_link:
        #     raise Exception("Không tìm thấy kết quả tìm kiếm")
        
        # # Click để mở tab mới
        # self.actions.click_element(result_link, wait_after=2)
        
        # # Chuyển sang tab mới
        # # self.browser.switch_to_new_tab()
        # # self.browser.wait_for_page_load()
        
        # print("Đã mở kết quả tìm kiếm trong tab mới")


        
        try:
            # Chờ có ít nhất 1 link kết quả khả dụng
            links = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='Default.aspx#StaffResult/']"))
            )

            if not links:
                raise Exception("Không tìm thấy kết quả tìm kiếm")

            # Click link đầu tiên
            first_link = links[0]
            print(f"Đang click vào link đầu tiên: {first_link.get_attribute('href')}")
            self.actions.click_element(first_link, wait_after=2)

            self.browser.switch_to_new_tab()
            # self.browser.wait_for_page_load()

            print("Đã mở kết quả tìm kiếm trong tab mới")

        except Exception as e:
            print(f"Lỗi khi mở kết quả tìm kiếm: {e}")
    
    def download_file(self):
        """Tải file PDF"""
        print("\n=== Bước 3: Tải file PDF ===")
        
        # Đợi page load
        time.sleep(Config.DOWNLOAD_WAIT_TIME)
        
        # Tìm link download
        # download_link = self.finder.find_clickable_by_id(Config.DOWNLOAD_LINK_ID)
        # if not download_link:
        #     raise Exception("Không tìm thấy link download")
        
        # # Click để download
        # self.actions.click_element(download_link, wait_after=2)

        # Kiêm tra nếu bị overlay modal
        prevent_btn = self.finder.find_clickable_by_id("btnNO")
        if prevent_btn:
            print("Tìm thấy nút đóng overlay (btnNO) — đang click...")
            self.actions.click_element(prevent_btn, wait_after=3)
        else:
            print("Không tìm thấy nút btnNO — bỏ qua và tiếp tục.")
        # Chờ có ít nhất 1 link kết quả khả dụng
        links = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='/Portal.IU.CMS/Upload/files/']"))
        )

        if not links:
            raise Exception("Không tìm thấy link download")

       # Click để download
        download_link = links[0]
        print(f"Đang click vào link download: {download_link.get_attribute('href')}")
        self.actions.click_element(download_link, wait_after=2)
        print("Đã download file")
        time.sleep(30)
    
    def execute_workflow(self, keyword: str):
        """Thực hiện toàn bộ workflow"""
        try:
            # Setup authentication
            self.setup_authentication()
            
            # Tìm kiếm
            self.search_from_file("keywords.txt")
            # self.search_keyword(keyword)
            
            # Mở kết quả
            self.open_search_result()
            
            # Download file
            self.download_file()
            
            print("\n✓ Hoàn thành workflow!")
            return True
            
        except Exception as e:
            print(f"\n✗ Lỗi: {e}")
            return False


