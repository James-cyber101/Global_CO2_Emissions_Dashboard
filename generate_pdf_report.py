from fpdf import FPDF
import os
import pandas as pd

# Create PDF object
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Title (use only ASCII characters)
pdf.set_font("Arial", 'B', 16)
pdf.cell(0, 10, "Global CO2 Emissions EDA Report", ln=True, align='C')
pdf.ln(10)

# Load dataset
df = pd.read_csv("cleaned_co2.csv")

# Dataset summary
pdf.set_font("Arial", '', 12)
pdf.multi_cell(0, 8, f"Dataset Summary:\nRows: {df.shape[0]} | Columns: {df.shape[1]}")
pdf.ln(5)
pdf.multi_cell(0, 8, f"Columns: {', '.join(df.columns)}")
pdf.ln(10)

# Add charts
charts_folder = "charts"
charts_list = [
    "regional_trends.png",
    "corr_heatmap_2022.png",
    "decoupling_2000_2022.png",
    "intensity_trend_key_economies.png",
    "top_emitters_2022.png",
    "bubble_co2_gdp_2022.png",
    "decadal_trends.png",
    "sectoral_top5_2022.png"
]

pdf.set_font("Arial", 'B', 14)
pdf.cell(0, 10, "Charts:", ln=True)
pdf.ln(5)

for chart in charts_list:
    chart_path = os.path.join(charts_folder, chart)
    if os.path.exists(chart_path):
        # Chart title without special characters
        pdf.set_font("Arial", 'I', 12)
        pdf.cell(0, 8, chart.replace("_", " ").replace(".png", "").title(), ln=True)
        pdf.image(chart_path, w=180)
        pdf.ln(5)

# Save PDF
output_file = "Global_CO2_EDA_Report.pdf"
pdf.output(output_file)
print(f"PDF report generated successfully: {output_file}")

