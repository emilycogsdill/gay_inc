#top_first_and_last_names.py

'''
# PREMIUM subdomains

1) common words and bigrams (see get_top_words_and_bigrams.py)

2) most common first names and last names



### Top first names

Source: https://raw.githubusercontent.com/hadley/data-baby-names/master/baby-names.csv

Take baby names given to >0.05% of population (split by sex) in any year 1980 or later

### Top last names

Top 100 surnames according to https://www.thoughtco.com/most-common-us-surnames-1422656
'''

import os
import glob
import re
import pandas as pd
import itertools

#Process the names lists

first_names_df = pd.read_csv(os.getcwd()+'/to_process/first-names.csv')
last_names_df = pd.read_csv(os.getcwd()+'/to_process/last-names.csv')

first_names = [str(x).lower() for x in first_names_df['name']]
last_names = [str(x).lower() for x in last_names_df['name']]
all_top_names = first_names + last_names

#write to CSV (this is what we upload to the hosts table as "premium" subdomains)
pd.DataFrame(all_top_names).to_csv('all_top_names.csv',index=False,header=['name'])    