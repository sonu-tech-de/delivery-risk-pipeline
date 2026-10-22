import subprocess
import sys

steps = ["load_weather.py", "scrape_holidays.py", "build_risk_table.py"]

for step in steps:
    print(f"Running {step}...")
    result = subprocess.run([sys.executable, step])
    if result.returncode != 0:
        print(f"{step} failed. Stopping the pipeline.")
        sys.exit(1)

print("Pipeline finished successfully")