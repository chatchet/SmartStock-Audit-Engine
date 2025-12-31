# 🚀 SmartStock Audit Engine V5.1 (Bilingual)
### 工业级交易决策审计引擎 / Industrial-Grade Trading Decision Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge.svg)](https://share.streamlit.io/) 
*注：部署后可在此处替换你的专属 Streamlit 链接*

---

## 🛡️ Disclaimer & System Boundaries / 免责与边界声明
> **[English]**
> 1. **Not Financial Advice**: This tool is an execution logic engine based on rules. It does NOT predict future price movements.
> 2. **Timestamp Priority**: Always check the SGT (Singapore Time) on the chart. Stale reports are dangerous.
> 3. **Failure Audit**: If the system status is marked "FAILED", stop execution immediately.
>
> **[中文]**
> 1. **非财务建议**：本工具是基于量化规则的执行逻辑引擎，不具备预测未来涨跌的功能。
> 2. **时间戳优先**：请务必核查图表上的新加坡时间戳（SGT）。在波动市场中，过时的报告是危险的。
> 3. **失败判定**：如果系统审计状态显示为“FAILED（失效）”，请立即停止任何执行动作。

---

## 📖 Introduction / 系统介绍
**SmartStock V5.1** 是一套专为「去模糊化决策」设计的审计系统。它通过三层过滤网（趋势、动能、结构），将复杂的市场信息压缩为唯一的**操作指令**与**仓位建议**。

**Core Philosophy / 核心哲学：**
"Let the system think, let the user act." / “让系统多想，让用户少动。”

---

## 🛠️ Key Features / 核心功能
- **Hard Tri-State Output / 强制三态输出**: No "Wait-and-see". Only **BUY**, **HOLD**, or **SELL**. / 杜绝含糊，只输出“买入”、“持有”或“卖出”。
- **Dual-Track Momentum / 双轨动能**: Uses B-Xtrender (Short-term bars + Long-term baseline) to confirm "True Attack". / 使用 B-Xtrender 双轨系统识别真正的进攻波。
- **Dynamic Risk Control / 动态风控**: 20-day dynamic support line (Hard Stop-loss). / 基于20日低点的动态止损线。
- **Bilingual Interface / 双语界面**: All rationale and commands in both English and Chinese. / 决策逻辑与指令全中英双语对照。

---

## 📊 How to Read the Audit / 如何解读审计结果


### 1. Command Panel / 指令面板
- **Command / 指令**: The only action for today. / 今日唯一核心指令。
- **Position / 仓位**: Precise percentage suggestion. / 确定性的仓位百分比。
- **Next Action / 下一步动作**: Clear instruction for execution. / 明确的操作指导。

### 2. Chart Legend / 图表线义解释
- **Blue Line / 蓝色实线**: MA200 (Long-term Trend / 长期牛熊线)
- **Purple Dash / 紫色虚线**: 52W High (Structural Resistance / 52周压力位)
- **Orange Dots / 橙色点线**: 20D Low (Hard Stop Line / 20日硬核止损线)
- **BX Dark Blue / BX蓝线**: Momentum Baseline (Trend Strength / 动能趋势基准)

---

## 🚀 Setup & Installation / 安装与运行
1. **Clone this repository / 克隆仓库**
2. **Install dependencies / 安装依赖**:
   ```bash
   pip install -r requirements.txt
