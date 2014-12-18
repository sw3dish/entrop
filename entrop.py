#!/usr/bin/python

from nltk.corpus import wordnet as wn
import datetime

#create filename for new novel
#format = entrop_novel_yy_mm_dd_HH_MM_SS
basename = "entrop_novel"
suffix = datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S")

filename = "_".join(basename, suffix)
#open new .txt file with filename = filename, write permissions
file = open(filename + ".txt", w)

#list to hold values for the first adjective
adjective_1 = ["quick"]
#list to hold values for the second adjective
adjective_2 = ["brown"]
#list to hold values for the first noun
noun_1 = ["fox"]
#list to hold values for first verb
verb_1 = ["jumps"]


#counter for words in novel
word_count = 0

while word_count < 50000:
    file.write(generate_sentence() + "\n")

file.write("\nFin.")


