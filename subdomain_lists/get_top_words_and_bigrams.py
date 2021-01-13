#get_top_words_and_bigrams.py

#source data: https://www.cs.utexas.edu/~gdurrett/courses/fa2020/nyt.txt

import pandas as pd
import nltk
from nltk.tokenize import RegexpTokenizer


common_word_subdomains = []

#read in text data
string = open('nyt.txt', 'r').read().lower()

#tokenize it (this flavor ignores punctuation)
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(string)

#get list of bigrams from the tokens list
bigrams_list = list(nltk.bigrams(tokens))
bifreq = nltk.FreqDist(bigrams_list)


#Top 500 individual words (excluding numbers and single-word tokens)
top_words = unifreq.most_common(500)
for word in top_words:
    word = word[0]
    if len(word)>1 and not word.isnumeric():
        common_word_subdomains.append(word)

#Top 100 bigrams        
top_bigrams = bifreq.most_common(100)
for bigram in top_bigrams:
    bigram = bigram[0][0]+bigram[0][1]
    common_word_subdomains.append(bigram)
    
#write output to CSV
pd.DataFrame(common_word_subdomains).to_csv("common_words_and_bigrams.csv",index=False,header=['name'])

# common_words_and_bigrams.csv is what we need to add to the database. Upload it to file manager in cPanel and run 

'''
from mysql_utils import *
AddCSVToBlacklist('common_words_and_bigrams.csv')

'''