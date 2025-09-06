import pandas as pd

# Load dataset (CSV)
df = pd.read_csv("owid-co2-data.csv")

# Select important columns
columns = [
    "country", "year", "co2", "co2_per_capita", "population",
    "gdp", "coal_co2", "oil_co2", "gas_co2", "cement_co2"
]
df = df[columns]

# Filter data (1960–2022)
df = df[(df["year"] >= 1960) & (df["year"] <= 2022)]

# Drop rows with missing essential values
df = df.dropna(subset=["co2", "population"])

# Convert Mt to Gt for global scale
df["co2_gt"] = df["co2"] / 1000

# Derived fields
df["gdp_per_capita"] = df["gdp"] / df["population"]
df["co2_intensity"] = df["co2"] / df["gdp"]  # CO₂ per $ GDP

# Save cleaned dataset
df.to_csv("cleaned_co2.csv", index=False)

print("Cleaned dataset saved as cleaned_co2.csv")
print(df.head(10))  # Show first 10 rows for confirmation
