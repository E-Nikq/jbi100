import csv
import pandas as pd
from typing import List, Dict


# important columns: Month, Age, Annual_Income, Monthly_Inhand_Salary, Num_Bank_Accounts, Num_Credit_Card, Interest_Rate
#Num_of_Loan, Type_of_Loan, Delay_from_due_date, Num_of_Delayed_Payment, Changed_Credit_Limit, Num_Credit_Inquiries, Credit_Mix
# Outstanding_Debt, Credit_Utilization_Ratio, Credit_History_Age, Payment_of_Min_Amount, Total_EMI_per_month, Amount_invested_monthly
# Payment_Behaviour, Monthly_Balance


list_of_dicts: List[Dict[any, any]] = []

with open("all_data.csv", "r", newline='') as file:
    reader = csv.DictReader(file, delimiter=";")
    for row in reader:
        try:
            row["Age"] = int(row["Age"])
        except:
            pass
        if type(row["Age"]) == int:
            pass
        else:
            print(type(row["Age"]))
        list_of_dicts.append(row)











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