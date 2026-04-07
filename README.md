# Module 3 — AI Replenishment & Safety Stock Coach

**Part of the Supply Chain AI Suite** | By Sebastián Rueda, Supply Chain AI Orchestrator

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://m3-replenishment-coach-public.streamlit.app)

---

## 🎯 The Problem

In Pharma and CPG companies, procurement teams face a constant challenge:

- **How much should we order RIGHT NOW?** (Too much = tied-up capital; too little = stockouts)
- **What safety stock do we really need?** (Against what demand/lead time variance?)
- **Which SKUs need immediate attention?** (Stock-out risk by category and ABC class)

Manual replenishment planning in Excel takes **days of analysis** and relies on guesswork. The result? **Stockouts losing revenue** or **excess inventory draining working capital**.

This tool translates Module 2's diagnosis into **actionable procurement strategies** — calculating optimal reorder points, safety stock buffers, and purchase quantities in **seconds**, with full 90-day execution simulation.

---

## 💡 The Solution

**Module 3** is an AI-powered replenishment coach that:

✅ Integrates **Module 2 diagnosis data** (stock levels, ABC classification, demand forecasts)
✅ Calculates **Reorder Point (ROP)** with configurable lead time + demand variance
✅ Computes **optimal Safety Stock** with manual padding controls
✅ Generates **Suggested Order Quantities** covering demand + protection buffer
✅ Simulates **90-day execution** showing stock trajectory and PO triggers
✅ Quantifies **purchasing capital requirements** for executive planning
✅ Provides **AI Coach recommendations** based on demand spikes and logistics delays
✅ Exports **Module 4 handoff data** (OTIF risk, vendor allocation)
✅ Generates **executive PDF reports** for supply chain QBRs

---

## 🚀 Live Demo

### **👉 [Launch the App](https://m3-replenishment-coach-public.streamlit.app)**

Try it now with **demo supply chain data** (Kellanova CPG portfolio) or **upload Module 2 diagnosis output**.

### What you'll see:

**📊 Dashboard KPIs**
- **Reorder Point (ROP):** Threshold stock level triggering purchase order
- **Safety Stock (Adjusted):** Buffer units protecting against demand spikes and logistics delays
- **Suggested Order Quantity (SOQ):** Total units to purchase today
- **Purchasing Capital Required:** Working capital allocation for this replenishment

**📉 Tab 1 — Execution Simulator**
- 90-day stock trajectory (sawtooth pattern showing consumption and receipts)
- ROP threshold line (red dashed)
- Safety stock buffer zone (yellow dotted)
- Inbound receipt arrivals (green bars)
- Interactive hover to see daily details

**📋 Tab 2 — Daily Simulation Audit**
- Full 90-day day-by-day breakdown
- Projected stock levels by day
- Purchase order triggers
- Inbound receipt arrivals
- CSV-ready for system import

**🤖 Tab 3 — AI Coach Recommendations**
- Strategic context: SKU importance, category, ABC class
- Execution alert: Stock-out risk with current parameters
- Decision support: Safety stock financial impact
- Actionable recommendations for approval to Module 4

---

## 📊 Key Metrics

| Metric | What It Means |
|--------|---------------|
| **Reorder Point (ROP)** | Stock threshold triggering purchase order = (Demand × LT) + Safety Stock |
| **Safety Stock** | Protective buffer units = Base × (1 + manual padding %) |
| **Suggested Order Qty (SOQ)** | Total units to purchase = ROP + (Demand × coverage days) - Current Stock |
| **Lead Time** | Days to receive order from vendor (configurable what-if) |
| **Demand Spike** | Simulated demand increase (%) for scenario planning |
| **Purchasing Capital** | Dollar amount required = SOQ × Unit Cost |
| **Days of Coverage** | How many days of demand the ROP provides protection for |

---

## 🏗 Architecture

```
Module 2 Output (Inventory Diagnosis)
    ↓
Data Enrichment (Daily Demand inference, Lead Time mapping)
    ├─ Category & ABC Classification filters
    ├─ SKU selection with demand history
    └─ What-If parameter adjustments (safety buffer, demand spike, LT delay)
    ↓
Replenishment Calculation Engine
    ├─ ROP Calculation: (Demand × LT) + Safety Stock
    ├─ Safety Stock: Base × (1 + padding %), where Base ≈ Demand × 0.8 × √(LT)
    ├─ SOQ Calculation: ROP + (Demand × 14 days) - Current Stock
    └─ Validation: Max(0, SOQ) to prevent negative orders
    ↓
90-Day Execution Simulator
    ├─ Daily stock physics (arrival + consumption)
    ├─ Pending receipt tracking (in-transit inventory)
    ├─ ROP-triggered purchase decisions
    └─ Inventory position visualization
    ↓
Streamlit Dashboard
    ├─ 4 KPI Cards (ROP, Safety Stock, SOQ, Capital)
    ├─ 3 Interactive Tabs (Simulator, Audit, Coach)
    ├─ Plotly visualization (90-day trajectory)
    └─ Export functions (Excel, PDF, Module 4 handoff)
    ↓
Outputs
    ├─ Replenishment Plan (Excel) → Procurement
    ├─ Module 4 Handoff (OTIF Risk data) → Procurement
    ├─ Executive Report (PDF) → QBR
    └─ Daily Audit (CSV) → SAP/ERP import
```

---

## 📥 Input Format

**Primary:** Upload Module 2 Diagnosis output (CSV or Excel)

Required columns:
| Column | Type | Example |
|--------|------|---------|
| `SKU` | String | "SKU-7721" |
| `Product_Name` | String | "Crispy Bites 500g" |
| `Category` | String | "Snacks" |
| `ABC_Classification` | String | "A" |
| `Unit_Price` | Float | 4.50 |
| `Cost_Price` | Float | 2.80 |
| `Current_Stock` | Integer | 1200 |
| `Lead_Time_Days` | Integer | 10 |
| `Forecasted_Demand_30d` | Integer | 2550 |

**Optional columns** (auto-generated if missing):
- `Daily_Demand` (calculated from 30-day forecast)

**Sidebar filters:**
- Category (multiselect)
- ABC Classification (multiselect)
- Target SKU (single select)

**What-If parameters:**
- Safety Buffer Padding: 0-100% (default: 25%)
- Demand Spike: 0-100% (default: 0%)
- Lead Time Delay: 0-20 days (default: 0 days)

If no file is uploaded, the app runs with **demo Kellanova CPG data** (5 SKUs across Snacks, Beauty, Electronics, Accessories, Pharma).

---

## 💻 Tech Stack

- **Frontend:** Streamlit (Python web framework)
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly (interactive charts)
- **Reporting:** fpdf2 (PDF generation), ExcelWriter (Excel export)
- **Simulation Engine:** Custom Python logic (ROP/Safety Stock algorithms)
- **Deployment:** Streamlit Community Cloud
- **Styling:** Custom CSS (Glassmorphism UI, dark header gradient)

---

## 🔄 Part of the Supply Chain AI Suite

| Module | Tool | Status | Link |
|--------|------|--------|------|
| **M1** | Demand Planning — AI Forecast Comparator | ✅ **LIVE** | [Demo](https://m1-demand-forecast-public-fyjvowtsbgsa6yfovy82xk.streamlit.app) |
| **M2** | Inventory Diagnosis & Coverage Analyzer | ✅ **LIVE** | [Demo](https://m2-inventory-diagnosis-public-emthenygqlck7srnw4dejt.streamlit.app) |
| **M3** | Replenishment Coach — Safety Stock Calculator | ✅ **THIS** | [Demo](https://m3-replenishment-coach-public.streamlit.app) |
| **M4** | Procurement — OTIF Risk Tracker | 🔄 In Dev | — |
| **M5** | Control Tower 360 — Executive Dashboard | 🔄 In Dev | — |

Module flow: **M1 → M2 → M3 → M4 → M5**

---

## 👤 About

**Sebastián Rueda** — Supply Chain AI Orchestrator

- 7+ years in **Pharma** (Novartis Colombia) and **CPG** (Kellanova)
- Pioneered **Kinaxis Maestro** implementation in Colombia
- Expert in: Demand Planning, Inventory Optimization, Supply Chain Analytics, AI/ML for SCM

**Connect:**
- [LinkedIn](https://www.linkedin.com/in/sebastiaan-rueda)
- [GitHub](https://github.com/SebsRu)

---

## 📜 License

Code available under **NDA** for commercial use. Contact for licensing.

---

## 🎓 Learn More

**Want to understand the replenishment math?**

**Reorder Point (ROP)**
- Formula: `ROP = (Daily Demand × Lead Time Days) + Safety Stock`
- Decision rule: When `(Physical Stock + In-Transit) ≤ ROP`, trigger purchase order
- Example: If daily demand = 85 units, LT = 10 days, SS = 100 units → ROP = 950 units

**Safety Stock Calculation**
- Base formula: `SS_base = Daily Demand × 0.8 × √(Lead Time)`
- Adjusted: `SS = SS_base × (1 + manual padding %)`
- Protects against: demand variance and lead time variability
- Example: If daily demand = 85, LT = 10 days, padding = 25% → SS ≈ 214 units

**Suggested Order Quantity (SOQ)**
- Formula: `SOQ = ROP + (Demand × 14 days coverage) - Current Stock`
- Covers: 1) replenishing to ROP + 2) two additional weeks of demand
- Constraint: `max(0, SOQ)` to prevent negative orders
- Example: ROP = 950, Demand × 14 = 1190, Current = 1200 → SOQ = 940 units

**Lead Time Variance**
- Longer LT → higher ROP (more protection needed)
- What-If: Add delay days to simulate supplier risk scenarios
- Example: 5-day delay increases effective LT from 10 → 15 days

**Working Capital Impact**
- Formula: `Capital Required = SOQ × Unit Cost Price`
- Decision point: Executive approval threshold for procurement authorization
- Example: 940 units × $2.80 cost = $2,632 capital allocation

---

**Ready to optimize your replenishment strategy?** 👉 [Launch the App](https://m3-replenishment-coach-public.streamlit.app)
