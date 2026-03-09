"""
东盟轨道交通研究Agent核心系统
功能：数据采集、需求分析、竞争情报、风险预警、政策追踪、机会匹配
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import re

class ASEANRailResearchAgent:
    """东盟轨道交通研究Agent主类"""

    def __init__(self):
        self.version = "1.0.0"
        self.init_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 核心数据库
        self.countries_db = self._load_countries_db()
        self.companies_db = self._load_companies_db()
        self.projects_db = self._load_projects_db()
        self.risks_db = self._load_risks_db()
        self.sources_db = self._load_sources_db()

    def _load_countries_db(self) -> Dict:
        """加载东盟10国轨道交通基础数据"""
        return {
            "vietnam": {
                "name_zh": "越南",
                "name_en": "Vietnam",
                "population": "10000万",
                "urbanization_rate": "38%",
                "rail_status": {
                    "operational_lrt": "超过180公里运营",
                    "under_construction": "约150公里",
                    "planned": "200+公里"
                },
                "key_projects": [
                    {
                        "name": "胡志明市地铁网络",
                        "total_investment": "580亿美元（两阶段）",
                        "total_length": "510公里（12条线路）",
                        "timeline": "2045年全线贯通",
                        "stage1": "2035年前完成1-7号线，355公里，402.1亿美元",
                        "stage2": "2036-2045年完成8-10号线，155公里，179.5亿美元"
                    },
                    {
                        "name": "河内地铁5号线",
                        "investment": "28亿美元",
                        "length": "39.5公里",
                        "status": "2025年12月开工，预计2030年竣工"
                    }
                ],
                "market_access": {
                    "localization_requirement": "逐步提升",
                    "tech_standards": "中国标准、欧洲标准、本地标准适配",
                    "financing_modes": ["ODA", "PPP", "国际贷款", "主权债券"]
                }
            },
            "thailand": {
                "name_zh": "泰国",
                "name_en": "Thailand",
                "population": "7000万",
                "urbanization_rate": "52%",
                "rail_status": {
                    "operational_lrt": "曼谷MRT网络约140公里",
                    "bts_system": "BTS空中列车系统"
                },
                "key_projects": [
                    {
                        "name": "中泰高铁",
                        "investment": "40-90亿美元区间",
                        "status": "一期（曼谷-呵叻）完成35%，计划4年内完工",
                        "phase2": "呵叻-廊开府，预计2028年完工"
                    },
                    {
                        "name": "曼谷MRT环线",
                        "investment": "约250亿泰铢",
                        "length": "51.6公里",
                        "stations": 32,
                        "opening_target": "2030年代"
                    }
                ],
                "market_access": {
                    "joint_venture_requirement": "外资必须与本地企业组成联合体，本地控股60%",
                    "financing_modes": ["PPP", "政府预算", "双边贷款"]
                }
            },
            "malaysia": {
                "name_zh": "马来西亚",
                "name_en": "Malaysia",
                "population": "3300万",
                "urbanization_rate": "77%",
                "rail_status": {
                    "operational_lrt": "吉隆坡Klang Valley LRT超过90公里",
                    "daily_ridership": "超过60万人次"
                },
                "key_projects": [
                    {
                        "name": "MRT-3环线",
                        "investment": "450亿马币（约310亿人民币）",
                        "length": "51.6公里",
                        "stations": 32,
                        "structure": "C型环线，40公里高架+11公里地下",
                        "status": "2025年7月获批，2026年底前完成征地",
                        "opening_target": "2030年代"
                    },
                    {
                        "name": "马来西亚东海岸铁路",
                        "investment": "约600亿人民币",
                        "length": "600+公里",
                        "purpose": "连通马来西亚东西海岸",
                        "chinese_participation": "中国中铁承建",
                        "status": "建设完成超过70%"
                    }
                ],
                "market_access": {
                    "localization_rate": "中车马来西亚项目90%员工本地化",
                    "joint_venture_requirement": "外资必须与本地企业组成联合体，本地控股60%",
                    "tech_standards": "中国标准、欧洲标准"
                }
            },
            "indonesia": {
                "name_zh": "印度尼西亚",
                "name_en": "Indonesia",
                "population": "2.78亿",
                "urbanization_rate": "57%",
                "rail_status": {
                    "railway_length": "6600公里",
                    "core_networks": "爪哇岛和苏门答腊岛"
                },
                "key_projects": [
                    {
                        "name": "雅万高铁",
                        "length": "142公里",
                        "speed": "350公里/小时",
                        "investment": "约60亿美元",
                        "status": "2023年9月通车运营",
                        "passenger_volume": "累计超过540万人次（截至2024年9月）"
                    },
                    {
                        "name": "万隆轻轨",
                        "investment": "30万亿印尼盾（约19亿美元）",
                        "length": "25.3公里",
                        "lines": 2,
                        "financing": "PPP模式",
                        "status": "法国表示有兴趣提供融资支持"
                    }
                ],
                "market_access": {
                    "financing_modes": ["PPP", "国家预算", "多边机构贷款"],
                    "localization_requirement": "逐步提升"
                }
            },
            "singapore": {
                "name_zh": "新加坡",
                "name_en": "Singapore",
                "population": "570万",
                "urbanization_rate": "100%",
                "rail_status": {
                    "operational_length": "超过200公里",
                    "target_2030": "360公里",
                    "target_2040": "400公里"
                },
                "key_projects": [
                    {
                        "name": "跨岛线（CRL）",
                        "status": "第八条也是最长的铁路线",
                        "opening": "2030年开始分阶段通车"
                    },
                    {
                        "name": "裕廊区域线西延段",
                        "investment": "10亿新元",
                        "status": "已获批，分两阶段实施",
                        "phase1": "2030年代末",
                        "phase2": "2040年代初"
                    }
                ],
                "market_access": {
                    "procurement_platform": "Government Electronic Business (GeBIZ)",
                    "procurement_principles": ["透明度", "公平竞争", "物有所值"],
                    "chinese_companies": [
                        "中国电建",
                        "中铁一局",
                        "中铁十一局",
                        "中铁隧道局",
                        "中交新加坡公司",
                        "中国港湾",
                        "中铁装备",
                        "隧道股份"
                    ]
                }
            },
            "philippines": {
                "name_zh": "菲律宾",
                "name_en": "Philippines",
                "population": "1.14亿",
                "urbanization_rate": "47%",
                "rail_status": {
                    "metro_manila": "LRT-1和LRT-2覆盖33公里"
                },
                "key_projects": [
                    {
                        "name": "马尼拉LRT-1 Cavite Extension",
                        "length": "11.7公里",
                        "status": "接近完成"
                    },
                    {
                        "name": "北吕宋铁路项目教训",
                        "lesson": "2003-2017年14年拉锯，最终和解仅获6270万美元",
                        "key_lessons": [
                            "打破'政府间协议'万能迷信",
                            "防范'人走茶凉'的政权更迭",
                            "低估土地私有制下的工程阻力"
                        ]
                    }
                ],
                "market_access": {
                    "legal_challenge": "菲律宾最高法院可判定合同无效",
                    "procurement_law": "政府采购法强制公开招标",
                    "political_risk": "政权更迭严重影响项目"
                }
            },
            "myanmar": {
                "name_zh": "缅甸",
                "name_en": "Myanmar",
                "population": "5400万",
                "urbanization_rate": "31%",
                "rail_status": {
                    "development_stage": "初期阶段"
                },
                "market_access": {
                    "political_risk": "高",
                    "infrastructure_gap": "严重不足"
                }
            },
            "cambodia": {
                "name_zh": "柬埔寨",
                "name_en": "Cambodia",
                "population": "1700万",
                "urbanization_rate": "25%",
                "rail_status": {
                    "development_stage": "初期阶段"
                },
                "key_projects": [
                    {
                        "name": "暹粒-新吴哥机场LRT",
                        "status": "政府提案阶段"
                    }
                ]
            },
            "laos": {
                "name_zh": "老挝",
                "name_en": "Laos",
                "population": "740万",
                "urbanization_rate": "36%",
                "rail_status": {
                    "china_laos_railway": "全长1035公里，2021年通车",
                    "freight_volume": "2024年达478.6万吨",
                    "benefit": "从'陆锁国'变为'陆联国'"
                },
                "key_projects": [
                    {
                        "name": "中老铁路",
                        "passenger_volume": "累计6600万人次（截至2026年2月）",
                        "cross_border_trains": "每日4列",
                        "coverage": "覆盖19个国家和地区"
                    }
                ]
            },
            "brunei": {
                "name_zh": "文莱",
                "name_en": "Brunei",
                "population": "44万",
                "urbanization_rate": "78%",
                "rail_status": {
                    "development_stage": "无轨道交通系统"
                }
            }
        }

    def _load_companies_db(self) -> Dict:
        """加载中国企业出海能力库"""
        return {
            "vehicle_manufacturing": {
                "category": "车辆制造",
                "companies": [
                    {
                        "name": "中国中车",
                        "subsidiaries": ["中车四方", "中车长客", "中车株机"],
                        "core_advantages": [
                            "成本优势",
                            "全谱系产品",
                            "本土化生产能力"
                        ],
                        "asean_cases": [
                            {
                                "project": "马来西亚东盟制造中心",
                                "localization_rate": "90%",
                                "capacity": "年产100辆、架修150辆"
                            },
                            {
                                "project": "雅万高铁二期",
                                "investment": "42亿元，35列动车组",
                                "localization_rate": "60%"
                            }
                        ],
                        "market_share_malaysia": "85%",
                        "international_business_ratio": "16.8%（2025年Q1）"
                    }
                ]
            },
            "engineering_construction": {
                "category": "工程总包",
                "companies": [
                    {
                        "name": "中国铁建",
                        "subsidiaries": ["中国土木", "中铁十一局", "中铁十二局"],
                        "core_advantages": [
                            "隧道工程技术",
                            "施工效率",
                            "融资能力"
                        ],
                        "asean_cases": [
                            {
                                "project": "马来西亚东海岸铁路",
                                "role": "承建",
                                "status": "建设完成超过70%"
                            },
                            {
                                "project": "沙特麦加轻轨",
                                "lesson": "低价中标导致巨亏41.53亿元",
                                "key_issues": [
                                    "报价120亿 vs 本地200亿",
                                    "工程量严重低估",
                                    "土石方开挖从200万增至520万立方米"
                                ]
                            }
                        ],
                        "risk_case": {
                            "project": "菲律宾北吕宋铁路",
                            "outcome": "历时14年，最终和解6270万美元",
                            "lessons": [
                                "严格审查当地《政府采购法》",
                                "与反对派、国会保持沟通",
                                "将项目塑造成'国家民生项目'"
                            ]
                        }
                    },
                    {
                        "name": "中国中铁",
                        "subsidiaries": ["中铁一局", "中铁二局", "中铁三局", "中铁隧道局"],
                        "core_advantages": [
                            "综合实力强",
                            "桥梁技术",
                            "高原铁路经验"
                        ],
                        "asean_cases": [
                            {
                                "project": "中老铁路",
                                "role": "主要承建",
                                "outcome": "老挝人均铁路保有量从最后一名跃升至第28名"
                            },
                            {
                                "project": "雅万高铁",
                                "role": "主要承建"
                            }
                        ]
                    },
                    {
                        "name": "中国交建",
                        "subsidiaries": ["中交一公局", "中交二公局", "中国港湾"],
                        "core_advantages": [
                            "港口建设",
                            "海外经验丰富",
                            "投融资能力"
                        ],
                        "asean_cases": [
                            {
                                "project": "马来西亚吉隆坡地铁二号线",
                                "length": "57.7公里",
                                "stations": 36,
                                "completion": "2023年全线通车"
                            }
                        ]
                    }
                ]
            },
            "system_integration": {
                "category": "系统集成",
                "companies": [
                    {
                        "name": "中国通号",
                        "core_advantages": [
                            "CBTC信号系统",
                            "全自动运行",
                            "互联互通"
                        ],
                        "asean_cases": [
                            {
                                "project": "越南河内轻轨",
                                "scope": "信号系统供应"
                            }
                        ]
                    },
                    {
                        "name": "交控科技",
                        "core_advantages": [
                            "列车控制系统",
                            "智能运维平台"
                        ]
                    }
                ]
            },
            "operation_service": {
                "category": "运营服务",
                "companies": [
                    {
                        "name": "深圳地铁",
                        "core_advantages": [
                            "运营管理经验",
                            "智慧运维解决方案"
                        ],
                        "asean_cases": [
                            {
                                "project": "越南河内地铁5号线",
                                "role": "联合体成员，EPC总承包",
                                "contract_value": "23亿美元"
                            }
                        ]
                    },
                    {
                        "name": "南宁轨道交通投资集团",
                        "core_advantages": [
                            "MaaS模式",
                            "智慧出行解决方案"
                        ],
                        "asean_cases": [
                            {
                                "project": "泰国孔敬市MaaS数字交通生态系统",
                                "model": "技术输出+联合运营",
                                "features": [
                                    "一码通行、一键预约",
                                    "整合城市巴士、双条车、短途客运",
                                    "融入旅游景点导览、餐饮推荐、酒店预订"
                                ]
                            }
                        ]
                    },
                    {
                        "name": "港铁公司",
                        "core_advantages": [
                            "国际运营标准",
                            "TOD开发经验"
                        ]
                    }
                ]
            }
        }

    def _load_projects_db(self) -> Dict:
        """加载重点项目数据库"""
        return {
            "vietnam": {
                "hcmc_metro_2": {
                    "name": "胡志明市地铁2号线",
                    "chinese_participation": "广州地铁设计院提供设计服务",
                    "investment": "21亿美元",
                    "length": "11.3公里",
                    "stations": 11,
                    "timeline": "2026年1月开工，预计2028-2030年陆续运营",
                    "opportunities": [
                        "信号系统供应（中国通号、交控科技）",
                        "车辆采购（中车，需提供欧洲标准方案）",
                        "运维服务（深圳地铁、港铁）"
                    ],
                    "risks": [
                        "征地拆迁延迟风险",
                        "本地化率要求"
                    ]
                },
                "hcmc_metro_network": {
                    "name": "胡志明市地铁网络",
                    "total_investment": "580亿美元",
                    "total_length": "510公里（12条线路）",
                    "financing_structure": {
                        "central_fiscal": "209.5万亿越南盾（约80亿美元）",
                        "local_budget": "地方预算弹性调配",
                        "international_capital": "目标外资占比35%",
                        "modes": ["ODA", "PPP", "国际贷款", "TOD开发"]
                    },
                    "innovation": [
                        "采用'地铁+轻轨+单轨'三制式融合",
                        "TOD开发带动车站1公里内地价上涨40%"
                    ],
                    "regional_benefits": {
                        "coverage": "合并三地后覆盖2500万人口",
                        "economic_circle": "构建'1小时经济圈'",
                        "connections": ["平阳制造业", "巴地-头顿深水港", "胡志明金融中心"]
                    },
                    "targets": {
                        "daily_passenger_volume": "480万人次（2045年）",
                        "coverage_rate": "从40%提升至60%",
                        "gdp_growth": "拉动GDP年增长1.2-1.5%"
                    }
                },
                "hanoi_metro_5": {
                    "name": "河内地铁5号线",
                    "epc_consortium": [
                        "越南长山建设集团",
                        "越南铁路总公司",
                        "中国太平洋建设集团",
                        "深圳市市政设计研究院",
                        "深圳地铁国际投资咨询有限公司",
                        "深圳市建材交易集团有限公司"
                    ],
                    "contract_value": "23亿美元",
                    "length": "39.5公里",
                    "stations": 20,
                    "contract_duration": "60个月",
                    "completion": "2030年12月前"
                }
            },
            "thailand": {
                "china_thai_hsr": {
                    "name": "中泰高铁",
                    "phase1": {
                        "route": "曼谷-呵叻",
                        "progress": "已完成35%",
                        "completion_target": "4年内完工"
                    },
                    "phase2": {
                        "route": "呵叻-廊开府",
                        "completion_target": "2028年",
                        "connection": "可跨境与中老铁路相连"
                    },
                    "investment": "40-90亿美元区间",
                    "strategic_importance": "提升泰国在东南亚地区的交通枢纽地位"
                },
                "bangkok_mrt_expansion": {
                    "name": "曼谷地铁扩建",
                    "projects": [
                        {
                            "name": "粉色线",
                            "length": "34.5公里",
                            "opening": "2023年部分运营，2025年全面完成",
                            "daily_passenger_volume": "超过10万人次"
                        },
                        {
                            "name": "黄色线",
                            "status": "开发中"
                        }
                    ]
                }
            },
            "malaysia": {
                "mrt3_ring_line": {
                    "name": "MRT-3环线",
                    "investment": "450亿马币（约310亿人民币）",
                    "length": "51.6公里",
                    "stations": 32,
                    "structure": "C型环线，40公里高架+11公里地下",
                    "operational_characteristics": {
                        "single_circle_time": "约73分钟",
                        "design_capacity": "每小时2.5万人"
                    },
                    "status": "2025年7月获批，2026年底前完成征地",
                    "opening_target": "2030年代",
                    "tender_requirements": [
                        "超10亿马币级别铁路履约经验",
                        "参与官方强制说明会(Briefing)",
                        "外资公司必须与马来企业组成联合体，且马方必须控股至少60%"
                    ],
                    "chinese_opportunities": [
                        "聚焦大型施工包或系统设备包",
                        "尤其是CMC303这类含地下盾构综合枢纽的大包",
                        "提升项目增值能力：绿色施工、数字化管理平台、本地员工培训"
                    ]
                },
                "penang_lrt": {
                    "name": "槟城捷运Mutiara轻轨",
                    "owner": "马来西亚国家捷运公司(MRTCorp)",
                    "status": "第二标段招标评估阶段",
                    "tender_info": {
                        "briefing_date": "11月5日",
                        "document_sale": "11月6日至12月5日"
                    }
                }
            },
            "indonesia": {
                "jakaw_bandung_hsr": {
                    "name": "雅万高铁",
                    "length": "142公里",
                    "speed": "350公里/小时",
                    "opening": "2023年9月通车",
                    "naming": "Whoosh（印尼语'省时'、'高效'、'先进'首字母缩写）",
                    "passenger_volume": "累计超过540万人次（截至2024年9月）",
                    "chinese_standards": "首次全面采用中国标准"
                },
                "bandung_lrt": {
                    "name": "万隆轻轨",
                    "investment": "30万亿印尼盾（约19亿美元）",
                    "length": "25.3公里",
                    "lines": 2,
                    "financing": "PPP模式",
                    "french_interest": "法国表示有兴趣提供融资支持",
                    "world_bank_study": "单条10公里线路建设成本高达10万亿印尼盾"
                }
            },
            "singapore": {
                "cross_island_line": {
                    "name": "跨岛线(CRL)",
                    "status": "第八条也是最长的铁路线",
                    "opening": "2030年开始分阶段通车",
                    "chinese_participation": [
                        "中国电建",
                        "中铁一局",
                        "中铁十一局",
                        "中铁隧道局",
                        "中交新加坡公司",
                        "中国港湾",
                        "中铁装备",
                        "隧道股份"
                    ]
                },
                "jurong_line_extension": {
                    "name": "裕廊区域线西延段",
                    "investment": "10亿新元",
                    "status": "已获批，分两阶段实施",
                    "phase1": "2030年代末",
                    "phase2": "2040年代初",
                    "chinese_participation": "中车四方为跨岛线提供地铁列车"
                }
            }
        }

    def _load_risks_db(self) -> Dict:
        """加载风险案例库"""
        return {
            "political_risks": {
                "philippines_northrail": {
                    "project": "菲律宾北吕宋铁路",
                    "duration": "2003-2017年（14年）",
                    "outcome": "最终和解6270万美元",
                    "root_causes": [
                        "打破'政府间协议'万能迷信",
                        "防范'人走茶凉'的政权更迭",
                        "低估土地私有制下的工程阻力"
                    ],
                    "key_incident": "2010年阿基诺三世上台，下令暂停所有前任政府留下的中资大额项目",
                    "legal_outcome": "2012年菲律宾最高法院认定国机集团是商业公司而非主权实体，合同无效",
                    "lessons_learned": [
                        "严格审查东道国《政府采购法》",
                        "与反对派、国会及地方门阀保持沟通",
                        "项目应被塑造成'国家民生项目'而非'总统项目'"
                    ]
                },
                "iran_hsr": {
                    "project": "伊朗德黑兰-库姆-伊斯法罕高速铁路",
                    "investment": "84亿欧元",
                    "outcome": "因伊朗核活动遭受欧美和联合国制裁，被无限期终止"
                }
            },
            "bidding_risks": {
                "saudi_makkah_lrt": {
                    "project": "沙特麦加轻轨",
                    "contractor": "中国铁建",
                    "contract": "EPC+O&M总承包模式",
                    "bidding_issue": {
                        "local_bid": "约200亿元",
                        "crcc_bid": "120亿元（让步过大）"
                    },
                    "cost_overrun": {
                        "contract_revenue": "120.70亿元",
                        "contract_cost": "160.69亿元",
                        "loss": "39.99亿元",
                        "with_financial_cost": "41.53亿元"
                    },
                    "root_causes": [
                        "报价时间仓促，对当地市场情况不熟悉",
                        "工程量估计出现失误",
                        "设计和施工标准规范不熟悉（美国标准+欧洲标准）",
                        "风险估计不足",
                        "低价中标"
                    ],
                    "quantity_increase": {
                        "earthwork_excavation": "从200万立方米变更为520多万立方米，增加320万立方米"
                    },
                    "unit_cost_issue": "国内1立方米约20元，沙特可能100-200元，增加成本约4-5亿元",
                    "lessons_learned": [
                        "强化市场调研，拒绝恶性竞价",
                        "充分了解当地标准和法规",
                        "避免EPC模式风险过大"
                    ]
                },
                "usa_west_high_speed_rail": {
                    "project": "美国西部快线",
                    "outcome": "2016年6月9日，西部快线公司单方面终止与中国铁路国际的合作",
                    "chinese_response": "违反协议，错误且不负责任",
                    "lesson": "地缘政治风险对海外项目的直接影响"
                }
            },
            "legal_compliance_risks": {
                "south_africa_transnet": {
                    "project": "南非Transnet机车采购",
                    "contractor": "中车",
                    "issues": [
                        {
                            "type": "合同争议",
                            "detail": "2014年采购1064台机车，总价21亿欧元",
                            "investigation": "2017年南非媒体调查质疑招标中可能存在回扣等腐败问题",
                            "outcome": "2022年2月确认合同存在价格夸大和招标违规，被认定为'非法授予'"
                        },
                        {
                            "type": "合规问题",
                            "detail": "南非储备银行和税务局调查发现中车南非公司涉嫌违反外汇管理和税法规定",
                            "fund_frozen": "累计约46.5亿兰特（约合人民币21亿元）资金被冻结"
                        },
                        {
                            "type": "付款与合同执行纠纷",
                            "detail": "transnet停止履行剩余合同，不再接受余下机车交付",
                            "dispute": "中车扣留备件，transnet拒付剩余款项"
                        }
                    ],
                    "impact": "161台中车机车因缺少零件和维护而无法运行，几乎占中车机车队的全部",
                    "lessons_learned": [
                        "高度重视本地法律法规和合规要求",
                        "解决好税务合规和外汇管制问题",
                        "配合调查，解除资金冻结"
                    ]
                }
            },
            "market_access_risks": {
                "bulgaria_hsr": {
                    "project": "保加利亚高铁列车采购",
                    "requirements": "20辆电动列车+15年维护",
                    "budget": "6.1亿欧元",
                    "bids": {
                        "crcc": {
                            "bid": "3亿欧元",
                            "delivery": "33个月"
                        },
                        "talgo": {
                            "bid": "接近6亿欧元（预算上限）"
                        }
                    },
                    "eu_action": "2024年2月16日，欧盟委员会根据外国补贴条例对中车启动调查",
                    "outcome": "中车退出招标，保加利亚转向塔尔高",
                    "subsequent_issues": "塔尔高在2025年1月因电池故障导致全线停运，暴露技术稳定性短板",
                    "lessons_learned": "欧盟反补贴调查已成为中企出海的重要障碍"
                }
            }
        }

    def _load_sources_db(self) -> Dict:
        """加载数据源数据库"""
        return {
            "tender_platforms": {
                "singapore": {
                    "name": "新加坡陆路交通管理局(LTA)",
                    "platform": "Government Electronic Business (GeBIZ)",
                    "url": "https://www.lta.gov.sg/content/ltagov/en/industry_innovations/industry_matters/tender.html",
                    "procurement_principles": ["透明度", "公平竞争", "物有所值"],
                    "features": [
                        "2018年7月16日后的招标不再发布，仅在GeBIZ平台发布",
                        "严格遵守新加坡政府采购政策",
                        "反贿赂政策"
                    ]
                },
                "malaysia": {
                    "name": "马来西亚MRTCorp",
                    "url": "https://www.mymrt.com.my/",
                    "tender_features": [
                        "政府主导的权威平台",
                        "覆盖全国所有公共资源交易",
                        "信息分散，需要多翻几页"
                    ]
                },
                "international": {
                    "name": "千里马招标网",
                    "features": [
                        "公示信息10分钟内同步",
                        "一天能更新30万条信息",
                        "AI写标书、项目监控功能",
                        "订阅推送功能"
                    ],
                    "users": ["联通", "华为", "黑龙江省纪委监委"]
                }
            },
            "market_intelligence": {
                "imarc_group": {
                    "name": "IMARC Group",
                    "report": "South East Asia Railroad Market Size, Share, Trends and Forecast",
                    "market_size_2025": "USD 1,394.4 Million",
                    "market_forecast_2034": "USD 2,143.0 Million",
                    "cagr": "4.89%",
                    "forecast_period": "2026-2034"
                },
                "railzoom": {
                    "name": "Railzoom",
                    "description": "专注于全球轨道交通行业的智能数据与情报服务机构",
                    "capabilities": [
                        "海外实时资讯",
                        "战略规划研究",
                        "竞争对手追踪",
                        "国际招投标信息服务",
                        "关键决策人对接"
                    ],
                    "coverage": "实时监测150多个国家的铁路建设规划、政策动态和企业活动"
                }
            },
            "policy_sources": {
                "asean_secretariat": {
                    "name": "东盟秘书处",
                    "key_report": "《东盟铁路战略规划研究报告（2026）》",
                    "key_findings": [
                        "未来十年铁路将成为东盟交通领域投资规模最大的基础设施板块",
                        "已规划或在建的新建及升级铁路总里程超过8000公里",
                        "跨境铁路通道约3200公里",
                        "多边金融机构深度参与，采购流程国际化"
                    ],
                    "financing_structure": {
                        "government_fiscal": "45%",
                        "multilateral_institutions": "30%",
                        "ppp_and_bilateral": "25%"
                    }
                },
                "adb": {
                    "name": "亚洲开发银行(ADB)",
                    "role": "提供优惠贷款和技术支持",
                    "project_involvement": [
                        "胡志明市地铁融资",
                        "越南河内地铁5号线融资支持"
                    ]
                },
                "aiib": {
                    "name": "亚洲基础设施投资银行(AIIB)",
                    "role": "为东盟铁路项目提供融资"
                }
            }
        }

    def analyze_market_opportunities(self, country: str) -> Dict:
        """分析某国市场机会"""
        if country not in self.countries_db:
            return {"error": f"国家 {country} 不在数据库中"}

        country_data = self.countries_db[country]
        opportunities = []

        # 分析重点项目
        if "key_projects" in country_data:
            for project in country_data["key_projects"]:
                # 识别中国企业参与机会
                chinese_opps = self._identify_chinese_opportunities(project, country)
                if chinese_opps:
                    opportunities.append({
                        "project_name": project["name"],
                        "chinese_opportunities": chinese_opps,
                        "risk_level": self._assess_project_risk(project, country)
                    })

        return {
            "country": country_data["name_zh"],
            "opportunities": opportunities
        }

    def _identify_chinese_opportunities(self, project: Dict, country: str) -> List[str]:
        """识别中国企业的参与机会"""
        opportunities = []

        # 车辆采购机会
        if "length" in project or "stations" in project:
            opportunities.append("车辆采购（中车、提供多标准方案）")

        # 系统集成机会
        if "status" in project and "under_construction" in str(project.get("status", "")) or "construction" in str(project.get("status", "")):
            opportunities.append("信号系统供应（中国通号、交控科技）")

        # 工程建设机会
        if "investment" in project and ("亿美元" in project["investment"] or "billion" in str(project.get("investment", "")).lower()):
            opportunities.append("工程建设（中铁建、中铁工、中国交建）")

        # 运维服务机会
        if "timeline" in project and ("2030" in project["timeline"] or "2028" in project["timeline"]):
            opportunities.append("运维服务（深圳地铁、港铁、南宁轨道）")

        return opportunities

    def _assess_project_risk(self, project: Dict, country: str) -> str:
        """评估项目风险等级"""
        risk_level = "中"

        # 菲律宾高风险
        if country == "philippines":
            risk_level = "高"

        # 大型项目风险中等
        if "investment" in project:
            investment_str = project["investment"]
            if "500" in investment_str or "580" in investment_str:
                risk_level = "高"

        # 政权更迭风险
        if country in ["philippines", "myanmar", "cambodia"]:
            if risk_level != "高":
                risk_level = "中高"

        return risk_level

    def analyze_competitive_landscape(self, country: str) -> Dict:
        """分析竞争格局"""
        if country not in self.countries_db:
            return {"error": f"国家 {country} 不在数据库中"}

        country_data = self.countries_db[country]

        # 识别中国企业在该国的参与情况
        chinese_companies = []

        for category, companies in self.companies_db.items():
            for company in companies["companies"]:
                if "asean_cases" in company:
                    for case in company["asean_cases"]:
                        if country.lower() in str(case).lower():
                            chinese_companies.append({
                                "company_name": company["name"],
                                "category": companies["category"],
                                "project": case.get("project", ""),
                                "role": case.get("role", "")
                            })

        # 识别国际竞争对手
        international_competitors = []
        if country == "malaysia":
            international_competitors = [
                {"name": "阿尔斯通", "market_position": "技术品牌、欧洲标准"},
                {"name": "西门子", "market_position": "技术品牌、欧洲标准"}
            ]
            # 中车市场份额
            chinese_companies.append({
                "company_name": "中国中车",
                "category": "车辆制造",
                "project": "马来西亚市场",
                "role": "市场份额85%",
                "localization": "90%员工本地化"
            })
        elif country == "indonesia":
            international_competitors = [
                {"name": "阿尔斯通", "market_position": "万隆轻轨融资支持"},
                {"name": "三菱重工", "market_position": "技术实力"}
            ]
        elif country == "singapore":
            international_competitors = [
                {"name": "阿尔斯通", "market_position": "欧洲标准"},
                {"name": "西门子", "market_position": "欧洲标准"}
            ]

        return {
            "country": country_data["name_zh"],
            "chinese_companies": chinese_companies,
            "international_competitors": international_competitors,
            "competitive_advantage": self._assess_chinese_advantage(country)
        }

    def _assess_chinese_advantage(self, country: str) -> Dict:
        """评估中国企业的竞争优势"""
        advantages = []

        if country == "malaysia":
            advantages = [
                "成本优势：中车报价通常低于竞争对手30-50%",
                "本土化生产：东盟制造中心，90%员工本地化",
                "全产业链：产品+服务+投资+技术模式"
            ]
        elif country == "indonesia":
            advantages = [
                "雅万高铁示范效应：成功运营建立信任",
                "成本优势：适合发展中国家预算",
                "技术适应性：适应热带气候条件"
            ]
        elif country == "vietnam":
            advantages = [
                "地理优势：陆上相邻，运输成本低",
                "政治关系稳定：中越关系良好",
                "全产业链能力：从设计到运营"
            ]
        else:
            advantages = [
                "成本优势",
                "全产业链能力",
                "一带一路政策支持"
            ]

        return {
            "country": self.countries_db.get(country, {}).get("name_zh", country),
            "advantages": advantages
        }

    def assess_project_risks(self, project_name: str) -> Dict:
        """评估项目风险"""
        risks = {
            "political_risk": "低",
            "financial_risk": "中",
            "legal_risk": "中",
            "technical_risk": "中",
            "mitigation_strategies": []
        }

        # 基于项目名称和历史案例评估风险
        if "菲律宾" in project_name or "philippines" in project_name.lower():
            risks["political_risk"] = "高"
            risks["legal_risk"] = "高"
            risks["mitigation_strategies"] = [
                "与反对派、国会及地方门阀保持沟通",
                "项目应被塑造成'国家民生项目'",
                "严格遵守当地《政府采购法》"
            ]

        if "沙特" in project_name or "saudi" in project_name.lower():
            risks["financial_risk"] = "高"
            risks["mitigation_strategies"] = [
                "强化市场调研，拒绝恶性竞价",
                "充分了解当地标准和法规",
                "避免EPC模式风险过大"
            ]

        if "南非" in project_name or "south_africa" in project_name.lower():
            risks["legal_risk"] = "高"
            risks["financial_risk"] = "高"
            risks["mitigation_strategies"] = [
                "高度重视本地法律法规和合规要求",
                "解决好税务合规和外汇管制问题"
            ]

        return risks

    def match_opportunities(self, query: str) -> List[Dict]:
        """机会匹配"""
        matches = []

        # 解析查询关键词
        keywords = self._extract_keywords(query)

        # 在项目数据库中匹配
        for country, projects in self.projects_db.items():
            for project_key, project in projects.items():
                if self._match_keywords(project, keywords):
                    matches.append({
                        "country": self.countries_db[country]["name_zh"],
                        "project_name": project.get("name", project_key),
                        "opportunities": project.get("opportunities", []),
                        "risks": project.get("risks", []),
                        "timeline": project.get("timeline", "")
                    })

        return matches

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单的关键词提取
        keywords = []

        if "地铁" in text or "metro" in text.lower():
            keywords.append("metro")
        if "轻轨" in text or "lrt" in text.lower():
            keywords.append("lrt")
        if "信号" in text or "signaling" in text.lower():
            keywords.append("signaling")
        if "车辆" in text or "vehicle" in text.lower():
            keywords.append("vehicle")
        if "高铁" in text or "hsr" in text.lower():
            keywords.append("hsr")
        if "运维" in text or "operation" in text.lower():
            keywords.append("operation")

        return keywords

    def _match_keywords(self, project: Dict, keywords: List[str]) -> bool:
        """匹配关键词"""
        project_text = json.dumps(project, ensure_ascii=False).lower()

        for keyword in keywords:
            if keyword.lower() in project_text:
                return True

        return False

    def generate_intelligence_report(self) -> Dict:
        """生成综合情报报告"""
        report = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "agent_version": self.version,
            "summary": {
                "total_asean_population": "约6.8亿",
                "rail_investment_outlook": "东盟铁路市场规模2025年13.94亿美元，预计2034年达21.43亿美元，CAGR 4.89%",
                "chinese_market_presence": "中车在马来西亚市场份额85%，越南、印尼、泰国市场持续扩大",
                "key_trends": [
                    "跨境铁路成为重点：3200公里跨境通道",
                    "融资多元化：45%政府财政、30%多边机构、25%PPP",
                    "技术标准'有限统一'：跨境干线优先标准轨"
                ]
            },
            "top_opportunities": [],
            "risk_alerts": []
        }

        # 识别顶级机会
        for country in ["vietnam", "thailand", "malaysia", "indonesia"]:
            opps = self.analyze_market_opportunities(country)
            for opp in opps.get("opportunities", []):
                if opp.get("risk_level") in ["中", "中高"]:
                    report["top_opportunities"].append({
                        "country": opps["country"],
                        "project": opp["project_name"],
                        "chinese_opportunities": opp["chinese_opportunities"],
                        "risk_level": opp["risk_level"]
                    })

        # 风险预警
        report["risk_alerts"] = [
            {
                "type": "政治风险",
                "severity": "高",
                "countries": ["菲律宾"],
                "description": "政权更迭可能导致项目中断",
                "reference_case": "北吕宋铁路（2003-2017）"
            },
            {
                "type": "低价中标风险",
                "severity": "高",
                "regions": ["中东"],
                "description": "报价过低可能导致巨额亏损",
                "reference_case": "沙特麦加轻轨（中铁建亏损41.53亿元）"
            },
            {
                "type": "法律合规风险",
                "severity": "中高",
                "countries": ["南非"],
                "description": "税务合规和外汇管制问题",
                "reference_case": "南非Transnet机车采购"
            },
            {
                "type": "市场准入风险",
                "severity": "中",
                "regions": ["欧盟"],
                "description": "反补贴调查成为重要障碍",
                "reference_case": "保加利亚高铁列车采购"
            }
        ]

        return report

    def export_data_to_json(self, filename: str = "asean_rail_intelligence.json"):
        """导出数据到JSON文件"""
        data = {
            "metadata": {
                "version": self.version,
                "generated_at": self.init_date
            },
            "countries": self.countries_db,
            "companies": self.companies_db,
            "projects": self.projects_db,
            "risks": self.risks_db,
            "sources": self.sources_db
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"数据已导出到: {filename}")

    def interactive_query(self):
        """交互式查询界面"""
        print("\n" + "="*60)
        print("东盟轨道交通研究Agent - 交互式查询系统")
        print("="*60)
        print("\n可用命令:")
        print("1. 市场机会分析 - 输入: oppo <国家>")
        print("   示例: oppo vietnam")
        print("\n2. 竞争格局分析 - 输入: comp <国家>")
        print("   示例: comp malaysia")
        print("\n3. 风险评估 - 输入: risk <项目名称>")
        print("   示例: risk 菲律宾北吕宋铁路")
        print("\n4. 机会匹配 - 输入: match <查询关键词>")
        print("   示例: match 越南地铁车辆采购")
        print("\n5. 生成情报报告 - 输入: report")
        print("\n6. 导出数据 - 输入: export")
        print("\n7. 退出 - 输入: quit")
        print("\n" + "="*60)

        while True:
            try:
                user_input = input("\n请输入命令: ").strip()

                if not user_input:
                    continue

                if user_input.lower() == "quit":
                    print("感谢使用东盟轨道交通研究Agent!")
                    break

                elif user_input.lower() == "report":
                    report = self.generate_intelligence_report()
                    print("\n【综合情报报告】")
                    print(f"生成时间: {report['generated_at']}")
                    print(f"\n市场概要:")
                    for item in report['summary']['key_trends']:
                        print(f"  - {item}")
                    print(f"\n顶级机会: {len(report['top_opportunities'])}个")
                    print(f"风险预警: {len(report['risk_alerts'])}个")
                    # 详细报告
                    full_report_filename = "asean_rail_intelligence_report.json"
                    with open(full_report_filename, 'w', encoding='utf-8') as f:
                        json.dump(report, f, ensure_ascii=False, indent=2)
                    print(f"完整报告已保存到: {full_report_filename}")

                elif user_input.lower() == "export":
                    self.export_data_to_json()

                elif user_input.startswith("oppo"):
                    parts = user_input.split()
                    if len(parts) == 2:
                        country = parts[1]
                        result = self.analyze_market_opportunities(country)
                        print(f"\n【市场机会分析 - {result.get('country', country)}】")
                        for opp in result.get("opportunities", []):
                            print(f"\n项目: {opp['project_name']}")
                            print(f"中国机会: {', '.join(opp['chinese_opportunities'])}")
                            print(f"风险等级: {opp['risk_level']}")
                    else:
                        print("用法: oppo <国家>")
                        print("示例: oppo vietnam")

                elif user_input.startswith("comp"):
                    parts = user_input.split()
                    if len(parts) == 2:
                        country = parts[1]
                        result = self.analyze_competitive_landscape(country)
                        print(f"\n【竞争格局分析 - {result.get('country', country)}】")
                        print(f"\n中国企业参与:")
                        for company in result.get("chinese_companies", []):
                            print(f"  - {company['company_name']} ({company['category']})")
                            print(f"    项目: {company['project']}")
                            print(f"    角色: {company['role']}")
                        print(f"\n国际竞争对手:")
                        for comp in result.get("international_competitors", []):
                            print(f"  - {comp['name']}")
                            print(f"    位置: {comp['market_position']}")
                        print(f"\n中国优势:")
                        for advantage in result.get("competitive_advantage", {}).get("advantages", []):
                            print(f"  - {advantage}")
                    else:
                        print("用法: comp <国家>")
                        print("示例: comp malaysia")

                elif user_input.startswith("risk"):
                    parts = user_input.split(maxsplit=2)
                    if len(parts) >= 2:
                        project_name = " ".join(parts[1:])
                        result = self.assess_project_risks(project_name)
                        print(f"\n【风险评估 - {project_name}】")
                        print(f"政治风险: {result['political_risk']}")
                        print(f"财务风险: {result['financial_risk']}")
                        print(f"法律风险: {result['legal_risk']}")
                        print(f"技术风险: {result['technical_risk']}")
                        if result['mitigation_strategies']:
                            print(f"\n缓解策略:")
                            for strategy in result['mitigation_strategies']:
                                print(f"  - {strategy}")
                    else:
                        print("用法: risk <项目名称>")
                        print("示例: risk 菲律宾北吕宋铁路")

                elif user_input.startswith("match"):
                    parts = user_input.split(maxsplit=1)
                    if len(parts) == 2:
                        query = parts[1]
                        matches = self.match_opportunities(query)
                        print(f"\n【机会匹配 - {query}】")
                        print(f"找到 {len(matches)} 个匹配")
                        for match in matches:
                            print(f"\n国家: {match['country']}")
                            print(f"项目: {match['project_name']}")
                            if match['opportunities']:
                                print(f"中国机会: {', '.join(match['opportunities'])}")
                            if match['risks']:
                                print(f"风险: {', '.join(match['risks'])}")
                            if match['timeline']:
                                print(f"时间表: {match['timeline']}")
                    else:
                        print("用法: match <查询关键词>")
                        print("示例: match 越南地铁车辆采购")

                else:
                    print("未知命令，请重新输入")

            except KeyboardInterrupt:
                print("\n\n感谢使用东盟轨道交通研究Agent!")
                break
            except Exception as e:
                print(f"发生错误: {e}")
                print("请重新输入命令")


def main():
    """主函数"""
    print("\n东盟轨道交通研究Agent")
    print(f"版本: {ASEANRailResearchAgent().version}")
    print(f"初始化时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n正在初始化系统...")

    # 创建Agent实例
    agent = ASEANRailResearchAgent()

    print(f"✓ 已加载 {len(agent.countries_db)} 个国家数据")
    print(f"✓ 已加载 {len(agent.companies_db)} 个企业类别")
    print(f"✓ 已加载 {len(agent.projects_db)} 个国家项目数据")
    print(f"✓ 已加载 {len(agent.risks_db)} 个风险案例")
    print(f"✓ 已加载 {len(agent.sources_db)} 个数据源")
    print("\n系统初始化完成!")

    # 启动交互式查询
    agent.interactive_query()


if __name__ == "__main__":
    main()
