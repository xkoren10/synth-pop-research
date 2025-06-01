from config import TEST_TYPE, MODEL
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Define the file path and temperature range
file_path = f'outputs/reports/{MODEL}/{TEST_TYPE}'

# Get the number of files in the directory
try:
    num_files = len([f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))])
except FileNotFoundError:
    print(f"Error: Directory '{file_path}' not found.")
    exit()
temperatures = [round(t * 0.1, 1) for t in range(num_files)]

num_questions = 10 if TEST_TYPE == "bfi" else 9


# Dictionary to store responses: key will be persona name, value will be list of responses
personas_responses = {}

# Read responses from each file
for temp in temperatures:
    file_name = f"{file_path}/response_{temp}.txt"

    with open(file_name, 'r') as f:
        for line in f.readlines():
            # Extract persona name and their responses
            name, responses = line.split(':')
            name = name.strip()  # Remove any extra spaces

            # If the persona is not already in the dictionary, initialize an empty list for their responses
            if name not in personas_responses:
                personas_responses[name] = []

            # Convert the response values to integers and add them to the dictionary
            response_values = list(map(int, responses.split()))

            # Ensure we have exactly 10 response values per persona (one for each question)

            if len(response_values) == num_questions and all(1 <= value <= 5 for value in response_values):
                personas_responses[name].append(response_values)
            else:
                print(
                    f"Skipping {name} due to incorrect number of responses: {len(response_values)} or invalid response values.")

# Now generate graphs for each persona
for persona, responses in personas_responses.items():
    # Ensure there are exactly 21 temperature files, and each has 10 responses
    if len(responses) == num_files:  # 21 temperature files
        # Convert responses into a numpy array for easier handling
        responses = np.array(responses)

        # Create a new plot for this persona
        plt.figure(figsize=(10, 6))

        # Plot each question's responses across the temperatures
        for i in range(num_questions):  # Assuming 10 questions
            plt.plot(temperatures, responses[:, i], marker='o', label=f'Q{i + 1}')

        # Set plot labels and title
        plt.xlabel('Temperature')
        plt.ylabel('Response')
        plt.title(f'Responses for {persona} across Temperatures')
        plt.xticks(temperatures)
        plt.legend(title="Questions")
        plt.grid(True)

        # Save the plot as an image file
        plt.savefig(f'outputs/graphs/{MODEL}/{TEST_TYPE}/{persona}.png')
        plt.close()
    else:
        print(f"Skipping {persona} due to incorrect number of temperatures: {len(responses)}")

print("Graphs generated and saved successfully!")

# Load the combined statistics from the CSV file
input_file = f'outputs/statistics/{MODEL}/{TEST_TYPE}/combined_responses_with_average.csv'
combined_df = pd.read_csv(input_file, index_col=0)

# Prepare output directory for boxplots
output_dir = f'outputs/plots/{MODEL}/{TEST_TYPE}'
os.makedirs(output_dir, exist_ok=True)

# Separate mean and standard deviation columns
mean_columns = [f'Q{i + 1}_mean' for i in range(num_questions)]
std_columns = [f'Q{i + 1}_std' for i in range(num_questions)]

# Iterate through each persona and generate a plot with error bars
for persona in combined_df.index:
    plt.figure(figsize=(8, 6))

    # Extract mean and standard deviation data
    means = combined_df.loc[persona, mean_columns].values
    stds = combined_df.loc[persona, std_columns].values
    questions = [f'Q{i + 1}' for i in range(num_questions)]

    # Plot error bars without connecting lines
    plt.errorbar(questions, means, yerr=stds, fmt='o', capsize=5, label='Mean ± SD', color='blue')

    # Add red horizontal lines at each whole number
    for y in range(7):
        plt.axhline(y, color='red', linestyle='--', linewidth=0.7, alpha=0.6)

    plt.ylim(0, 6)
    plt.yticks(np.arange(0, 6.5, 0.5))

    plt.title(f'Response Distribution for {persona}')
    plt.xlabel('Questions')
    plt.ylabel('Response Value')
    plt.xticks(rotation=45)
    plt.legend()

    plt.tight_layout()

    # Save the plot as an image file
    plot_file = os.path.join(output_dir, f'{persona}_boxplot.png')
    plt.savefig(plot_file)
    plt.close()

print("All boxplots generated and saved successfully!")
