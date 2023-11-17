import pandas as pd

credit_data = pd.read_csv("all_data.csv", delimiter=";")


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