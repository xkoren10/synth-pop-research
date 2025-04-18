from send_prompt import send_prompt
import re
from prompts import generate_pop_prompt, rate_prompt, bfi_prompt, narcissism_prompt, psychopathy_prompt, machiavellianism_prompt
from tqdm import tqdm
from config import TEST_TYPE, MODEL

""" For generating populations """
# response = send_prompt(generate_pop_prompt, 0.0)
#
# # Write the response to the output file for the current temperature
# with open(f'outputs/populations/100_pop.txt', 'a') as out_f:
#     out_f.write(response)
# exit()

""" Main program """
# Load the response file and process each line through send_prompt
with open('outputs/populations/100_pop_5.txt', 'r') as f:
    personas = f.readlines()

temp = 2.0

test_prompts = {
    "bfi": bfi_prompt,
    "narcis": narcissism_prompt,
    "machiavellianism": machiavellianism_prompt,
    "psycho": psychopathy_prompt
}

with (tqdm(personas, desc=f"Processing personas at temperature {temp}", ncols=100) as pbar):
    for persona in pbar:
        cleaned_line = re.sub(r'^\d+\.\s*', '', persona.strip())
        name, _, _ = cleaned_line.partition(',')

        assert TEST_TYPE in test_prompts
        # Construct the ranking prompt with the current persona
        ranking_prompt = f"Imagine the following person: {persona}." + rate_prompt + test_prompts[TEST_TYPE]

        # Call send_prompt with the current temperature
        response = send_prompt(ranking_prompt, temp)

        # Write the response to the output file for the current temperature
        with open(f'outputs/reports/{MODEL}/{TEST_TYPE}/response_{temp}.txt', 'a') as out_f:
            out_f.write(f'{name}: {response}\n')

