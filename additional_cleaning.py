import pickle

# Load the data from the file
with open("outdated_files/cleaned_data.pkl", "rb") as file:
    data = pickle.load(file)

# Iterate through each dictionary in the list
for entry in data:
    # Check if Monthly_Balance is not None before division
    if entry['Monthly_Balance'] is not None:
        entry['Monthly_Balance'] /= 10**7

    # Check if Amount_invested_monthly is not None before division
    if entry['Amount_invested_monthly'] is not None:
        entry['Amount_invested_monthly'] /= 10**6  # Updated to move 2 places to the right

    # Check if Total_EMI_per_month is not None before division
    if entry['Total_EMI_per_month'] is not None:
        entry['Total_EMI_per_month'] /= 10**8

    # Check if Credit_Utilization_Ratio is not None before division
    if entry['Credit_Utilization_Ratio'] is not None:
        entry['Credit_Utilization_Ratio'] /= 10**8  # Updated to move 1 place to the left

    # Check if Outstanding_Debt is not None before division
    if entry['Outstanding_Debt'] is not None:
        entry['Outstanding_Debt'] /= 10**2

    # Check if Changed_Credit_Limit is not None before division
    if entry['Changed_Credit_Limit'] is not None:
        entry['Changed_Credit_Limit'] /= 10**2

    # Check if Monthly_Inhand_Salary is not None before division
    if entry['Monthly_Inhand_Salary'] is not None:
        entry['Monthly_Inhand_Salary'] /= 10**6

    entry['Annual_Income'] /= 10**2

    # Convert Credit_History_Age to an integer
    if entry['Credit_History_Age'] is not None and isinstance(entry['Credit_History_Age'], str):
        age_parts = entry['Credit_History_Age'].split(' ')
        if age_parts[0].isdigit():
            entry['Credit_History_Age'] = int(age_parts[0])

# Save the modified data to a new file
with open("outdated_files/modified_data.pkl", "wb") as file:
    pickle.dump(data, file)