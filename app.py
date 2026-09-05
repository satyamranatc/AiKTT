import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Page Configuration - Clean Professional Setup
st.set_page_config(
    page_title="PPFAS Portfolio Analytics & AI Forecast Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Top Nav Bar & Dark Theme - No Emojis)
st.markdown("""
<style>
    .main {
        background-color: #0d1117;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .stMetric {
        background: #161b22;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #30363d;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #f0f6fc;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #8b949e;
        font-size: 1rem;
        margin-bottom: 1.2rem;
    }
    .badge-actual {
        background-color: #1f6feb;
        color: #ffffff;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .badge-prediction {
        background-color: #8957e5;
        color: #ffffff;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .section-desc {
        background-color: #161b22;
        border-left: 4px solid #58a6ff;
        padding: 14px 18px;
        border-radius: 4px;
        margin-bottom: 1.5rem;
        color: #c9d1d9;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .ai-desc {
        background-color: #161b22;
        border-left: 4px solid #8957e5;
        padding: 14px 18px;
        border-radius: 4px;
        margin-bottom: 1.5rem;
        color: #c9d1d9;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    /* Top Navigation Bar Styling */
    div.row-widget.stRadio > div {
        flex-direction: row;
        background-color: #161b22;
        padding: 8px;
        border-radius: 8px;
        border: 1px solid #30363d;
        margin-bottom: 1.5rem;
    }
    div.row-widget.stRadio > div > label {
        background-color: transparent;
        padding: 8px 16px;
        border-radius: 6px;
        color: #c9d1d9;
        font-weight: 600;
        margin-right: 4px;
    }
    div.row-widget.stRadio > div > label:hover {
        background-color: #21262d;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Data Loaders
DATA_DIR = os.path.join(os.path.dirname(__file__), 'cleaned_data')

@st.cache_data
def load_all_datasets():
    summary_df = pd.read_csv(os.path.join(DATA_DIR, 'monthly_fund_summary_2016.csv'))
    holdings_df = pd.read_csv(os.path.join(DATA_DIR, 'all_portfolio_holdings_2016.csv'))
    derivs_df = pd.read_csv(os.path.join(DATA_DIR, 'derivative_positions_2016.csv'))
    sectors_df = pd.read_csv(os.path.join(DATA_DIR, 'sector_breakdown_2016.csv'))
    summary_2017_df = pd.read_csv(os.path.join(DATA_DIR, 'monthly_fund_summary_2017_prediction.csv'))
    holdings_2017_df = pd.read_csv(os.path.join(DATA_DIR, 'all_portfolio_holdings_2017_prediction.csv'))
    master_pred_df = pd.read_csv(os.path.join(DATA_DIR, 'predictive_portfolio_2017_master.csv'))
    combined_df = pd.read_csv(os.path.join(DATA_DIR, 'master_2016_2017_combined_portfolio.csv'))
    
    return summary_df, holdings_df, derivs_df, sectors_df, summary_2017_df, holdings_2017_df, master_pred_df, combined_df

try:
    summary_df, holdings_df, derivs_df, sectors_df, summary_2017_df, holdings_2017_df, master_pred_df, combined_df = load_all_datasets()
except Exception as e:
    st.error(f"Error loading required datasets: {e}")
    st.stop()

# Header Brand Banner
st.markdown("## PPFAS Portfolio Intelligence Platform")

# TOP NAVIGATION BAR (Rendered across top of every page)
nav_choice = st.radio(
    "Navigation Menu",
    [
        "Executive Overview (2016)",
        "Holdings & Sectors",
        "Stock AI Predictor (2017)",
        "Risk & Hedging",
        "AI Portfolio Forecast (2017)",
        "Investor Commentary"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

# Sidebar Download Panel & Quick Info
st.sidebar.title("PPFAS Platform")
st.sidebar.caption("Parag Parikh Long Term Value Fund")
st.sidebar.markdown("---")

excel_path = os.path.join(DATA_DIR, 'PPFAS_Portfolio_Intelligence_2016_2017_Master.xlsx')
if os.path.exists(excel_path):
    st.sidebar.markdown("### Master Excel Workbook")
    with open(excel_path, "rb") as f:
        st.sidebar.download_button(
            label="Download Master Formatted Excel (.xlsx)",
            data=f,
            file_name="PPFAS_Portfolio_Intelligence_2016_2017_Master.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
st.sidebar.markdown("---")
st.sidebar.markdown("### Dataset Summary")
st.sidebar.info("• 2016 Actuals: 297 Holdings\n• 2017 AI Predictions: 360 Holdings\n• Total Holdings Tracked: 657 Records")

# -------------------------------------------------------------
# MODULE 1: EXECUTIVE OVERVIEW (2016 ACTUALS)
# -------------------------------------------------------------
if nav_choice == "Executive Overview (2016)":
    st.markdown('<div class="main-title">Executive Portfolio Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">High-Level Financial Performance & Fund Asset Metrics for Calendar Year 2016</div>', unsafe_allow_html=True)
    st.markdown('<div class="badge-actual">DATA SOURCE: 2016 HISTORICAL ACTUALS</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-desc">
        <strong>What is this section?</strong><br>
        This dashboard provides a bird's-eye view of the mutual fund's growth throughout 2016. You can track how Assets Under Management (AUM) expanded, how Direct and Regular Net Asset Values (NAVs) performed month-by-month, and what percentage of funds were allocated to global US/UK equities and risk hedging.
    </div>
    """, unsafe_allow_html=True)

    active_summary = summary_df.dropna(subset=['aum_crores']).copy()
    latest_aum = active_summary['aum_crores'].iloc[-1]
    peak_nav = active_summary['direct_nav_end'].max()
    avg_foreign = active_summary['foreign_equity_pct'].mean()
    avg_hedged = active_summary['hedged_pct'].mean()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Closing AUM (Dec 2016)", f"Rs. {latest_aum:.2f} Cr", delta="+7.6% YoY Growth")
    m2.metric("Peak Direct Plan NAV", f"Rs. {peak_nav:.4f}", delta="Oct 2016 High")
    m3.metric("Avg Foreign Equity Exposure", f"{avg_foreign:.2f}% NAV", delta="US & Global ADRs")
    m4.metric("Avg Hedged Assets Ratio", f"{avg_hedged:.2f}% NAV", delta="USD/INR & Equity Futures")

    st.markdown("---")

    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("Assets Under Management Trend (2016)")
        fig_aum = px.line(active_summary, x='month', y='aum_crores', markers=True,
                          labels={'aum_crores': 'AUM (Rs. Crores)', 'month': 'Month'},
                          color_discrete_sequence=['#2da44e'])
        fig_aum.update_layout(template="plotly_dark", height=380, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_aum, use_container_width=True)

    with col_r:
        st.subheader("Direct Plan vs Regular Plan NAV (2016)")
        fig_nav = go.Figure()
        fig_nav.add_trace(go.Scatter(x=active_summary['month'], y=active_summary['direct_nav_end'],
                                     mode='lines+markers', name='Direct Plan NAV', line=dict(color='#58a6ff', width=3)))
        fig_nav.add_trace(go.Scatter(x=active_summary['month'], y=active_summary['regular_nav_end'],
                                     mode='lines+markers', name='Regular Plan NAV', line=dict(color='#8b949e', width=2, dash='dot')))
        fig_nav.update_layout(template="plotly_dark", height=380, yaxis_title="NAV (Rs.)", margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_nav, use_container_width=True)

# -------------------------------------------------------------
# MODULE 2: STOCK HOLDINGS & SECTOR EXPLORER
# -------------------------------------------------------------
elif nav_choice == "Holdings & Sectors":
    st.markdown('<div class="main-title">Stock Holdings & Sector Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Interactive Inspection Panel for Stock Positions and Industry Sector Allocations</div>', unsafe_allow_html=True)
    st.markdown('<div class="badge-actual">DATA SOURCE: 2016 HISTORICAL ACTUALS</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-desc">
        <strong>What is this section?</strong><br>
        This interactive explorer lets you filter the fund's monthly holdings by month, asset category (Core Indian Equity, Foreign Equity/ADRs, Special Situation Arbitrage), and industry sector. You can see exact share quantities, rupee market values, and individual stock weights.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    month_list = list(holdings_df['month'].unique())
    sel_m = c1.selectbox("Select Report Month", month_list, index=len(month_list)-1)

    cat_list = ["All Asset Categories"] + list(holdings_df['category'].unique())
    sel_cat = c2.selectbox("Filter Asset Category", cat_list)

    sec_list = ["All Industry Sectors"] + sorted([s for s in holdings_df['industry_sector'].unique() if pd.notna(s) and s != ''])
    sel_sec = c3.selectbox("Filter Industry Sector", sec_list)

    m_df = holdings_df[holdings_df['month'] == sel_m].copy()
    if sel_cat != "All Asset Categories":
        m_df = m_df[m_df['category'] == sel_cat]
    if sel_sec != "All Industry Sectors":
        m_df = m_df[m_df['industry_sector'] == sel_sec]

    st.markdown(f"#### Position Statement: **{sel_m} 2016** ({len(m_df)} Holdings Found)")

    col_t, col_p = st.columns([3, 2])

    with col_t:
        st.dataframe(
            m_df[['sr_no', 'category', 'instrument_name', 'industry_sector', 'quantity', 'market_value_lakhs', 'pct_nav']]
            .sort_values(by='market_value_lakhs', ascending=False)
            .rename(columns={
                'sr_no': 'Sr No', 'category': 'Category', 'instrument_name': 'Stock Name',
                'industry_sector': 'Sector', 'quantity': 'Quantity',
                'market_value_lakhs': 'Value (Rs. Lakhs)', 'pct_nav': '% of NAV'
            })
            .style.format({'Quantity': '{:,.0f}', 'Value (Rs. Lakhs)': 'Rs. {:,.2f} L', '% of NAV': '{:.2f}%'}),
            height=460,
            use_container_width=True
        )

    with col_p:
        st.subheader("Industry Sector Share")
        sec_agg = m_df.groupby('industry_sector')['market_value_lakhs'].sum().reset_index()
        fig_sec = px.pie(sec_agg, names='industry_sector', values='market_value_lakhs',
                         color_discrete_sequence=px.colors.qualitative.Safe)
        fig_sec.update_layout(template="plotly_dark", height=460, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_sec, use_container_width=True)

# -------------------------------------------------------------
# MODULE 3: STOCK-BY-STOCK AI PREDICTOR (2017)
# -------------------------------------------------------------
elif nav_choice == "Stock AI Predictor (2017)":
    st.markdown('<div class="main-title">Interactive Stock-by-Stock AI Predictor (2017)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Deep Data Inspection Tool Comparing 2016 Stock History with 2017 AI Predictions</div>', unsafe_allow_html=True)
    st.markdown('<div class="badge-prediction">MODEL OUTPUT: INDIVIDUAL STOCK FORECASTS</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="ai-desc">
        <strong>What is this section?</strong><br>
        Select ANY individual stock in the mutual fund to view its complete 2016 holding trajectory alongside the AI's predicted 2017 weight, market value, action strategy, and machine learning investment rationale!
    </div>
    """, unsafe_allow_html=True)

    all_stocks = sorted(list(holdings_df['instrument_name'].unique()))
    selected_stock = st.selectbox("🔍 Select Stock to Analyze & Predict", all_stocks, index=all_stocks.index('Alphabet INC') if 'Alphabet INC' in all_stocks else 0)

    s_history_2016 = holdings_df[holdings_df['instrument_name'] == selected_stock].copy()
    s_pred_2017 = master_pred_df[master_pred_df['instrument_name'] == selected_stock].copy()

    stock_category = s_history_2016['category'].iloc[0] if len(s_history_2016) > 0 else 'N/A'
    stock_sector = s_history_2016['industry_sector'].iloc[0] if len(s_history_2016) > 0 else 'N/A'
    months_active = len(s_history_2016)

    if len(s_pred_2017) > 0:
        pred_action = s_pred_2017['ai_action_strategy'].iloc[0]
        pred_weight_2017 = s_pred_2017['predicted_pct_nav'].iloc[-1]
        pred_val_2017 = s_pred_2017['predicted_market_value_lakhs'].iloc[-1]
    else:
        pred_action = "Maintain"
        pred_weight_2017 = s_history_2016['pct_nav'].iloc[-1] if len(s_history_2016) > 0 else 0.0
        pred_val_2017 = s_history_2016['market_value_lakhs'].iloc[-1] if len(s_history_2016) > 0 else 0.0

    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    col_k1.metric("Stock Category", stock_category)
    col_k2.metric("Industry Sector", stock_sector)
    col_k3.metric("2016 Holding Consistency", f"{months_active} / 10 Months")
    col_k4.metric("AI Predicted 2017 Action", pred_action)

    st.markdown("---")

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("2016 Actual Stock Weight (% NAV)")
        fig_s1 = px.line(s_history_2016, x='month', y='pct_nav', markers=True,
                         labels={'pct_nav': '% of NAV', 'month': 'Month'}, color_discrete_sequence=['#58a6ff'])
        fig_s1.update_layout(template="plotly_dark", height=360)
        st.plotly_chart(fig_s1, use_container_width=True)

    with col_chart2:
        st.subheader("2016 Actual vs 2017 AI Forecast Weight Trajectory")
        fig_s2 = go.Figure()
        fig_s2.add_trace(go.Scatter(x=s_history_2016['month'] + ' 16', y=s_history_2016['pct_nav'], mode='lines+markers', name='2016 Actual Weight %', line=dict(color='#58a6ff', width=3)))
        if len(s_pred_2017) > 0:
            fig_s2.add_trace(go.Scatter(x=s_pred_2017['month'] + ' 17', y=s_pred_2017['predicted_pct_nav'], mode='lines+markers', name='2017 AI Forecast Weight %', line=dict(color='#bc8cff', width=3, dash='dash')))
        fig_s2.update_layout(template="plotly_dark", height=360, yaxis_title="% of NAV")
        st.plotly_chart(fig_s2, use_container_width=True)

    st.markdown("### 📋 Historical vs Predicted Data Table for " + selected_stock)
    col_t1, col_t2 = st.columns(2)

    with col_t1:
        st.markdown("#### 2016 Actual Records")
        st.dataframe(
            s_history_2016[['month', 'quantity', 'market_value_lakhs', 'pct_nav']]
            .rename(columns={'month': 'Month', 'quantity': 'Shares', 'market_value_lakhs': 'Value (Rs. Lakhs)', 'pct_nav': '% NAV'})
            .style.format({'Shares': '{:,.0f}', 'Value (Rs. Lakhs)': 'Rs. {:,.2f} L', '% NAV': '{:.2f}%'}),
            height=300, use_container_width=True
        )

    with col_t2:
        st.markdown("#### 2017 AI Prediction Records")
        if len(s_pred_2017) > 0:
            st.dataframe(
                s_pred_2017[['month', 'predicted_quantity', 'predicted_market_value_lakhs', 'predicted_pct_nav', 'ai_action_strategy']]
                .rename(columns={'month': 'Month', 'predicted_quantity': 'Pred Shares', 'predicted_market_value_lakhs': 'Pred Value (Rs. L)', 'predicted_pct_nav': 'Pred % NAV', 'ai_action_strategy': 'AI Action'})
                .style.format({'Pred Shares': '{:,.0f}', 'Pred Value (Rs. L)': 'Rs. {:,.2f} L', 'Pred % NAV': '{:.2f}%'}),
                height=300, use_container_width=True
            )

# -------------------------------------------------------------
# MODULE 4: RISK MANAGEMENT & HEDGING
# -------------------------------------------------------------
elif nav_choice == "Risk & Hedging":
    st.markdown('<div class="main-title">Risk Management & Derivative Hedging</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Currency Futures Exposure, Arbitrage Legs, and Portfolio Turnover Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="badge-actual">DATA SOURCE: 2016 HISTORICAL ACTUALS</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-desc">
        <strong>What is this section?</strong><br>
        This section analyzes how PPFAS protected investor capital from stock market volatility and US Dollar exchange rate shifts. It breaks down derivative hedging positions (USD/INR currency futures and equity stock futures) and compares total turnover ratio against core stock turnover.
    </div>
    """, unsafe_allow_html=True)

    active_summary = summary_df.dropna(subset=['hedged_pct']).copy()
    col_h, col_p = st.columns(2)

    with col_h:
        st.subheader("Hedged Assets Ratio (% of AUM)")
        fig_h = px.bar(active_summary, x='month', y='hedged_pct', text='hedged_pct',
                       color_discrete_sequence=['#a5d6ff'])
        fig_h.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_h.update_layout(template="plotly_dark", height=380, yaxis_range=[0, 45], yaxis_title="Hedged % of NAV")
        st.plotly_chart(fig_h, use_container_width=True)

    with col_p:
        st.subheader("Portfolio Turnover Ratio Breakdown")
        fig_ptr = go.Figure()
        fig_ptr.add_trace(go.Bar(x=active_summary['month'], y=active_summary['ptr_inc_arbitrage']*100, name='Total PTR (Inc. Arbitrage)', marker_color='#f85149'))
        fig_ptr.add_trace(go.Bar(x=active_summary['month'], y=active_summary['ptr_exc_arbitrage']*100, name='Core PTR (Excl. Arbitrage)', marker_color='#ff7b72'))
        fig_ptr.update_layout(template="plotly_dark", height=380, barmode='group', yaxis_title="Turnover Ratio %")
        st.plotly_chart(fig_ptr, use_container_width=True)

# -------------------------------------------------------------
# MODULE 5: AI 2017 PORTFOLIO FORECAST MODEL
# -------------------------------------------------------------
elif nav_choice == "AI Portfolio Forecast (2017)":
    st.markdown('<div class="main-title">AI Predictive Portfolio & Stock Forecast (2017)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Full Machine Learning Forecast for 2017 Portfolio Holdings, Target Weights, Strategy Actions, and Sector Shifts</div>', unsafe_allow_html=True)
    st.markdown('<div class="badge-prediction">MODEL OUTPUT: 2017 AI PREDICTIONS</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="ai-desc">
        <strong>What is this section?</strong><br>
        This module displays the complete <strong>360-row AI Predicted Stock Holdings DataFrame</strong> for all 12 months of 2017. The machine learning algorithm extrapolates holding consistency, target weight momentum, and manager risk constraints to project the 2017 portfolio horizon.
    </div>
    """, unsafe_allow_html=True)

    col_fm, col_fs = st.columns(2)
    m_2017_list = list(holdings_2017_df['month'].unique())
    selected_2017_m = col_fm.selectbox("Filter 2017 Prediction Month", ["All 12 Months (Full DataFrame)"] + m_2017_list, index=0)

    if selected_2017_m == "All 12 Months (Full DataFrame)":
        display_2017_df = holdings_2017_df.copy()
    else:
        display_2017_df = holdings_2017_df[holdings_2017_df['month'] == selected_2017_m].copy()

    st.markdown(f"#### 📊 AI Forecasted Holdings DataFrame for 2017 ({len(display_2017_df)} Records)")

    st.dataframe(
        display_2017_df[[
            'month', 'report_date', 'category', 'instrument_name', 'industry_sector',
            'predicted_quantity', 'predicted_market_value_lakhs', 'predicted_pct_nav', 'ai_action_strategy'
        ]]
        .rename(columns={
            'month': 'Month', 'report_date': 'Date', 'category': 'Category',
            'instrument_name': 'Stock Name', 'industry_sector': 'Sector',
            'predicted_quantity': 'Predicted Quantity', 'predicted_market_value_lakhs': 'Predicted Value (Rs. Lakhs)',
            'predicted_pct_nav': 'Predicted % NAV', 'ai_action_strategy': 'AI Action Strategy'
        })
        .style.format({
            'Predicted Quantity': '{:,.0f}',
            'Predicted Value (Rs. Lakhs)': 'Rs. {:,.2f} L',
            'Predicted % NAV': '{:.2f}%'
        }),
        height=450,
        use_container_width=True
    )

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        csv_h2017 = holdings_2017_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Full 2017 Predicted Stock Holdings (CSV)",
            data=csv_h2017, file_name="all_portfolio_holdings_2017_prediction.csv", mime="text/csv"
        )
    with col_d2:
        if os.path.exists(excel_path):
            with open(excel_path, "rb") as f:
                st.download_button(
                    label="Download Formatted Master Excel (.xlsx)",
                    data=f, file_name="PPFAS_Portfolio_Intelligence_2016_2017_Master.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    st.markdown("---")

    # Macro Timeline Prediction
    st.subheader("Macro Performance Trajectory (2016 Actual vs 2017 AI Forecast)")
    active_summary = summary_df.dropna(subset=['aum_crores']).copy()

    c_aum_chart, c_nav_chart = st.columns(2)

    with c_aum_chart:
        fig_combined_aum = go.Figure()
        fig_combined_aum.add_trace(go.Scatter(
            x=active_summary['month'] + ' 2016', y=active_summary['aum_crores'],
            mode='lines+markers', name='2016 Actual AUM', line=dict(color='#58a6ff', width=3)
        ))
        fig_combined_aum.add_trace(go.Scatter(
            x=summary_2017_df['month'] + ' 2017', y=summary_2017_df['predicted_aum_crores'],
            mode='lines+markers', name='2017 AI Predicted AUM', line=dict(color='#bc8cff', width=3, dash='dash')
        ))
        fig_combined_aum.update_layout(template="plotly_dark", height=380, title="AUM: 2016 Actual vs 2017 AI Prediction", yaxis_title="AUM (Rs. Crores)")
        st.plotly_chart(fig_combined_aum, use_container_width=True)

    with c_nav_chart:
        fig_combined_nav = go.Figure()
        fig_combined_nav.add_trace(go.Scatter(
            x=active_summary['month'] + ' 2016', y=active_summary['direct_nav_end'],
            mode='lines+markers', name='2016 Actual Direct NAV', line=dict(color='#3fb950', width=3)
        ))
        fig_combined_nav.add_trace(go.Scatter(
            x=summary_2017_df['month'] + ' 2017', y=summary_2017_df['predicted_direct_nav'],
            mode='lines+markers', name='2017 AI Predicted Direct NAV', line=dict(color='#d2a8ff', width=3, dash='dash')
        ))
        fig_combined_nav.update_layout(template="plotly_dark", height=380, title="Direct NAV: 2016 Actual vs 2017 AI Prediction", yaxis_title="NAV (Rs.)")
        st.plotly_chart(fig_combined_nav, use_container_width=True)

# -------------------------------------------------------------
# MODULE 6: AUTOMATED COMMENTARY
# -------------------------------------------------------------
elif nav_choice == "Investor Commentary":
    st.markdown('<div class="main-title">Automated Monthly Investor Commentary</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Natural Language Generation (NLG) Report Synthesis</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-desc">
        <strong>What is this section?</strong><br>
        Select any reporting month from 2016 to automatically synthesize a professional monthly investor letter summarizing fund size, NAV changes, international asset allocation, risk hedging, and trading expenses.
    </div>
    """, unsafe_allow_html=True)

    valid_months = summary_df.dropna(subset=['aum_crores'])['month']
    chosen_month = st.selectbox("Select Target Month for Investor Update", valid_months)
    row_data = summary_df[summary_df['month'] == chosen_month].iloc[0]

    st.markdown('<div class="badge-actual">GENERATED REPORT BASED ON 2016 ACTUALS</div>', unsafe_allow_html=True)

    report_text = f"""
### PPFAS MUTUAL FUND - MONTHLY INVESTOR UPDATE ({chosen_month.upper()} 2016)

**Scheme**: Parag Parikh Long Term Value Fund  
**Reporting Date**: {row_data['report_date']}

**1. Fund Assets & Net Asset Value (NAV)**  
* **Assets Under Management (AUM)**: Closed at **Rs. {row_data['aum_crores']:.2f} Crores**.  
* **Direct Plan NAV**: Closed at **Rs. {row_data['direct_nav_end']:.4f}**.  
* **Regular Plan NAV**: Closed at **Rs. {row_data['regular_nav_end']:.4f}**.  

**2. Asset Allocation & International Exposure**  
* **Foreign Equity / ADR Exposure**: **{row_data['foreign_equity_pct']:.2f}%** of total NAV held in international equities (including Alphabet INC, Apple, UPS, IBM, and 3M).  
* **Risk Hedging Ratio**: **{row_data['hedged_pct']:.2f}%** of portfolio assets hedged via USD/INR currency futures and equity stock futures.  

**3. Trading Operations & Costs**  
* **Distributor Commission Paid**: Rs. {row_data['commission_paid_rs']:,.2f}  
* **Brokerage Fees Paid**: Rs. {row_data['brokerage_paid_rs']:,.2f}  
* **Portfolio Turnover Ratio (Excl. Arbitrage)**: {row_data['ptr_exc_arbitrage']*100:.2f}%  
"""
    st.info(report_text)
