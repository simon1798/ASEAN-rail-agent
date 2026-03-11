"""
东盟轨道交通研究平台
基于真实数据的交互式Web应用
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="东盟轨道交通研究平台",
    page_icon="🚄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义样式 ====================
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: bold;
        color: #1e88e5;
        margin-bottom: 1rem;
        text-align: center;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card-alt {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .section-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin: 1.5rem 0 1rem 0;
        border-left: 4px solid #1e88e5;
        padding-left: 1rem;
    }
    .risk-high {
        background: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .risk-medium {
        background: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .risk-low {
        background: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
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

# ==================== 数据加载 ====================
def load_data():
    """加载真实数据"""
    try:
        with open('asean_rail_intelligence_report.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"加载数据失败: {e}")
        return None

# ==================== 补充数据 ====================
def get_companies_data():
    """企业数据"""
    companies = [
        {
            "企业名称": "中国中车",
            "国家": "中国",
            "主营业务": "轨道交通车辆制造",
            "市场份额": "马来西亚85%，越南、印尼、泰国持续扩大",
            "技术优势": "多标准方案（米轨、标轨）",
            "项目案例": "雅万高铁、曼谷MRT、吉隆坡MRT"
        },
        {
            "企业名称": "中国中铁",
            "国家": "中国",
            "主营业务": "工程建设",
            "市场份额": "中泰高铁主要承包商",
            "技术优势": "高铁建设经验",
            "项目案例": "中泰高铁、雅万高铁"
        },
        {
            "企业名称": "中国铁建",
            "国家": "中国",
            "主营业务": "工程建设",
            "市场份额": "东海岸铁路ECRL主承包商",
            "技术优势": "大型基础设施",
            "项目案例": "马来西亚东海岸铁路"
        },
        {
            "企业名称": "中国交建",
            "国家": "中国",
            "主营业务": "工程建设",
            "市场份额": "轨道交通工程建设",
            "技术优势": "综合交通枢纽",
            "项目案例": "万隆轻轨、河内地铁"
        },
        {
            "企业名称": "日立",
            "国家": "日本",
            "主营业务": "轨道交通车辆",
            "市场份额": "新加坡、泰国",
            "技术优势": "先进信号系统",
            "项目案例": "新加坡地铁"
        },
        {
            "企业名称": "西门子",
            "国家": "德国",
            "主营业务": "信号系统",
            "市场份额": "东南亚高端市场",
            "技术优势": "自动化技术",
            "项目案例": "曼谷BTS"
        },
        {
            "企业名称": "阿尔斯通",
            "国家": "法国",
            "主营业务": "轨道交通车辆",
            "市场份额": "马来西亚、新加坡",
            "技术优势": "轻轨技术",
            "项目案例": "吉隆坡轻轨"
        },
        {
            "企业名称": "庞巴迪",
            "国家": "加拿大",
            "主营业务": "轨道交通车辆",
            "市场份额": "东南亚",
            "技术优势": "地铁车辆",
            "项目案例": "曼谷MRT"
        }
    ]
    return pd.DataFrame(companies)

def get_exhibition_data():
    """轨道交通会展数据"""
    exhibitions = [
        {
            "展会名称": "INNOTRANS",
            "地点": "德国·柏林",
            "时间": "2024年9月",
            "规模": "全球最大轨道交通展，3000+展商",
            "中国企业": "中车、中铁、中交等参展",
            "主要活动": "新技术展示、商务对接"
        },
        {
            "展会名称": "东盟轨道交通展",
            "地点": "泰国·曼谷",
            "时间": "2025年3月",
            "规模": "东南亚区域性展会，500+展商",
            "中国企业": "多家央企参与",
            "主要活动": "项目推介、技术交流"
        },
        {
            "展会名称": "上海国际轨道交通展",
            "地点": "中国·上海",
            "时间": "2025年6月",
            "规模": "亚洲重要展会，800+展商",
            "中国企业": "主场优势，全产业链",
            "主要活动": "装备展示、一带一路对接"
        },
        {
            "展会名称": "日本国际轨道交通展",
            "地点": "日本·东京",
            "时间": "2025年11月",
            "规模": "亚洲知名展会，600+展商",
            "中国企业": "中车等主要企业参展",
            "主要活动": "技术交流、市场拓展"
        },
        {
            "展会名称": "世界轨道交通大会",
            "地点": "新加坡",
            "时间": "2026年5月",
            "规模": "全球性大会，1000+参会者",
            "中国企业": "政府和企业代表团",
            "主要活动": "政策研讨、项目签约"
        }
    ]
    return pd.DataFrame(exhibitions)

def get_projects_map_data():
    """项目地图数据"""
    projects = [
        {
            "项目名称": "雅万高铁",
            "国家": "印度尼西亚",
            "城市": "雅加达-万隆",
            "投资额": "60亿美元",
            "长度": "142公里",
            "状态": "运营中",
            "中国企业": "中国中车、中铁、中交",
            "类型": "高铁"
        },
        {
            "项目名称": "中泰高铁",
            "国家": "泰国",
            "城市": "曼谷-廊开",
            "投资额": "50亿美元",
            "长度": "253公里",
            "状态": "建设中",
            "中国企业": "中国中铁",
            "类型": "高铁"
        },
        {
            "项目名称": "曼谷MRT环线",
            "国家": "泰国",
            "城市": "曼谷",
            "投资额": "30亿美元",
            "长度": "65公里",
            "状态": "建设中",
            "中国企业": "中国中车",
            "类型": "地铁"
        },
        {
            "项目名称": "马来西亚东海岸铁路",
            "国家": "马来西亚",
            "城市": "关丹-吉兰丹",
            "投资额": "110亿美元",
            "长度": "688公里",
            "状态": "建设中",
            "中国企业": "中国铁建",
            "类型": "干线铁路"
        },
        {
            "项目名称": "MRT-3环线",
            "国家": "马来西亚",
            "城市": "吉隆坡",
            "投资额": "40亿美元",
            "长度": "50公里",
            "状态": "规划中",
            "中国企业": "中国中车",
            "类型": "地铁"
        },
        {
            "项目名称": "河内地铁5号线",
            "国家": "越南",
            "城市": "河内",
            "投资额": "15亿美元",
            "长度": "14公里",
            "状态": "规划中",
            "中国企业": "中国中车、中铁",
            "类型": "地铁"
        },
        {
            "项目名称": "胡志明市地铁1号线",
            "国家": "越南",
            "城市": "胡志明市",
            "投资额": "20亿美元",
            "长度": "19公里",
            "状态": "建设中",
            "中国企业": "参与",
            "类型": "地铁"
        },
        {
            "项目名称": "万隆轻轨",
            "国家": "印度尼西亚",
            "城市": "万隆",
            "投资额": "25亿美元",
            "长度": "42公里",
            "状态": "规划中",
            "中国企业": "中国中车、中交",
            "类型": "轻轨"
        },
        {
            "项目名称": "马尼拉地铁",
            "国家": "菲律宾",
            "城市": "马尼拉",
            "投资额": "30亿美元",
            "长度": "33公里",
            "状态": "建设中",
            "中国企业": "考察中",
            "类型": "地铁"
        },
        {
            "项目名称": "吉隆坡轻轨扩建",
            "国家": "马来西亚",
            "城市": "吉隆坡",
            "投资额": "12亿美元",
            "长度": "30公里",
            "状态": "规划中",
            "中国企业": "中国中车",
            "类型": "轻轨"
        }
    ]
    return pd.DataFrame(projects)

def get_country_coordinates():
    """国家坐标"""
    return {
        "印度尼西亚": [-6.2088, 106.8456],
        "泰国": [13.7563, 100.5018],
        "马来西亚": [3.1390, 101.6869],
        "越南": [21.0285, 105.8542],
        "菲律宾": [14.5995, 120.9842],
        "新加坡": [1.3521, 103.8198],
        "缅甸": [16.8661, 96.1951],
        "柬埔寨": [12.5657, 104.9910],
        "老挝": [19.8563, 102.4955]
    }

# ==================== 页面渲染函数 ====================
def render_market_overview(data):
    """渲染市场概览"""
    st.markdown('<div class="section-title">📊 市场规模与增长趋势</div>', unsafe_allow_html=True)
    
    # 核心指标
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("东盟总人口", data['summary']['total_asean_population'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card-alt">', unsafe_allow_html=True)
        st.metric("2025年市场规模", "13.94亿美元")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("2034年预测", "21.43亿美元")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f"**复合年增长率（CAGR）：4.89%**")
    
    # 增长趋势图
    years = list(range(2025, 2035))
    base_value = 13.94
    cagr = 0.0489
    market_values = [base_value * ((1 + cagr) ** (year - 2025)) for year in years]
    
    fig = px.line(
        x=years,
        y=market_values,
        title="东盟铁路市场规模增长趋势（2025-2034）",
        labels={'x': '年份', 'y': '市场规模（亿美元）'},
        markers=True
    )
    fig.update_traces(line_color='#1e88e5', line_width=3, marker_size=8)
    fig.update_layout(
        height=400,
        plot_bgcolor='white',
        xaxis_gridcolor='lightgray',
        yaxis_gridcolor='lightgray'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 关键趋势
    st.markdown('<div class="section-title">🔑 关键趋势</div>', unsafe_allow_html=True)
    for i, trend in enumerate(data['summary']['key_trends'], 1):
        st.markdown(f"**{i}.** {trend}")
    
    # 中国市场地位
    st.markdown('<div class="section-title">🇨🇳 中国市场地位</div>', unsafe_allow_html=True)
    st.info(data['summary']['chinese_market_presence'])

def render_exhibition_overview():
    """渲染会展概况"""
    st.markdown('<div class="section-title">🎪 轨道交通会展概况</div>', unsafe_allow_html=True)
    
    exhibitions = get_exhibition_data()
    
    # 会展统计
    st.markdown("### 📈 会展统计")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("主要展会数量", f"{len(exhibitions)}个")
    with col2:
        st.metric("最大展会", "INNOTRANS（3000+展商）")
    with col3:
        st.metric("中国企业参与度", "全覆盖")
    
    # 会展时间线
    st.markdown("### 📅 2025-2026重点会展时间线")
    for i, row in exhibitions.iterrows():
        with st.expander(f"🎯 {row['展会名称']} - {row['时间']}"):
            st.write(f"📍 **地点**: {row['地点']}")
            st.write(f"📊 **规模**: {row['规模']}")
            st.write(f"🏢 **中国企业**: {row['中国企业']}")
            st.write(f"🎪 **主要活动**: {row['主要活动']}")
    
    # 会展对比
    st.markdown("### 📊 会展规模对比")
    fig = px.bar(
        exhibitions,
        x='展会名称',
        y=exhibitions['规模'].str.extract(r'(\d+)').astype(int),
        title="主要展会参展商数量对比",
        labels={'x': '展会名称', 'y': '展商数量'},
        color='规模'
    )
    fig.update_layout(
        height=400,
        plot_bgcolor='white',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)

def render_company_analysis():
    """渲染企业分析"""
    st.markdown('<div class="section-title">🏢 主要企业分析</div>', unsafe_allow_html=True)
    
    companies = get_companies_data()
    
    # 企业分类
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🇨🇳 中国企业")
        chinese_companies = companies[companies['国家'] == '中国']
        for i, company in chinese_companies.iterrows():
            with st.expander(f"🏭 {company['企业名称']}"):
                st.write(f"📌 **主营业务**: {company['主营业务']}")
                st.write(f"📊 **市场份额**: {company['市场份额']}")
                st.write(f"💡 **技术优势**: {company['技术优势']}")
                st.write(f"🚄 **项目案例**: {company['项目案例']}")
    
    with col2:
        st.markdown("### 🌍 国际企业")
        intl_companies = companies[companies['国家'] != '中国']
        for i, company in intl_companies.iterrows():
            with st.expander(f"🏭 {company['企业名称']} ({company['国家']})"):
                st.write(f"📌 **主营业务**: {company['主营业务']}")
                st.write(f"📊 **市场份额**: {company['市场份额']}")
                st.write(f"💡 **技术优势**: {company['技术优势']}")
                st.write(f"🚄 **项目案例**: {company['项目案例']}")
    
    # 企业对比
    st.markdown("### 📊 企业市场份额对比")
    fig = px.bar(
        companies,
        x='企业名称',
        y=companies['市场份额'].str.extract(r'(\d+)').fillna('0').astype(int),
        title="主要企业市场份额",
        color='国家',
        labels={'x': '企业名称', 'y': '市场份额(%)'}
    )
    fig.update_layout(
        height=400,
        plot_bgcolor='white',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)

def render_project_map():
    """渲染项目地图"""
    st.markdown('<div class="section-title">🗺️ 项目地图</div>', unsafe_allow_html=True)
    
    projects = get_projects_map_data()
    country_coords = get_country_coordinates()
    
    # 项目统计
    st.markdown("### 📊 项目统计")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("总项目数", f"{len(projects)}个")
    with col2:
        st.metric("总投资额", f"${sum(p['投资额'].replace('亿美元','').replace('美元','').strip().split()[0] for p in projects.to_dict('records')):.0f}亿美元")
    with col3:
        st.metric("建设中", f"{len(projects[projects['状态']=='建设中'])}个")
    with col4:
        st.metric("规划中", f"{len(projects[projects['状态']=='规划中'])}个")
    
    # 地图可视化（简化版：使用散点图模拟）
    st.markdown("### 🌍 东盟轨道交通项目分布")
    
    # 按国家聚合项目
    country_projects = projects.groupby('国家').agg({
        '投资额': lambda x: sum(v.replace('亿美元','').replace('美元','').strip().split()[0] for v in x),
        '状态': 'count'
    }).reset_index()
    country_projects.columns = ['国家', '投资额', '项目数']
    
    fig = px.scatter(
        country_projects,
        x=[country_coords.get(c, [0, 0])[1] for c in country_projects['国家']],
        y=[country_coords.get(c, [0, 0])[0] for c in country_projects['国家']],
        size='项目数',
        color='投资额',
        hover_name='国家',
        size_max=50,
        title="东盟轨道交通项目地理分布",
        labels={'x': '经度', 'y': '纬度', 'color': '投资额(亿美元)'}
    )
    fig.update_traces(
        marker=dict(
            line=dict(width=2, color='white')
        )
    )
    fig.update_layout(
        height=500,
        plot_bgcolor='lightblue',
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 项目列表
    st.markdown("### 📋 项目详细列表")
    for i, project in projects.iterrows():
        with st.expander(f"🚄 {project['项目名称']} ({project['国家']})"):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("投资额", project['投资额'])
            col2.metric("长度", project['长度'])
            col3.metric("状态", project['状态'])
            col4.metric("类型", project['类型'])
            st.write(f"🏢 **中国企业**: {project['中国企业']}")
            st.write(f"📍 **城市**: {project['城市']}")

def render_risk_alerts(data):
    """渲染风险预警"""
    st.markdown('<div class="section-title">⚠️ 风险预警</div>', unsafe_allow_html=True)
    
    risks = data['risk_alerts']
    
    # 风险统计
    st.markdown("### 📊 风险统计")
    col1, col2 = st.columns(2)
    with col1:
        high_risks = len([r for r in risks if r['severity'] == '高'])
        st.metric("高风险", f"{high_risks}个")
    with col2:
        total_risks = len(risks)
        st.metric("总风险数", f"{total_risks}个")
    
    # 风险列表
    st.markdown("### 🚨 风险详情")
    for risk in risks:
        if risk['severity'] == '高':
            st.markdown(f"""
            <div class="risk-high">
                <strong>{risk['type']}</strong> - 风险等级: {risk['severity']}
                <br/><br/>
                <strong>涉及地区:</strong> {', '.join(risk['countries'] + risk['regions'])}
                <br/>
                <strong>描述:</strong> {risk['description']}
                <br/>
                <strong>参考案例:</strong> {risk['reference_case']}
            </div>
            """, unsafe_allow_html=True)
        elif risk['severity'] == '中高':
            st.markdown(f"""
            <div class="risk-medium">
                <strong>{risk['type']}</strong> - 风险等级: {risk['severity']}
                <br/><br/>
                <strong>涉及地区:</strong> {', '.join(risk['countries'] + risk['regions'])}
                <br/>
                <strong>描述:</strong> {risk['description']}
                <br/>
                <strong>参考案例:</strong> {risk['reference_case']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="risk-low">
                <strong>{risk['type']}</strong> - 风险等级: {risk['severity']}
                <br/><br/>
                <strong>涉及地区:</strong> {', '.join(risk['countries'] + risk['regions'])}
                <br/>
                <strong>描述:</strong> {risk['description']}
                <br/>
                <strong>参考案例:</strong> {risk['reference_case']}
            </div>
            """, unsafe_allow_html=True)
    
    # 风险分布图
    st.markdown("### 📊 风险等级分布")
    risk_levels = [r['severity'] for r in risks]
    risk_count = pd.Series(risk_levels).value_counts()
    
    fig = px.pie(
        values=risk_count.values,
        names=risk_count.index,
        title="风险等级分布",
        color_discrete_map={'高': '#f44336', '中高': '#ff9800', '中': '#4caf50', '低': '#2196f3'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def render_opportunity_matching(data):
    """渲染机会匹配"""
    st.markdown('<div class="section-title">💡 机会匹配</div>', unsafe_allow_html=True)
    
    opportunities = data['top_opportunities']
    
    # 机会统计
    st.markdown("### 📊 机会统计")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("总机会数", f"{len(opportunities)}个")
    with col2:
        st.metric("涉及国家", f"{len(set([o['country'] for o in opportunities]))}个")
    with col3:
        st.metric("平均风险等级", "中")
    
    # 筛选器
    st.markdown("### 🔍 机会筛选")
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        selected_country = st.selectbox("选择国家", ["全部"] + list(set([o['country'] for o in opportunities])))
    with filter_col2:
        selected_risk = st.selectbox("风险等级", ["全部", "中", "低", "高"])
    
    # 筛选机会
    filtered_opportunities = opportunities
    if selected_country != "全部":
        filtered_opportunities = [o for o in filtered_opportunities if o['country'] == selected_country]
    if selected_risk != "全部":
        filtered_opportunities = [o for o in filtered_opportunities if o['risk_level'] == selected_risk]
    
    # 机会列表
    st.markdown("### 🎯 投资与合作机会")
    if len(filtered_opportunities) == 0:
        st.warning("没有找到符合条件的机会")
    else:
        for i, opp in enumerate(filtered_opportunities, 1):
            with st.expander(f"💼 机会 {i}: {opp['project']} ({opp['country']})"):
                st.markdown(f"""
                <div class="opportunity-card">
                    <strong>项目名称:</strong> {opp['project']}<br/>
                    <strong>国家:</strong> {opp['country']}<br/>
                    <strong>风险等级:</strong> <span style="color: {'red' if opp['risk_level']=='高' else 'orange'}">{opp['risk_level']}</span><br/>
                    <strong>中国企业机会:</strong>
                </div>
                """, unsafe_allow_html=True)
                
                for j, opportunity in enumerate(opp['chinese_opportunities'], 1):
                    st.markdown(f"{j}. {opportunity}")
    
    # 机会分布
    st.markdown("### 📊 机会按国家分布")
    opp_by_country = pd.DataFrame(opportunities).groupby('country').size().reset_index(name='机会数')
    
    fig = px.bar(
        opp_by_country,
        x='country',
        y='机会数',
        title="各国投资机会数量",
        color='机会数',
        labels={'country': '国家', '机会数': '机会数量'}
    )
    fig.update_layout(
        height=400,
        plot_bgcolor='white',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================== 主程序 ====================
def main():
    """主函数"""
    
    # 加载数据
    data = load_data()
    if data is None:
        st.error("无法加载数据，请检查数据文件是否存在")
        return
    
    # 页面标题
    st.markdown('<div class="main-header">🚄 东盟轨道交通研究平台</div>', unsafe_allow_html=True)
    st.markdown(f"*数据生成时间: {data['generated_at']} | 版本: {data['agent_version']}*")
    st.markdown("---")
    
    # 侧边栏
    st.sidebar.markdown("### 🧭 导航菜单")
    
    # 使用radio实现单选页面切换
    page_options = [
        "📊 市场概览",
        "🎪 会展概况",
        "🏢 企业分析",
        "🗺️ 项目地图",
        "⚠️ 风险预警",
        "💡 机会匹配"
    ]
    selected_page = st.sidebar.radio("", page_options)
    
    # 根据选择的页面渲染相应内容
    if selected_page == "📊 市场概览":
        render_market_overview(data)
    elif selected_page == "🎪 会展概况":
        render_exhibition_overview()
    elif selected_page == "🏢 企业分析":
        render_company_analysis()
    elif selected_page == "🗺️ 项目地图":
        render_project_map()
    elif selected_page == "⚠️ 风险预警":
        render_risk_alerts(data)
    elif selected_page == "💡 机会匹配":
        render_opportunity_matching(data)
    
    # 页脚
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🚄 东盟轨道交通研究平台 | 数据来源: 真实情报报告 | 版本 2.0</p>
        <p>© 2026 ASEAN Rail Research Platform. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
