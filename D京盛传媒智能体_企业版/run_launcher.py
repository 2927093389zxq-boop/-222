# =========================================================================
# ===== 1. 关键修复：解决 Windows 环境下 Playwright 的兼容性问题 =====
# =========================================================================
# 这段代码必须放在所有其他代码之前执行
import asyncio
import platform

# 检查当前操作系统是否为 Windows
if platform.system() == "Windows":
    # 如果是，则设置一个不同的异步事件循环策略
    # 这是解决 Playwright 在某些 Windows 环境下报错 "NotImplementedError" 的标准方法
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# =======================================================================
# ===== 2. 导入所有需要的模块 (已为您整理好) =====
# =======================================================================
import streamlit as st
from datetime import datetime
import os
import json
import socket
from dotenv import load_dotenv

# 导入许可证和遥测模块
from distribution.license_manager import LicenseManager
from distribution.telemetry import TelemetrySystem

# 在 .env 加载后导入您的UI和核心模块
load_dotenv()
from ui.dashboard import render_dashboard
from ui.analytics import render_analytics
from ui.prototype_view import render_prototype
from core.collectors.market_collector import fetch_all_trends
from core.collectors.youtube_collector import fetch_channel_stats
from core.collectors.policy_collector import fetch_latest_policies
from ui.api_admin import render_api_admin
from ui.auto_evolution import render_auto_evolution
from ui.auto_patch_view import render_auto_patch
from ui.ai_learning_center import render_ai_learning_center
from ui.source_attribution import render_sources


# =======================================================================
# ===== 3. 许可证验证功能 (来自您的代码) =====
# =======================================================================
telemetry = None # 全局遥测变量

def check_license():
    """检查许可证是否有效"""
    license_manager = LicenseManager()
    if not os.path.exists("license.json"):
        if os.path.exists(".dev"): return {"valid": True, "feature_set": "all"}
        return {"valid": False, "reason": "未找到许可证文件"}
    
    try:
        with open("license.json", "r") as f:
            license_data = json.load(f)
        result = license_manager.verify_license(license_data)
        if result["valid"] and license_data["data"].get("telemetry_enabled", True):
            global telemetry
            telemetry = TelemetrySystem()
            telemetry.collect_system_info()
        return result
    except Exception as e:
        return {"valid": False, "reason": f"许可证验证失败: {str(e)}"}

def render_license_page():
    """渲染许可证页面"""
    st.title("📜 许可证激活")
    st.write("请上传有效的许可证文件以激活软件。")
    uploaded_file = st.file_uploader("选择许可证文件", type=["json"])
    if uploaded_file is not None:
        try:
            license_data = json.load(uploaded_file)
            license_manager = LicenseManager()
            result = license_manager.verify_license(license_data)
            if result["valid"]:
                with open("license.json", "w") as f:
                    json.dump(license_data, f)
                st.success("许可证已激活！")
                st.write(f"功能集: {result.get('feature_set', 'N/A')}")
                st.write(f"有效期: {result.get('expires_in_days', 'N/A')} 天")
                if st.button("开始使用"):
                    st.rerun()
            else:
                st.error(f"无效的许可证: {result['reason']}")
        except Exception as e:
            st.error(f"无法读取许可证文件: {str(e)}")


# =======================================================================
# ===== 4. 主程序入口 (已为您合并整理) =====
# =======================================================================
def main():
    """程序主入口"""
    # 首先设置页面配置
    st.set_page_config(page_title="京盛传媒 企业版智能体", layout="wide")

    # 进行许可证检查
    license_result = check_license()
    if not license_result.get("valid"):
        render_license_page()
        return # 如果许可证无效，则停止执行后续代码

    # 许可证有效，渲染主应用界面
    st.title("京盛传媒 企业版智能体")

    # ===== 侧边栏菜单 =====
    menu = st.sidebar.selectbox(
        "导航",
        [
            "主页", "智能分析", "原型测试",
            "权威数据中心", "数据来源追踪", "YouTube", "TikTok",
            "AI 学习中心", "AI 自主迭代", "AI 自动修复", 
            "API 管理", "政策中心", "系统概览", "日志与设置"
        ]
    )
    
    # 跟踪功能使用
    if telemetry:
        telemetry.track_feature_usage(menu)

    # ===== 页面路由逻辑 =====
    if menu == "主页":
        render_dashboard()
    elif menu == "系统概览":
        st.header("系统概览")
        st.metric("主机", socket.gethostname())
        st.metric("系统", platform.platform())
        st.metric("时间", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    elif menu == "智能分析":
        render_analytics()
    elif menu == "原型测试":
        render_prototype()
    elif menu == "权威数据中心":
        st.header("权威数据中心")
        st.info("数据来自：1688 / QuestMobile / 艾瑞 / 易观 等（示例）")
        for d in fetch_all_trends():
            st.markdown(f"**来源**：[{d.get('source')}]({d.get('url')})  \n- 时间：{d.get('fetched_at')}  \n- 内容：{d.get('metric', d.get('data',''))}  \n- 权威度：{d.get('credibility','N/A')}")
    elif menu == "数据来源追踪":
        render_sources()
    elif menu == "YouTube":
        st.header("YouTube 频道查询")
        cid = st.text_input("频道 ID")
        if st.button("获取频道统计"):
            try:
                res = fetch_channel_stats(cid)
                st.json(res)
            except Exception as e:
                st.error(str(e))
    elif menu == "TikTok":
        st.header("TikTok 趋势（占位）")
        st.write("当前使用公共占位源，正式接入请在 API 管理中添加接口。")
    elif menu == "API 管理":
        render_api_admin()
    elif menu == "政策中心":
        st.header("政策中心")
        lst = fetch_latest_policies()
        for p in lst:
            st.markdown(f"**{p.get('source',{}).get('agency','未知')}** - {p.get('fetched_at')}  \n{p.get('snippet','')}")
    elif menu == "AI 学习中心":
        render_ai_learning_center()
    elif menu == "AI 自主迭代":
        render_auto_evolution()
    elif menu == "AI 自动修复":
        render_auto_patch()
    elif menu == "日志与设置":
        st.header("日志与设置")
        st.write("请在 config/config.json 中管理邮箱、调度等设置。")

# --- 程序启动 ---
if __name__ == "__main__":
    main()