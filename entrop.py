#!/usr/bin/python
from nltk.corpus import wordnet as wn
import en
import datetime
import random

#create filename for new novel
#format = entrop_novel_yy_mm_dd_HH_MM_SS
basename = "entrop_novel"
suffix = datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S")

filename = "_".join([basename, suffix])
#open new .txt file with filename = filename, write permissions
file = open(filename + '.txt', 'w')

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


def generate_word(list, pos):
    #33% chance to generate new word
    if random.randint(0,2) == 0:
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
            while True:
                word = synset.lemma_names()[random.randint(0, len(synset.lemma_names()) - 1)]
                if "_" not in word and "-" not in word:
                    break

            if ((pos == wn.NOUN and en.is_noun(word)) or 
                (pos == wn.VERB and en.is_verb(word)) or
                (pos == wn.ADJ and en.is_adjective(word))):
                
                #fix word based on pos
                #if verb, make sure the verb has a conjugation, 
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
file.write(sentence_1 + "\n")
while word_count < 50000:
    sentence = generate_sentence()
    file.write(sentence + "\n")
    word_count += len(sentence.split())
file.write(', '.join(adjective_1) + "\n")
file.write("\nFin.")
print "Done."


