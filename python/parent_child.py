#######################################################################################################################
# Developer    : Rohan Tandel
# Description  : Find Ultimate Parent Loan ID for given Loan_id and Parent_Loan_id data assigned in this script
# Execution    : python3 parent_child.py
#######################################################################################################################

import pandas as pd

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

# initialize source data as list of lists (we can also assign more loan ids by uncommenting data variable)
#data = [[100, 600],[200,],[600,200],[300,]]
data = [[100,600],[200,],[600,200],[300,],[400,600],[500,400],[700,500],[800,300],[900,800],[1000,900],[1001,900],[1002,1001],[1003,1002],[1004,1003],[1005,1004]]

# Create the pandas DataFrame
src_df = pd.DataFrame(data, columns=['Loan_id', 'Parent_Loan_id'], dtype='Int64')

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