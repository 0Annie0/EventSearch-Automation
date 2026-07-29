#EventSearch/config.py
# ========== 门户登录相关 ==========
PORTAL_URL = "https://your-portal-url.com"
USERNAME = "your_username"          # 登录用户名
PASSWORD = "your_password"          # 登录密码

# ========== Excel 数据 ==========
EXCEL_FILE = r"test_data.xlsx"   # 待搜索的 Excel 文件
SHEET_NAME = "事件测试"
DATA_COLUMN = "C"

# ========== 结果写入 Excel 配置 ==========
RESULT_COLUMN = "H"          # 结果写入的列字母（如 H 列）
RESULT_FILE_SUFFIX = "_结果.xlsx"  # 生成的结果文件名后缀

# ========== VIN 数据 ==========
VIN = "你的VIN码"

# ========== 查询事件的全局时间 ==========
START_TIME = "2026-07-10 00:00:00"
END_TIME   = "2026-07-13 23:59:59"

# ========== 浏览器设置 ==========
IMPLICIT_WAIT = 3               # 隐式等待秒数
EXPLICIT_WAIT = 20              # 显式等待超时秒数