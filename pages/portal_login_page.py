# EventSearch/pages/portal_login_page.py
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
import time
from config import PORTAL_URL

class PortalLoginPage:
    """门户登录页面对象"""
    USERNAME_INPUT = (By.XPATH, "//input[contains(@data-bind, 'username')]")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password' and contains(@data-bind, 'password')]")
    LOGIN_BUTTON = (By.XPATH, "//a[contains(@class, 'submit') and contains(text(), '登录')]")
    LOGIN_SUCCESS_INDICATOR = (By.XPATH, "//strong[text()='子系统列表']")

    def __init__(self, driver: WebDriver, explicit_wait: int = 20):
        self.driver = driver
        self.wait = WebDriverWait(driver, explicit_wait)

    def login(self, username: str, password: str) -> None:
        """填写用户名、密码并点击登录，等待页面跳转到门户主页"""
        self.driver.get(PORTAL_URL)

        # 用户名
        username_elem = self.wait.until(EC.element_to_be_clickable(self.USERNAME_INPUT))
        username_elem.clear()
        username_elem.send_keys(username)

        # 密码
        password_elem = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_INPUT))
        password_elem.click()          # 某些前端需点击才能激活输入
        time.sleep(0.3)
        password_elem.clear()
        password_elem.send_keys(password)

        # 登录按钮
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()

        # 等待登录成功标志出现（例如“子系统列表”文字可见）
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_SUCCESS_INDICATOR))