import pandas as pd
from scipy import stats
from config import MODEL, TEST_TYPE, CRED, CGREEN, CEND


# Load the dataset with computed means and standard deviations
input_file = f'outputs/statistics/{MODEL}/{TEST_TYPE}/temperature_stats.csv'
df = pd.read_csv(input_file, index_col=0)

# Significance level
alpha = 0.05

# === Linear Trend Analysis (Linregress) ===
print("\n=== Linear Trend Analysis Across Temperatures ===")
print(f"=== Model: {MODEL}, Test: {TEST_TYPE} ===")
temperatures = df.index.astype(float)  # assuming index is temperature

diff_mean_count = 0
diff_std_count = 0

for col in df.columns:
    y = df[col].values
    slope, intercept, r_value, p_value, std_err = stats.linregress(temperatures, y)
    if p_value < alpha:
        sig = "✅"
        if col.endswith("_mean"):
            diff_mean_count += 1
        elif col.endswith("_std"):
            diff_std_count += 1
    else:
        sig = "❌"
    print(f"{col}: p = {p_value:.5f}, slope = {slope:.4f} {sig}")
print("="*40)
print(f"Mean count: " + CGREEN + str(diff_mean_count) + CEND + ", Std count: " + CGREEN + str(diff_std_count) + CEND)