import matplotlib.pyplot as plt
from collections import defaultdict, Counter
import numpy as np
import os

# Replace with your file path
file_path = 'outputs/populations/100_pop.txt'
output_path = 'outputs/populations/plots/age_distribution_100.png'
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

# Identify non-empty bins
non_empty_indices = [
    i for i in range(len(bin_labels))
    if any(bin_counts[gender][i] > 0 for gender in gender_list)
]

# Filter labels and counts
filtered_bin_labels = [bin_labels[i] for i in non_empty_indices]
filtered_bin_counts = {
    gender: [bin_counts[gender][i] for i in non_empty_indices]
    for gender in gender_list
}

# Plotting
x = np.arange(len(filtered_bin_labels))  # label positions
width = 0.8 / len(gender_list)  # divide bar width among genders

plt.figure(figsize=(12, 6))

for idx, gender in enumerate(gender_list):
    offset = (idx - len(gender_list) / 2) * width + width / 2
    plt.bar(x + offset, filtered_bin_counts[gender], width=width, label=gender)

# Summary box
mean_age = np.mean(all_ages)
summary_text = f"Mean Age: {mean_age:.1f}\n"
for gender in gender_count:
    percent = (gender_count[gender] / total_count) * 100
    summary_text += f"{gender}: {percent:.1f}%\n"

# Labels and formatting with increased font sizes
plt.xticks(x, filtered_bin_labels, rotation=45, fontsize=12)
plt.xlabel('Age Range', fontsize=20)
plt.ylabel('Number of People', fontsize=20)
plt.legend(fontsize=20)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add summary box with larger font
plt.gcf().text(0.75, 0.6, summary_text.strip(), bbox=dict(facecolor='white', alpha=0.8), fontsize=20)

plt.tight_layout()
plt.savefig(output_path, dpi=300)
print(f"Plot saved to {os.path.abspath(output_path)}")

plt.close()
