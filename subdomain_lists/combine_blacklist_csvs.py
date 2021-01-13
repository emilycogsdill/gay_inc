import os
import glob
import re
import pandas as pd
import itertools


def ProcessCSV(file):

    df = pd.read_csv(file, error_bad_lines=False)
    
    #extract names from the "title" field
    names = df['title']
    
    #lowercase and remove underscores
    names = [name.lower().split('(')[0] for name in names]
    
    #remove any non-alphanumeric characters
    names = [re.sub(r'[\W_]+', '', name).lower() for name in names]
    
    #write to csv in "processed" directory
    processed_directory = file.split('to_process')[0]+'processed/'
    processed_filename = file.split('/')[-1]
    pd.DataFrame(names).to_csv(processed_directory+processed_filename,index=False,header=['name'])


def main():
    #Once the function is ready, iterate it over the csv files in /to_process/
    csv_files = glob.glob(os.getcwd()+'/csvs/to_process/*.csv')
    
    for file in csv_files:   
        ProcessCSV(file)
        
    #take all the names in the processed CSVs and add them to a single big damn list
    
    full_names_list = []
    
    processed_csvs = glob.glob(os.getcwd()+'/csvs/processed/*.csv')
    
    for file in processed_csvs:   
        names = pd.read_csv(file, error_bad_lines=False)['name']
        full_names_list.append(names)
        
    
    #flatten the list so that instead of a list of lists it's just a list
    full_names_list=list(itertools.chain.from_iterable(full_names_list))
    
    #remove any that have "list" in the name
    final_names_list = [x for x in full_names_list if 'list' not in str(x)]
    
    #write to csv in "combined" directory
    combined_directory = file.split('processed')[0]+'combined/'
    pd.DataFrame(final_names_list).to_csv(combined_directory+'combined.csv',index=False,header=['name'])        


if __name__ == "__main__":
    main()
