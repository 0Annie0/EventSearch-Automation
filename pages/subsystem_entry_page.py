# EventSearch/pages/subsystem_entry_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

class SubsystemEntryPage:
    """登录后门户主页，提供进入子系统并点击具体菜单的能力"""
    SUBSYSTEM_LIST_LABEL = (By.XPATH, "//strong[text()='子系统列表']")
    OPERATIONS_CARD = (By.XPATH, "//div[@title='B端运营管理系统3.0']")
    VEHICLE_INCIDENT_MENU = (By.XPATH, "//span[normalize-space()='车辆事件']")

    def __init__(self, driver: WebDriver, explicit_wait: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, explicit_wait)

    def open_subsystem_in_new_tab(self) -> str:
        """
        依次点击「子系统列表」 → 「B端运营管理系统3.0」 → 「车辆事件」，
        假设每次点击都会打开新标签页，最终返回子系统窗口的句柄。
        """
        # 1. 点击“子系统列表”（可能只是为了展开，不一定打开新窗口）
        subsystem_list = self.wait.until(EC.element_to_be_clickable(self.SUBSYSTEM_LIST_LABEL))
        subsystem_list.click()

        # 2. 点击“B端运营管理系统3.0”，通常会打开新标签页
        operations_card = self.wait.until(EC.element_to_be_clickable(self.OPERATIONS_CARD))
        operations_card.click()

        # 获取新窗口句柄
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            new_window = all_windows[-1]
            self.driver.switch_to.window(new_window)
        else:
            # 如果没有新窗口，可能是在当前页跳转，使用当前窗口
            new_window = self.driver.current_window_handle

        # 3. 在子系统页面中点击“车辆事件”菜单（可能也是新窗口？）
        vehicle_menu = self.wait.until(EC.element_to_be_clickable(self.VEHICLE_INCIDENT_MENU))
        vehicle_menu.click()

        # 再次检查是否有新窗口（如果点击“车辆事件”也打开了新窗口）
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            new_window = all_windows[-1]
            self.driver.switch_to.window(new_window)

        return new_window