"""
Script to calculate the frequency of each letter at each position across all words
in the english dictionary

Words are taken from: https://github.com/dwyl/english-words
"""
import json
import matplotlib.pyplot as plt

import numpy as np
from numpy import inf
import seaborn as sns
from string import ascii_lowercase

# Read in the words
with open('alpha_words.txt', 'r') as in_file:
    words = [line.strip().lower() for line in in_file]
longest_word = max(words, key=len)

"""
Create a matrix of n letters * n characters in the longest word.
Fill the matrix by counting the occurrence of each letter at their given position
"""
freq_matrix = np.zeros((len(ascii_lowercase), len(longest_word)), np.int)
letter_idx = {letter: idx for idx, letter in enumerate(ascii_lowercase)}
for word in words:
    for i, letter in enumerate(word):
        freq_matrix[letter_idx[letter], i] += 1

# Convert the freq matrix to log
log_10 = np.log10(freq_matrix)
log_10[log_10 == -inf] = 0
sns.heatmap(log_10)
plt.show()

# Save the data as a JSON
with open('letter_occupancy.json', 'w') as out_json:
    data = {
        'data': [
            {
                'letter': ascii_lowercase[i],
                'occupancy': row.tolist()
            } for i, row in enumerate(log_10)
        ]
    }
    json.dump(data, out_json)
