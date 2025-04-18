import matplotlib.pyplot as plt
from collections import defaultdict, Counter
import numpy as np
import os

# Replace with your file path
file_path = 'outputs/populations/10_pop.txt'
output_path = 'outputs/populations/plots/age_distribution_10.png'
ages_by_gender = defaultdict(list)
total_count = 0
gender_count = defaultdict(int)
all_ages = []

# Parse the file
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            parts = line.strip().split(',')
            if len(parts) < 3:
                continue  # skip malformed lines

            age = int(parts[1].strip())
            gender = parts[2].split('-')[0].strip().capitalize()

            ages_by_gender[gender].append(age)
            gender_count[gender] += 1
            all_ages.append(age)
            total_count += 1
        except Exception as e:
            print(f"Skipping line due to error: {e}")

# Bin setup
bins = np.arange(0, 101, 5)
bin_labels = [f'{i}-{i + 4}' for i in bins[:-1]]

# Prepare bin counts per gender
gender_list = sorted(ages_by_gender.keys())
bin_counts = {gender: [0] * (len(bins) - 1) for gender in gender_list}

for gender in gender_list:
    age_counts = Counter(ages_by_gender[gender])
    for i in range(len(bins) - 1):
        bin_range = range(bins[i], bins[i + 1])
        bin_counts[gender][i] = sum(age_counts[age] for age in bin_range)

# Plotting side-by-side bars
x = np.arange(len(bin_labels))  # label positions
width = 0.8 / len(gender_list)  # divide bar width among genders

plt.figure(figsize=(12, 6))

for idx, gender in enumerate(gender_list):
    offset = (idx - len(gender_list) / 2) * width + width / 2
    plt.bar(x + offset, bin_counts[gender], width=width, label=gender)

# Summary box
mean_age = np.mean(all_ages)
summary_text = f"Mean Age: {mean_age:.1f}\n"
for gender in gender_count:
    percent = (gender_count[gender] / total_count) * 100
    summary_text += f"{gender}: {percent:.1f}%\n"

# Labels and formatting
plt.xticks(x, bin_labels, rotation=45)
plt.xlabel('Age Range')
plt.ylabel('Number of People')
plt.title('Age Distribution by Gender (Side-by-Side Bars)')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add summary box
plt.gcf().text(0.75, 0.75, summary_text.strip(), bbox=dict(facecolor='white', alpha=0.8), fontsize=10)

plt.tight_layout()
plt.savefig(output_path, dpi=300)
print(f"Plot saved to {os.path.abspath(output_path)}")

plt.close()