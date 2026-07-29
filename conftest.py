# EventSearch/conftest.py
import pytest
import logging
import os
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import (
    USERNAME, PASSWORD, IMPLICIT_WAIT, EXPLICIT_WAIT,
    VIN, START_TIME, END_TIME, EXCEL_FILE, SHEET_NAME, RESULT_COLUMN
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 模块级结果收集容器
test_results = []

@pytest.fixture(scope="module")
def driver_module():
    logger.info("===== 启动 Chrome 浏览器 =====")
    driver_path = os.path.join(os.path.dirname(__file__), 'drivers', 'chromedriver.exe')
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.implicitly_wait(IMPLICIT_WAIT)  # 现在为0

    from pages.portal_login_page import PortalLoginPage
    login_page = PortalLoginPage(driver, EXPLICIT_WAIT)
    login_page.login(USERNAME, PASSWORD)
    logger.info("✅ 登录成功，当前URL: %s", driver.current_url)

    from pages.subsystem_entry_page import SubsystemEntryPage
    entry_page = SubsystemEntryPage(driver, EXPLICIT_WAIT)
    new_handle = entry_page.open_subsystem_in_new_tab()
    driver.switch_to.window(new_handle)
    logger.info("✅ 已切换到子系统页面，URL: %s", driver.current_url)

    from pages.event_search_page import EventSearchPage
    search_page = EventSearchPage(driver, EXPLICIT_WAIT)
    search_page.condition(VIN, START_TIME, END_TIME)

    yield driver

    # teardown：写入 Excel
    logger.info("所有用例执行完毕，开始生成测试结果文件...")
    from utils.excel_writer import write_results_to_excel
    write_results_to_excel(EXCEL_FILE, SHEET_NAME, RESULT_COLUMN, test_results)

    driver.quit()
    logger.info("===== 浏览器已关闭 =====")


# ========= 失败自动截图（可选） =========
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试用例失败时自动截图，并附加到 allure 报告"""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver_module")
        if driver:
            try:
                screenshot_name = f"screenshot_{item.name}.png"
                driver.save_screenshot(screenshot_name)
                allure.attach.file(screenshot_name, name="失败截图", attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                logger.error(f"截图失败: {e}")

# 在 conftest.py 末尾添加
def pytest_sessionfinish(session, exitstatus):
    """测试会话结束时，生成结果汇总并附加到 Allure 报告"""
    total = len(test_results)
    has_data_count = sum(1 for _, _, passed in test_results if passed)
    no_data_count = total - has_data_count

    summary = f"总用例数: {total}\n有数据: {has_data_count}\n暂无数据: {no_data_count}"
    logger.info(summary)

    # 如果产生了 Allure 结果目录，将汇总保存为文件附件
    allure_dir = session.config.getoption("alluredir", None)
    if allure_dir:
        summary_file = os.path.join(allure_dir, "summary.txt")
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(summary)