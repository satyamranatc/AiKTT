import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Page Configuration - Clean Professional Setup
st.set_page_config(
    page_title="PPFAS Portfolio Analytics & AI Forecast",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Professional Clean Dark Theme - No Emojis)
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
        margin-bottom: 1.5rem;
    }
    .badge-actual {
        background-color: #1f6feb;
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .badge-prediction {
        background-color: #8957e5;
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #161b22;
        border-left: 4px solid #8957e5;
        padding: 14px 18px;
        border-radius: 4px;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Data Loader
DATA_DIR = os.path.join(os.path.dirname(__file__), 'cleaned_data')

@st.cache_data
def load_datasets():
    summary_df = pd.read_csv(os.path.join(DATA_DIR, 'monthly_fund_summary_2016.csv'))
    holdings_df = pd.read_csv(os.path.join(DATA_DIR, 'all_portfolio_holdings_2016.csv'))
    derivs_df = pd.read_csv(os.path.join(DATA_DIR, 'derivative_positions_2016.csv'))
    sectors_df = pd.read_csv(os.path.join(DATA_DIR, 'sector_breakdown_2016.csv'))
    
    # 2017 AI Prediction Datasets
    summary_2017_df = pd.read_csv(os.path.join(DATA_DIR, 'monthly_fund_summary_2017_prediction.csv'))
    holdings_2017_df = pd.read_csv(os.path.join(DATA_DIR, 'all_portfolio_holdings_2017_prediction.csv'))
    
    return summary_df, holdings_df, derivs_df, sectors_df, summary_2017_df, holdings_2017_df

try:
    summary_df, holdings_df, derivs_df, sectors_df, summary_2017_df, holdings_2017_df = load_datasets()
except Exception as e:
    st.error(f"Error loading required CSV dataset files: {e}")
    st.stop()

# Sidebar Navigation
st.sidebar.title("PPFAS Intelligence Platform")
st.sidebar.caption("Parag Parikh Long Term Value Fund Analysis")
st.sidebar.markdown("---")

nav_choice = st.sidebar.radio("Select View Module", [
    "Executive Overview (2016 Actuals)",
    "Holdings & Sector Allocations (2016 Actuals)",
    "Risk & Derivative Hedging (2016 Actuals)",
    "AI 2017 Stock & Portfolio Forecast (AI Machine Learning)",
    "Automated Investor Commentary"
])

excel_path = os.path.join(DATA_DIR, 'PPFAS_Portfolio_Intelligence_2016_2017_Master.xlsx')
if os.path.exists(excel_path):
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Master Excel Download")
    with open(excel_path, "rb") as f:
        st.sidebar.download_button(
            label="Download Master Formatted Excel (.xlsx)",
            data=f,
            file_name="PPFAS_Portfolio_Intelligence_2016_2017_Master.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# -------------------------------------------------------------
# MODULE 1: EXECUTIVE OVERVIEW (2016 ACTUALS)
# -------------------------------------------------------------
if nav_choice == "Executive Overview (2016 Actuals)":
    st.markdown('<div class="main-title">Executive Portfolio Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Historical Financial Performance and Metrics (Calendar Year 2016)</div>', unsafe_allow_html=True)
    st.markdown('<div class="badge-actual">DATA SOURCE: 2016 HISTORICAL ACTUALS</div>', unsafe_allow_html=True)

    active_summary = summary_df.dropna(subset=['aum_crores']).copy()
    latest_aum = active_summary['aum_crores'].iloc[-1]
    peak_nav = active_summary['direct_nav_end'].max()
    avg_foreign = active_summary['foreign_equity_pct'].mean()
    avg_hedged = active_summary['hedged_pct'].mean()

    # KPI Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Closing AUM (Dec 2016)", f"Rs. {latest_aum:.2f} Cr", delta="+7.6% YoY Growth")
    m2.metric("Peak Direct Plan NAV", f"Rs. {peak_nav:.4f}", delta="Oct 2016 High")
    m3.metric("Average Foreign Equity Exposure", f"{avg_foreign:.2f}% NAV", delta="US & Global ADRs")
    m4.metric("Average Hedged Assets Ratio", f"{avg_hedged:.2f}% NAV", delta="USD/INR & Equity Futures")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Assets Under Management Trend (2016 Actuals)")
        fig_aum = px.line(active_summary, x='month', y='aum_crores', markers=True,
                          labels={'aum_crores': 'AUM (Rs. Crores)', 'month': 'Month'},
                          color_discrete_sequence=['#2da44e'])
        fig_aum.update_layout(template="plotly_dark", height=380, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_aum, use_container_width=True)

    with col_right:
        st.subheader("Direct Plan vs Regular Plan NAV (2016 Actuals)")
        fig_nav = go.Figure()
        fig_nav.add_trace(go.Scatter(x=active_summary['month'], y=active_summary['direct_nav_end'],
                                     mode='lines+markers', name='Direct Plan NAV (Actual)', line=dict(color='#58a6ff', width=3)))
        fig_nav.add_trace(go.Scatter(x=active_summary['month'], y=active_summary['regular_nav_end'],
                                     mode='lines+markers', name='Regular Plan NAV (Actual)', line=dict(color='#8b949e', width=2, dash='dot')))
        fig_nav.update_layout(template="plotly_dark", height=380, yaxis_title="NAV (Rs.)", margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_nav, use_container_width=True)

# -------------------------------------------------------------
# MODULE 2: HOLDINGS & SECTORS (2016 ACTUALS)
# -------------------------------------------------------------
elif nav_choice == "Holdings & Sector Allocations (2016 Actuals)":
    st.markdown('<div class="main-title">Portfolio Holdings and Sector Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Detailed Stock Positions and Sector Distribution (2016 Actuals)</div>', unsafe_allow_html=True)
    st.markdown('<div class="badge-actual">DATA SOURCE: 2016 HISTORICAL ACTUALS</div>', unsafe_allow_html=True)

    col_m, col_c = st.columns(2)
    month_list = list(holdings_df['month'].unique())
    selected_month = col_m.selectbox("Select Portfolio Report Month", month_list, index=len(month_list)-1)

    cat_list = ["All Asset Categories"] + list(holdings_df['category'].unique())
    selected_category = col_c.selectbox("Filter Asset Category", cat_list)

    month_data = holdings_df[holdings_df['month'] == selected_month].copy()
    if selected_category != "All Asset Categories":
        month_data = month_data[month_data['category'] == selected_category]

    st.markdown(f"#### Portfolio Position Statement: **{selected_month} 2016** ({len(month_data)} Holdings)")

    c_table, c_chart = st.columns([3, 2])

    with c_table:
        st.dataframe(
            month_data[['sr_no', 'category', 'instrument_name', 'industry_sector', 'market_value_lakhs', 'pct_nav']]
            .sort_values(by='market_value_lakhs', ascending=False)
            .rename(columns={
                'sr_no': 'Sr No',
                'category': 'Category',
                'instrument_name': 'Stock / Instrument Name',
                'industry_sector': 'Industry Sector',
                'market_value_lakhs': 'Market Value (Rs. Lakhs)',
                'pct_nav': '% of NAV'
            })
            .style.format({'Market Value (Rs. Lakhs)': 'Rs. {:,.2f} L', '% of NAV': '{:.2f}%'}),
            height=460,
            use_container_width=True
        )

    with c_chart:
        st.subheader("Industry Sector Distribution")
        sector_agg = month_data.groupby('industry_sector')['market_value_lakhs'].sum().reset_index()
        fig_sector = px.pie(sector_agg, names='industry_sector', values='market_value_lakhs',
                            color_discrete_sequence=px.colors.qualitative.Safe)
        fig_sector.update_layout(template="plotly_dark", height=460, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_sector, use_container_width=True)

# -------------------------------------------------------------
# MODULE 3: RISK & DERIVATIVE HEDGING (2016 ACTUALS)
# -------------------------------------------------------------
elif nav_choice == "Risk & Derivative Hedging (2016 Actuals)":
    st.markdown('<div class="main-title">Risk Management and Hedging Operations</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Currency Futures Exposure and Portfolio Turnover Ratios (2016 Actuals)</div>', unsafe_allow_html=True)
    st.markdown('<div class="badge-actual">DATA SOURCE: 2016 HISTORICAL ACTUALS</div>', unsafe_allow_html=True)

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
# MODULE 4: AI 2017 STOCK & PORTFOLIO FORECAST (AI ML MODEL)
# -------------------------------------------------------------
elif nav_choice == "AI 2017 Stock & Portfolio Forecast (AI Machine Learning)":
    st.markdown('<div class="main-title">AI Predictive Portfolio & Stock Forecast (2017 DataFrame)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Machine Learning Model Predicting 2017 Stock Holdings, Target Weights, Action Strategies, and Sector Shifts</div>', unsafe_allow_html=True)
    st.markdown('<div class="badge-prediction">MODEL OUTPUT: 2017 AI PREDICTIONS</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <strong>2017 AI Prediction Datasets:</strong><br>
        This module displays the complete <strong>360-row AI Predicted Stock Holdings DataFrame</strong> for all 12 months of 2017, alongside manager strategy classifications and forecasted sector shifts.
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
            'month': 'Month',
            'report_date': 'Date',
            'category': 'Category',
            'instrument_name': 'Stock Name',
            'industry_sector': 'Sector',
            'predicted_quantity': 'Predicted Quantity',
            'predicted_market_value_lakhs': 'Predicted Value (Rs. Lakhs)',
            'predicted_pct_nav': 'Predicted % NAV',
            'ai_action_strategy': 'AI Action Strategy'
        })
        .style.format({
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
            data=csv_h2017,
            file_name="all_portfolio_holdings_2017_prediction.csv",
            mime="text/csv"
        )
    with col_d2:
        if os.path.exists(excel_path):
            with open(excel_path, "rb") as f:
                st.download_button(
                    label="Download Formatted Excel Workbook (.xlsx)",
                    data=f,
                    file_name="PPFAS_Portfolio_Intelligence_2016_2017_Master.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    st.markdown("---")

    # Macro Timeline Prediction (2016 Actual vs 2017 AI Prediction)
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
# MODULE 5: AUTOMATED COMMENTARY
# -------------------------------------------------------------
elif nav_choice == "Automated Investor Commentary":
    st.markdown('<div class="main-title">Automated Monthly Commentary Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Natural Language Generation (NLG) Report Synthesis</div>', unsafe_allow_html=True)

    valid_months = summary_df.dropna(subset=['aum_crores'])['month']
    chosen_month = st.selectbox("Select Target Month for Commentary", valid_months)
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
