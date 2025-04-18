import numpy as np
import pandas as pd
from config import TEST_TYPE, MODEL
import os

# Define the file path and temperature range
file_path = f'outputs/reports/{MODEL}/{TEST_TYPE}'

# Get the number of files in the directory
try:
    num_files = len([f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))])
except FileNotFoundError:
    print(f"Error: Directory '{file_path}' not found.")
    exit()

temperatures = [round(t * 0.1, 1) for t in range(num_files)]  # From 0.0 to 2.0

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

            # Initialize the persona if not already present
            if name not in personas_responses:
                personas_responses[name] = []

            # Convert responses to integers and store them
            response_values = list(map(int, responses.split()))

            # Ensure 10 responses per line (one per question)
            personas_responses[name].append(response_values)

# Prepare data structures for combined statistics
combined_data = {}

# Calculate mean and standard deviation for each persona
for persona, responses in personas_responses.items():
    if len(responses) == num_files:  # Ensure we have responses for all 21 temperatures
        responses_array = np.array(responses)  # Convert to numpy array (21, 10)

        # Calculate mean and standard deviation across all temperatures (axis 0)
        mean_values = np.mean(responses_array, axis=0)
        std_values = np.std(responses_array, axis=0)

        # Combine mean and std into one row with labeled columns
        combined_data[persona] = np.concatenate([mean_values, std_values])

# Create DataFrame for combined statistics
num_questions = 10 if TEST_TYPE == "bfi" else 9

questions = [f'Q{i + 1}' for i in range(num_questions)]
columns = [f'{q}_mean' for q in questions] + [f'{q}_std' for q in questions]

combined_df = pd.DataFrame(combined_data, index=columns).T

# Save the combined results to a CSV file
output_file = f'outputs/statistics/{MODEL}/{TEST_TYPE}/combined_responses.csv'
combined_df.to_csv(output_file)

print(f"Combined statistics calculated and saved successfully to {output_file}!")


import pandas as pd

# Load the combined statistics from the CSV file
input_file = f'outputs/statistics/{MODEL}/{TEST_TYPE}/combined_responses.csv'
combined_df = pd.read_csv(input_file, index_col=0)

# Calculate the average of the mean and standard deviation columns
mean_columns = [col for col in combined_df.columns if '_mean' in col]
std_columns = [col for col in combined_df.columns if '_std' in col]

# Calculate the average values for means and standard deviations
average_means = combined_df[mean_columns].mean()
average_stds = combined_df[std_columns].mean()

# Create a new row with the computed averages
average_row = pd.concat([average_means, average_stds])
average_row.name = 'Average'

# Append the row to the DataFrame
combined_df = pd.concat([combined_df, average_row.to_frame().T])

# Save the updated DataFrame with the 'Average' row included
output_file = f'outputs/statistics/{MODEL}/{TEST_TYPE}/combined_responses_with_average.csv'
combined_df.to_csv(output_file)

print(f"Updated dataframe with average row saved to {output_file}")
