# SmartStock Audit Engine V5.1

### 🛡️ Disclaimer & Boundaries / 免责与边界声明
- **Decision Engine**: This is a rule-based execution tool, NOT financial advice. / 本工具为规则执行引擎，非财务建议。
- **System Failure**: If price drops below the 20D support, the logic is considered FAILED. / 若价格跌破20日支撑，逻辑判定为失效。

### 🚀 How to use / 如何使用
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `streamlit run app.py`

### 📊 Strategy Logic / 策略逻辑
- **Trend**: MA200 Filter.
- **Momentum**: B-Xtrender (Short bars + Long-term line).
- **Risk**: 20D dynamic stop-loss.
