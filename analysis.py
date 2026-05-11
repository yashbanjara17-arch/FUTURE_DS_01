"""
Task 1 — Business Sales Performance Analytics
Dataset: Online Retail (online_retail.csv)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')
np.random.seed(42)

# ── Style ────────────────────────────────────────────────────
sns.set_theme(style="whitegrid")
PALETTE = {
    "primary":   "#2D6A9F",
    "secondary": "#1ABC9C",
    "accent":    "#E74C3C",
    "gold":      "#F39C12",
    "purple":    "#8E44AD",
    "bg":        "#F8F9FA",
    "text":      "#2C3E50",
}
# Paths are relative to Task_01/ directory (notebook's own folder)
DATA_FILE = "online_retail.csv"
OUT = "outputs"
os.makedirs(OUT, exist_ok=True)

# ════════════════════════════════════════════════════════════
# 1. DATA LOADING & CLEANING
# ════════════════════════════════════════════════════════════
print("=" * 60)
print("1. DATA LOADING & CLEANING")
print("=" * 60)

df_raw = pd.read_csv(DATA_FILE, encoding="ISO-8859-1")
print(f"\nRaw shape: {df_raw.shape}")
print(f"\nMissing values:\n{df_raw.isnull().sum()}")
print(f"\nDuplicates: {df_raw.duplicated().sum()}")

# Clean
df = df_raw.copy()
df.drop_duplicates(inplace=True)
df.dropna(subset=["CustomerID", "Description"], inplace=True)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
# Remove cancellations (InvoiceNo starting with 'C') and invalid prices/quantities
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
df["Revenue"] = (df["Quantity"] * df["UnitPrice"]).round(2)
df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month
df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")
df["MonthName"] = df["InvoiceDate"].dt.strftime("%b")
df["Quarter"] = df["InvoiceDate"].dt.to_period("Q")

# Outlier detection
q1 = df["Revenue"].quantile(0.01)
q99 = df["Revenue"].quantile(0.99)
outliers = df[(df["Revenue"] < q1) | (df["Revenue"] > q99)]
print(f"\nCleaned shape: {df.shape}")
print(f"Outliers (top/bottom 1%): {len(outliers)}")
print(f"\nDate range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")

# ════════════════════════════════════════════════════════════
# 2. EDA — KPIs
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("2. KEY PERFORMANCE INDICATORS (EDA)")
print("=" * 60)

total_revenue  = df["Revenue"].sum()
total_orders   = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()
avg_order_value = total_revenue / total_orders
total_units    = df["Quantity"].sum()

print(f"  Total Revenue    : £{total_revenue:,.2f}")
print(f"  Total Orders     : {total_orders:,}")
print(f"  Total Customers  : {total_customers:,}")
print(f"  Avg Order Value  : £{avg_order_value:,.2f}")
print(f"  Total Units Sold : {total_units:,}")

# ── KPI Figure ───────────────────────────────────────────────
fig, axes = plt.subplots(1, 5, figsize=(18, 3.5))
fig.patch.set_facecolor("white")
kpis = [
    ("£{:,.0f}".format(total_revenue),  "Total Revenue",    PALETTE["primary"]),
    ("{:,}".format(total_orders),         "Total Orders",     PALETTE["secondary"]),
    ("{:,}".format(total_customers),      "Unique Customers", PALETTE["gold"]),
    ("£{:,.2f}".format(avg_order_value),  "Avg Order Value",  PALETTE["purple"]),
    ("{:,}".format(total_units),          "Units Sold",       PALETTE["accent"]),
]
for ax, (val, lbl, col) in zip(axes, kpis):
    ax.set_facecolor(col)
    ax.text(0.5, 0.6, val, ha="center", va="center", fontsize=17, fontweight="bold",
            color="white", transform=ax.transAxes)
    ax.text(0.5, 0.25, lbl, ha="center", va="center", fontsize=10,
            color="white", alpha=0.9, transform=ax.transAxes)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
plt.suptitle("Business Sales KPI Dashboard", fontsize=14, fontweight="bold",
             color=PALETTE["text"], y=1.02)
plt.tight_layout()
plt.savefig(f"{OUT}/01_kpi_cards.png", dpi=150, bbox_inches="tight")
plt.close()
print("  Saved: 01_kpi_cards.png")

# ── Monthly Revenue Trend ─────────────────────────────────────
monthly = df.groupby("YearMonth")["Revenue"].sum().reset_index()
monthly["YearMonth_str"] = monthly["YearMonth"].astype(str)

fig, ax = plt.subplots(figsize=(14, 5))
ax.fill_between(range(len(monthly)), monthly["Revenue"] / 1e3,
                alpha=0.18, color=PALETTE["primary"])
ax.plot(range(len(monthly)), monthly["Revenue"] / 1e3,
        color=PALETTE["primary"], lw=2.5, marker="o", ms=5)
ax.set_xticks(range(len(monthly)))
ax.set_xticklabels(monthly["YearMonth_str"], rotation=45, ha="right", fontsize=9)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:.0f}K"))
ax.set_title("Monthly Revenue Trend", fontsize=14, fontweight="bold", color=PALETTE["text"])
ax.set_ylabel("Revenue (£K)"); ax.set_xlabel("")
ax.set_facecolor(PALETTE["bg"]); fig.patch.set_facecolor("white")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(f"{OUT}/02_monthly_revenue_trend.png", dpi=150, bbox_inches="tight")
plt.close()
print("  Saved: 02_monthly_revenue_trend.png")

# ── Yearly Growth ─────────────────────────────────────────────
yearly = df.groupby("Year")["Revenue"].sum()
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(yearly.index.astype(str), yearly.values / 1e3,
              color=[PALETTE["primary"], PALETTE["secondary"]], edgecolor="white", width=0.5)
for bar, val in zip(bars, yearly.values / 1e3):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f"£{val:.0f}K", ha="center", fontsize=11, fontweight="bold")
ax.set_title("Yearly Revenue Growth", fontsize=13, fontweight="bold", color=PALETTE["text"])
ax.set_ylabel("Revenue (£K)"); ax.set_facecolor(PALETTE["bg"])
ax.spines[["top", "right"]].set_visible(False); fig.patch.set_facecolor("white")
plt.tight_layout()
plt.savefig(f"{OUT}/03_yearly_growth.png", dpi=150, bbox_inches="tight")
plt.close()
print("  Saved: 03_yearly_growth.png")

# ── Monthly Seasonality ────────────────────────────────────────
season = df.groupby("Month")["Revenue"].sum()
month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
fig, ax = plt.subplots(figsize=(12, 4.5))
clrs = [PALETTE["accent"] if v == season.max() else PALETTE["primary"] for v in season.values]
ax.bar(month_names[:len(season)], season.values / 1e3, color=clrs, edgecolor="white", width=0.65)
ax.set_title("Seasonal Sales Pattern (Monthly)", fontsize=13, fontweight="bold", color=PALETTE["text"])
ax.set_ylabel("Revenue (£K)"); ax.set_facecolor(PALETTE["bg"])
ax.spines[["top", "right"]].set_visible(False); fig.patch.set_facecolor("white")
plt.tight_layout()
plt.savefig(f"{OUT}/04_seasonality.png", dpi=150, bbox_inches="tight")
plt.close()
print("  Saved: 04_seasonality.png")

# ════════════════════════════════════════════════════════════
# 3. PRODUCT ANALYSIS
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("3. PRODUCT ANALYSIS")
print("=" * 60)

prod = df.groupby("Description").agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Quantity=("Quantity", "sum"),
    Avg_Price=("UnitPrice", "mean"),
    Orders=("InvoiceNo", "nunique")
).reset_index().sort_values("Total_Revenue", ascending=False)

top10 = prod.head(10)
bot10 = prod.tail(10)

print(f"\nTop 5 Products by Revenue:")
print(top10[["Description","Total_Revenue","Total_Quantity"]].head())

# High-sales, low-quantity-per-order (proxy for high price, possibly low volume)
prod["Revenue_per_Order"] = prod["Total_Revenue"] / prod["Orders"]
high_sales_low_qty = prod[(prod["Total_Revenue"] > prod["Total_Revenue"].quantile(0.75)) &
                           (prod["Total_Quantity"] < prod["Total_Quantity"].quantile(0.25))]
print(f"\nHigh Revenue, Low Quantity count: {len(high_sales_low_qty)}")

# Top 10 Products Chart
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
# By Revenue
top10_r = top10.sort_values("Total_Revenue")
axes[0].barh(range(len(top10_r)), top10_r["Total_Revenue"] / 1e3,
             color=PALETTE["primary"], edgecolor="white")
axes[0].set_yticks(range(len(top10_r)))
axes[0].set_yticklabels([d[:35] for d in top10_r["Description"]], fontsize=8)
axes[0].set_title("Top 10 Products — Revenue (£K)", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Revenue (£K)")
axes[0].set_facecolor(PALETTE["bg"])
axes[0].spines[["top","right"]].set_visible(False)

# By Quantity
top10_q = prod.nlargest(10, "Total_Quantity").sort_values("Total_Quantity")
axes[1].barh(range(len(top10_q)), top10_q["Total_Quantity"],
             color=PALETTE["secondary"], edgecolor="white")
axes[1].set_yticks(range(len(top10_q)))
axes[1].set_yticklabels([d[:35] for d in top10_q["Description"]], fontsize=8)
axes[1].set_title("Top 10 Products — Quantity Sold", fontsize=12, fontweight="bold")
axes[1].set_xlabel("Units Sold")
axes[1].set_facecolor(PALETTE["bg"])
axes[1].spines[["top","right"]].set_visible(False)

fig.patch.set_facecolor("white")
plt.suptitle("Product Performance Analysis", fontsize=14, fontweight="bold",
             color=PALETTE["text"])
plt.tight_layout()
plt.savefig(f"{OUT}/05_product_analysis.png", dpi=150, bbox_inches="tight")
plt.close()
print("  Saved: 05_product_analysis.png")

# Bottom 10
fig, ax = plt.subplots(figsize=(12, 5))
bot10_s = bot10.sort_values("Total_Revenue")
ax.barh(range(len(bot10_s)), bot10_s["Total_Revenue"],
        color=PALETTE["accent"], edgecolor="white")
ax.set_yticks(range(len(bot10_s)))
ax.set_yticklabels([d[:40] for d in bot10_s["Description"]], fontsize=8)
ax.set_title("Bottom 10 Products (Least Revenue)", fontsize=12, fontweight="bold",
             color=PALETTE["text"])
ax.set_facecolor(PALETTE["bg"]); fig.patch.set_facecolor("white")
ax.spines[["top","right"]].set_visible(False)
plt.tight_layout()
plt.savefig(f"{OUT}/06_bottom_products.png", dpi=150, bbox_inches="tight")
plt.close()
print("  Saved: 06_bottom_products.png")

# ════════════════════════════════════════════════════════════
# 4. REGIONAL ANALYSIS
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("4. REGIONAL ANALYSIS")
print("=" * 60)

country = df.groupby("Country").agg(
    Revenue=("Revenue", "sum"),
    Orders=("InvoiceNo", "nunique"),
    Customers=("CustomerID", "nunique")
).reset_index().sort_values("Revenue", ascending=False)

country["Rev_Share_%"] = (country["Revenue"] / country["Revenue"].sum() * 100).round(2)
print(country.head(10).to_string(index=False))

# Top 10 Countries
top_countries = country.head(10)
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Bar chart
top_c_sorted = top_countries.sort_values("Revenue")
axes[0].barh(top_c_sorted["Country"], top_c_sorted["Revenue"] / 1e3,
             color=[PALETTE["accent"] if c == "United Kingdom" else PALETTE["primary"]
                    for c in top_c_sorted["Country"]],
             edgecolor="white")
axes[0].set_title("Top 10 Countries — Revenue (£K)", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Revenue (£K)")
axes[0].set_facecolor(PALETTE["bg"])
axes[0].spines[["top","right"]].set_visible(False)

# Donut chart — excluding UK to show other markets
non_uk = country[country["Country"] != "United Kingdom"].head(9)
others = country[country["Country"] != "United Kingdom"].iloc[9:]["Revenue"].sum()
donut_data = list(non_uk["Revenue"]) + [others]
donut_labels = list(non_uk["Country"]) + ["Others"]
donut_colors = sns.color_palette("Set2", len(donut_data))
wedges, texts, autotexts = axes[1].pie(
    donut_data, labels=donut_labels, autopct="%1.1f%%",
    colors=donut_colors, startangle=90,
    wedgeprops=dict(width=0.55, edgecolor="white")
)
for at in autotexts:
    at.set_fontsize(8)
axes[1].set_title("Revenue Share — International (ex-UK)", fontsize=12, fontweight="bold")

fig.patch.set_facecolor("white")
plt.suptitle("Regional Sales Analysis", fontsize=14, fontweight="bold", color=PALETTE["text"])
plt.tight_layout()
plt.savefig(f"{OUT}/07_regional_analysis.png", dpi=150, bbox_inches="tight")
plt.close()
print("  Saved: 07_regional_analysis.png")

# ── Country Quarterly Heatmap ─────────────────────────────────
top5_countries = country.head(5)["Country"].tolist()
df_top5 = df[df["Country"].isin(top5_countries)]
pivot_hm = df_top5.pivot_table(values="Revenue", index="Country",
                                columns="Quarter", aggfunc="sum") / 1e3
pivot_hm.columns = [str(c) for c in pivot_hm.columns]
fig, ax = plt.subplots(figsize=(12, 4))
sns.heatmap(pivot_hm, annot=True, fmt=".0f", cmap="YlOrRd",
            linewidths=0.5, ax=ax, cbar_kws={"label": "Revenue (£K)"})
ax.set_title("Quarterly Revenue Heatmap — Top 5 Countries (£K)",
             fontsize=13, fontweight="bold", color=PALETTE["text"])
plt.tight_layout()
plt.savefig(f"{OUT}/08_country_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
print("  Saved: 08_country_heatmap.png")

# ════════════════════════════════════════════════════════════
# 5. CUSTOMER INSIGHTS
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("5. CUSTOMER / RFM INSIGHTS")
print("=" * 60)

snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)
rfm = df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda x: (snapshot_date - x.max()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("Revenue", "sum")
).reset_index()

rfm["R_Score"] = pd.qcut(rfm["Recency"], 4, labels=[4,3,2,1]).astype(int)
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1,2,3,4]).astype(int)
rfm["M_Score"] = pd.qcut(rfm["Monetary"], 4, labels=[1,2,3,4]).astype(int)
rfm["RFM_Score"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]

def segment(score):
    if score >= 10: return "Champions"
    elif score >= 8: return "Loyal"
    elif score >= 6: return "Potential"
    else: return "At-Risk"

rfm["Segment"] = rfm["RFM_Score"].apply(segment)
seg_rev = rfm.groupby("Segment")["Monetary"].sum().sort_values(ascending=False)
print(f"\nRFM Segments:\n{rfm['Segment'].value_counts()}")
print(f"\nRevenue by Segment:\n{seg_rev}")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
seg_colors = {"Champions": PALETTE["gold"], "Loyal": PALETTE["secondary"],
              "Potential": PALETTE["primary"], "At-Risk": PALETTE["accent"]}
seg_cnt = rfm["Segment"].value_counts()
axes[0].bar(seg_cnt.index, seg_cnt.values,
            color=[seg_colors[s] for s in seg_cnt.index], edgecolor="white", width=0.55)
for i, v in enumerate(seg_cnt.values):
    axes[0].text(i, v + 5, str(v), ha="center", fontweight="bold")
axes[0].set_title("Customer Count by RFM Segment", fontsize=12, fontweight="bold")
axes[0].set_facecolor(PALETTE["bg"]); axes[0].spines[["top","right"]].set_visible(False)

axes[1].bar(seg_rev.index, seg_rev.values / 1e3,
            color=[seg_colors[s] for s in seg_rev.index], edgecolor="white", width=0.55)
axes[1].set_title("Revenue by RFM Segment (£K)", fontsize=12, fontweight="bold")
axes[1].set_ylabel("Revenue (£K)")
axes[1].set_facecolor(PALETTE["bg"]); axes[1].spines[["top","right"]].set_visible(False)

fig.patch.set_facecolor("white")
plt.suptitle("Customer RFM Segmentation", fontsize=14, fontweight="bold", color=PALETTE["text"])
plt.tight_layout()
plt.savefig(f"{OUT}/09_rfm_segments.png", dpi=150, bbox_inches="tight")
plt.close()
print("  Saved: 09_rfm_segments.png")

# ── Revenue Scatter: Frequency vs Monetary ─────────────────
fig, ax = plt.subplots(figsize=(9, 6))
for seg, col in seg_colors.items():
    sub = rfm[rfm["Segment"] == seg]
    ax.scatter(sub["Frequency"], sub["Monetary"] / 1e3, c=col,
               label=seg, alpha=0.6, s=40, edgecolors="white", linewidth=0.3)
ax.set_xlabel("Purchase Frequency (Orders)"); ax.set_ylabel("Total Spend (£K)")
ax.set_title("Customer Frequency vs Spend — RFM Segments",
             fontsize=13, fontweight="bold", color=PALETTE["text"])
ax.legend(); ax.set_facecolor(PALETTE["bg"]); fig.patch.set_facecolor("white")
ax.spines[["top","right"]].set_visible(False)
plt.tight_layout()
plt.savefig(f"{OUT}/10_rfm_scatter.png", dpi=150, bbox_inches="tight")
plt.close()
print("  Saved: 10_rfm_scatter.png")

# ════════════════════════════════════════════════════════════
# 6. PRINT SUMMARY STATS
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("SUMMARY STATS")
print("=" * 60)
print(f"  Best Month (Revenue)   : {monthly.loc[monthly['Revenue'].idxmax(), 'YearMonth_str']}")
print(f"  Best Country           : {country.iloc[0]['Country']} (£{country.iloc[0]['Revenue']:,.0f})")
print(f"  Top Product            : {top10.iloc[0]['Description'][:50]}")
print(f"  Champion Customers     : {(rfm['Segment']=='Champions').sum()}")
print(f"  At-Risk Customers      : {(rfm['Segment']=='At-Risk').sum()}")
print("\n✅ Task 1 Analysis Complete — all charts saved to Task_01/outputs/")
