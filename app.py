import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import mplfinance as mpf
from datetime import datetime, timedelta
import pytz

# ==========================================
# 1. 页面基础配置
# ==========================================
st.set_page_config(page_title="SmartStock V5.1 Audit Engine", layout="wide")

# ==========================================
# 2. 免责声明与边界 (中英双语)
# ==========================================
st.error("""
**[IMPORTANT / 重要声明] Disclaimer & System Boundaries / 免责与边界声明**
1. **Not Financial Advice / 非财务建议**: This tool is an execution logic engine. It does NOT predict the future. / 本工具为规则执行引擎，不具备预测功能。
2. **Timestamp Priority / 时间戳优先**: Check the SGT Timestamp. Stale reports are dangerous. / 请务必检查新加坡时间戳，过时报告具有风险。
3. **Failure Audit / 失败判定**: If the system marks "FAILED", stop execution immediately. / 若系统标记为“失败判定”，请立即停止执行。
""")

# ==========================================
# 3. 侧边栏输入
# ==========================================
st.sidebar.header("Control Panel / 控制面板")
symbol = st.sidebar.text_input("Stock Symbol (e.g. D05.SI, AAPL)", value="D05.SI")
run_audit = st.sidebar.button("Run System Audit / 执行系统审计")

if run_audit:
    # --- 数据抓取 ---
    sgt = pytz.timezone('Asia/Singapore')
    now_sg = datetime.now(sgt)
    time_str = now_sg.strftime('%Y-%m-%d %H:%M:%S')
    
    with st.spinner('Engine Running... / 引擎运行中...'):
        df = yf.download(symbol, start=(now_sg - timedelta(days=730)), end=now_sg, progress=False, auto_adjust=True)
        if df.empty:
            st.error("Error: Could not fetch data. Check the symbol.")
        else:
            if isinstance(df.columns, pd.MultiIndex): df.columns = [str(c[0]) for c in df.columns]
            
            # --- 核心指标层 (V5.1) ---
            df['MA200'] = ta.sma(df['Close'], length=200)
            df['target_52w'] = df['High'].rolling(window=252).max()
            df['dynamic_support'] = df['Low'].rolling(window=20).min()
            # B-Xtrender 逻辑
            df['bx_short'] = ta.ema(ta.rsi(df['Close'], length=5) - 50, length=3)
            df['bx_long'] = ta.ema(ta.rsi(df['Close'], length=20) - 50, length=10)
            
            df_clean = df.dropna().copy()
            latest = df_clean.iloc[-1]
            prev = df_clean.iloc[-2]
            
            # --- 决策状态机 (三态强制) ---
            is_attacking = latest['bx_short'] > 0
            is_failed = latest['Close'] < latest['dynamic_support']
            
            decision_en, decision_cn = "HOLD", "HOLD (持有/观望)"
            pos_val = 0
            next_action = "Maintain current state."

            if is_failed:
                decision_en, decision_cn = "SELL (EXIT)", "强制清仓 (离场)"
                pos_val = 0
                next_action = "Liquidate all positions immediately. / 立即执行清仓。"
            elif is_attacking and prev['bx_short'] <= 0:
                decision_en, decision_cn = "BUY (ENTER)", "买入 (建仓)"
                pos_val = 60
                next_action = "Execute 60% position entry. / 执行60%仓位买入。"
            elif is_attacking:
                decision_en, decision_cn = "HOLD (TREND)", "持股 (顺势)"
                pos_val = 100 if latest['Close'] > latest['target_52w'] else 60
                next_action = "Trend intact. Do nothing. / 趋势未破，无需操作。"
            else:
                decision_en, decision_cn = "SELL (WEAK)", "减仓 (走弱)"
                pos_val = 20
                next_action = "Momentum faded. Reduce to 20%. / 动能消失，减仓至20%。"

            # ==========================================
            # 4. 双语面板展示
            # ==========================================
            st.divider()
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Command / 指令", decision_en)
                st.write(f"({decision_cn})")
            with c2:
                st.metric("Position / 仓位", f"{pos_val}%")
            with c3:
                status_color = "red" if is_failed else "green"
                st.markdown(f"**Audit / 审计状态**: :{status_color}[{'FAILED/失效' if is_failed else 'NORMAL/正常'}]")

            st.info(f"**Next Action / 下一步动作**: {next_action}")
            st.caption(f"Generated at: {time_str} (Singapore Time)")

            # ==========================================
            # 5. 图表输出 (全英文专业版)
            # ==========================================
            st.subheader(f"Technical Audit Chart: {symbol}")
            plot_df = df_clean.tail(100)
            bx_colors = ['#26a69a' if x > 0 else '#ef5350' for x in plot_df['bx_short']]
            
            apds = [
                mpf.make_addplot(plot_df['MA200'], color='blue', width=1),
                mpf.make_addplot(plot_df['target_52w'], color='purple', linestyle='--'),
                mpf.make_addplot(plot_df['dynamic_support'], color='orange', linestyle=':'),
                mpf.make_addplot(plot_df['bx_short'], type='bar', color=bx_colors, panel=2, ylabel='BX-Mom'),
                mpf.make_addplot(plot_df['bx_long'], color='darkblue', panel=2, width=1.5)
            ]
            
            fig, _ = mpf.plot(plot_df, type='candle', style='charles', addplot=apds,
                              title=f"\n{symbol} System V5.1",
                              ylabel='Price', volume=True, panel_ratios=(6,2,2),
                              figratio=(16, 11), returnfig=True)
            st.pyplot(fig)

            # 线义解释
            st.markdown("""
            **Chart Legend / 线义解释:**
            - **Blue / 蓝线**: MA200 (Long-term Bull/Bear)
            - **Purple Dash / 紫虚线**: 52W High (Resistance)
            - **Orange Dot / 橙点线**: 20D Low (Hard Stop Line)
            - **BX Dark Blue / BX蓝线**: Long-term Momentum Baseline
            """)
