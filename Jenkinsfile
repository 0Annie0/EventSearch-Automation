pipeline {
    agent any   // 在任何可用节点上运行

    environment {
        // 定义全局环境变量，方便后面使用
        ALLURE_RESULTS = "allure-results"
    }

    stages {
        stage('Checkout') {
            steps {
                // 从 Git 拉取代码
                git branch: 'main', url: 'https://github.com/你的用户名/EventSearch.git'
            }
        }

        stage('Setup Python') {
            steps {
                // 使用 Windows 的 bat 命令
                bat '''
                    echo "正在创建虚拟环境..."
                    python -m venv venv
                    venv\\Scripts\\activate.bat && pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    venv\\Scripts\\activate.bat && pytest --alluredir=%ALLURE_RESULTS% --clean-alluredir
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                script {
                    allure includeProperties: false,
                           jdk: '',
                           results: [[path: "${ALLURE_RESULTS}"]]
                }
            }
        }
    }

    post {
        always {
            // 无论成功或失败，都清理工作空间（可选）
            cleanWs()
        }
    }
}