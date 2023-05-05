import os
import re
import numpy as np
import matplotlib.pyplot as plt

def read_ligand_data(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    data = []
    for i, line in enumerate(lines):
        if line.startswith("Ligand file:"):
            test_number = int(line.split('.')[0].split()[-1])
            affinity_avg_std = [float(x) for x in re.findall(r"[-+]?\d*\.\d+|\d+", lines[i + 5])]
            cnn_pose_avg_std = [float(x) for x in re.findall(r"[-+]?\d*\.\d+|\d+", lines[i + 6])]
            cnn_affinity_avg_std = [float(x) for x in re.findall(r"[-+]?\d*\.\d+|\d+", lines[i + 7])]
            data.append((test_number, (affinity_avg_std[0], affinity_avg_std[1]), (cnn_pose_avg_std[0], cnn_pose_avg_std[1]), (cnn_affinity_avg_std[0], cnn_affinity_avg_std[1])))

    return data

def extract_vina_scores(filename):
    scores = []
    with open(filename, 'r') as f:
        for line in f:
            if "REMARK VINA RESULT:" in line:
                score = float(line.split()[3])
                scores.append(score)
    return scores

def plot_data(data, vina_results):
    test_numbers = np.array([x[0] for x in data])
    affinity_scores = np.array([x[1] for x in data])
    cnn_pose_scores = np.array([x[2] for x in data])
    cnn_affinity_scores = np.array([x[3] for x in data])

    # Subtract the specified average from the CNN affinity scores
    specified_avg = 2.436
    cnn_affinity_scores_adj = cnn_affinity_scores[:, 0] - specified_avg

    # New error bars (subtracting the specified average)
    specified_std_dev = 0.0206
    cnn_affinity_error_adj = np.sqrt(cnn_affinity_scores[:, 1]**2 - specified_std_dev**2)
    vina_test_numbers = np.array([x[0] for x in vina_results])
    vina_avg_scores = np.array([x[1] for x in vina_results])
    vina_std_dev = np.array([x[2] for x in vina_results])

    # Plot 1: Average GNINA scores with error bars
    plt.figure()
    plt.errorbar(test_numbers, affinity_scores[:, 0], yerr=affinity_scores[:, 1], fmt='o', capsize=5, elinewidth=2, markeredgewidth=2)
    plt.xlabel("Test Index")
    plt.ylabel("GNINA Affinity Scores (kJ/mol)")
    plt.title("Average GNINA Affinity Scores with Error Bars")
    plt.grid()

    # Plot 2: GNINA scores and average VINA scores
    plt.figure()
    plt.errorbar(test_numbers, affinity_scores[:, 0], yerr=affinity_scores[:, 1], fmt='o', capsize=5, elinewidth=2, markeredgewidth=2, label='GNINA Affinity Scores')
    plt.errorbar(vina_test_numbers, vina_avg_scores, yerr=vina_std_dev, fmt='o', capsize=5, elinewidth=2, markeredgewidth=2, label='VINA Scores')
    plt.xlabel("Test Index")
    plt.ylabel("Scores (kJ/mol)")
    plt.title("GNINA and VINA Scores")
    plt.legend()
    plt.grid()

    # Plot 3: Average CNN pose score with error bars
    plt.figure()
    plt.errorbar(test_numbers, cnn_pose_scores[:, 0], yerr=cnn_pose_scores[:, 1], fmt='o', capsize=5, elinewidth=2, markeredgewidth=2)
    plt.xlabel("Test Index")
    plt.ylabel("CNN Pose Scores")
    plt.title("Average CNN Pose Scores with Error Bars")
    plt.grid()

        # Plot 4: Average CNN affinity scores with error bars
    plt.figure()
    plt.errorbar(test_numbers, cnn_affinity_scores_adj, yerr=cnn_affinity_error_adj, fmt='o', capsize=5, elinewidth=2, markeredgewidth=2)
    plt.xlabel("Test Index")
    plt.ylabel("CNN Affinity Scores (Adjusted)")
    plt.title("Average Adjusted CNN Affinity Scores with Error Bars")
    plt.grid()

    # Plot 5: Subplots with affinity and CNN scores corresponding to RMSD
    fig, axs = plt.subplots(3, 1, sharex=True)
    fig.suptitle("Affinity and CNN Scores Corresponding to Lowest RMSD")
    axs[0].scatter(test_numbers, affinity_scores[:, 0], marker='o', edgecolor='k')
    axs[0].set(ylabel="Affinity Scores (kJ/mol)")
    axs[0].grid()

    axs[1].scatter(test_numbers, cnn_pose_scores[:, 0], marker='o', edgecolor='k')
    axs[1].set(ylabel="CNN Pose Scores")
    axs[1].grid()

    axs[2].scatter(test_numbers, cnn_affinity_scores[:, 0], marker='o', edgecolor='k')
    axs[2].set(xlabel="Test Index", ylabel="CNN Affinity Scores")
    axs[2].grid()

    plt.show()

input_file = "minimumRMSDoutput.txt"  # Change this to the name of your input file
data = read_ligand_data(input_file)

file_prefix = "test"
vina_results = []

for i in range(1, 41):
    filename = f"./output/{file_prefix}{i}.txt"
    if os.path.isfile(filename):
        scores = extract_vina_scores(filename)
        avg_score = np.mean(scores)
        std_dev = np.std(scores)
        min_score = np.min(scores)
        max_score = np.max(scores)
        vina_results.append((i, avg_score, std_dev, min_score, max_score))

plot_data(data, vina_results)