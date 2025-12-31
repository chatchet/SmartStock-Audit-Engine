import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import mplfinance as mpf
from datetime import datetime, timedelta
import pytz
import io

# ==========================================
# 1. Page Config / 页面配置
# ==========================================
st.set_page_config(page_title="SmartStock V5.1 Audit Engine", layout="wide")

# ==========================================
# 2. Disclaimer & Boundaries / 免责与边界声明 (中英双语)
# ==========================================
st.warning("""
**Disclaimer & System Boundaries / 免责与边界声明**
1. **Not Financial Advice / 非财务建议**: This tool is an execution logic engine based on momentum and risk rules. It does not predict the future. / 本工具是基于动能与风控规则的执行引擎，不具备预测未来的功能。
2. **Timestamp Priority / 时间戳优先**: Always check the SGT Timestamp. Stale reports are dangerous in volatile markets. / 请务必检查新加坡时间戳。在波动市场中，过时的报告是危险的。
3. **Failure Audit / 失败判定**: If the system marks "FAILED", stop execution immediately. / 如果系统标记为“失败判定”，请立即停止执行。
""")

# ==========================================
# 3. Sidebar Inputs / 侧边栏输入 (中英双语)
# ==========================================
st.sidebar.header("System Controls / 系统控制")
symbol = st.sidebar.text_input("Stock Symbol / 股票代码", value="D05.SI")
analyze_btn = st.sidebar.button("Run Audit / 执行审计")

if analyze_btn:
    # --- Data Fetching ---
    sgt = pytz.timezone('Asia/Singapore')
    now_sg = datetime.now(sgt)
    
    with st.spinner('Calculating... / 计算中...'):
        df = yf.download(symbol, start=(now_sg - timedelta(days=730)), end=now_sg, progress=False, auto_adjust=True)
        if isinstance(df.columns, pd.MultiIndex): df.columns = [str(c[0]) for c in df.columns]
        
        # --- Logic Layer (V5.1 Core) ---
        df['MA200'] = ta.sma(df['Close'], length=200)
        df['target_52w'] = df['High'].rolling(window=252).max()
        df['dynamic_support'] = df['Low'].rolling(window=20).min()
        df['bx_short'] = ta.ema(ta.rsi(df['Close'], length=5) - 50, length=3)
        df['bx_long'] = ta.ema(ta.rsi(df['Close'], length=20) - 50, length=10)
        
        df_clean = df.dropna().copy()
        latest = df_clean.iloc[-1]
        prev = df_clean.iloc[-2]
        
        # Decision Logic
        is_attacking = latest['bx_short'] > 0
        decision_en, decision_cn = "HOLD", "HOLD (持有/观望)"
        pos_val = 0
        
        if latest['Close'] < latest['dynamic_support']:
            decision_en, decision_cn = "SELL (EXIT)", "清仓 (离场)"
            pos_val = 0
        elif is_attacking and prev['bx_short'] <= 0:
            decision_en, decision_cn = "BUY (ENTER)", "买入 (建仓)"
            pos_val = 60
        elif is_attacking:
            decision_en, decision_cn = "HOLD (TREND)", "持股 (顺势)"
            pos_val = 100 if latest['Close'] > latest['target_52w'] else 60
        else:
            decision_en, decision_cn = "SELL (WEAK)", "减仓 (走弱)"
            pos_val = 20

    # ==========================================
    # 4. Results Display / 结果展示 (中英双语)
    # ==========================================
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Core Command / 核心指令")
        st.info(f"**{decision_en} / {decision_cn}**")
        st.write(f"**Target Position / 目标仓位:** {pos_val}%")
        st.write(f"**SGT Timestamp / 时间戳:** {now_sg.strftime('%Y-%m-%d %H:%M:%S')}")

    with col2:
        st.subheader("System Facts / 系统事实")
        st.write(f"52W High / 52周前高: {latest['target_52w']:.2f}")
        st.write(f"Stop Line / 止损线: {latest['dynamic_support']:.2f}")
        is_failed = latest['Close'] < latest['dynamic_support']
        st.write(f"Audit Status / 审计状态: {'❌ FAILED/失效' if is_failed else '✅ NORMAL/正常'}")

    # --- Chart Generation (English Only as requested) ---
    st.subheader("Technical Analysis Chart (English Version)")
    plot_df = df_clean.tail(100)
    bx_colors = ['#26a69a' if x > 0 else '#ef5350' for x in plot_df['bx_short']]
    
    apds = [
        mpf.make_addplot(plot_df['MA200'], color='blue', width=1),
        mpf.make_addplot(plot_df['target_52w'], color='purple', linestyle='--'),
        mpf.make_addplot(plot_df['dynamic_support'], color='orange', linestyle=':'),
        mpf.make_addplot(plot_df['bx_short'], type='bar', color=bx_colors, panel=2),
        mpf.make_addplot(plot_df['bx_long'], color='darkblue', panel=2, width=1.5)
    ]
    
    fig, axlist = mpf.plot(plot_df, type='candle', style='charles', addplot=apds,
                           title=f"{symbol} Audit Engine V5.1",
                           ylabel='Price', volume=True, panel_ratios=(6,2,2),
                           figratio=(16, 11), returnfig=True)
    st.pyplot(fig)

    # --- Legend / 线义解释 (Bilingual) ---
    st.markdown("""
    **Chart Legend / 图表线义解释:**
    - **Blue Line / 蓝色实线**: MA200 (Major Trend / 长期牛熊线)
    - **Purple Dash / 紫色虚线**: 52W High (Resistance / 52周压力位)
    - **Orange Dots / 橙色点线**: 20D Low (Hard Stop / 20日止损硬线)
    - **BX Blue Line / BX蓝线**: Long-term Momentum Baseline / BX长期动能基准线
    """)
