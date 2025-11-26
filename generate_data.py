import pandas as pd
import numpy as np
import os

# Create data
np.random.seed(42)
data = {
    "Transaction ID": range(1, 101),
    "Date": pd.date_range(start="2023-01-01", periods=100),
    "Amount": np.random.uniform(1000, 50000, 100).round(2),
    "Description": ["Transaction " + str(i) for i in range(1, 101)]
}

df = pd.DataFrame(data)

# Save to ODS
output_path = "tasks/banking/cash_flows.ods"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_excel(output_path, engine="odf", index=False)

print(f"Generated {output_path}")
