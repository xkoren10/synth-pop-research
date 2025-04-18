import pandas as pd
import scipy.stats as stats
from config import MODEL, TEST_TYPE


# Load the dataset with computed means and standard deviations
input_file = f'outputs/statistics/{MODEL}/{TEST_TYPE}/combined_responses.csv'
df = pd.read_csv(input_file, index_col=0)

# Extract only standard deviation columns
std_columns = [col for col in df.columns if '_std' in col]
mean_columns = [col for col in df.columns if '_mean' in col]

from scipy import stats

# Prepare data
std_values = [df[col].dropna().values for col in std_columns]  # Per-question stds
mean_values = [df[col].dropna().values for col in mean_columns]  # Per-question means

# Levene’s test for variances
stat_std, p_value_std = stats.levene(*std_values)

# Kruskal-Wallis test for means
stat_mean, p_value_mean = stats.kruskal(*mean_values)

# Significance level
alpha = 0.05

# Output
if p_value_std < alpha:
    print(f"Levene’s test result: p = {p_value_std:.5f} → Significant difference in variances (reject H₀)")
else:
    print(f"Levene’s test result: p = {p_value_std:.5f} → No significant difference in variances (fail to reject H₀)")

if p_value_mean < alpha:
    print(f"Kruskal-Wallis test result: p = {p_value_mean:.5f} → Significant difference in means (reject H₀)")
else:
    print(f"Kruskal-Wallis test result: p = {p_value_mean:.5f} → No significant difference in means (fail to reject H₀)")
