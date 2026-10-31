StockScope Learn｜收益、风险与资产配置整合版

本版更新目标
把原来的「收益与风险」与「资产配置与模拟练习」合并为一条完整的学习流程，而不是简单拼接两个页面。

主要改动
1. 合并为「收益、风险与资产配置」一课，课程总数从 10 课变为 9 课。
2. 保留单项资产表现比较：区间收益率、年化波动率、最大回撤，并以共同交易日期比较所选资产。
3. 增加投资目标时间范围的引导说明，帮助学习者理解期限与风险承受能力会影响配置选择；这只是教学提示，不构成个人投资建议。
4. 加入资产配置模拟：三项资产权重合计固定为 100%，可以查看组合净值路径和回撤路径。
5. 同时比较初始权重买入并持有与每月再平衡，强调再平衡不是保证提高收益的技巧，而是让配置回到目标权重的一种纪律方法。
6. 增加日收益相关性热图，让分散化的学习不止停留在「持有不同代码」的概念上。
7. 新增 BND（美国综合债券 ETF）和 SGOV（美国 0–3 个月美国国债 ETF）作为跨资产类别教学样例。ETF 本身仍会有价格、利率及其他风险，不应视为保本现金替代品。
8. 迁移旧课程的完成状态和小测验记录；旧导航自动指向合并后的课程，减少升级后的状态丢失。
9. 清理重复的独立课程入口，并更新首页课程卡片、侧边导航、完成进度与综合测验的课程名称。

模拟假设与限制
- 行情由原项目的 yfinance 日线数据加载逻辑提供。
- 组合仅使用三项资产均有行情的共同交易日期。
- 起始组合价值由用户选择；各资产按初始权重分配。
- 买入并持有策略允许权重随相对表现漂移；每月再平衡策略在月度日期边界恢复目标权重。
- 模拟没有纳入交易佣金、买卖价差、税费、滑点、ETF 分派现金流的精确税务处理或个人账户限制。
- 数据区间收益率、波动率和最大回撤是历史描述性指标，不代表未来表现或最大可能损失。
- 历史相关性可能变化；相关性热图不能保证未来资产之间仍保持相同关系。
- BND 和 SGOV 仅是教学示例；SGOV 持有短期美国国债，但 ETF 市价仍会波动，不是银行存款或保证本金产品。

本次验证
- Python 语法编译通过。
- 合并课程元数据、导航路由、旧课程状态迁移结构通过测试。
- 使用合成价格序列测试组合净值、月度再平衡、收益率、年化波动率、最大回撤、权重总和校验和空输入边界。
- 测试 Plotly 相关性热图配置可序列化。
- 当前执行环境未安装 Streamlit 与 yfinance，因此没有完成真实浏览器端到端运行和联网数据加载验收。启动后仍需在本机确认行情接口和页面视觉效果。

研究依据（用于课程设计，不代表投资建议）
- Investor.gov, Asset Allocation and Diversification: https://www.investor.gov/introduction-investing/getting-started/asset-allocation
- Investor.gov, Beginners' Guide to Asset Allocation, Diversification, and Rebalancing: https://www.investor.gov/additional-resources/general-resources/publications-research/info-sheets/beginners-guide-asset
- FINRA, Diversification and Concentration Risk: https://www.finra.org/investors/insights/concentration-risk
- Vanguard, BND product information: https://investor.vanguard.com/investment-products/etfs/profile/bnd
- iShares, SGOV product information: https://www.ishares.com/us/products/314116/ishares-0-3-month-treasury-bond-etf
