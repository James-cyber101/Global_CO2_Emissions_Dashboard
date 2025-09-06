import warnings
warnings.filterwarnings("ignore")


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Style settings
plt.style.use("seaborn-v0_8")
sns.set_palette("Set2")

# Load cleaned dataset
df = pd.read_csv("cleaned_co2.csv")

# Create charts folder if not exists
if not os.path.exists("charts"):
    os.makedirs("charts")

# 1. Global CO₂ Emissions Trend
global_trend = df.groupby("year")["co2_gt"].sum()
plt.figure(figsize=(10,6))
plt.plot(global_trend.index, global_trend.values, color="red", linewidth=2.5)
plt.title("Global CO₂ Emissions Trend (1960–2022)", fontsize=14)
plt.xlabel("Year")
plt.ylabel("CO₂ Emissions (Gt)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig("charts/global_trend.png")
plt.close()

# 2. Top 10 Emitting Countries (2022)
top_emitters = df[df["year"] == 2022].groupby("country")["co2_gt"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,6))
sns.barplot(x=top_emitters.values, y=top_emitters.index, palette="Reds_r")
plt.title("Top 10 CO₂ Emitting Countries (2022)", fontsize=14)
plt.xlabel("CO₂ Emissions (Gt)")
plt.ylabel("Country")
plt.savefig("charts/top_emitters.png")
plt.close()

# 3. Per Capita CO₂ Emissions (Top 10 in 2022)
top_per_capita = df[df["year"] == 2022].groupby("country")["co2_per_capita"].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,6))
sns.barplot(x=top_per_capita.values, y=top_per_capita.index, palette="Blues_r")
plt.title("Per Capita CO₂ Emissions (2022)", fontsize=14)
plt.xlabel("CO₂ per Capita (tons/person)")
plt.ylabel("Country")
plt.savefig("charts/per_capita.png")
plt.close()

# 4. World CO₂ by Source (2022)
sources = df[df["year"] == 2022][["coal_co2","oil_co2","gas_co2","cement_co2"]].sum()
plt.figure(figsize=(8,6))
plt.pie(sources, labels=sources.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set3"))
plt.title("World CO₂ Emissions by Source (2022)", fontsize=14)
plt.savefig("charts/world_sources.png")
plt.close()

# 5. GDP vs CO₂ (2022)
data_2022 = df[df["year"] == 2022]
plt.figure(figsize=(10,6))
sns.scatterplot(data=data_2022, x="gdp_per_capita", y="co2_per_capita", size="population",
                hue="country", legend=False, alpha=0.7)
plt.xscale("log")
plt.yscale("log")
plt.title("GDP per Capita vs CO₂ per Capita (2022)", fontsize=14)
plt.xlabel("GDP per Capita (log scale)")
plt.ylabel("CO₂ per Capita (log scale)")
plt.savefig("charts/gdp_vs_co2.png")
plt.close()

print("All charts saved in 'charts' folder!")
