#######################################################################################################################
# Developer    : Rohan Tandel
# Description  : Find Ultimate Parent Loan ID for given Loan_id and Parent_Loan_id data in file
# Execution    : python3 parent_child_load_csv.py --file 'file_path'
#              : ex - python3 parent_child_load_csv.py --file '/Users/rohantandel/Downloads/Zions/python/Loan_data.csv'
#######################################################################################################################

import pandas as pd
import argparse
import os

# Recursive function to find ultimate parent loan id
def find_ult_prnt_loan_id(pl_id):
   rec_df = trgt_df[trgt_df['Loan_id'] == pl_id]

   if not rec_df.empty:
       ln_id = rec_df['Parent_Loan_id'].values[0]
       if not pd.isna(ln_id):
           find_ult_prnt_loan_id(ln_id)
       else:
           trgt_df.loc[counter,'Ultimate_Parent_Loan_ID'] = rec_df['Loan_id'].values[0]

# Function to load data into the database
def load_into_database(target_dataframe):
    pass
    # we can add code here to load data into database


# Create parser to read arguments
parser = argparse.ArgumentParser()
parser.add_argument('--file', help='CSV file path')
args = parser.parse_args()
options = vars(args)
file_path = options['file']

# Check if provided file path is valid
if not os.path.isfile(file_path):
   print('{} is not a valid file.'.format(file_path))
   quit(1)

# Create the pandas DataFrame using csv file
src_df = pd.read_csv(file_path, dtype={'Loan_id':'Int64','Parent_Loan_id':'Int64'})

# Create target dataframe using source dataframe and adding new column
trgt_df = src_df.assign(Ultimate_Parent_Loan_ID=None)

# Loop through all the rows in the dataframe
for i in range(0,trgt_df.shape[0]):
   prnt_ln_id = trgt_df['Parent_Loan_id'][i]
   counter = i

   # if parent loan id is present find the ultimate parent loan id
   # else assign loan id as ultimate customer parent loan id
   if not pd.isna(prnt_ln_id):
       find_ult_prnt_loan_id(prnt_ln_id)
   else:
    trgt_df.loc[counter,'Ultimate_Parent_Loan_ID'] = trgt_df['Loan_id'][counter]

# Print the source
print('\nSource:')
print(src_df.to_string(index=False).replace('<NA>','null'))

# Print final output
print('\nTarget:')
print(trgt_df.to_string(index=False).replace('<NA>','null'))

# Load data into database
load_into_database(trgt_df)