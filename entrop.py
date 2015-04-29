#!/usr/bin/python
from nltk.corpus import wordnet as wn
import en
import datetime
import random
import os

#create filename for new novel
#format = entrop_novel_yy_mm_dd_HH_MM_SS
basename = "entrop_novel"
suffix = datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S")

filename = "_".join([basename, suffix])

#find the directory that the script is located in
script_dir = os.path.dirname(os.path.abspath(__file__))
rel_path = script_dir + '/drafts/'

#open new .txt file with filename = filename, write permissions
file = open(os.path.join(rel_path, filename + '.txt'), 'w')

#only article is the 
article = "the"
#list to hold values for the first adjective
adjective_1 = ["quick"]
#list to hold values for the second adjective
adjective_2 = ["brown"]
#list to hold values for the first noun
noun_1 = ["fox"]
#list to hold values for first verb
verb_1 = ["jump"]
#list to hold all values for prepositions (since wordnet can't prep)
preposition = [
    "among", "behind",
    "below", "beside",
    "between", "near",
    "toward", "under",
    "upon", "with",
    "over"
    ]
#list to hold the third adjective
adjective_3 = ["lazy"]
#list to hold the second noun
noun_2 = ["dog"]

#counter for words in novel
word_count = 0

#counter for every (sentence_factor) sentences generated, one is written
sentence_count = 0

#for every... sentences, one is written (choose random int between 1 and 500)
sentence_factor = random.randint(1, 500)

#percentage_chance to generate new word (choose between 0 and 1)
percentage_chance = random.random()

def generate_word(list, pos):
    #% chance to generate new word
    if random.random() < percentage_chance:
        #repeat until word = pos
        while True:
            #get all synsets of random word in list
            synsets = wn.synsets(list[random.randint(0, len(list) - 1)], pos=pos)
            #get random synset
            synset = synsets[random.randint(0, len(synsets) - 1)]
            ran = random.randint(0,3)
            if ran == 0 and synset.hypernyms():
                synset = synset.hypernyms()[random.randint(0, len(synset.hypernyms()) - 1)]
            elif ran == 1 and synset.hyponyms():
                synset = synset.hyponyms()[random.randint(0, len(synset.hyponyms()) - 1)]
            #get random name from synset that does not contain an _ or - (these make the lib go insane)
            #words = the names of the synset
            words = synset.lemma_names()
            #this loop is to make sure an infinite loop does not occur
            #where you are picking from all invalid choices
            while len(words) > 0:
                word = words[random.randint(0, len(words) - 1)]
                if "_" not in word and "-" not in word:
                    break
                else:
                    words.remove(word)
                    continue
            #if words doesn't have words in it, pick a new word from beginning
            if(len(words) == 0):
                continue
            if ((pos == wn.NOUN and en.is_noun(word)) or 
                (pos == wn.VERB and en.is_verb(word)) or
                (pos == wn.ADJ and en.is_adjective(word))):
                
                #fix word based on pos
                #if verb, make sure the verb has a conjugation,
                #if it does, or is not a verb, the word gets appended to the word array,
                #and a word is returned 
                if pos == wn.VERB:
                    try:
                        en.verb.present(word, person=3, negate=False)
                    except KeyError:
                        continue
                    else:
                        if word not in list:
                            list.append(word)
                        return word
                else:
                    if word not in list:
                        list.append(word)
                    return word
    else:
        #just select a random word from the existing ones
        return list[random.randint(0, len(list) - 1)]




def generate_sentence():
    #piece everything together
    sentence = ""
    sentence += article + " "
    sentence += generate_word(adjective_1, pos=wn.ADJ) + " "
    sentence += generate_word(adjective_2, pos=wn.ADJ) + " "
    sentence += generate_word(noun_1, pos=wn.NOUN) + " "
    sentence += en.verb.present(generate_word(verb_1, pos=wn.VERB), person=3, negate=False) + " "
    sentence += preposition[random.randint(0, len(preposition) - 1)] + " "
    sentence += article + " "
    sentence += generate_word(adjective_3, pos=wn.ADJ) + " "
    sentence += generate_word(noun_2, pos=wn.NOUN) + "."
    return sentence
    


#main novel generation

#start with the epitomic sentence
sentence_1 = article + " " + adjective_1[0] + " " + adjective_2[0] + " " + noun_1[0] + " " + \
             en.verb.present(verb_1[0], person=3, negate=False) + " " + \
             preposition[10] + " " + article + " " + \
             adjective_3[0] + " " + noun_2[0] + "."



print "Generating..."
print sentence_factor
print percentage_chance
file.write("entrop.py -- an exercise in randomness\n\n")
file.write("--- metadata ---\n")
file.write("sentence_factor = " + str(sentence_factor) + "\n")
file.write("percentage_chance = " + str(percentage_chance) + "\n")
file.write("----------------\n\n")
file.write(sentence_1 + "\n")
while word_count < 50000:
    sentence = generate_sentence()
    sentence_count += 1
    if sentence_count % sentence_factor == 0:
        file.write(sentence + "\n")
        word_count += len(sentence.split())
file.write("\nFin.")
print "Done."


