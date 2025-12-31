# SmartStock Audit Engine V5.1

### 🌍 Overview / 概述
An industrial-grade trading decision engine based on the B-Xtrender system. Designed for clarity and strict execution.
基于 B-Xtrender 系统的工业级交易决策引擎，专为执行力与清晰度设计。

### 🛡️ Disclaimer / 免责声明
**This is NOT financial advice.** The tool provides rule-based logic. Always audit the "Failure Status" before following commands.
**本工具非财务建议。** 仅提供基于规则的逻辑。在跟随指令前，务必核查“审计失效状态”。

### 🛠️ Setup / 安装
1. Clone this repo.
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

### 📈 Logic / 逻辑
- **Single Output**: BUY, HOLD, or SELL only.
- **Hard Stops**: Based on 20-day price lows.
- **Momentum**: Dual-track B-Xtrender.
