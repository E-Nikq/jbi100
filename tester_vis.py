import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_excel("outdated_files/final_cleaned_data_new.xlsx")

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
    'Credit_Score': most_frequent_credit_score
}).reset_index()

avg_debt_per_occupation_age = avg_debt_per_occupation_age.round({'Outstanding_Debt': 0,
                                                                'Age': 0,
                                                                'Annual_Income': 0,
                                                                'Credit_Utilization_Ratio': 0,
                                                                'Credit_Score': 0})

min_age = int(df['Credit_History_Age'].min())
max_age = min(33, int(df['Credit_History_Age'].max()))

app = dash.Dash(__name__)

app.layout = html.Div(
    style={'backgroundColor': 'black', 'color': 'white'},
    children=[
        dcc.Location(id='url', refresh=False),
        html.H1("Credit Analysis Dashboard", style={'color': '#FF6347', 'text-align': 'center', 'margin-top': '20px'}),
        html.P("Task Abstraction: Explore the relationship between outstanding debts, occupations, and the age of credit history. Specifically, understand how different occupations impact debts and how this relationship varies with the age of credit history. Use Dash for an interactive visualization to provide dynamic insights from the data.", style={'margin-bottom': '20px'}),
        html.P("Additional Information: Data Source - Financial records of individuals in Finance, Economics, Business Analytics, or Data Science fields.", style={'margin-bottom': '20px'}),
        html.P("Visualization Components: Y-Axis (Vertical): Average outstanding debt, X-Axis (Horizontal): Occupation, Third Variable (Interactive): Age of Credit History. Starting Point: Data from the 50002nd row onward will be considered, as credit score values are available and reliable from this point.", style={'margin-bottom': '20px'}),
        html.P("Interactivity: Users can interact with the dashboard to dynamically explore how different occupations influence credit scores and observe how this relationship changes with the age of credit history.", style={'margin-bottom': '20px'}),
        html.Div([
            html.Label("Select Age of Credit History:", style={'color': '#FF6347'}),
            dcc.Slider(
                id='credit-age-slider',
                min=min_age,
                max=max_age,
                step=1,
                marks={i: str(i) for i in range(min_age, max_age + 1)},
                value=min_age,
            ),
            html.Label("Select Occupation:", style={'color': '#FF6347', 'margin-top': '20px'}),
            dcc.Dropdown(
                id='occupation-dropdown',
                options=[{'label': 'All', 'value': 'all'}] + [{'label': occ, 'value': occ} for occ in df['Occupation'].unique()],
                value=['all'],
                multi=True,
                style={'color': 'black', 'width': '150px', 'backgroundColor': '#144E78'}  # Set background color to a navy blue shade
            ),
        ]),
        dcc.Graph(id='credit-score-graph'),
        html.Div(id='page-content', style={'margin': 'auto', 'width': '50%'}),
    ]
)

@app.callback(
    Output('credit-score-graph', 'figure'),
    [Input('credit-age-slider', 'value'),
     Input('occupation-dropdown', 'value')]
)
def update_graph(selected_age, selected_occupation):
    if 'all' in selected_occupation:
        filtered_df = avg_debt_per_occupation_age[avg_debt_per_occupation_age['Credit_History_Age'] == selected_age]
    else:
        filtered_df = avg_debt_per_occupation_age[
            (avg_debt_per_occupation_age['Credit_History_Age'] == selected_age) &
            (avg_debt_per_occupation_age['Occupation'].isin(selected_occupation))
        ]

    figure = {
        'data': [
            {
                'x': filtered_df['Occupation'],
                'y': filtered_df['Outstanding_Debt'],
                'type': 'bar',
                'name': 'Average Debt per Occupation',
                'marker': {'color': filtered_df['Annual_Income'], 'colorbar': {'title': 'Average Annual Income'}},
            },
        ],
        'layout': {
            'title': f'Average Outstanding Debt by Occupation (Age of Credit History: {selected_age} Years)',
            'xaxis': {'title': 'Occupation', 'categoryorder': 'total ascending'},
            'yaxis': {'title': 'Average Outstanding Debt'},
            'clickmode': 'event+select',
            'plot_bgcolor': 'black',
            'paper_bgcolor': 'black',
            'legend': {'title': {'text': 'Average Annual Income'}, 'bgcolor': 'black', 'bordercolor': 'white', 'borderwidth': 1, 'font': {'color': 'white'}},
        }
    }

    return figure

@app.callback(
    Output('page-content', 'children'),
    [Input('credit-score-graph', 'clickData'),
     Input('credit-age-slider', 'value')]
)
def display_selected_data_new(chart_click_data, selected_age):
    if chart_click_data:
        selected_occupation_index = chart_click_data['points'][0]['pointIndex']
        selected_occupation = chart_click_data['points'][0]['x']
        selected_data = avg_debt_per_occupation_age[
            (avg_debt_per_occupation_age['Occupation'] == selected_occupation) &
            (avg_debt_per_occupation_age['Credit_History_Age'] == selected_age)
        ]

        if not selected_data.empty:
            selected_data = selected_data.iloc[0]

            table_data = [
                {'Metric': 'Average Outstanding Debt in $', 'Value': selected_data['Outstanding_Debt']},
                {'Metric': 'Average Age in Years', 'Value': selected_data['Age']},
                {'Metric': 'Average Annual Income in $', 'Value': selected_data['Annual_Income']},
                {'Metric': 'Credit Utilization Ratio', 'Value': selected_data['Credit_Utilization_Ratio']},
                {'Metric': 'Credit Score', 'Value': selected_data['Credit_Score']},
            ]

            return html.Div([
                html.H2(f"Occupation: {selected_occupation} - Age of credit history: {selected_age} Years", style={'color': '#FF6347'}),
                html.P("Only data corresponding to the specified occupation and the specified 'Age of Credit \n"
                       "History' are being used for the calculations", style={'margin-bottom': '20px'}),
                dash_table.DataTable(
                    id='selected-data-table',
                    columns=[{'name': 'Metric', 'id': 'Metric'}, {'name': 'Value', 'id': 'Value'}],
                    data=table_data,
                    style_table={'overflowX': 'auto'},
                    style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
                    style_cell={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
                )
            ])

    return html.Div()

if __name__ == '__main__':
    app.run_server(debug=True)
