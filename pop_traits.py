import statistics
import numpy as np

import matplotlib.pyplot as plt

from config import TEST_TYPE, MODEL, CEND,CGREEN, CRED
from pop_traits.test_mapping import bfi_map, psychopathy_map, narcissism_map, machiavellianism_map

def reverse(score):
    return 6 - score

reverse_map = {
    "bfi": bfi_map,
    "narcis": narcissism_map,
    "machiavellianism": machiavellianism_map,
    "psycho": psychopathy_map
}

reference_population_bfi = {
    "Extraversion": {"avg": 3.24, "std": 0.88},
    "Agreeableness": {"avg": 3.20, "std": 0.83},
    "Conscientiousness": {"avg": 4.10, "std": 0.69},
    "Neuroticism": {"avg": 3.49, "std": 0.85},  # Reversed from Emotional Stability
    "Openness": {"avg": 3.41, "std": 0.88}
}

reference_population_triad = {
"Machiavellianism" : {"avg": 2.96, "std":  0.65},
"Narcissism" :    {"avg": 2.97, "std": 0.61},
"Psychopathy" : {"avg": 2.09, "std": 0.63}
}
def calculate_stats(file_path, test_type):
    trait_scores = {}
    for trait, _ in reverse_map[test_type]:
        if trait not in trait_scores:
            trait_scores[trait] = []

    try:
        with open(file_path, "r") as f:
            for line in f:
                if ':' not in line: continue
                _, scores_part = line.strip().split(":")
                scores = list(map(int, scores_part.strip().split()))
                for i, (trait, is_reversed) in enumerate(reverse_map[test_type]):
                    score = reverse(scores[i]) if is_reversed else scores[i]
                    trait_scores[trait].append(score)
    except FileNotFoundError:
        return None

    stats = {}
    for trait, values in trait_scores.items():
        if values:
            stats[trait] = {
                "avg": round(statistics.mean(values), 2),
                "std": round(statistics.stdev(values), 2) if len(values) > 1 else 0.0
            }
    return stats

def mse_distance(stats1, stats2):
    errors = []
    for trait in stats1:
        if trait in stats2:
            mean_diff = (stats1[trait]["avg"] - stats2[trait]["avg"]) ** 2
            std_diff = (stats1[trait]["std"] - stats2[trait]["std"]) ** 2
            errors.append((mean_diff + std_diff) / 2)
    if TEST_TYPE == "bfi":
        return round(sum(errors) / len(errors), 4)  # mean MSE across BFI traits
    else:
        return round(sum(errors), 4)  # total MSE for single-trait tests


# Run over temperatures from 0.0 to 2.0 (step = 0.1)
results = {}
best_temp = None
lowest_error = float("inf")

# Choose the appropriate reference population based on the TEST_TYPE
# Select appropriate reference population based on test type
if TEST_TYPE == "bfi":
    reference_population = reference_population_bfi
elif TEST_TYPE == "machiavellianism":
    reference_population = {"Machiavellianism": reference_population_triad["Machiavellianism"]}
elif TEST_TYPE == "narcis":
    reference_population = {"Narcissism": reference_population_triad["Narcissism"]}
elif TEST_TYPE == "psycho":
    reference_population = {"Psychopathy": reference_population_triad["Psychopathy"]}
else:
    raise ValueError(f"Unknown TEST_TYPE: {TEST_TYPE}")


for temp in [round(x * 0.1, 1) for x in range(0, 21)]:
    file_path = f"outputs/reports/{MODEL}/{TEST_TYPE}/response_{temp}.txt"
    stats = calculate_stats(file_path, TEST_TYPE)
    if not stats:
        continue
    error = mse_distance(stats, reference_population)
    results[temp] = {"stats": stats, "mse": error}
    if error < lowest_error:
        lowest_error = error
        best_temp = temp

# Report results
print(CRED + "\n=== Temperature Matching Results ===" + CEND)
for temp in sorted(results):
    print(f"Temp {temp}: MSE = {results[temp]['mse']}")

print("="*50)
print("Best matching temperature: " + CGREEN + str(best_temp) + CEND, end="")
print(" with MSE = " + CGREEN + str(lowest_error) + CEND)
print("="*50)

print("Stats at best temperature:")
for trait, values in results[best_temp]['stats'].items():
    print(f"  {trait}: avg = {values['avg']}, std = {values['std']}")

# === Plot error bars ===
if best_temp:
    traits = list(reference_population.keys())
    x = np.arange(len(traits))

    synthetic_means = [results[best_temp]["stats"][t]["avg"] for t in traits]
    synthetic_stds = [results[best_temp]["stats"][t]["std"] for t in traits]
    baseline_means = [reference_population[t]["avg"] for t in traits]
    baseline_stds = [reference_population[t]["std"] for t in traits]

    plt.figure(figsize=(10, 6))
    plt.errorbar(x - 0.1, synthetic_means, yerr=synthetic_stds, fmt='o', capsize=5,
                 label=f'Synthetic (Temp {best_temp})', color='tab:blue')
    plt.errorbar(x + 0.1, baseline_means, yerr=baseline_stds, fmt='o', capsize=5,
                 label='Baseline (Study)', color='tab:orange')

    plt.xticks(x, traits)
    plt.ylabel("Score")
    plt.title(f"{TEST_TYPE.capitalize()} Trait Comparison: Synthetic vs. Baseline (Mean ± STD)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(f"pop_traits/{TEST_TYPE}/best_pop_{TEST_TYPE}_{MODEL}_{best_temp}.png")