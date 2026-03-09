"""
东盟轨道交通研究Agent - Web仪表盘启动脚本
运行此脚本以启动Streamlit可视化界面
"""

import subprocess
import sys
import os

def check_dependencies():
    """检查依赖是否安装"""
    required_packages = ['streamlit', 'pandas', 'plotly']

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("⚠️  缺少以下依赖包:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        print("\n请安装依赖包:")
        print("pip install streamlit pandas plotly")
        return False

    return True

def start_dashboard():
    """启动Streamlit仪表盘"""
    if not check_dependencies():
        sys.exit(1)

    print("🚀 正在启动东盟轨道交通研究Agent仪表盘...")
    print("📊 可访问地址: http://localhost:8501")
    print("\n按 Ctrl+C 停止服务器\n")

    # 检查核心文件是否存在
    required_files = [
        'asean_rail_research_agent.py',
        'asean_rail_dashboard.py',
        'asean_rail_intelligence_report.json'
    ]

    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 缺少必要文件: {file}")
            sys.exit(1)

    print("✓ 所有必要文件已就绪")
    print("✓ 启动Streamlit服务器...\n")

    # 启动Streamlit
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run',
            'asean_rail_dashboard.py',
            '--server.headless', 'true',
            '--server.port', '8501'
        ])
    except KeyboardInterrupt:
        print("\n\n👋 仪表盘已关闭")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_dashboard()
