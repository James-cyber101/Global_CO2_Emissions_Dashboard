# eda_advanced.py
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- Setup ----------
sns.set(style="whitegrid", palette="muted")
os.makedirs("charts", exist_ok=True)

# Load cleaned data
df = pd.read_csv("cleaned_co2.csv")

# Aggregates to exclude for country-only analyses
aggregates = {
    "World","Asia","Europe","Africa","North America","South America","Oceania",
    "European Union (27)","European Union (28)","International transport"
}

# ---------- 1) Regional CO₂ trends (1960–2022) ----------
regions = ["World","Asia","Europe","Africa","North America","South America","Oceania"]
regional = df[df["country"].isin(regions) & (df["year"].between(1960, 2022))].copy()

plt.figure(figsize=(11,6))
for r in regions:
    sub = regional[regional["country"]==r]
    if not sub.empty:
        plt.plot(sub["year"], sub["co2_gt"], label=r)
plt.title("Regional CO2 Emissions (1960–2022)")
plt.xlabel("Year"); plt.ylabel("CO2 Emissions (Gt)")
plt.legend(title="Region", ncol=3, frameon=False)
plt.tight_layout()
plt.savefig("charts/regional_trends.png", dpi=200)
plt.close()

# ---------- 2) Correlation heatmap across countries (2022) ----------
data_2022 = df[(df["year"]==2022) & (~df["country"].isin(aggregates))].copy()
data_2022 = data_2022[data_2022["population"] > 1e6]  # remove microstates

corr_cols = [
    "co2","co2_per_capita","population","gdp","gdp_per_capita",
    "coal_co2","oil_co2","gas_co2","cement_co2","co2_intensity"
]
corr_df = data_2022[corr_cols].dropna()
corr = corr_df.corr()

plt.figure(figsize=(9,7))
sns.heatmap(corr, annot=False, cmap="coolwarm", center=0, square=True,
            cbar_kws={"shrink": .8})
plt.title("Correlation Heatmap (Countries, 2022)")
plt.tight_layout()
plt.savefig("charts/corr_heatmap_2022.png", dpi=220)
plt.close()

# ---------- 3) Decoupling analysis: 2000 → 2022 ----------
def pct_change(series):
    start, end = series.get(2000), series.get(2022)
    if start is not None and end is not None and start != 0:
        return (end - start) / abs(start) * 100
    return np.nan

countries = df[~df["country"].isin(aggregates)]["country"].unique()
rows = []
for c in countries:
    sub = df[(df["country"]==c) & (df["year"].isin([2000, 2022]))].set_index("year")
    if {"gdp_per_capita","co2_per_capita"}.issubset(sub.columns):
        gdp_pc = pct_change(sub["gdp_per_capita"])
        co2_pc = pct_change(sub["co2_per_capita"])
        if not (pd.isna(gdp_pc) or pd.isna(co2_pc)):
            rows.append({"country": c, "gdp_pc_change_%": gdp_pc, "co2_pc_change_%": co2_pc})
decoup = pd.DataFrame(rows)

plt.figure(figsize=(10,7))
plt.axvline(0, linestyle="--", linewidth=1)
plt.axhline(0, linestyle="--", linewidth=1)
plt.scatter(decoup["gdp_pc_change_%"], decoup["co2_pc_change_%"], alpha=0.5)
plt.title("Decoupling (2000→2022): GDP per Capita vs CO2 per Capita")
plt.xlabel("GDP per Capita Change (%)")
plt.ylabel("CO2 per Capita Change (%)")
highlights = ["European Union (27)", "United States", "China", "India", "Japan", "Germany"]
for name in highlights:
    row = decoup[decoup["country"]==name]
    if not row.empty:
        x = row["gdp_pc_change_%"].values[0]
        y = row["co2_pc_change_%"].values[0]
        plt.scatter([x],[y], s=60)
        plt.text(x, y, "  "+name, fontsize=9)
plt.tight_layout()
plt.savefig("charts/decoupling_2000_2022.png", dpi=220)
plt.close()

# ---------- 4) CO2 intensity trend (key economies) ----------
keys = ["European Union (27)", "United States", "China", "India"]
intensity = df[df["country"].isin(keys) & (df["year"].between(2000, 2022))].copy()
intensity["co2_intensity"] = intensity["co2_intensity"].replace([np.inf, -np.inf], np.nan)

plt.figure(figsize=(11,6))
for k in keys:
    sub = intensity[intensity["country"]==k].dropna(subset=["co2_intensity"])
    if not sub.empty:
        plt.plot(sub["year"], sub["co2_intensity"], label=k)
plt.title("CO2 Intensity of GDP (2000–2022)\n(tCO2 per $ of GDP)")
plt.xlabel("Year"); plt.ylabel("CO2 / GDP")
plt.legend(title="Economy", ncol=2, frameon=False)
plt.tight_layout()
plt.savefig("charts/intensity_trend_key_economies.png", dpi=200)
plt.close()

# ---------- 5) Top CO2 emitters (2022) ----------
top_emitters = data_2022.sort_values("co2", ascending=False).head(10)
plt.figure(figsize=(10,6))
sns.barplot(data=top_emitters, x="co2", y="country", palette="Reds_r")
plt.title("Top 10 CO2 Emitting Countries (2022)")
plt.xlabel("CO2 Emissions (Mt)")
plt.ylabel("")
plt.tight_layout()
plt.savefig("charts/top_emitters_2022.png", dpi=220)
plt.close()

# ---------- 6) Bubble plot: CO2 per capita vs GDP per capita ----------
bubble_data = data_2022.dropna(subset=["co2_per_capita","gdp_per_capita"])
plt.figure(figsize=(12,8))
sns.scatterplot(
    data=bubble_data, x="gdp_per_capita", y="co2_per_capita",
    size="population", sizes=(20,800),
    hue="continent" if "continent" in bubble_data.columns else None,
    alpha=0.6, palette="tab10", legend=False
)
plt.xscale("log"); plt.yscale("log")
plt.xlabel("GDP per Capita (log scale)")
plt.ylabel("CO2 per Capita (log scale)")
plt.title("CO2 per Capita vs GDP per Capita (2022)")
plt.tight_layout()
plt.savefig("charts/bubble_co2_gdp_2022.png", dpi=220)
plt.close()

# ---------- 7) Decadal regional trends ----------
decades = list(range(1960, 2030, 10))
plt.figure(figsize=(12,7))
for r in regions:
    sub = df[df["country"]==r]
    decade_avg = sub.groupby(sub["year"]//10*10)["co2_gt"].mean()
    plt.plot(decade_avg.index, decade_avg.values, marker='o', label=r)
plt.title("Decadal Average CO2 Emissions by Region")
plt.xlabel("Decade")
plt.ylabel("CO2 Emissions (Gt)")
plt.legend(title="Region", ncol=2, frameon=False)
plt.tight_layout()
plt.savefig("charts/decadal_trends.png", dpi=220)
plt.close()

# ---------- 8) Sectoral contributions for top 5 countries ----------
top5 = top_emitters.head(5)["country"].tolist()
sector_cols = ["coal_co2","oil_co2","gas_co2","cement_co2"]
sector_data = df[(df["country"].isin(top5)) & (df["year"]==2022)][["country"]+sector_cols]
sector_data.set_index("country", inplace=True)
sector_data.plot(kind="bar", stacked=True, figsize=(10,6), colormap="tab20c")
plt.title("Sectoral CO2 Contributions (Top 5 Emitters, 2022)")
plt.ylabel("CO2 Emissions (Mt)")
plt.xlabel("")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/sectoral_top5_2022.png", dpi=220)
plt.close()

print(" Full Advanced EDA complete. Files saved in charts/:")
print(" - regional_trends.png")
print(" - corr_heatmap_2022.png")
print(" - decoupling_2000_2022.png")
print(" - intensity_trend_key_economies.png")
print(" - top_emitters_2022.png")
print(" - bubble_co2_gdp_2022.png")
print(" - decadal_trends.png")
print(" - sectoral_top5_2022.png")
