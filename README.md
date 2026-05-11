# 📊 Task 1 — Business Sales Performance Analytics

**Dataset:** Online Retail (UK-based e-commerce | Dec 2010 – Dec 2011)**Tools:** Python · Pandas · Matplotlib · Seaborn  
**Author:** Data Analytics Internship Project

---

## 📋 Table of Contents
1. [Project Overview](#overview)
2. [Data Cleaning](#cleaning)
3. [Key Performance Indicators](#kpis)
4. [Monthly & Seasonal Trends](#trends)
5. [Product Analysis](#products)
6. [Regional Analysis](#regional)
7. [Customer Segmentation (RFM)](#rfm)
8. [Dashboard Suggestions](#dashboard)
9. [Recommendations](#recommendations)

---

## 1. Project Overview <a name="overview"></a>

This project performs an end-to-end Business Sales Performance Analysis on a real-world UK-based online retail dataset containing **541,909 transactions** across **38 countries**.

**Business Questions Answered:**
- Which products, regions, and customer segments drive the most revenue?
- How does sales performance vary by season and month?
- Which customers are at risk of disengagement?
- Where should the business focus its growth strategy?

---

## 2. Data Cleaning <a name="cleaning"></a>

| Step | Action | Result |
|------|--------|--------|
| Missing Values | `CustomerID` had 135,080 NULLs; `Description` had 1,454 | Dropped rows with NULL CustomerID/Description |
| Duplicates | 5,268 duplicate rows detected | Removed |
| Cancellations | Transactions starting with 'C' = returns/refunds | Filtered out |
| Invalid Data | Negative Quantity or zero UnitPrice | Filtered out |
| Date Parsing | `InvoiceDate` stored as string | Converted to `datetime` |
| Feature Engineering | Added `Revenue`, `Year`, `Month`, `YearMonth`, `Quarter` | New computed columns |
| Outliers | Top/bottom 1% revenue rows = 7,149 records | Flagged (not removed) |

**Final Clean Dataset: 392,692 rows × 14 columns**

---

## 3. Key Performance Indicators (KPIs) <a name="kpis"></a>

| KPI | Value |
|-----|-------|
| 💰 Total Revenue | **£8,887,209** |
| 📦 Total Orders | **18,532** |
| 👥 Unique Customers | **4,338** |
| 🛒 Avg Order Value | **£479.56** |
| 📫 Total Units Sold | **5,152,002** |

> **Key Insight:** The average order value of £479.56 reflects a high-volume, wholesale-style business model. Most customers are repeat buyers (B2B or resellers).

---

## 4. Monthly & Seasonal Trends <a name="trends"></a>

### Monthly Revenue Trend
- Revenue shows a clear **upward trajectory** from Jan 2011 through November 2011.
- **Peak month: November 2011** — driven by pre-Christmas wholesale stocking.
- December shows a sharp drop due to incomplete data (dataset ends Dec 9, 2011).

### Yearly Growth
| Year | Revenue |
|------|---------|
| 2010 | £748,957 (partial — only Dec) |
| 2011 | £8,138,252 |

> **Growth is exceptional** when accounting for the fact that 2010 only has one month of data.

### Seasonal Patterns
- **Q4 (Oct–Nov)** is the clear peak season — festival/holiday gifting demand surges.
- **Q1 (Jan–Feb)** represents the slowest period — post-holiday dip.
- **Q3 (Jul–Sep)** shows moderate recovery, likely summer/back-to-school demand.

---

## 5. Product Analysis <a name="products"></a>

### Top 5 Products by Revenue
| Product | Revenue | Qty Sold |
|---------|---------|----------|
| PAPER CRAFT, LITTLE BIRDIE | £168,470 | 80,995 |
| REGENCY CAKESTAND 3 TIER | £142,265 | 12,374 |
| WHITE HANGING HEART T-LIGHT HOLDER | £100,392 | 36,706 |
| JUMBO BAG RED RETROSPOT | £85,041 | 46,078 |
| MEDIUM CERAMIC TOP STORAGE JAR | £81,417 | 77,916 |

### High Revenue, Low Quantity Products
- **REGENCY CAKESTAND 3 TIER** — High revenue despite moderate volume → premium priced item.
- These products have strong margin potential and should be actively promoted.

### Least-Performing Products
- Products with < £10 total revenue are typically damaged, returned, or discontinued items.
- **Recommendation:** Run quarterly SKU rationalization to remove dead inventory.

---

## 6. Regional Analysis <a name="regional"></a>

### Revenue by Country
| Rank | Country | Revenue | Share |
|------|---------|---------|-------|
| 1 | 🇬🇧 United Kingdom | £7,285,025 | **81.97%** |
| 2 | 🇳🇱 Netherlands | £285,446 | 3.21% |
| 3 | 🇮🇪 EIRE (Ireland) | £265,262 | 2.98% |
| 4 | 🇩🇪 Germany | £228,678 | 2.57% |
| 5 | 🇫🇷 France | £208,934 | 2.35% |
| 6 | 🇦🇺 Australia | £138,454 | 1.56% |

> **Key Insight:** The UK dominates (82%) but international markets — especially the Netherlands and Germany — show strong growth potential. Australia delivers high revenue with only 57 orders, indicating very high average order values.

### Quarterly Heatmap Findings
- UK shows consistent growth every quarter.
- Netherlands and Germany peak in Q4.
- EIRE (Ireland) is the most consistent international market.

**Low-performing regions:** Spain, Sweden, Belgium — high potential but low penetration. Targeted marketing campaigns recommended.

---

## 7. Customer Segmentation — RFM Analysis <a name="rfm"></a>

RFM (Recency, Frequency, Monetary) segmentation was applied to 4,338 customers:

| Segment | Count | Revenue Contribution |
|---------|-------|---------------------|
| 🏆 Champions | 1,267 | **£6,827,236 (76.8%)** |
| 💚 Loyal | 845 | £1,051,600 (11.8%) |
| 🌱 Potential | 935 | £650,529 (7.3%) |
| ⚠️ At-Risk | 1,291 | £357,844 (4.0%) |

> **Critical Insight:** Champions (29% of customers) generate **77% of revenue**. Retaining these customers is the single highest-ROI business priority.

---

## 8. Dashboard Suggestions <a name="dashboard"></a>

| Visual | Type | Metric |
|--------|------|--------|
| KPI Cards | Card | Revenue, Orders, Customers, AOV |
| Revenue Trend | Line Chart | Monthly Revenue + YoY comparison |
| Seasonal Heatmap | Heatmap | Month × Year Revenue |
| Top Products | Horizontal Bar | Revenue & Quantity |
| Country Map | Choropleth | Revenue by Country |
| RFM Segments | Pie/Donut | Customer Segment Distribution |
| Frequency vs Spend | Scatter | Customer clustering |
| Bottom Products | Bar | Least performing SKUs |

---

## 9. Recommendations <a name="recommendations"></a>

### 🚀 Growth
1. **Launch an international expansion campaign** — Netherlands, Germany, and France show strong demand. Localize marketing for these markets.
2. **Bundle premium products** — Pair REGENCY CAKESTAND with complementary items to increase AOV.
3. **Invest in Q1 promotions** — Counter the post-holiday dip with January/February clearance events.

### 🔒 Retention
4. **Create a VIP loyalty program** for Champion customers — they drive 77% of revenue and must be prioritized.
5. **Re-engagement campaign for At-Risk customers** — 1,291 customers have not purchased recently. An email win-back sequence could recover significant revenue.

### 📦 Operations
6. **Quarterly SKU rationalization** — Remove bottom-performing products to reduce inventory costs.
7. **Seasonal stock planning** — Pre-build inventory for Q4 (Oct–Nov) based on historical demand spikes.

---

## 📁 Output Files

| File | Description |
|------|-------------|
| `outputs/01_kpi_cards.png` | KPI Dashboard Cards |
| `outputs/02_monthly_revenue_trend.png` | Monthly Revenue & Trend Line |
| `outputs/03_yearly_growth.png` | Year-over-Year Revenue Bar |
| `outputs/04_seasonality.png` | Monthly Seasonal Pattern |
| `outputs/05_product_analysis.png` | Top Products by Revenue & Qty |
| `outputs/06_bottom_products.png` | Least-Performing Products |
| `outputs/07_regional_analysis.png` | Country Revenue Bar + Donut |
| `outputs/08_country_heatmap.png` | Quarterly Heatmap (Top 5 Countries) |
| `outputs/09_rfm_segments.png` | RFM Segment Count & Revenue |
| `outputs/10_rfm_scatter.png` | Customer Frequency vs Spend Scatter |

---

*Report generated as part of a Data Science & Analytics Internship Project.*  
*Tools: Python 3.11 · Pandas · Matplotlib · Seaborn*
