# import pickle
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_table

# Load the modified data from the file
# with open("final_cleaned_data.xlsx", "r") as file:
#     data = ?.load(file)
#
# # Filter data starting from the 50002nd row where credit scores are not None
# filtered_data = [entry for entry in data[50001:] if entry['Credit_Score'] is not None]
df = pd.read_excel("final_cleaned_data.xlsx")

# Calculate average outstanding debt per occupation and age of credit history
avg_debt_per_occupation_age = df.groupby(['Occupation', 'Credit_History_Age']).agg({
    'Outstanding_Debt': 'mean',
    'Age': 'mean',
    'Annual_Income': 'mean',
    'Credit_Utilization_Ratio': 'mean',
    'Credit_Score': lambda x: x.value_counts().idxmax()  # Most frequent credit score
}).reset_index()

# Convert min and max values to integers
min_age = int(df['Credit_History_Age'].min())
max_age = int(df['Credit_History_Age'].max())

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H1("Analysis Dashboard for students"),
    html.P("Task Abstraction: I want to explore the relationship between outstanding debts, occupations, and the age of credit history. Specifically, I am interested in understanding how different occupations impact debts and how this relationship varies with the age of credit history. I prefer an interactive visualization using the Dash framework to provide a dynamic and insightful exploration of the data."),
    html.P("Additional Information for the Dashboard: Data Source: The data is derived from financial records, focusing on individuals in the fields of Finance, Economics, Business Analytics, or Data Science."),
    html.P("Visualization Components: Y-Axis (Vertical): Average outstanding debt, X-Axis (Horizontal): Occupation, Third Variable (Interactive): Age of Credit History. Starting Point: Data from the 50002nd row onward will be considered, as credit score values are available and reliable from this point."),
    html.P("Interactivity: Users can interact with the dashboard to dynamically explore how different occupations influence credit scores and observe how this relationship changes with the age of credit history."),
    html.Div([
        html.Label("Select Age of Credit History:"),
        dcc.Slider(
            id='credit-age-slider',
            min=min_age,
            max=max_age,
            step=1,
            marks={i: str(i) for i in range(min_age, max_age + 1)},
            value=min_age,
        ),
    ]),
    dcc.Graph(id='credit-score-graph'),
    html.Div(id='page-content'),
])

# Define callback to update the graph based on user input
@app.callback(
    Output('credit-score-graph', 'figure'),
    [Input('credit-age-slider', 'value')]
)
def update_graph(selected_age):
    filtered_df = avg_debt_per_occupation_age[avg_debt_per_occupation_age['Credit_History_Age'] == selected_age]

    figure = {
        'data': [
            {
                'x': filtered_df['Occupation'],
                'y': filtered_df['Outstanding_Debt'],
                'type': 'bar',
                'name': 'Average Debt per Occupation',
                'text': [f"{occ} - Age: {selected_age} Years" for occ in filtered_df['Occupation']],
            },
        ],
        'layout': {
            'title': f'Average Outstanding Debt by Occupation (Age of Credit History: {selected_age} Years)',
            'xaxis': {'title': 'Occupation'},
            'yaxis': {'title': 'Average Outstanding Debt'},
            'clickmode': 'event+select',
        }
    }

    return figure

# Define callback to handle redirection
@app.callback(
    Output('page-content', 'children'),
    [Input('credit-score-graph', 'clickData'),
     Input('credit-age-slider', 'value')]
)
def display_selected_data(click_data, selected_age):
    if click_data:
        selected_occupation_index = click_data['points'][0]['pointIndex']
        selected_occupation = click_data['points'][0]['text'].split('-')[0].strip()
        selected_data = avg_debt_per_occupation_age[
            (avg_debt_per_occupation_age['Occupation'] == selected_occupation) &
            (avg_debt_per_occupation_age['Credit_History_Age'] == selected_age)
        ].iloc[0]

        # Create a DataTable for the selected occupation data
        table_data = [
            {'Metric': 'Average Outstanding Debt', 'Value': selected_data['Outstanding_Debt']},
            {'Metric': 'Average Age', 'Value': selected_data['Age']},
            {'Metric': 'Average Annual Income', 'Value': selected_data['Annual_Income']},
            {'Metric': 'Credit Utilization Ratio', 'Value': selected_data['Credit_Utilization_Ratio']},
            {'Metric': 'Frequency of Good Credit Score', 'Value': selected_data['Credit_Score']},
        ]

        return html.Div([
            html.H2(f"Occupation: {selected_occupation} - Age of credit history: {selected_age} Years"),
            dash_table.DataTable(
                id='selected-data-table',
                columns=[{'name': 'Metric', 'id': 'Metric'}, {'name': 'Value', 'id': 'Value'}],
                data=table_data,
            )
        ])

    return html.Div()

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)