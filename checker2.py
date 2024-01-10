import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd

# Load the modified data from the file
df = pd.read_excel("outdated_files/final_cleaned_data_new.xlsx")

# Calculate average outstanding debt per occupation and age of credit history
def most_frequent_credit_score(x):
    if not x.empty:
        value_counts = x.value_counts()
        if not value_counts.empty:
            return value_counts.idxmax()
    return None

avg_debt_per_occupation_age = df.groupby(['Occupation', 'Credit_History_Age']).agg({
    'Outstanding_Debt': 'mean',
    'Age': 'mean',
    'Annual_Income': 'mean',
    'Credit_Utilization_Ratio': 'mean',
    'Credit_Score': most_frequent_credit_score  # Use the defined function
}).reset_index()

# Convert min and max values to integers
min_age = int(df['Credit_History_Age'].min())
max_age = int(df['Credit_History_Age'].max())

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    style={'backgroundColor': 'black'},
    children=[
    dcc.Location(id='url', refresh=False),
    html.H1("Analysis Dashboard for students", style={'color': 'orange'}),
    html.P("Task Abstraction: I want to explore the relationship between outstanding debts, occupations, and the age of credit history. Specifically, I am interested in understanding how different occupations impact debts and how this relationship varies with the age of credit history. I prefer an interactive visualization using the Dash framework to provide a dynamic and insightful exploration of the data.", style={'color': 'white'}),
    html.P("Additional Information for the Dashboard: Data Source: The data is derived from financial records, focusing on individuals in the fields of Finance, Economics, Business Analytics, or Data Science.", style={'color': 'white'}),
    html.P("Visualization Components: Y-Axis (Vertical): Average outstanding debt, X-Axis (Horizontal): Occupation, Third Variable (Interactive): Age of Credit History. Starting Point: Data from the 50002nd row onward will be considered, as credit score values are available and reliable from this point.", style={'color': 'white'}),
    html.P("Interactivity: Users can interact with the dashboard to dynamically explore how different occupations influence credit scores and observe how this relationship changes with the age of credit history.", style={'color': 'white'}),
    html.Div([
        html.Label("Select Age of Credit History:", style={'color': 'orange'}),
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
                'text': [f"{occ}" for occ in filtered_df['Occupation']],
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
            {'Metric': 'Credit Score', 'Value': selected_data['Credit_Score']},
        ]

        return html.Div([
            html.H2(f"Occupation: {selected_occupation} - Age of credit history: {selected_age} Years", style={'color': 'orange'}),
            html.P("Only data corresponding to the specified occupation and the specified 'Age of Credit \n"
                   "History' are being used for the calculations", style={'color': 'white'}),
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