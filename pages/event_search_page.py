# EventSearch/pages/event_search_page.py
import time
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

class EventSearchPage:
    """子系统事件查询页面"""
    # VIN码输入框
    VIN_INPUT = (By.XPATH, "//input[contains(@placeholder, '请输入VIN')]")

    # 信号ID搜索区域
    SIGNAL_ID_INPUT = (By.XPATH, "//input[contains(@placeholder, '请选择signal_id')]")
    # 下拉选项（精确匹配文本）
    DROPDOWN_OPTION_TEMPLATE = "//li[contains(@class,'el-select-dropdown__item')]//span[normalize-space(text())='{keyword}']"
    # 备用：第一个可见的下拉选项
    FIRST_VISIBLE_OPTION = (By.XPATH, "//li[contains(@class,'el-select-dropdown__item') and not(contains(@class,'hidden'))][1]")
    # 搜索按钮
    SEARCH_BUTTON = (By.XPATH, "//button[contains(@class,'el-button--primary')]//span[text()='搜索']/parent::button")
    # 结果判断
    RESULT_TOTAL = (By.XPATH, "//*[contains(text(),'共') and contains(text(),'条')]")
    NO_DATA_TEXT = (By.XPATH, "//*[contains(text(),'暂无数据')]")

    def __init__(self, driver: WebDriver, explicit_wait: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, explicit_wait)

    def condition(self, vin: str, start_time: str, end_time: str) -> None:
        """前置操作：输入 VIN，并通过日期范围选择器设置起止时间"""
        # 输入VIN
        vin_input = self.wait.until(EC.element_to_be_clickable(self.VIN_INPUT))
        vin_input.clear()
        vin_input.send_keys(vin)

        # 打开日期范围选择器
        date_picker = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".el-date-editor--datetimerange"))
        )
        date_picker.click()

        # 等待面板出现
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "el-picker-panel__body")))

        # 拆分起止日期和时间
        start_date, start_time_str = start_time.split(' ')
        end_date, end_time_str = end_time.split(' ')

        # 四个输入框
        start_date_input = self.driver.find_element(
            By.XPATH, "//div[contains(@class,'el-date-range-picker__time-header')]//input[@placeholder='开始日期']"
        )
        start_time_input = self.driver.find_element(
            By.XPATH, "//div[contains(@class,'el-date-range-picker__time-header')]//input[@placeholder='开始时间']"
        )
        end_date_input = self.driver.find_element(
            By.XPATH, "//div[contains(@class,'el-date-range-picker__time-header')]//input[@placeholder='结束日期']"
        )
        end_time_input = self.driver.find_element(
            By.XPATH, "//div[contains(@class,'el-date-range-picker__time-header')]//input[@placeholder='结束时间']"
        )

        # 填入日期和时间（逐一点击再输入，触发前端响应）
        for field, value in [
            (start_date_input, start_date),
            (start_time_input, start_time_str),
            (end_date_input, end_date),
            (end_time_input, end_time_str),
        ]:
            field.click()
            field.clear()
            field.send_keys(value)
            time.sleep(0.2)  # 给前端一点反应时间

        # 点击确定按钮，关闭面板
        confirm_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='el-picker-panel__footer']//button[contains(.,'确定')]")
            )
        )
        confirm_btn.click()
        self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "el-picker-panel__body")))

    def search(self, keyword: str) -> bool:
        # 1. 输入关键字并选择下拉选项（同你原来的代码）
        input_elem = self.wait.until(EC.element_to_be_clickable(self.SIGNAL_ID_INPUT))
        input_elem.click()
        input_elem.clear()
        input_elem.send_keys(keyword)

        option_xpath = f"//li[contains(@class,'el-select-dropdown__item')]//span[normalize-space(text())='{keyword}']"
        option_locator = (By.XPATH, option_xpath)
        try:
            option = self.wait.until(EC.element_to_be_clickable(option_locator))
        except TimeoutException:
            option_locator = (By.XPATH,
                              "//li[contains(@class,'el-select-dropdown__item')]//span[not(contains(text(),'取消'))][1]")
            option = self.wait.until(EC.element_to_be_clickable(option_locator))
        option.click()

        # 2. 记录旧结果元素（如果有）
        try:
            old_total = self.driver.find_element(*self.RESULT_TOTAL)
        except:
            old_total = None

        # 3. 点击搜索按钮
        search_btn = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))
        search_btn.click()

        # 4. 等待旧元素失效（超时时间改为0.5秒，既保证检测节点复用，又快速跳过）
        if old_total:
            try:
                WebDriverWait(self.driver, 0.5).until(EC.staleness_of(old_total))
            except TimeoutException:
                # 0.5秒内旧元素没消失，说明节点复用，直接继续等待新结果
                pass

        # 5. 等待新结果出现（最多5秒）
        try:
            WebDriverWait(self.driver, 5).until(
                EC.any_of(
                    EC.presence_of_element_located(self.RESULT_TOTAL),
                    EC.presence_of_element_located(self.NO_DATA_TEXT)
                )
            )
        except TimeoutException:
            return False

        # 6. 判断数据
        if self._is_element_present(self.RESULT_TOTAL):
            total_text = self.driver.find_element(*self.RESULT_TOTAL).text
            count = int(''.join(filter(str.isdigit, total_text)) or 0)
            return count > 0
        elif self._is_element_present(self.NO_DATA_TEXT):
            return False
        return False

    def _is_element_present(self, locator: tuple) -> bool:
        """判断元素是否存在于DOM中（不关心是否可见）"""
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False