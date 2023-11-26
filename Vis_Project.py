import pandas as pd
import numpy as np
import re

df = pd.read_csv("C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/all_data.csv", delimiter=';')

Columns = df.columns
Cus_ID = df['Customer_ID']


def clean_Age():
    Age = df["Age"]
    Age = pd.to_numeric(Age, errors='coerce')
    disp_indices = np.where(pd.isna(Age).notnull() & ((Age < 0) | (Age > 100)))
    disp_indices = np.asarray(disp_indices)
    nan_indices = np.where(pd.isna(Age))[0]
    indices = np.concatenate((disp_indices,nan_indices), axis=None)

    for i in indices:
       cus_id = Cus_ID[i]
       condition = (Cus_ID == cus_id)
       mode_value = Age[condition].mode().iat[0]
       Age.loc[condition] = mode_value
    Age.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Age.csv')

def clean_SSN():
    SSN = df["SSN"]
    valid_format = r'\d{3}-\d{2}-\d{4}'
    indices = SSN[~SSN.str.contains(valid_format)].index
    indices = np.asarray(indices)
    for i in indices:
       cus_id = Cus_ID[i]
       condition = (Cus_ID == cus_id)
       mode_value = SSN[condition].mode().iat[0]
       df.loc[condition, "SSN"] = mode_value
    SSN = df["SSN"]
    SSN.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/SSN.csv')

def clean_Occupation():
    Occupation = df["Occupation"]
    indices = Occupation[Occupation.eq("_______")].index
    indices = np.asarray(indices)

    for i in indices:
        cus_id = Cus_ID[i]
        condition = (Cus_ID == cus_id)
        mode_value = Occupation[condition].mode().iat[0]
        df.loc[condition, "Occupation"] = mode_value
    Occupation = df["Occupation"]
    Occupation.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Occupation.csv')

def clean_Annual_Income():
    Annual_Income = df["Annual_Income"]
    Annual_Income = pd.to_numeric(Annual_Income.str.replace(',','.'), errors='coerce')
    indices = np.where(pd.isna(Annual_Income))[0]

    for i in indices:
       cus_id = Cus_ID[i]
       condition = (Cus_ID == cus_id)
       mode_value = Annual_Income[condition].mode().iat[0]
       Annual_Income.loc[condition] = mode_value
    Annual_Income.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Annual_Income.csv')

def clean_Monthly_Salary():
    Monthy_Salary = df['Monthly_Inhand_Salary']
    Monthy_Salary = pd.to_numeric(Monthy_Salary.str.replace(',', '.'), errors='coerce')
    indices = np.where(pd.isna(Monthy_Salary))[0]
    for i in indices:
       cus_id = Cus_ID[i]
       condition = (Cus_ID == cus_id)
       mode_value = Monthy_Salary[condition].mode().iat[0]
       Monthy_Salary.loc[condition] = mode_value
    Monthy_Salary.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Monthly_Salary.csv')

def clean_Num_Bank_Accounts():
    Num_Bank_Accounts = df["Num_Bank_Accounts"]
    Num_Bank_Accounts = pd.to_numeric(Num_Bank_Accounts, errors='coerce')
    disp_indices = np.where(pd.isna(Num_Bank_Accounts).notnull() & ((Num_Bank_Accounts < 0) | (Num_Bank_Accounts > 100)))
    disp_indices = np.asarray(disp_indices)
    nan_indices = np.where(pd.isna(Num_Bank_Accounts))[0]
    indices = np.concatenate((disp_indices,nan_indices), axis=None)

    for i in indices:
       cus_id = Cus_ID[i]
       condition = (Cus_ID == cus_id)
       mode_value = Num_Bank_Accounts[condition].mode().iat[0]
       Num_Bank_Accounts.loc[condition] = mode_value
    Num_Bank_Accounts.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Num_Bank_Accounts.csv')

def clean_Num_Credit_Card():
    Num_Credit_Card = df["Num_Credit_Card"]
    Num_Credit_Card = pd.to_numeric(Num_Credit_Card, errors='coerce')
    disp_indices = np.where(pd.isna(Num_Credit_Card).notnull() & ((Num_Credit_Card < 0) | (Num_Credit_Card > 100)))
    disp_indices = np.asarray(disp_indices)
    nan_indices = np.where(pd.isna(Num_Credit_Card))[0]
    indices = np.concatenate((disp_indices,nan_indices), axis=None)

    for i in indices:
       cus_id = Cus_ID[i]
       condition = (Cus_ID == cus_id)
       mode_value = Num_Credit_Card[condition].mode().iat[0]
       Num_Credit_Card.loc[condition] = mode_value
    Num_Credit_Card.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Num_Credit_Card.csv')


def clean_Interest_Rate():
    Interest_Rate = df["Interest_Rate"]
    Interest_Rate = pd.to_numeric(Interest_Rate, errors='coerce')
    disp_indices = np.where(pd.isna(Interest_Rate).notnull() & ((Interest_Rate < 0) | (Interest_Rate > 100)))
    disp_indices = np.asarray(disp_indices)
    nan_indices = np.where(pd.isna(Interest_Rate))[0]
    indices = np.concatenate((disp_indices,nan_indices), axis=None)

    for i in indices:
        cus_id = Cus_ID[i]
        condition = (Cus_ID == cus_id)
        mode_value = Interest_Rate[condition].mode().iat[0]
        Interest_Rate.loc[condition] = mode_value
    Interest_Rate.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Interest_Rate.csv')



def clean_Num_Of_Loan():
    Num_Of_Loan = df["Num_of_Loan"]
    Num_Of_Loan = pd.to_numeric(Num_Of_Loan , errors='coerce')
    disp_indices = np.where(pd.isna(Num_Of_Loan).notnull() & ((Num_Of_Loan  < 0) | (Num_Of_Loan  > 100)))
    disp_indices = np.asarray(disp_indices)
    nan_indices = np.where(pd.isna(Num_Of_Loan))[0]
    indices = np.concatenate((disp_indices, nan_indices), axis=None)

    for i in indices:
        cus_id = Cus_ID[i]
        condition = (Cus_ID == cus_id)
        mode_value = Num_Of_Loan [condition].mode().iat[0]
        Num_Of_Loan .loc[condition] = mode_value
    Num_Of_Loan .to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Num_Of_Loan.csv')


def clean_Num_Of_Delayed_Payment():
    Num_Of_Delayed_Payment = df["Num_of_Delayed_Payment"]
    Num_Of_Delayed_Payment = pd.to_numeric(Num_Of_Delayed_Payment, errors='coerce')
    disp_indices = np.where(pd.isna(Num_Of_Delayed_Payment).notnull() & ((Num_Of_Delayed_Payment < 0) | (Num_Of_Delayed_Payment > 100)))
    disp_indices = np.asarray(disp_indices)
    nan_indices = np.where(pd.isna(Num_Of_Delayed_Payment))[0]
    indices = np.concatenate((disp_indices, nan_indices), axis=None)

    for i in indices:
        cus_id = Cus_ID[i]
        condition = (Cus_ID == cus_id)
        mode_value = Num_Of_Delayed_Payment[condition].mode().iat[0]
        Num_Of_Delayed_Payment.loc[condition] = mode_value
    Num_Of_Delayed_Payment.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Num_Of_Delayed_Payment.csv')


def clean_Changed_Credit_Limit():
    Changed_Credit_Limit = df["Changed_Credit_Limit"]
    Changed_Credit_Limit = pd.to_numeric(Changed_Credit_Limit.str.replace(',','.'), errors='coerce')
    disp_indices = np.where(pd.isna(Changed_Credit_Limit).notnull() & ((Changed_Credit_Limit < 0) | (Changed_Credit_Limit > 100)))
    disp_indices = np.asarray(disp_indices)
    nan_indices = np.where(pd.isna(Changed_Credit_Limit))[0]
    indices = np.concatenate((disp_indices, nan_indices), axis=None)

    for i in indices:
       cus_id = Cus_ID[i]
       condition = (Cus_ID == cus_id)
       mode_value = Changed_Credit_Limit[condition].mode().iat[0]
       Changed_Credit_Limit.loc[condition] = mode_value
    Changed_Credit_Limit.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Changed_Credit_Limit.csv')

def clean_Credit_Inquiries():
    Num_Credit_Inquiries = df["Num_Credit_Inquiries"]
    Num_Credit_Inquiries = pd.to_numeric(Num_Credit_Inquiries, errors='coerce')
    disp_indices = np.where(pd.isna(Num_Credit_Inquiries).notnull() & ((Num_Credit_Inquiries < 0) | (Num_Credit_Inquiries > 100)))
    disp_indices = np.asarray(disp_indices)
    nan_indices = np.where(pd.isna(Num_Credit_Inquiries))[0]
    indices = np.concatenate((disp_indices, nan_indices), axis=None)

    for i in indices:
        cus_id = Cus_ID[i]
        condition = (Cus_ID == cus_id)
        mode_value = Num_Credit_Inquiries[condition].mode().iat[0]
        Num_Credit_Inquiries.loc[condition] = mode_value
    Num_Credit_Inquiries.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Num_Credit_Inquiries.csv')

def clean_Credit_Mix():
    Credit_Mix = df["Credit_Mix"]
    indices = Credit_Mix[Credit_Mix.eq("_")].index
    indices = np.asarray(indices)

    for i in indices:
        cus_id = Cus_ID[i]
        condition = (Cus_ID == cus_id)
        mode_value = Credit_Mix[condition].mode().iat[0]
        df.loc[condition, "Credit_Mix"] = mode_value
    Credit_Mix = df["Credit_Mix"]
    Credit_Mix.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Credit_Mix.csv')

def clean_Outstanding_Debt():
    Outstanding_Debt = df['Outstanding_Debt']
    Outstanding_Debt = pd.to_numeric(Outstanding_Debt.str.replace(',', '.'), errors='coerce')
    indices = np.where(pd.isna(Outstanding_Debt))[0]
    for i in indices:
        cus_id = Cus_ID[i]
        condition = (Cus_ID == cus_id)
        mode_value = Outstanding_Debt[condition].mode().iat[0]
        Outstanding_Debt.loc[condition] = mode_value
    Outstanding_Debt.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Outstanding_Debt.csv')

def clean_Credit_Utilization_Ratio():
    Credit_Utilization_Ratio = df['Credit_Utilization_Ratio']
    Credit_Utilization_Ratio = pd.to_numeric(Credit_Utilization_Ratio.str.replace(',','.'))
    Credit_Utilization_Ratio.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Credit_Utilization_Ratio.csv')

def clean_Payment_of_Min_Amount():
    Payment_of_Min_Amount = df["Payment_of_Min_Amount"]
    indices = Payment_of_Min_Amount[Payment_of_Min_Amount.eq("NM")].index
    indices = np.asarray(indices)

    for i in indices:
        cus_id = Cus_ID[i]
        condition = (Cus_ID == cus_id)
        mode_value = Payment_of_Min_Amount[condition].mode().iat[0]
        df.loc[condition, "Payment_of_Min_Amount"] = mode_value
    Payment_of_Min_Amount = df["Payment_of_Min_Amount"]
    Payment_of_Min_Amount.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Payment_of_Min_Amount.csv')

def clean_Total_EMI_per_month():
    Total_EMI_per_month = df["Total_EMI_per_month"]
    Total_EMI_per_month = pd.to_numeric(Total_EMI_per_month.str.replace(',', '.'))
    Total_EMI_per_month.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Total_EMI_per_month.csv')

clean_Total_EMI_per_month()

def clean_Amount_invested_monthly():
    Amount_invested_monthly = df["Amount_invested_monthly"]
    Amount_invested_monthly = pd.to_numeric(Amount_invested_monthly.str.replace(',', '.'), errors='coerce')
    nan_indices = np.where(pd.isna(Amount_invested_monthly))[0]
    for i in nan_indices:
        cus_id = Cus_ID[i]
        condition = (Cus_ID == cus_id)
        mode_value = Amount_invested_monthly[condition].mode().iat[0]
        Amount_invested_monthly.loc[condition] = mode_value

    Amount_invested_monthly.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Amount_invested_monthly.csv')

def clean_Payment_Behaviour():
    Payment_Behaviour = df["Payment_Behaviour"]
    pattern = re.compile(r'^[A-Za-z]+_[A-Za-z]+_[A-Za-z]+_[A-Za-z]+$')

    for i in range(150000):
        if pattern.match(Payment_Behaviour[i]):
            Payment_Behaviour[i] = ""

def clean_Monthly_Balance():
    Monthly_Balance = df['Monthly_Balance']
    Monthly_Balance = pd.to_numeric(Monthly_Balance.str.replace(',', '.'), errors='coerce')
    nan_indices = np.where(pd.isna(Monthly_Balance))[0]
    for i in nan_indices:
        cus_id = Cus_ID[i]
        condition = (Cus_ID == cus_id)
        mode_value = Monthly_Balance[condition].mode().iat[0]
        Monthly_Balance.loc[condition] = mode_value

    Monthly_Balance.to_csv('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/Monthly_Balance.csv')

clean_Monthly_Balance()
