import pandas as pd

excel_file_path = 'used_data.xlsx'

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file_path)

# Replace 'output_csv_file.csv' with the desired name for your CSV file
csv_file_path = 'used_data.csv'

# Write the DataFrame to a CSV file
df.to_csv(csv_file_path, index=False)

print(f"Conversion completed. CSV file saved at: {csv_file_path}")
