import pandas as pd

# Load data from pickle file
data_list = pd.read_pickle('modified_data.pkl')

# Convert list of dictionaries to DataFrame
data_df = pd.DataFrame(data_list)

# Convert DataFrame to Excel
data_df.to_excel('output_cleaned_data.xlsx', index=False)