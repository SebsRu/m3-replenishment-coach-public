import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io
import os
import textwrap
from fpdf import FPDF

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Replenishment & Safety Stock Coach | Module 3",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# PREMIUM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #f8f9fa;
}

/* ── Header ── */
.mod-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 8px 32px rgba(15,52,96,0.25);
}
.mod-badge {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 8px;
    padding: 6px 14px;
    color: #a8d8f0;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.mod-title {
    color: #ffffff;
    font-size: 1.9rem;
    font-weight: 800;
    margin: 8px 0 4px 0;
    line-height: 1.2;
}
.mod-subtitle {
    color: #8bb8d4;
    font-size: 0.92rem;
    font-weight: 400;
}
.mod-tag {
    background: rgba(99,179,237,0.15);
    border: 1px solid rgba(99,179,237,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    color: #63b3ed;
    font-size: 0.75rem;
    font-weight: 500;
    margin-top: 10px;
    display: inline-block;
}

/* ── KPI Cards ── */
.kpi-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 22px 20px 18px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #e9ecef;
    border-top: 4px solid #0f3460;
    height: 100%;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.10); }
.kpi-card.blue { border-top-color: #3182ce; }
.kpi-card.gold { border-top-color: #d69e2e; }
.kpi-card.red  { border-top-color: #e53e3e; }
.kpi-card.green{ border-top-color: #38a169; }

.kpi-label { font-size: 0.75rem; font-weight: 600; color: #718096; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; }
.kpi-value { font-size: 1.8rem; font-weight: 800; color: #1a202c; line-height: 1; margin-bottom: 6px; }
.kpi-delta { font-size: 0.78rem; font-weight: 500; padding: 3px 8px; border-radius: 12px; display: inline-block; }
.kpi-delta.blue { background: #ebf8ff; color: #2b6cb0; }
.kpi-delta.red  { background: #fff5f5; color: #e53e3e; }
.kpi-delta.gold { background: #fffff0; color: #b7791f; }
.kpi-delta.green{ background: #f0fff4; color: #38a169; }

/* ── AI Coach Card ── */
.ai-coach-card {
    background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
    border-radius: 14px;
    padding: 28px 32px;
    margin: 24px 0;
    box-shadow: 0 8px 24px rgba(15,52,96,0.2);
}
.ai-coach-title { color: #ffffff; font-size: 1.05rem; font-weight: 700; margin-bottom: 18px; display: flex; align-items: center; gap: 8px; }
.ai-rec {
    background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12);
    border-left: 3px solid #63b3ed; border-radius: 8px;
    padding: 14px 16px; margin-bottom: 10px; color: #e2e8f0; font-size: 0.88rem; line-height: 1.55;
}
.ai-rec strong { color: #90cdf4; }
.ai-rec.gold-border { border-left-color: #f6e05e; }
.ai-rec.red-border  { border-left-color: #fc8181; }

/* ── Sidebar ── */
[data-testid="stSidebar"] { background: #1a1a2e !important; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1) !important; }
[data-testid="stSidebar"] .stSlider label, [data-testid="stSidebar"] .stSelectbox label {
    color: #a0aec0 !important; font-size: 0.82rem !important; text-transform: uppercase; letter-spacing: 0.5px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { background: #ffffff; border-radius: 12px; padding: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.stTabs [aria-selected="true"] { background: #0f3460 !important; color: white !important; border-radius: 8px; }

/* ── Section Headers ── */
.section-header { font-size: 1.1rem; font-weight: 700; color: #1a202c; border-left: 4px solid #0f3460; padding-left: 12px; margin: 28px 0 18px 0; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE INITIALIZATION ──
if 'mod3_sim_results' not in st.session_state:
    st.session_state.mod3_sim_results = None

# ─────────────────────────────────────────────
# DATA LOGIC & ENRICHMENT
# ─────────────────────────────────────────────
@st.cache_data
def load_default_data():
    return pd.DataFrame({
        "SKU": ["SKU-7721", "SKU-8842", "SKU-1120", "SKU-4409", "SKU-9951"],
        "Product_Name": ["Crispy Bites 500g", "Premium SkinCare Pro", "Switch-V3 Console", "Wrist-Strap Sport", "Cold Relief Pharma"],
        "Category": ["Snacks", "Beauty", "Electronics", "Accessories", "Pharma"],
        "ABC_Classification": ["A", "B", "A", "C", "B"],
        "Unit_Price": [4.50, 32.00, 299.00, 15.20, 9.80],
        "Cost_Price": [2.80, 21.00, 185.00, 8.40, 5.20],
        "Current_Stock": [1200, 450, 180, 620, 290],
        "Lead_Time_Days": [10, 7, 14, 5, 8],
        "Daily_Demand": [85, 35, 12, 30, 20]
    })

def run_simulation(row, ss_padding, spike_pct, delay_days, horizon=90):
    # Core variables with What-If adjustments
    eff_demand = row['Daily_Demand'] * (1 + spike_pct/100)
    eff_lt = row['Lead_Time_Days'] + delay_days
    
    # Calculate ROP & Safety Stock (Standard Heuristic)
    # ROP = (Demand * LT) + SS
    base_ss = int(eff_demand * 0.8 * (eff_lt**0.5))
    adj_ss = int(base_ss * (1 + ss_padding/100))
    rop = int((eff_demand * eff_lt) + adj_ss)
    
    # Suggested Order Quantity (Net Requirement to cover 21 days + LT)
    soq_today = int(rop + (eff_demand * 14) - row['Current_Stock'])
    soq_today = max(0, soq_today)
    
    # 90-Day Pipeline Simulation
    dates = pd.date_range(start=datetime.now(), periods=horizon)
    stock_levels = []
    po_triggers = []
    arrivals = []
    curr_physics = row['Current_Stock']
    pending_receipts = {}
    
    for i in range(horizon):
        # 1. Check Receipts
        if i in pending_receipts:
            curr_physics += pending_receipts[i]
            arrivals.append(pending_receipts[i])
        else:
            arrivals.append(0)
            
        # 2. Consumption
        curr_physics -= eff_demand
        curr_physics = max(0, curr_physics)
        stock_levels.append(curr_physics)
        
        # 3. Decision Logic (ROP)
        in_transit = sum(q for d, q in pending_receipts.items() if d > i)
        inv_pos = curr_physics + in_transit
        
        if inv_pos <= rop:
            po_qty = soq_today if (i == 0 and soq_today > 0) else int(rop + (eff_demand * 14))
            po_triggers.append(po_qty)
            pending_receipts[i + eff_lt] = po_qty
        else:
            po_triggers.append(0)
            
    return {
        "dates": dates, "stock": stock_levels, "receipts": arrivals, "pos": po_triggers,
        "rop": rop, "ss": adj_ss, "soq": soq_today, "eff_demand": eff_demand, "eff_lt": eff_lt
    }

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 18px 0 10px 0; text-align:center;'>
        <div style='font-size:2rem;'>🚀</div>
        <div style='color:#ffffff;font-weight:700;font-size:1.05rem;margin-top:6px;'>Module 3</div>
        <div style='color:#8bb8d4;font-size:0.75rem;'>AI Replenishment Coach</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("<div style='color:#a0aec0;font-size:0.78rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;'>📥 Data Connectivity</div>", unsafe_allow_html=True)
    st.info("Connected to Module 2 Diagnosis ✅")
    
    upload = st.file_uploader("Upload Module 2 Diagnosis (CSV/XLSX)", type=["csv", "xlsx"])
    if upload:
        try:
            if upload.name.endswith(".csv"): df_raw = pd.read_csv(upload)
            else: df_raw = pd.read_excel(upload)
            st.success("Module 2 Data Loaded ✅")
            
            # Critical Mapping for Simulation
            if "Forecasted_Demand_30d" in df_raw.columns:
                df_raw["Daily_Demand"] = df_raw["Forecasted_Demand_30d"] / 30
            elif "Daily_Demand" not in df_raw.columns:
                df_raw["Daily_Demand"] = 50
        except: 
            df_raw = load_default_data()
    else: 
        df_raw = load_default_data()

    # Re-verify and fulfill standard columns
    standard_cols = ["SKU", "Product_Name", "Category", "ABC_Classification", "Unit_Price", "Current_Stock", "Forecasted_Demand_30d"]
    for c in standard_cols:
        if c not in df_raw.columns:
            if c == "Forecasted_Demand_30d":
                df_raw[c] = (df_raw["Daily_Demand"] * 30).astype(int)
            else:
                df_raw[c] = load_default_data()[c] if c in load_default_data().columns else "N/A"

    st.divider()
    st.markdown("<div style='color:#a0aec0;font-size:0.78rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;'>🔍 Portfolio Filtering</div>", unsafe_allow_html=True)
    
    cat_list = sorted(df_raw['Category'].unique().tolist())
    sel_cats = st.multiselect("Filter by Category:", cat_list, default=cat_list)
    
    abc_list = sorted(df_raw['ABC_Classification'].unique().tolist())
    sel_abc = st.multiselect("Filter by ABC Class:", abc_list, default=abc_list)
    
    # Filter the SKU list dynamically
    df_filtered = df_raw[(df_raw['Category'].isin(sel_cats)) & (df_raw['ABC_Classification'].isin(sel_abc))]
    sku_list = sorted(df_filtered['Product_Name'].unique().tolist())
    
    if not sku_list:
        st.warning("No SKUs match your filters.")
        st.stop()
        
    sel_sku = st.selectbox("Select Target SKU to Plan:", sku_list)
    sku_row = df_filtered[df_filtered['Product_Name'] == sel_sku].iloc[0]

    st.divider()
    st.markdown("<div style='color:#a0aec0;font-size:0.78rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;'>🎯 Simulation Overrides</div>", unsafe_allow_html=True)
    ss_pad = st.slider("Extra Safety Buffer (%)", 0, 100, 25)
    d_spike = st.slider("Demand Spike (%)", 0, 100, 0)
    lt_delay = st.slider("Lead Time Delay (Days)", 0, 20, 0)
    
    st.divider()
    if st.button("🚀 Regenerate Purchase Plan", use_container_width=True, type="primary"):
        st.session_state.mod3_sim_results = run_simulation(sku_row, ss_pad, d_spike, lt_delay)
        st.success("Plan Regenerated!")

    st.markdown("""
    <div style='margin-top:10px; padding:12px; background:rgba(255,255,255,0.05); border-radius:10px; border:1px solid rgba(255,255,255,0.1);'>
        <div style='color:#63b3ed;font-size:0.72rem;font-weight:600;'>🔗 Suite Navigation</div>
        <div style='color:#718096;font-size:0.7rem;margin-top:4px;'>Mod 1 → Mod 2 → <b>Mod 3</b> → Mod 4</div>
    </div>
    """, unsafe_allow_html=True)

# Generate default sim if empty
if st.session_state.mod3_sim_results is None:
    st.session_state.mod3_sim_results = run_simulation(sku_row, ss_pad, d_spike, lt_delay)

sim = st.session_state.mod3_sim_results
cap_req = sim['soq'] * sku_row.get('Cost_Price', (sku_row['Unit_Price']*0.6))
forecast_30d = int(sim['eff_demand'] * 30)

# ── HEADER ──
st.markdown("""
<div class="mod-header">
    <div>
        <div class="mod-badge">MODULE 3 · REPLENISHMENT COACH</div>
        <div class="mod-title">🚀 AI Replenishment & Safety Stock Coach</div>
        <div class="mod-subtitle">Translating inventory diagnosis into actionable procurement and capital allocation strategies</div>
        <span class="mod-tag">⚡ Connected to Module 2 Diagnosis</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI GRID ──
c1, c2, c3, c4 = st.columns(4)
def kpi_html(label, value, delta, d_class, c_class="neutral"):
    return f"""<div class="kpi-card {c_class}"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><span class="kpi-delta {d_class}">{delta}</span></div>"""

with c1: st.markdown(kpi_html("Reorder Point (ROP)", f"{sim['rop']} units", f"Threshold: {sim['eff_lt']}d LT", "blue", "blue"), unsafe_allow_html=True)
with c2: st.markdown(kpi_html("Safety Stock (Adj)", f"{sim['ss']} units", f"+{ss_pad}% Manual Padding", "gold", "gold"), unsafe_allow_html=True)
with c3: st.markdown(kpi_html("Order Suggested (SOQ)", f"{sim['soq']} units", "Total today", "green", "green"), unsafe_allow_html=True)
with c4: st.markdown(kpi_html("Purchasing Capital", f"${cap_req:,.0f}", f"Forecast: {forecast_30d} units", "red", "red"), unsafe_allow_html=True)

st.divider()

t1, t2, t3 = st.tabs(["📉 Execution Simulator", "📋 Daily Simulation Audit", "🤖 AI Coach Recommendations"])

with t1:
    st.markdown('<div class="section-header">📈 Execution Simulator — Logistic Sawtooth Pattern</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sim['dates'], y=sim['stock'], name='Physical Stock', line=dict(color='#2b6cb0', width=4), fill='tozeroy', fillcolor='rgba(43, 108, 176, 0.1)'))
    fig.add_trace(go.Scatter(x=sim['dates'], y=[sim['rop']]*90, name='Reorder Point (ROP)', line=dict(color='#e53e3e', dash='dash')))
    fig.add_trace(go.Scatter(x=sim['dates'], y=[sim['ss']]*90, name='Safety Stock Buffer', line=dict(color='#d69e2e', dash='dot')))
    fig.add_trace(go.Bar(x=sim['dates'], y=sim['receipts'], name='Inbound Receipts', marker_color='#38a169'))
    fig.update_layout(height=480, template="plotly_white", hovermode="x unified", legend=dict(orientation="h", y=1.1, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)

with t2:
    st.markdown('<div class="section-header">📋 Daily Simulation Audit Hub — Full Lifecycle Detail</div>', unsafe_allow_html=True)
    audit_df = pd.DataFrame({
        "Day": range(1, 91),
        "Date": sim['dates'].strftime('%Y-%m-%d'),
        "SKU": sku_row['SKU'],
        "Category": sku_row['Category'],
        "ABC": sku_row['ABC_Classification'],
        "Unit_Price": sku_row['Unit_Price'],
        "Projected_Stock": sim['stock'],
        "PO_Triggered": sim['pos'],
        "Receipt_Arrival": sim['receipts']
    })
    st.dataframe(audit_df.style.format({"Unit_Price": "${:,.2f}", "Projected_Stock": "{:,.0f}", "PO_Triggered": "{:,.0f}", "Receipt_Arrival": "{:,.0f}"}), use_container_width=True, hide_index=True)

with t3:
    st.markdown(textwrap.dedent(f"""
    <div class="ai-coach-card">
        <div class="ai-coach-title">🤖 AI Strategy Coach - Replenishment Alert</div>
        <div class="ai-rec gold-border">
            <strong>🏆 Strategic Context:</strong> SKU <strong>{sel_sku}</strong> is a high-priority <strong>Class {sku_row['ABC_Classification']}</strong> product in <strong>{sku_row['Category']}</strong>. At <strong>${sku_row['Unit_Price']:.2f}</strong>/unit, every stock-out event generates significant revenue leakage.
        </div>
        <div class="ai-rec red-border">
            <strong>🚨 Execution Alert:</strong> Given a {d_spike}% demand spike and {lt_delay}d LT delay, physical stock falls below ROP on <strong>Day 1</strong>. Immediate purchase of <strong>{sim['soq']} units</strong> is required to protect week 1 deliveries.
        </div>
        <div class="ai-rec">
            <strong>💡 Decision Support:</strong> Your <strong>{ss_pad}%</strong> safety buffer protects <strong>${(sim['ss']*sku_row['Unit_Price']):,.0f}</strong>. Recommendation: Approve current PO to Module 4 for immediate vendor allocation.
        </div>
    </div>
    """), unsafe_allow_html=True)

# ─────────────────────────────────────────────
# EXPORT & INTEGRATION ACTIONS
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">📤 Professional Exports & Suite Integration</div>', unsafe_allow_html=True)
c_ex1, c_ex2, c_ex3 = st.columns(3)

# Build Comprehensive Export Data
full_export_df = pd.DataFrame([{
    "SKU": sku_row['SKU'],
    "Product_Name": sel_sku,
    "Category": sku_row['Category'], 
    "ABC_Classification": sku_row['ABC_Classification'],
    "Unit_Price": sku_row['Unit_Price'],
    "Current_Stock": sku_row['Current_Stock'],
    "Forecasted_Demand_30d": forecast_30d,
    "Reorder_Point": sim['rop'],
    "Safety_Stock_Adjusted": sim['ss'],
    "Suggested_Order_Qty": sim['soq'],
    "Plan_Date": datetime.now().strftime("%Y-%m-%d"),
    "Module": "Module 3 — AI Replenishment Coach"
}])

with c_ex1:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        full_export_df.to_excel(writer, index=False, sheet_name='Replenishment_Plan')
    st.download_button(
        label="📥 Export Plan (Excel)",
        data=buffer.getvalue(),
        file_name="Mod3_Replenish_Plan.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        key="mod3_main_excel"
    )

with c_ex2:
    mod4_export = full_export_df.copy()
    mod4_export['OTIF_Threshold'] = 0.95
    mod4_export['Vendor_Status'] = "Pending Allocation"
    buffer4 = io.BytesIO()
    with pd.ExcelWriter(buffer4, engine='xlsxwriter') as writer:
        mod4_export.to_excel(writer, index=False, sheet_name='Mod4_Handoff')
    st.download_button(
        label="🚚 Send to Mod 4",
        data=buffer4.getvalue(),
        file_name="Mod4_Handoff_Data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        key="mod3_m4_handoff"
    )

with c_ex3:
    def build_pdf():
        pdf = FPDF()
        pdf.add_page(); pdf.set_fill_color(26, 26, 46); pdf.rect(0, 0, 210, 35, 'F')
        pdf.set_font("Helvetica", "B", 16); pdf.set_text_color(255, 255, 255)
        pdf.set_xy(10, 8); pdf.cell(0, 10, "AI Replenishment Strategy Report", ln=True)
        pdf.set_font("Helvetica", "", 10); pdf.set_text_color(160, 160, 160)
        pdf.cell(0, 8, f"SKU: {sel_sku} | Category: {sku_row['Category']} | ABC: {sku_row['ABC_Classification']}", ln=True)
        
        pdf.ln(15); pdf.set_text_color(0,0,0); pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "1. Executive Planning Parameters", ln=True)
        pdf.set_font("Helvetica", "", 10)
        items = [("Current Stock", sku_row['Current_Stock']), ("30d Forecast", forecast_30d), ("Reorder Point", sim['rop']), ("Safety Stock (Adj)", sim['ss']), ("Suggested Order", sim['soq']), ("Capital Required", f"${cap_req:,.2f}")]
        for k, v in items:
            pdf.cell(60, 7, k, border=0); pdf.cell(0, 7, f": {v}", ln=True)
            
        pdf.ln(10); pdf.set_font("Helvetica", "B", 12); pdf.cell(0, 10, "2. Strategic AI Coach Recommendation", ln=True)
        pdf.set_font("Helvetica", "I", 9); pdf.multi_cell(0, 6, f"SKU {sel_sku} is a high-impact item in {sku_row['Category']}. We recommend immediate ordering of {sim['soq']} units to cover current demand spikes and logistics delays while maintaining a service level protection value of ${sim['ss']*sku_row['Unit_Price']:,.0f}.")
        
        pdf.ln(10); pdf.set_text_color(150, 150, 150); pdf.set_font("Helvetica", "I", 8); pdf.cell(0, 10, "Supply Chain AI Suite | Module 3 | Enterprise Edition", align="C")
        out = pdf.output(dest='S')
        return bytes(out) if not isinstance(out, str) else out.encode('latin1')

    try:
        st.download_button(
            label="📄 Generate Report (PDF)",
            data=build_pdf(),
            file_name="Strateg_Report_Mod3.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="mod3_pdf_report"
        )
    except Exception as e: st.error(f"PDF Error: {e}")

st.markdown("---")
st.markdown(f"<div style='text-align:center; color:#718096; font-size:0.75rem;'>🚀 <b>Module 3: AI Replenishment Coach</b> · v2.2 · Kellanova Project · Current SKU: {sku_row['SKU']}</div>", unsafe_allow_html=True)
