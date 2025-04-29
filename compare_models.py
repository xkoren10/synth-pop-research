import pandas as pd
from config import TEST_TYPE, CRED, CGREEN, CEND
from scipy.stats import ttest_ind

# Define file paths
model1_path = f'outputs/statistics/llama/{TEST_TYPE}/combined_responses.csv'
model2_path = f'outputs/statistics/deepseek/{TEST_TYPE}/combined_responses.csv'

# Load the data
df_model1 = pd.read_csv(model1_path)
df_model2 = pd.read_csv(model2_path)
df_model1 = df_model1.iloc[:, 1:]
df_model2 = df_model2.iloc[:, 1:]

# Ensure both dataframes have the same columns
if not df_model1.columns.equals(df_model2.columns):
    print("Error: Dataframes have different columns. Ensure they match before comparison.")
else:
    # Perform statistical tests for each column
    for column in df_model1.columns:
        stat, p_value = ttest_ind(df_model1[column], df_model2[column], equal_var=False)  # Use ttest_rel() if paired data
        print(f"{column}: t-statistic = {stat:.3f}, p-value = {p_value:.3f}", end="")

        # Check significance
        if p_value < 0.05:
            print(CGREEN + f"   → Significant difference found for {column}" + CEND)
        else:
            print(CRED + f"   → No significant difference found for {column}" + CEND)
