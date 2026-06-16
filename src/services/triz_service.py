from typing import List, Dict, Any
from src.models.schemas import TrizPrinciple, TrizContradiction


class TrizService:
    """TRIZ 理论服务"""

    # TRIZ 39 个工程参数
    PARAMETERS = [
        "运动物体的重量", "静止物体的重量", "运动物体的长度", "静止物体的长度",
        "运动物体的面积", "静止物体的面积", "运动物体的体积", "静止物体的体积",
        "速度", "力", "应力或压力", "形状",
        "物体结构的稳定性", "强度", "运动物体的耐久性", "静止物体的耐久性",
        "温度", "照度", "运动物体消耗的能量", "静止物体消耗的能量",
        "功率", "能量损失", "物质损失", "信息损失",
        "时间损失", "物质的量", "可靠性", "测量精度",
        "制造精度", "作用于物体的有害因素", "有害的副作用", "可制造性",
        "使用的方便性", "可维修性", "适应性/通用性", "装置的复杂性",
        "控制的复杂性", "自动化程度", "生产率"
    ]

    # TRIZ 40 个创新原理
    PRINCIPLES = {
        1: {"name": "分割", "description": "将物体分成独立的部分；使物体成为可拆卸的；增加物体的分割程度"},
        2: {"name": "抽取", "description": "从物体中抽取有害的部分或特性；仅抽取物体中必要的部分或特性"},
        3: {"name": "局部质量", "description": "将物体或环境的均匀结构变为不均匀的；让物体的不同部分执行不同的功能"},
        4: {"name": "非对称", "description": "用非对称的形状取代对称的形状；如果物体已经是不对称的，增加其不对称程度"},
        5: {"name": "合并", "description": "在空间上合并同类或相关的物体或操作；在时间上合并同类或相关的操作"},
        6: {"name": "多用性", "description": "使一个物体执行多种功能，消除对其他物体的需求"},
        7: {"name": "嵌套", "description": "将一个物体嵌入另一个物体内；使一个物体穿过另一个物体的空腔"},
        8: {"name": "重量补偿", "description": "与其他物体结合产生升力或浮力；利用环境动力（如空气动力、流体动力）"},
        9: {"name": "预先反作用", "description": "预先施加反向作用以消除有害因素；如果物体处于张力状态，预先施加压力"},
        10: {"name": "预先作用", "description": "预先完成必要的改变；预先将物体放置好，使其能从最方便的位置起作用"},
        11: {"name": "预先防护", "description": "预先准备好应急措施，如备用系统、安全装置"},
        12: {"name": "等势性", "description": "改变操作条件，使物体不需要升高或降低"},
        13: {"name": "反向", "description": "用相反的动作代替问题指定的动作；使物体可动部分变为固定，固定部分变为可动"},
        14: {"name": "曲面化", "description": "用曲线代替直线，曲面代替平面，球面代替立方体；使用滚轮、球体、螺旋"},
        15: {"name": "动态化", "description": "使物体或环境的特性自动调整到最佳状态；将物体分成可相对移动的若干部分"},
        16: {"name": "未达到或过度", "description": "如果精确难以达到，允许稍多或稍少，简化问题"},
        17: {"name": "维度变化", "description": "将物体从一维变为二维，二维变为三维；利用多层结构；倾斜物体"},
        18: {"name": "机械振动", "description": "使物体振动；增加振动频率；利用共振频率"},
        19: {"name": "周期性动作", "description": "用周期性动作代替连续动作；如果已经是周期性的，改变其频率"},
        20: {"name": "有效作用的连续性", "description": "使物体所有部分持续满负荷工作；消除空闲和间歇性动作"},
        21: {"name": "快速通过", "description": "以极快的速度执行有害操作；快速通过有害环境或过程"},
        22: {"name": "变害为利", "description": "利用有害因素获得有益效果；通过有害因素强化有用效应"},
        23: {"name": "反馈", "description": "引入反馈；如果已有反馈，改变其大小或作用"},
        24: {"name": "中介物", "description": "使用中间物体来传递或执行动作；临时将物体与另一个容易移动的物体结合"},
        25: {"name": "自服务", "description": "使物体通过辅助功能自我服务；利用废弃的能量与物质"},
        26: {"name": "复制", "description": "用简化的廉价的复制品代替复杂的昂贵的物体；使用光学复制品"},
        27: {"name": "廉价短寿命", "description": "用多个廉价物体代替昂贵的物体，牺牲某些特性（如寿命）"},
        28: {"name": "机械系统的替代", "description": "用光学、声学、热学系统代替机械系统；使用电场、磁场"},
        29: {"name": "气动与液压结构", "description": "使用气体或液体代替固体零件；利用气垫、液体静压、流体动力"},
        30: {"name": "柔性壳体和薄膜", "description": "用柔性壳体和薄膜代替传统结构；使用柔性壳体和薄膜将物体与环境隔离"},
        31: {"name": "多孔材料", "description": "使物体多孔或添加多孔元素；如果已多孔，用孔隙填充有用物质"},
        32: {"name": "改变颜色", "description": "改变物体或环境的颜色；改变物体或环境的透明度"},
        33: {"name": "同质性", "description": "使相互作用的物体由同种材料制成"},
        34: {"name": "抛弃与再生", "description": "抛弃已完成功能的部分；在过程中直接再生物体的消耗部分"},
        35: {"name": "物理/化学参数变化", "description": "改变物体的物理状态；改变浓度或密度；改变柔性；改变温度"},
        36: {"name": "相变", "description": "利用相变过程中发生的现象，如体积改变、吸热或放热"},
        37: {"name": "热膨胀", "description": "利用热膨胀或热收缩；利用不同材料的不同热膨胀系数"},
        38: {"name": "强氧化剂", "description": "用富氧空气代替普通空气；用纯氧代替富氧空气；使用电离辐射"},
        39: {"name": "惰性环境", "description": "用惰性环境代替正常环境；使用真空环境"},
        40: {"name": "复合材料", "description": "从单一材料变为复合材料"}
    }

    # 简化版矛盾矩阵（部分常用组合）
    CONTRADICTION_MATRIX = {
        # 改善: 速度 (9) -> 恶化参数对应的原理
        "速度": {
            "运动物体的重量": [2, 8, 15, 38],
            "静止物体的重量": [8, 10, 18, 37],
            "力": [10, 15, 36, 28],
            "能量损失": [10, 13, 28, 38],
        },
        # 改善: 力 (10)
        "力": {
            "运动物体的重量": [10, 36, 37, 40],
            "速度": [13, 28, 15, 19],
            "能量损失": [2, 36, 25, 35],
        },
        # 改善: 可靠性 (27)
        "可靠性": {
            "运动物体的重量": [11, 3, 10, 32],
            "静止物体的重量": [3, 10, 13, 28],
            "速度": [11, 35, 13, 21],
            "成本": [27, 17, 40, 29],
        },
        # 改善: 生产率 (39)
        "生产率": {
            "运动物体的重量": [26, 35, 10, 28],
            "精度": [28, 2, 10, 24],
            "能量损失": [35, 20, 10, 28],
        },
    }

    def get_all_parameters(self) -> List[str]:
        """获取所有工程参数"""
        return self.PARAMETERS

    def get_all_principles(self) -> List[TrizPrinciple]:
        """获取所有创新原理"""
        return [
            TrizPrinciple(
                id=k,
                name=v["name"],
                description=v["description"],
                examples=[]
            )
            for k, v in self.PRINCIPLES.items()
        ]

    def get_principle_by_id(self, principle_id: int) -> TrizPrinciple:
        """根据 ID 获取创新原理"""
        if principle_id in self.PRINCIPLES:
            p = self.PRINCIPLES[principle_id]
            return TrizPrinciple(
                id=principle_id,
                name=p["name"],
                description=p["description"],
                examples=[]
            )
        return None

    def find_principles_for_contradiction(self, improving: str, worsening: str) -> List[TrizPrinciple]:
        """根据矛盾查找推荐原理"""
        if improving in self.CONTRADICTION_MATRIX:
            matrix = self.CONTRADICTION_MATRIX[improving]
            if worsening in matrix:
                principle_ids = matrix[worsening]
                return [self.get_principle_by_id(pid) for pid in principle_ids if self.get_principle_by_id(pid)]
        return []

    def analyze_contradiction(self, problem: str, improving: str, worsening: str) -> Dict[str, Any]:
        """分析矛盾"""
        principles = self.find_principles_for_contradiction(improving, worsening)

        return {
            "contradictions": [
                TrizContradiction(
                    improving_parameter=improving,
                    worsening_parameter=worsening,
                    description=f"在解决问题'{problem}'时，改善'{improving}'可能导致'{worsening}'恶化"
                )
            ],
            "principles": principles,
            "suggestions": [
                f"考虑使用{principle.name}原理：{principle.description}"
                for principle in principles
            ]
        }


triz_service = TrizService()
