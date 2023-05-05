import os
import matplotlib.pyplot as plt
import numpy as np

def extract_vina_scores(filename):
    scores = []
    with open(filename, 'r') as f:
        for line in f:
            if "REMARK VINA RESULT:" in line:
                score = float(line.split()[3])
                scores.append(score)
    return scores

file_prefix = "test"
results = []

mevalonate_score = -4.8

for i in range(1, 41):
    filename = f"./output/{file_prefix}{i}.txt"
    if os.path.isfile(filename):
        scores = extract_vina_scores(filename)
        avg_score = np.mean(scores)
        std_dev = np.std(scores)
        min_score = np.min(scores)
        max_score = np.max(scores)
        results.append((i, avg_score, std_dev, min_score, max_score))

x = [result[0] for result in results]
y = [result[1] - mevalonate_score for result in results]
yerr = [result[2] for result in results]

plt.figure()
plt.errorbar(x, y, yerr=yerr, fmt='o', capsize=5, elinewidth=2, markeredgewidth=2)
plt.xlabel("Test Index")
plt.ylabel("Difference to Mevalonate Score")
plt.title("Average VINA Score Differences to Mevalonate Score with Error Bars")
plt.grid()
plt.show()

import pyperclip
# Create table header
table = "Test Number\tAverage Score\tStandard Deviation\tLowest Score\tHighest Score\n"

# Create table rows
for result in results:
    row = f"{result[0]}\t{result[1]:.4f}\t{result[2]:.4f}\t{result[3]:.4f}\t{result[4]:.4f}\n"
    table += row

# Copy the table to clipboard
pyperclip.copy(table)
print("Table copied to clipboard!")