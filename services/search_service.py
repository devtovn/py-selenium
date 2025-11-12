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
    
    # def open_search_result(self):
    #     """Mở kết quả tìm kiếm đầu tiên"""
    #     print("\n=== Bước 2: Mở kết quả tìm kiếm ===")
        
    #     # # Tìm link kết quả
    #     # result_link = self.finder.find_clickable_by_id(Config.RESULT_LINK_ID)
    #     # if not result_link:
    #     #     raise Exception("Không tìm thấy kết quả tìm kiếm")
        
    #     # # Click để mở tab mới
    #     # self.actions.click_element(result_link, wait_after=2)
        
    #     # # Chuyển sang tab mới
    #     # # self.browser.switch_to_new_tab()
    #     # # self.browser.wait_for_page_load()
        
    #     # print("Đã mở kết quả tìm kiếm trong tab mới")


        
    #     try:
    #         # Chờ có ít nhất 1 link kết quả khả dụng
    #         links = WebDriverWait(self.driver, 10).until(
    #             EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='Default.aspx#StaffResult/']"))
    #         )

    #         if not links:
    #             raise Exception("Không tìm thấy kết quả tìm kiếm")

    #         # Click link đầu tiên
    #         first_link = links[0]
    #         print(f"Đang click vào link đầu tiên: {first_link.get_attribute('href')}")
    #         self.actions.click_element(first_link, wait_after=2)

    #         self.browser.switch_to_new_tab()
    #         # self.browser.wait_for_page_load()

    #         print("Đã mở kết quả tìm kiếm trong tab mới")

    #     except Exception as e:
    #         print(f"Lỗi khi mở kết quả tìm kiếm: {e}")

    def open_search_result(self):
        """Mở từng kết quả tìm kiếm và xử lý trong tab mới"""
        print("\n=== Bước 2: Mở từng kết quả tìm kiếm ===")
        self.actionCloseAlert()
        try:
            selector = f"a[href^='{Config.RESULT_LINK_ID}']"
            links = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, selector)
                )
            )

            if not links:
                raise Exception("Không tìm thấy kết quả tìm kiếm")

            print(f"Tìm thấy {len(links)} kết quả. Bắt đầu xử lý...")

            # Lấy tất cả href (vì khi load lại trang, element cũ có thể bị mất)
            link_hrefs = [link.get_attribute("href") for link in links]

            for index, href in enumerate(link_hrefs):
                print(f"\n [{index+1}/{len(link_hrefs)}] Đang mở link: {href}")

                # Mở tab mới
                self.driver.execute_script("window.open(arguments[0], '_blank');", href)

                # Chuyển sang tab mới
                self.driver.switch_to.window(self.driver.window_handles[-1])
                print("Đã chuyển sang tab kết quả thi")

                try:
                    # Gọi hàm download file trong tab mới
                    self.download_file()
                    self.actionCloseAlert()
                except Exception as e:
                    print(f"Lỗi khi tải file ở link này: {e}")

                # Đóng tab kết quả
                self.driver.close()
                print("Đã đóng tab chi tiết")

                # Quay lại tab chính
                self.driver.switch_to.window(self.driver.window_handles[0])
                print("Quay lại danh sách để xử lý link tiếp theo")

                # Đợi trang ổn định một chút
                time.sleep(2)

            print("\n Hoàn tất xử lý tất cả kết quả tìm kiếm.")

        except Exception as e:
            print(f"Lỗi khi mở kết quả tìm kiếm: {e}")

    
    def download_file(self):
        """Tải tất cả file trong trang chi tiết"""
        print("\n=== Bước 3: Tải tất cả file trong trang chi tiết ===")

        # Đợi trang load
        time.sleep(Config.DOWNLOAD_WAIT_TIME)

        # Đóng popup / overlay nếu có
        self.actionCloseAlert()

        try:
            selector = f"a[href^='{Config.DOWNLOAD_LINK_ID}']"
            links = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, selector)
                )
            )

            if not links:
                raise Exception("Không tìm thấy link download")

            print(f"Tìm thấy {len(links)} link file cần tải.")

            # Duyệt qua từng link và click
            for index, link in enumerate(links, start=1):
                href = link.get_attribute("href")
                print(f"[{index}/{len(links)}] Đang click tải file: {href}")
                try:
                    self.actions.click_element(link, wait_after=2)
                    print("Đã click tải file thành công.")
                except Exception as e:
                    print(f"Lỗi khi click link: {e}")
                
                # Đợi 1 chút giữa các lần click (tránh lỗi browser hoặc mạng)
                time.sleep(1)

            print("Hoàn tất tải tất cả file trong trang.")

        except Exception as e:
            print(f"Lỗi khi tải file: {e}")

        # Nghỉ thêm 2s để đảm bảo download hoàn tất
        time.sleep(2)

    
    def actionCloseAlert(self):
        # Kiêm tra nếu bị overlay modal
        prevent_btn = self.finder.find_clickable_by_id("btnNO")
        if prevent_btn:
            print("Tìm thấy nút đóng overlay (btnNO) — đang click...")
            self.actions.click_element(prevent_btn, wait_after=3)
        else:
            print("Không tìm thấy nút btnNO — bỏ qua và tiếp tục.")
    
    # def download_file(self):
    #     """Tải file hoặc mở kết quả thi"""
    #     print("\n=== Bước 3: Mở link kết quả thi ===")

    #     # Đợi trang ổn định
    #     time.sleep(Config.DOWNLOAD_WAIT_TIME)

    #     # Đóng overlay nếu có
    #     prevent_btn = self.finder.find_clickable_by_id("btnNO")
    #     if prevent_btn:
    #         print("Tìm thấy nút đóng overlay (btnNO) — đang click...")
    #         self.actions.click_element(prevent_btn, wait_after=3)
    #     else:
    #         print("Không tìm thấy nút btnNO — bỏ qua và tiếp tục.")

    #     # Chờ bảng kết quả load xong
    #     table_rows = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tr"))
    #     )
    #     print(f"Tìm thấy {len(table_rows)} hàng trong bảng, đang kiểm tra link...")

    #     target_links = []

    #     # Duyệt từng hàng để tìm <a> có href bắt đầu bằng "Default.aspx#StaffResult/"
    #     for row in table_rows:
    #         links_in_row = row.find_elements(By.CSS_SELECTOR, "a[href^='Default.aspx#StaffResult/']")
    #         if links_in_row:
    #             href = links_in_row[0].get_attribute("href")
    #             print(f" Tìm thấy link trong hàng: {href}")
    #             target_links.append(links_in_row[0])

    #     if not target_links:
    #         raise Exception("Không tìm thấy link nào chứa 'Default.aspx#StaffResult/'")

    #     # Click từng link (hoặc chỉ click link đầu tiên)
    #     for link in target_links:
    #         href = link.get_attribute("href")
    #         print(f"Đang click vào link: {href}")
    #         self.actions.click_element(link, wait_after=3)

    #     print(" Đã click tất cả link kết quả trong bảng.")


    
    def execute_workflow(self, keyword: str):
        """Thực hiện toàn bộ workflow"""
        try:
            # Setup authentication
            self.setup_authentication()
            
            # # Tìm kiếm
            self.search_from_file(Config.FILE_SEARCH)
            # # self.search_keyword(keyword)
            
            # # Mở kết quả
            self.open_search_result()
            
            # Download file
            # self.download_file()
            
            print("\n✓ Hoàn thành workflow!")
            return True
            
        except Exception as e:
            print(f"\n✗ Lỗi: {e}")
            return False


