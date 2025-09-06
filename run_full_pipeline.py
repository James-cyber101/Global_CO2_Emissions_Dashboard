import os

scripts = ["preprocess.py", "eda_charts.py", "eda_advanced.py", "generate_pdf_report.py", "dashboard_full.py"]  # add 'generate_pdf_report.py' , 'launches the dashboard if ready

for script in scripts:
    print(f"\n--> Running {script} ...\n")
    os.system(f"python {script}")

print("\n All scripts completed. Charts saved in 'charts/' folder.")
import os


