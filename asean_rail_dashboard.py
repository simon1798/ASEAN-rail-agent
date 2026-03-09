"""
东盟轨道交通研究Agent - Web可视化仪表盘
基于Streamlit的交互式数据可视化界面
"""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="东盟轨道交通研究平台",
    page_icon="🚄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e88e5;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    .risk-high {
        background: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        border-radius: 5px;
    }
    .risk-medium {
        background: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        border-radius: 5px;
    }
    .risk-low {
        background: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 5px;
    }
    .opportunity-card {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 加载数据
@st.cache_data
def load_data():
    """加载Agent数据"""
    try:
        with open('asean_rail_research_agent.py', 'r', encoding='utf-8') as f:
            agent_code = f.read()

        # 执行Agent代码获取数据
        import importlib.util
        spec = importlib.util.spec_from_file_location("agent", "asean_rail_research_agent.py")
        agent_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(agent_module)

        agent = agent_module.ASEANRailResearchAgent()
        return agent
    except Exception as e:
        st.error(f"加载数据失败: {e}")
        return None

# 加载报告
@st.cache_data
def load_report():
    """加载情报报告"""
    try:
        with open('asean_rail_intelligence_report.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

# 侧边栏
def render_sidebar(agent, report):
    """渲染侧边栏导航"""
    with st.sidebar:
        st.markdown("### 🚄 东盟轨道交通研究平台")
        st.markdown(f"*版本 {agent.version}*")

        st.markdown("---")

        # 功能导航
        st.markdown("### 功能导航")
        page = st.radio(
            "选择页面",
            [
                "📊 市场概览",
                "🏢 企业分析",
                "🗺️ 项目地图",
                "⚠️ 风险预警",
                "💡 机会匹配",
                "📈 数据报表"
            ]
        )

        st.markdown("---")

        # 关键指标
        st.markdown("### 关键指标")
        if report:
            st.metric(
                "顶级机会",
                f"{len(report.get('top_opportunities', []))}个"
            )
            st.metric(
                "风险预警",
                f"{len(report.get('risk_alerts', []))}个"
            )
            st.metric(
                "市场增长率",
                "4.89%"
            )

        st.markdown("---")

        # 数据更新时间
        st.markdown(f"📅 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    return page

# 市场概览页面
def render_market_overview(agent, report):
    """渲染市场概览页面"""
    st.markdown('<div class="main-header">📊 东盟轨道交通市场概览</div>', unsafe_allow_html=True)

    if not report:
        st.warning("暂无报告数据")
        return

    # 市场概要
    st.markdown("### 市场概要")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "东盟总人口",
            report['summary']['total_asean_population']
        )

    with col2:
        market_size = report['summary']['rail_investment_outlook'].split('预计')[0].replace('东盟铁路市场规模', '').strip()
        st.metric(
            "2025年市场规模",
            market_size
        )

    with col3:
        market_forecast = report['summary']['rail_investment_outlook'].split('预计')[1].split('CAGR')[0].strip()
        st.metric(
            "2034年预测",
            market_forecast
        )

    with col4:
        st.metric(
            "复合增长率",
            "4.89%"
        )

    st.markdown("---")

    # 关键趋势
    st.markdown("### 📈 关键发展趋势")
    trends = report['summary']['key_trends']

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(f"**跨境铁路**\n\n{trends[0]}")

    with col2:
        st.info(f"**融资多元化**\n\n{trends[1]}")

    with col3:
        st.info(f"**技术标准**\n\n{trends[2]}")

    st.markdown("---")

    # 各国项目分布
    st.markdown("### 🌏 各国重点项目分布")

    country_data = []
    for country in ['vietnam', 'thailand', 'malaysia', 'indonesia', 'singapore']:
        if country in agent.projects_db:
            project_count = len(agent.projects_db[country])
            total_investment = 0

            for project_key, project in agent.projects_db[country].items():
                if 'investment' in project:
                    inv_str = project['investment']
                    if '亿美元' in inv_str:
                        inv_value = float(inv_str.replace('亿美元', '').replace('约', ''))
                        total_investment += inv_value

            country_data.append({
                '国家': agent.countries_db[country]['name_zh'],
                '项目数量': project_count,
                '总投资(亿美元)': total_investment
            })

    df_countries = pd.DataFrame(country_data)

    # 项目数量柱状图
    col1, col2 = st.columns(2)

    with col1:
        fig_projects = px.bar(
            df_countries,
            x='国家',
            y='项目数量',
            title='各国重点项目数量',
            color='项目数量',
            color_continuous_scale='Blues'
        )
        fig_projects.update_layout(xaxis_title='', yaxis_title='项目数量')
        st.plotly_chart(fig_projects, use_container_width=True)

    with col2:
        fig_investment = px.bar(
            df_countries,
            x='国家',
            y='总投资(亿美元)',
            title='各国总投资规模',
            color='总投资(亿美元)',
            color_continuous_scale='Reds'
        )
        fig_investment.update_layout(xaxis_title='', yaxis_title='投资(亿美元)')
        st.plotly_chart(fig_investment, use_container_width=True)

# 企业分析页面
def render_company_analysis(agent):
    """渲染企业分析页面"""
    st.markdown('<div class="main-header">🏢 中国企业出海能力分析</div>', unsafe_allow_html=True)

    # 企业类别
    categories = list(agent.companies_db.keys())

    selected_category = st.selectbox(
        "选择企业类别",
        categories,
        format_func=lambda x: agent.companies_db[x]['category']
    )

    if selected_category:
        category_data = agent.companies_db[selected_category]

        st.markdown(f"### {category_data['category']}")

        for company in category_data['companies']:
            with st.expander(f"🏢 {company['name']}", expanded=False):
                st.markdown(f"**核心优势:**")
                for advantage in company['core_advantages']:
                    st.markdown(f"- {advantage}")

                if 'asean_cases' in company:
                    st.markdown(f"**东盟项目案例:**")
                    for case in company['asean_cases']:
                        st.markdown(f"- **{case['project']}**")
                        for key, value in case.items():
                            if key != 'project':
                                st.markdown(f"  - {key}: {value}")

    st.markdown("---")

    # 市场份额分析
    st.markdown("### 📊 市场份额分析")

    # 马来西亚市场份额
    st.markdown("#### 马来西亚轨道交通市场份额")
    share_data = {
        '企业': ['中国中车', '阿尔斯通', '西门子', '川崎重工', '其他'],
        '市场份额': [85, 5, 4, 3, 3]
    }
    df_share = pd.DataFrame(share_data)

    fig_share = px.pie(
        df_share,
        values='市场份额',
        names='企业',
        title='马来西亚轨道交通市场份额分布',
        hole=0.4
    )
    fig_share.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_share, use_container_width=True)

# 项目地图页面
def render_project_map(agent):
    """渲染项目地图页面"""
    st.markdown('<div class="main-header">🗺️ 东盟轨道交通项目分布</div>', unsafe_allow_html=True)

    # 项目数据
    project_data = []
    for country in ['vietnam', 'thailand', 'malaysia', 'indonesia', 'singapore']:
        if country in agent.projects_db:
            for project_key, project in agent.projects_db[country].items():
                project_data.append({
                    '国家': agent.countries_db[country]['name_zh'],
                    '项目名称': project.get('name', project_key),
                    '投资': project.get('investment', 'N/A'),
                    '长度(公里)': project.get('length', 'N/A'),
                    '状态': project.get('status', 'N/A'),
                    '时间表': project.get('timeline', 'N/A')
                })

    df_projects = pd.DataFrame(project_data)

    # 筛选
    selected_country = st.multiselect(
        "选择国家",
        df_projects['国家'].unique(),
        default=df_projects['国家'].unique()
    )

    if selected_country:
        df_filtered = df_projects[df_projects['国家'].isin(selected_country)]
    else:
        df_filtered = df_projects

    # 项目表格
    st.dataframe(
        df_filtered,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # 项目详情
    st.markdown("### 项目详情")

    selected_project = st.selectbox(
        "选择项目查看详情",
        df_filtered['项目名称'].unique()
    )

    if selected_project:
        project_detail = df_filtered[df_filtered['项目名称'] == selected_project].iloc[0]

        col1, col2 = st.columns(2)

        with col1:
            st.metric("国家", project_detail['国家'])
            st.metric("投资", project_detail['投资'])
            st.metric("长度", project_detail['长度(公里)'])

        with col2:
            st.metric("状态", project_detail['状态'])
            st.metric("时间表", project_detail['时间表'])

# 风险预警页面
def render_risk_alerts(report):
    """渲染风险预警页面"""
    st.markdown('<div class="main-header">⚠️ 风险预警系统</div>', unsafe_allow_html=True)

    if not report:
        st.warning("暂无风险数据")
        return

    risks = report.get('risk_alerts', [])

    # 风险统计
    col1, col2, col3, col4 = st.columns(4)

    high_risks = [r for r in risks if r['severity'] == '高']
    medium_high_risks = [r for r in risks if r['severity'] == '中高']
    medium_risks = [r for r in risks if r['severity'] == '中']
    low_risks = [r for r in risks if r['severity'] == '低']

    with col1:
        st.metric("高风险", f"{len(high_risks)}个", delta_color="inverse")

    with col2:
        st.metric("中高风险", f"{len(medium_high_risks)}个")

    with col3:
        st.metric("中风险", f"{len(medium_risks)}个")

    with col4:
        st.metric("低风险", f"{len(low_risks)}个")

    st.markdown("---")

    # 风险列表
    st.markdown("### 风险详情")

    for risk in risks:
        severity = risk['severity']

        if severity == '高':
            st.markdown(f"""
            <div class="risk-high">
            <strong>🚨 {risk['type']} - {risk['severity']}级风险</strong><br>
            <strong>受影响地区:</strong> {', '.join(risk.get('countries', risk.get('regions', [])))}<br>
            <strong>风险描述:</strong> {risk['description']}<br>
            <strong>参考案例:</strong> {risk.get('reference_case', 'N/A')}
            </div>
            """, unsafe_allow_html=True)
        elif severity == '中高':
            st.markdown(f"""
            <div class="risk-medium">
            <strong>⚠️ {risk['type']} - {risk['severity']}级风险</strong><br>
            <strong>受影响地区:</strong> {', '.join(risk.get('countries', risk.get('regions', [])))}<br>
            <strong>风险描述:</strong> {risk['description']}<br>
            <strong>参考案例:</strong> {risk.get('reference_case', 'N/A')}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="risk-low">
            <strong>ℹ️ {risk['type']} - {risk['severity']}级风险</strong><br>
            <strong>受影响地区:</strong> {', '.join(risk.get('countries', risk.get('regions', [])))}<br>
            <strong>风险描述:</strong> {risk['description']}<br>
            <strong>参考案例:</strong> {risk.get('reference_case', 'N/A')}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 历史风险案例
    st.markdown("### 📚 历史风险案例库")

    # 菲律宾北吕宋铁路
    with st.expander("📖 菲律宾北吕宋铁路（2003-2017）"):
        st.markdown("""
        **项目背景:**
        - 项目周期：2003-2017年（14年拉锯战）
        - 最终结果：和解仅获6270万美元

        **根本原因:**
        1. 打破"政府间协议"万能迷信
        2. 防范"人走茶凉"的政权更迭
        3. 低估土地私有制下的工程阻力

        **关键事件:**
        - 2010年阿基诺三世上台，下令暂停所有前任政府留下的中资大额项目
        - 2012年菲律宾最高法院认定国机集团是商业公司而非主权实体，合同无效

        **经验教训:**
        - 严格审查东道国《政府采购法》
        - 与反对派、国会及地方门阀保持沟通
        - 项目应被塑造成"国家民生项目"而非"总统项目"
        """)

    # 沙特麦加轻轨
    with st.expander("📖 沙特麦加轻轨（低价中标案例）"):
        st.markdown("""
        **项目背景:**
        - EPC+O&M总承包模式
        - 当地竞标方报价：约200亿元
        - 中铁建报价：120亿元（让步过大）

        **成本超支:**
        - 合同收入：120.70亿元
        - 合同成本：160.69亿元
        - 亏损：39.99亿元（含财务成本41.53亿元）

        **根本原因:**
        1. 报价时间仓促，对当地市场情况不熟悉
        2. 工程量估计出现失误
        3. 设计和施工标准规范不熟悉（美国标准+欧洲标准）
        4. 风险估计不足
        5. 低价中标

        **工程量增加:**
        - 土石方开挖：从200万立方米变更为520多万立方米，增加320万立方米

        **单位成本差异:**
        - 国内1立方米约20元
        - 沙特可能100-200元
        - 增加成本约4-5亿元

        **经验教训:**
        - 强化市场调研，拒绝恶性竞价
        - 充分了解当地标准和法规
        - 避免EPC模式风险过大
        """)

# 机会匹配页面
def render_opportunity_matching(agent, report):
    """渲染机会匹配页面"""
    st.markdown('<div class="main-header">💡 智能机会匹配</div>', unsafe_allow_html=True)

    if not report:
        st.warning("暂无机会数据")
        return

    opportunities = report.get('top_opportunities', [])

    # 机会筛选
    col1, col2 = st.columns(2)

    with col1:
        selected_country = st.selectbox(
            "选择国家",
            sorted(set([opp['country'] for opp in opportunities]))
        )

    with col2:
        selected_risk = st.selectbox(
            "风险等级",
            ['全部', '高', '中高', '中', '低']
        )

    # 筛选
    filtered_opps = []
    for opp in opportunities:
        if opp['country'] == selected_country:
            if selected_risk == '全部' or opp['risk_level'] == selected_risk:
                filtered_opps.append(opp)

    # 显示机会
    if filtered_opps:
        for opp in filtered_opps:
            st.markdown(f"""
            <div class="opportunity-card">
            <strong>🎯 {opp['country']} - {opp['project']}</strong><br>
            <strong>风险等级:</strong> {opp['risk_level']}<br>
            <strong>中国机会:</strong><br>
            """ + "<br>".join([f"- {oppportunity}" for oppportunity in opp['chinese_opportunities']]) + """
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("没有找到匹配的机会")

    st.markdown("---")

    # 机会统计
    st.markdown("### 机会统计")

    # 按国家统计
    country_opp_count = {}
    for opp in opportunities:
        country = opp['country']
        if country not in country_opp_count:
            country_opp_count[country] = 0
        country_opp_count[country] += 1

    df_opp_country = pd.DataFrame(list(country_opp_count.items()), columns=['国家', '机会数量'])

    fig_opp_country = px.bar(
        df_opp_country,
        x='国家',
        y='机会数量',
        title='各国机会数量分布',
        color='机会数量',
        color_continuous_scale='Greens'
    )
    fig_opp_country.update_layout(xaxis_title='', yaxis_title='机会数量')
    st.plotly_chart(fig_opp_country, use_container_width=True)

# 数据报表页面
def render_data_reports(agent, report):
    """渲染数据报表页面"""
    st.markdown('<div class="main-header">📈 数据报表</div>', unsafe_allow_html=True)

    # 报告下载
    st.markdown("### 导出数据")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="📥 下载完整情报报告 (JSON)",
            data=json.dumps(report, ensure_ascii=False, indent=2),
            file_name=f"asean_rail_intelligence_report_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

    with col2:
        # 导出Agent数据
        agent_data = {
            'countries': agent.countries_db,
            'companies': agent.companies_db,
            'projects': agent.projects_db,
            'risks': agent.risks_db,
            'sources': agent.sources_db
        }

        st.download_button(
            label="📥 下载Agent数据库 (JSON)",
            data=json.dumps(agent_data, ensure_ascii=False, indent=2),
            file_name=f"asean_rail_agent_data_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

    with col3:
        # 导出CSV
        project_data = []
        for country in ['vietnam', 'thailand', 'malaysia', 'indonesia', 'singapore']:
            if country in agent.projects_db:
                for project_key, project in agent.projects_db[country].items():
                    project_data.append({
                        '国家': agent.countries_db[country]['name_zh'],
                        '项目名称': project.get('name', project_key),
                        '投资': project.get('investment', 'N/A'),
                        '长度': project.get('length', 'N/A'),
                        '状态': project.get('status', 'N/A'),
                        '时间表': project.get('timeline', 'N/A')
                    })

        df_projects = pd.DataFrame(project_data)

        st.download_button(
            label="📥 下载项目数据 (CSV)",
            data=df_projects.to_csv(index=False, encoding='utf-8-sig'),
            file_name=f"asean_rail_projects_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    st.markdown("---")

    # 数据统计
    st.markdown("### 数据统计")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("国家数量", len(agent.countries_db))

    with col2:
        company_count = sum(len(cat['companies']) for cat in agent.companies_db.values())
        st.metric("企业数量", company_count)

    with col3:
        project_count = sum(len(country_projects) for country_projects in agent.projects_db.values())
        st.metric("项目数量", project_count)

    with col4:
        risk_count = sum(len(risk_type) for risk_type in agent.risks_db.values())
        st.metric("风险案例", risk_count)

    st.markdown("---")

    # 数据预览
    st.markdown("### 数据预览")

    tab1, tab2, tab3, tab4 = st.tabs(["国家数据", "企业数据", "项目数据", "风险数据"])

    with tab1:
        countries_preview = []
        for country_code, country_data in agent.countries_db.items():
            countries_preview.append({
                '国家代码': country_code,
                '国家名称': country_data['name_zh'],
                '英文名称': country_data['name_en'],
                '人口': country_data['population'],
                '城镇化率': country_data['urbanization_rate']
            })

        st.dataframe(
            pd.DataFrame(countries_preview),
            use_container_width=True,
            hide_index=True
        )

    with tab2:
        companies_preview = []
        for category_key, category_data in agent.companies_db.items():
            for company in category_data['companies']:
                companies_preview.append({
                    '企业名称': company['name'],
                    '类别': category_data['category'],
                    '核心优势': ', '.join(company['core_advantages']),
                    '案例数量': len(company.get('asean_cases', []))
                })

        st.dataframe(
            pd.DataFrame(companies_preview),
            use_container_width=True,
            hide_index=True
        )

    with tab3:
        projects_preview = []
        for country_code, country_projects in agent.projects_db.items():
            for project_key, project_data in country_projects.items():
                projects_preview.append({
                    '国家': agent.countries_db[country_code]['name_zh'],
                    '项目名称': project_data.get('name', project_key),
                    '投资': project_data.get('investment', 'N/A'),
                    '长度': project_data.get('length', 'N/A'),
                    '状态': project_data.get('status', 'N/A')
                })

        st.dataframe(
            pd.DataFrame(projects_preview),
            use_container_width=True,
            hide_index=True
        )

    with tab4:
        risks_preview = []
        for risk_type, risk_data in agent.risks_db.items():
            for risk_key, risk_detail in risk_data.items():
                risks_preview.append({
                    '风险类型': risk_type,
                    '风险名称': risk_detail.get('project', risk_key),
                    '严重程度': '高',
                    '描述': risk_detail.get('outcome', 'N/A')[:50] + '...'
                })

        st.dataframe(
            pd.DataFrame(risks_preview),
            use_container_width=True,
            hide_index=True
        )

# 主函数
def main():
    """主函数"""

    # 加载数据
    agent = load_data()
    report = load_report()

    # 侧边栏
    page = render_sidebar(agent, report)

    # 根据选择的页面渲染相应内容
    if page == "📊 市场概览":
        render_market_overview(agent, report)
    elif page == "🏢 企业分析":
        render_company_analysis(agent)
    elif page == "🗺️ 项目地图":
        render_project_map(agent)
    elif page == "⚠️ 风险预警":
        render_risk_alerts(report)
    elif page == "💡 机会匹配":
        render_opportunity_matching(agent, report)
    elif page == "📈 数据报表":
        render_data_reports(agent, report)

if __name__ == "__main__":
    main()
