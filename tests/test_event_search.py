# EventSearch/tests/test_event_search.py
import allure
import pytest
import logging
from config import EXCEL_FILE, SHEET_NAME, DATA_COLUMN
from utils.excel_reader import load_test_data
from pages.event_search_page import EventSearchPage
from conftest import test_results

logger = logging.getLogger(__name__)

test_data = load_test_data(EXCEL_FILE, SHEET_NAME, DATA_COLUMN)

@allure.feature("事件查询")
@allure.story("信号ID数据验证")
@pytest.mark.parametrize("row_num, keyword", test_data)
def test_event_search(row_num: int, keyword: str, driver_module):
    """
    对每一个 signal_id 执行搜索，只记录结果，不因“暂无数据”而失败。
    """
    logger.info(f"开始测试第 {row_num} 行，关键字: {keyword}")
    page = EventSearchPage(driver_module)

    has_data = False
    try:
        with allure.step("输入关键字并搜索"):
            has_data = page.search(keyword)
    except Exception as e:
        logger.error(f"第 {row_num} 行搜索时发生异常: {e}")
        allure.attach(str(e), "异常信息", allure.attachment_type.TEXT)

    test_results.append((row_num, keyword, has_data))

    # ---- 根据结果动态更新 allure 标题和标签 ----
    if has_data:
        allure.dynamic.title(f"搜索信号ID: {keyword} [有数据]")
        allure.dynamic.tag("有数据")
    else:
        allure.dynamic.title(f"搜索信号ID: {keyword} [暂无数据]")
        allure.dynamic.tag("暂无数据")

    # 记录搜索结果到 Allure
    result_text = "有数据" if has_data else "暂无数据"
    allure.attach(result_text, f"搜索结果 ({keyword})", allure.attachment_type.TEXT)

    if has_data:
        logger.info(f"第 {row_num} 行: 找到数据")
    else:
        logger.info(f"第 {row_num} 行: 未找到数据")