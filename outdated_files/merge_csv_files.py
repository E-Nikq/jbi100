# import pandas as pd
#
# List of CSV file names to merge
folder = "csv_files_per_column"
file_paths = [f'{folder}/Age.csv', f'{folder}/Amount_invested_monthly.csv', f'{folder}/Annual_income.csv', f'{folder}/Changed_Credit_Limit.csv',
              f'{folder}/Credit_Mix.csv', f'{folder}/Interest_Rate.csv', f'{folder}/Monthly_Salary.csv', f'{folder}/Num_Bank_Accounts.csv',
              f'{folder}/Num_Credit_Card.csv', f'{folder}/Num_Credit_Inquiries.csv', f'{folder}/Num_Of_Delayed_Payment.csv', f'{folder}/Num_Of_Loan.csv',
              f'{folder}/Occupation.csv', f'{folder}/Outstanding_Debt.csv', f'{folder}/Payment_of_Min_Amount.csv',
              f'{folder}/SSN.csv', "modified_data_clean.csv"]

#
# # Create an empty list to store DataFrames
# dfs = []
#
# # Iterate through each file and append its data to the dfs list
# for file_name in file_names:
#     # Read each CSV file into a DataFrame
#     data = pd.read_csv(file_name)
#
#     # Append the DataFrame to the list
#     dfs.append(data)
#
# # Concatenate the list of DataFrames into a single DataFrame
# merged_data = pd.concat(dfs, ignore_index=True)
#
# # Write the merged data to a new CSV file
# merged_data.to_csv('merged_file.csv', index=False)


# # Create an empty DataFrame to store the merged data
# merged_data = pd.DataFrame()
#
# # Iterate through each file and append its data to the merged_data DataFrame
# for file_name in file_names:
#     # Read each CSV file into a DataFrame
#     data = pd.read_csv(file_name)
#
#     # Append the data to the merged_data DataFrame
#     merged_data = merged_data.append(data, ignore_index=True)
#
# # Write the merged data to a new CSV file
# merged_data.to_csv('merged_file.csv', index=False)
#
# import pandas as pd
#
# df = pd.read_csv("merged_file.csv")
# # df.to_excel("merged.xlsx", index=False)
# df.head(5)

import pandas as pd



merged_df = None

# Iterate through each file path and merge the datasets
for file_path in file_paths:
    # Read the dataset from the file
    current_df = pd.read_csv(file_path)

    # Merge the current dataset with the accumulated result
    if merged_df is None:
        merged_df = current_df
    else:
        merged_df = pd.concat([merged_df, current_df], axis=1)

# Display the merged DataFrame
print(merged_df)

merged_df.to_excel("merged_file_good.xlsx")

# import pandas as pd
# import pickle
#
# with open("modified_data.pkl", "rb") as file:
#     data = pickle.load(file)
#
# df = pd.DataFrame(data)
#
# df.to_csv("modified_data_clean.csv")

