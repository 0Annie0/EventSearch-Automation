# EventSearch Automation

基于 Python + Selenium + Pytest 的 Web UI 自动化测试框架，用于对 B 端管理平台「车辆事件」模块进行数据驱动批量搜索验证，并自动生成带结果的 Excel 文件及 Allure 可视化报告。

## 🚀 项目背景

在日常测试工作中，需要手动在车辆事件页面对数十个信号 ID 逐一搜索，核对是否有数据上报，操作重复且耗时。本项目将这一流程自动化，**单轮 46 条信号校验从约 30 分钟压缩至约 4 分钟**，极大提升回归效率。

## 🛠️ 技术栈

- **语言 & 框架**：Python 3.10+、Pytest 9.x
- **UI 自动化**：Selenium WebDriver、Page Object 模式
- **数据驱动**：openpyxl 读取 Excel 测试数据
- **等待策略**：显式等待（WebDriverWait + expected_conditions）
- **报告**：Allure 2.x（动态标题、标签、附件、失败截图）
- **其他**：webdriver-manager（驱动自动管理）、logging 日志

## 📦 环境要求

- Windows 10/11（也可适配 Linux，需更换 chromedriver 路径）
- Chrome 浏览器
- Python 3.10 或更高
- Allure 命令行工具（可选，用于本地查看报告）

## 📁 项目结构
```
EventSearch/
├── config.py # 全局配置（URL、账号、Excel路径等）
├── conftest.py # Pytest 夹具、钩子函数
├── pytest.ini # Pytest 运行参数
├── pages/ # Page Object 页面封装
│ ├── portal_login_page.py # 门户登录页
│ ├── subsystem_entry_page.py# 子系统入口页
│ └── event_search_page.py # 事件查询页（搜索逻辑）
├── tests/ # 测试用例
│ └── test_event_search.py # 参数化搜索验证
├── utils/ # 工具函数
│ ├── excel_reader.py # 从 Excel 读取测试数据
│ └── excel_writer.py # 将结果写入新的 Excel 文件
├── drivers/ # 存放 chromedriver.exe（已在.gitignore中忽略）
├── test_data.xlsx # 示例测试数据文件（脱敏版本）
└── README.md
```

## ⚙️ 安装与运行

### 1. 克隆仓库
```bash
git clone https://github.com/你的用户名/EventSearch.git
cd EventSearch
```

2. 创建虚拟环境并安装依赖
bash
```
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

注意：requirements.txt 内容为：
```
pytest
selenium
webdriver-manager
openpyxl
allure-pytest
```

3. 配置 config.py
复制 config.example.py 为 config.py，并填入自己的测试环境信息：
```
PORTAL_URL = "你的门户登录页完整URL"
USERNAME = "你的用户名"
PASSWORD = "你的密码"
EXCEL_FILE = r"test_data.xlsx"   # 待搜索的 Excel 文件
VIN = "你的VIN码"
START_TIME = "2026-07-10 00:00:00"
END_TIME = "2026-07-13 23:59:59"
```
4. 准备 ChromeDriver

项目默认从本地 drivers/chromedriver.exe 加载驱动（避免自动下载受网络影响）。
你也可以修改 conftest.py 中的启动方式，使用 webdriver-manager 自动匹配版本。

5. 运行测试
```
pytest
```
测试用例将依次执行搜索，并生成 _结果.xlsx 文件。
同时生成 Allure 原始数据目录 allure-results。

6. 查看 Allure 报告
```
allure serve allure-results
```
报告中将按“有数据/暂无数据”分类展示每条用例，失败用例自动附带截图。

📊 报告示例

https://docs/allure_overview.png 可上传截图到 docs 目录，这里展示占位

    左侧按 Feature/Story 分类

    每个用例标题动态显示搜索关键字和结果

    每条用例包含“输入关键字并搜索”步骤

    结果以文本附件形式附加在报告内

    测试结束后生成摘要统计：总用例数、有数据数、暂无数据数

🎯 核心亮点

    Page Object 设计模式：页面元素定位与业务逻辑分离，维护成本低。

    显式等待 + 智能结果判断：使用 staleness_of 检测 DOM 刷新，兼容节点复用，在准确性和速度间取得平衡。

    完整数据驱动：通过 @pytest.mark.parametrize 从 Excel 读取用例，一条用例覆盖多行数据。

    丰富的 Allure 报告：动态标签、步骤附件、失败截图、会话级汇总统计。

    结果自动输出：测试结束自动生成带“PASS/FAIL”标记和红底高亮的 Excel 文件，可直接交付。

    失败截图钩子：任何搜索异常都会自动截图并附加到报告，便于定位问题。

📝 待优化项

    □ 支持多 VIN 轮换查询
    □ 增加接口层（requests）进行后端数据一致性校验
    □ 集成 Jenkins / GitHub Actions 实现持续集成
    □ 改用 Playwright 对比实现，体验更现代的 API

📄 License

本项目使用 MIT License 开源。

如果这个项目对你有帮助，欢迎给个 ⭐ Star 支持！
