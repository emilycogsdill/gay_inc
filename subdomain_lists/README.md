# Blacklist

- Full names of famous people
- Hate speech
- Details below

# Whitelist

- Domains people can sign up for without needing a special request
- Common words, phrases, names
- The most common of these shall be PREMIUM subdomains

## Premium subdomains

- First names ()
- Most common last names
- Common nouns

### Top first names

Source: https://raw.githubusercontent.com/hadley/data-baby-names/master/baby-names.csv

Take baby names given to >0.05% of population (split by sex) in any year 1980 or later

### Top last names

Top 100 surnames according to https://www.thoughtco.com/most-common-us-surnames-1422656

### Top unigrams and bigrams (based on NYT.com data, thanks Eric)

https://www.cs.utexas.edu/~gdurrett/courses/fa2020/nyt.txt

# Reserved subdomains

- From google sheet.
- These are subdomains that we, Gay Inc., have plans to use for... purposes


# Extracting lists of famous people from Wikipedia

1) Enter categories into this tool https://petscan.wmflabs.org/. Configure it to go 10 levels deep to scrape up items in lists in all subcategories.

- American_actors
- Lists_of_heads_of_government
- Lists_of_heads_of_state
- Lists_of_current_office-holders

2) export to CSV

3) Post-processing (remove underscores, and any disambiguating terms like "(American actor)")

4) Concatenate CSVs and deduplicate names

5) Add those names to the "hosts" database with type "blacklist"



# To add list from a CSV to the blacklist:

After the post-processing described above, we will arrive at a single CSV to add to the blacklist.

```

#AddNamesToTable(db_table_string,path_to_csv) 

#e.g.:
from mysql_utils import *

AddNamesToTable('blacklist','blacklist/actor_names.csv') 

```