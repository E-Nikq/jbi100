import csv
import pandas as pd
from typing import List, Dict
import re
import pickle

# important columns: Month, Age, Annual_Income, Monthly_Inhand_Salary, Num_Bank_Accounts, Num_Credit_Card, Interest_Rate
# ...,Num_of_Loan, Type_of_Loan, Delay_from_due_date, Num_of_Delayed_Payment, Changed_Credit_Limit, Num_Credit_Inquiries, Credit_Mix
# ...,Outstanding_Debt, Credit_Utilization_Ratio, Credit_History_Age, Payment_of_Min_Amount, Total_EMI_per_month, Amount_invested_monthly
# ...,Payment_Behaviour, Monthly_Balance
def clean_value(value, data_type):
    """
    Cleans and converts the value based on the specified data type.
    """
    value_str = str(value).strip()

    if not value_str:
        return None  # Return None for empty strings

    if data_type == 'int':
        # Extract only digits from the value
        cleaned_value = int(''.join(filter(str.isdigit, value_str)))
    elif data_type == 'float':
        # Remove commas, replace invalid characters, and convert to float
        cleaned_value = None
        try:
            cleaned_value = float(re.sub(r'[^\d.]', '', value_str))
        except ValueError:
            pass
    elif data_type == 'str':
        # Remove leading/trailing whitespaces
        cleaned_value = value_str
    else:
        cleaned_value = value_str  # No specific cleaning for other data types

    return cleaned_value

file_path = 'outdated_files/all_data.csv'

# Initialize an empty list to store dictionaries
list_of_dicts = []

# Open the CSV file and read it into a list of dictionaries
with open(file_path, mode='r', newline='') as file:
    reader = csv.DictReader(file, delimiter=';')  # Specify the delimiter
    for row in reader:
        # Clean each column in the row
        cleaned_row = {}
        for key, value in row.items():
            if key == 'Age':
                cleaned_row[key] = clean_value(value, 'int')
            elif key in ['Annual_Income', 'Monthly_Inhand_Salary', 'Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate', 'Num_of_Loan', 'Num_of_Delayed_Payment', 'Changed_Credit_Limit', 'Num_Credit_Inquiries', 'Outstanding_Debt', 'Credit_Utilization_Ratio', 'Total_EMI_per_month', 'Amount_invested_monthly', 'Monthly_Balance']:
                cleaned_row[key] = clean_value(value, 'float')
            else:
                cleaned_row[key] = clean_value(value, 'str')

        # Add the cleaned row dictionary to the list
        list_of_dicts.append(cleaned_row)



# import pickle
#
# with open('cleaned_data.pkl', 'wb') as file:
#     pickle.dump(list_of_dicts, file)

# credit_data = pd.read_csv("all_data.csv", delimiter=";")

#IF YOU OPEN A NEW PYTHON FILE AND WANT TO USE THE credit_data, THEN WRITE THE FOLLOWING IN YOUR PYTHON FILE:
    # from data_loader.py import credit_data

#uncomment the following for more specific information.
# print(credit_data.info())
# print(credit_data.describe())
# print(credit_data.head())
# print(credit_data.shape)
# print(credit_data.index)
# print(credit_data.columns)
# print(credit_data.dtypes)
# print(credit_data)

# pd.plotting.scatter_matrix(credit_data[["age", "Annual_Income", "Monthly_Inhand_Salary", "Num_Bank_Accounts","Num_Credit_Card", "Interest_Rate", "Num_of_Loan", "Delay_from_due_date",
#                                         "Num_of_Delayed_Payment", "Changed_Credit_Limit", "Num_Credit_Inquiries",
#                                         "Outstanding_Debt", "Credit_Utilization_Ratio", "Total_EMI_per_month",
#                                         "Amount_invested_monthly", "Monthly_Balance"]], diagonal="kde", figsize=(10, 10))
