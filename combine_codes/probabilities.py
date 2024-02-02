import pandas as pd


df = pd.read_csv("used_data.csv")

credit_score_probabilities = df.groupby('Occupation')['Credit_Score'].apply(lambda x: (x == 'Poor').mean()).reset_index()
credit_score_probabilities.columns = ['Occupation', 'Credit_Score_Probability']
df_done = pd.merge(df, credit_score_probabilities, on='Occupation', how='left')

df_done.to_csv()

df.to_csv("done_data.csv", index=False)
