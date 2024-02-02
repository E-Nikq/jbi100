import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, dash_table, callback_context
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

df = pd.read_excel('used_data.xlsx')

app = Dash(__name__)

def most_frequent_credit_score(x):
    if not x.empty:
        value_counts = x.value_counts()
        if not value_counts.empty:
            return value_counts.idxmax()
    return None

avg_debt_per_occupation_age = df.groupby(['Occupation', 'Credit_History_Age']).agg({
    'Outstanding_Debt': 'mean',
    'Age': 'mean',
    'Annual_Income_Code2': 'mean',
    'Credit_Utilization_Ratio': 'mean',
    'Credit_Score': most_frequent_credit_score
}).reset_index()

avg_debt_per_occupation_age = avg_debt_per_occupation_age.round({'Outstanding_Debt': 0,
                                                                'Age': 0,
                                                                'Annual_Income_Code2': 0,
                                                                'Credit_Utilization_Ratio': 0,
                                                                'Credit_Score': 0})

avg_income_per_occupation = df.groupby('Occupation')['Annual_Income_Code2'].mean().reset_index()
avg_debt_per_occupation = df.groupby('Occupation')['Outstanding_Debt'].mean().reset_index()
avg_income_per_occupation.columns = ['Occupation', 'Avg_Annual_Income']
avg_debt_per_occupation.columns = ['Occupation', 'Avg_Outstanding_Debt']

min_age = int(df['Credit_History_Age'].min())
max_age = min(33, int(df['Credit_History_Age'].max()))

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# Calculate Credit Score Probability
credit_score_probabilities = df.groupby('Occupation')['Credit_Score'].apply(lambda x: (x == 'Poor').mean()).reset_index()
credit_score_probabilities.columns = ['Occupation', 'Credit_Score_Probability']

# Add the Columns to DataFrame
df = pd.merge(df, avg_income_per_occupation, on='Occupation', how='left')
df = pd.merge(df, avg_debt_per_occupation, on='Occupation', how='left')
df = pd.merge(df, credit_score_probabilities, on='Occupation', how='left')

scatter_fig = px.scatter(
    df,
    x='Avg_Annual_Income',
    y='Avg_Outstanding_Debt',
    size='Credit_Score_Probability',
    color='Occupation',
    labels={'Avg_Annual_Income': 'Average Annual Income in $', 'Avg_Outstanding_Debt': 'Average Outstanding Debt in $'},
    title='Scatter Plot with Credit Score Probability',
    hover_data={'Credit_Score_Probability': ':.2%'},
    size_max=250
)

scatter_fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    title='Scatter Plot with Credit Score Probability',
    annotations=[
        {
            'x': 0.5,
            'y': 1.07,
            'xref': 'paper',
            'yref': 'paper',
            'text': 'Bubble size is proportional to the probability of the credit score being \'Poor\'',
            'showarrow': False,
            'font': {'size': 14, 'color': colors['text']}
        }
    ],
    height=800
)

Categorical_names = ['Credit_Mix', 'Occupation', 'Payment_of_Min_Amount', 'Month', 'Credit_Score',
                     'Payment_Behaviour']
Numeric_names = ["Age", "Amount_invested_monthly", "Changed_Credit_Limit", "Interest_Rate",
                 "Monthly_Inhand_Salary",
                 "Num_Bank_Accounts", "Num_Credit_Card", "Num_Credit_Inquiries", "Num_of_Delayed_Payment",
                 "Num_of_Loan",
                 "Outstanding_Debt", "Delay_from_due_date", "Credit_Utilization_Ratio", "Credit_History_Age",
                 "Total_EMI_per_month", "Monthly_Balance", "Annual_Income"]
Aggregate_functions = ["mean","count","min","max","median","std"]

df_Num = df[Numeric_names]
corr = df_Num.corr()
corr = np.round(corr,2)

fig = px.imshow(corr, labels=dict(x="Numeric Attributes", y="Numeric Attributes", color='Correlation'),
                x=Numeric_names,
                y=Numeric_names,
                text_auto=True,
                color_continuous_scale='reds',
                color_continuous_midpoint=0)
fig.update_layout(
    title="Correlation Heat Map",
    width=1200, height=800,
    transition_duration=500,
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
fig.update_xaxes(tickangle=30, tickfont=dict(size=15))
fig.update_yaxes(tickfont=dict(size=15))
fig.update_traces(textfont=dict(size=12),
                  hovertemplate='%{x}<br>%{y}<br>Correlation: %{z:.2f}')

app.layout = html.Div(style={'backgroundColor': colors['background'], 'height': '100vh'}, children=[
    html.Div(style={'backgroundColor': colors['background']}, children=[
      dcc.Graph(id='Correlation Heat Map',
                style={'width': '100%', 'Align': 'center'},
                figure=fig)
    ]),

    html.Div(style={'flexgrow':1,'backgroundColor': colors['background']}, children=[
        html.H1(
            children='Radar Chart',
            style={'textAlign': 'left',
                   'color': colors['text'],
                   'margin-left': '40%'}
        ),

        html.Div(style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        dcc.Graph(
            id='Radar Chart',
            style={'width': '100%', 'Align': 'center'},
            clickData={'points': [{'theta': 'Num_of_Loan'}]},
        ),

        html.Div(style={'position': 'absolute', 'top': '850px', 'left': '10px', 'backgroundColor': colors['background'],'width': '10%'},
                 children=[
            html.Label("Select the attribute:", style={'color': colors["text"]}),
            dcc.Dropdown(options=[{'label': name, 'value': name} for name in Categorical_names],
                        value='Occupation',
                        id='DropdownAttribute'
                     ),
            html.Br(),
            html.Label("Select additional attributes:", style={'color': colors["text"]}),
            dcc.Dropdown(options=[{'label': name, 'value': name} for name in Numeric_names],
                     value=['Num_of_Loan', 'Num_Bank_Accounts'],
                     id='Multi',
                     multi=True)
        ])
    ]),

    html.Div(style={'margin-top': '0px', 'backgroundColor': colors["background"], 'padding-left': '10px','width': '100%'},
             children=[
                 html.Div(style={'width': '80%', 'color': colors['text'], 'backgroundColor':colors["background"]},children=[
                    dcc.RadioItems(id='distribution',
                        options=[{'label': 'Hist', 'value': 'Hist'}, {'label': 'None', 'value': 'None'}],
                        value='None', inline=True,
                        style={'color': colors["text"], 'width': '50%', 'display': 'inline-block','float': 'center'}
                    ),
                    dcc.RadioItems(id='X_axis_type',
                        options=[{'label': 'Linear', 'value': 'linear'}, {'label': 'Log', 'value': 'log'}],
                        value='linear',
                        style={'color': colors["text"], 'width': '50%',
                                'display': 'inline-block',
                                'float': 'right'},
                        inline=True,
                    )]),
                dcc.Graph(id="Add_chart")
             ]),
    html.Div(style={'backgroundColor': 'black', 'color': 'white', "margin-top": "0px"}, children=[
        html.H1(
            children='Bar Chart',
            style={'textAlign': 'center',
                   'color': colors['text']}
        ),
        dcc.Location(id='url', refresh=False),
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
                options=[{'label': 'All', 'value': 'all'}] + [{'label': occ, 'value': occ} for occ in
                                                              df['Occupation'].unique()],
                value=['all'],
                multi=True,
                style={'color': 'black', 'width': '150px', 'backgroundColor': '#144E78'}
                # Set background color to a navy blue shade
            ),
        ]),
        dcc.Graph(id='credit-score-graph'),
        html.Div(id='page-content', style={'margin': 'auto', 'width': '50%'}),
    ]),
    html.Div(style={'flexgrow':1,'backgroundColor': colors['background']}, children=[

        html.H1(
        children='Scatter Plot',
        style={'textAlign': 'center',
               'color': colors['text'] }
    ),
    html.Button(
            id='reset-scatter-button',
            children='Reset Scatter Plot',
            n_clicks=0,
            style={'margin-top': '5px'}
    ),
    dcc.Graph(
        id='Scatter Plot',
        style={'width': '100%', 'Align': 'center'},
        figure=scatter_fig
    )

    ])

])

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
                'marker': {'color': filtered_df['Annual_Income_Code2'], 'colorbar': {'title': 'Average Annual Income'}},
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
                {'Metric': 'Average Annual Income in $', 'Value': selected_data['Annual_Income_Code2']},
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


@app.callback(
    Output('Multi', 'options'),
    [Input('Correlation Heat Map', 'clickData')]
)
def set_multi_attributes_options(selected_data):
    if selected_data is None or not selected_data['points']:
        return [{'label': i, 'value' : i} for i in Numeric_names]
    else:
        Remove = [selected_data['points'][0]['x'], selected_data['points'][0]['y']]
        Numeric_names1 = Numeric_names.copy()
        for remove in Remove:
            if remove in Numeric_names1:
                Numeric_names1.remove(remove)
        return [{'label': i, 'value': i} for i in Numeric_names1]


@app.callback(
    Output('Multi', 'value'),
    [Input('Multi', 'options'),
    State('Multi', 'value')]
)
def set_multi_attributes_values(Available_options, Current_values):
    Av_Op_values = [option['value'] for option in Available_options]
    return [value for value in Av_Op_values if value in Current_values]



@app.callback(
    Output('Radar Chart', "clickData"),
    Input("Radar Chart", "clickData")
)
def set_dist_plots(Current_option):
    return Current_option


@app.callback(
    Output('Radar Chart', 'figure'),
    [Input('DropdownAttribute', 'value'),
     Input('Multi', 'value'),
     Input('Correlation Heat Map', 'clickData'),
     Input("Add_chart",'hoverData')
     ]
)
def update_RadarChart(DropdownAttribute, Multi, selected_data, hoverData):
    if callback_context.triggered_id == 'Add_chart':
        hoverDatavalue = hoverData["points"][0]["curveNumber"]
    else:
        hoverDatavalue = range(len(df[DropdownAttribute].unique()))

    if selected_data is None or not selected_data['points']:
        MultidropdownAttribute = Multi
    else:
        MultidropdownAttribute = [selected_data['points'][0]['x'], selected_data['points'][0]['y']]
        for multi in Multi:
            if multi not in MultidropdownAttribute:
                MultidropdownAttribute.append(multi)

    if type(hoverDatavalue) == int:
        Unique_Attributes = df[DropdownAttribute].unique()
        Unique_Attribute = [(Unique_Attributes[hoverDatavalue])]
    else:
        Unique_Attributes = df[DropdownAttribute].unique()
        Unique_Attribute = Unique_Attributes[hoverDatavalue]

    Mean_Multi_All = df[MultidropdownAttribute].mean()
    Std_Multi_Att = df[MultidropdownAttribute].std()


    fig = go.Figure()
    for name_uni in Unique_Attribute:
        Mean_Multi_AttData = df.loc[df[DropdownAttribute] == name_uni, MultidropdownAttribute].mean()
        Z_value_uni = (Mean_Multi_AttData - Mean_Multi_All) / Std_Multi_Att

        fig.add_trace(go.Scatterpolar(
            r=Z_value_uni,
            theta=pd.Series(MultidropdownAttribute),
            name=name_uni,
            fill='toself'
        ))

    fig.update_layout(showlegend=True,
                      polar=dict(radialaxis=dict(visible=True)),
                      plot_bgcolor=colors['background'],
                      paper_bgcolor=colors['background'],
                      font_color=colors['text'],
                      transition_duration=500,
                      )

    return fig

@app.callback(
    Output('Add_chart', 'figure'),
    [Input('DropdownAttribute', "value"),
     Input('X_axis_type', "value"),
     Input("distribution", "value"),
     Input('Radar Chart', "clickData")
    ])
def Update_add_charts(DropdownAttribute, X_axis_type, Hist_rug_none, clickData_Radar):
    clickedAttribute = clickData_Radar['points'][0]['theta']

    if Hist_rug_none == "Hist":
        Hist = True
    else:
        Hist = False

    hist_data = []
    for uni_name in df[DropdownAttribute].unique():
        Data_uni_att = df[df[DropdownAttribute] == uni_name][clickedAttribute]
        hist_data.append(Data_uni_att)

    fig = ff.create_distplot(hist_data, group_labels=df[DropdownAttribute].unique(), show_hist=Hist,
                             show_rug=False, curve_type='normal')

    fig.update_xaxes(title=clickedAttribute,
                     type='linear' if X_axis_type == 'linear' else 'log')

    fig.update_yaxes(title="Frequency")

    fig.update_layout(transition_duration=500,
                      plot_bgcolor=colors['background'],
                      paper_bgcolor=colors['background'],
                      font_color=colors['text'],
                      title="Distribution Chart")
    return fig


@app.callback(
    Output('Scatter Plot', 'figure'),
    [Input('credit-score-graph', 'clickData'),
     Input('reset-scatter-button', 'n_clicks')]
)
def update_scatter_plot(selected_bar, reset_button_clicks):
    ctx = callback_context
    if not ctx.triggered_id:
        raise PreventUpdate

    trigger_id = ctx.triggered_id.split('.')[0]

    if trigger_id == 'reset-scatter-button' or not selected_bar:
        # Reset the scatter plot to show all data points
        scatter_figure = scatter_fig
    else:
        selected_occupation = selected_bar['points'][0]['x']
        filtered_df = df[df['Occupation'] == selected_occupation]

        scatter_figure = px.scatter(
            filtered_df,
            x='Avg_Annual_Income',
            y='Avg_Outstanding_Debt',
            size='Credit_Score_Probability',
            color='Occupation',
            labels={'Avg_Annual_Income': 'Average Annual Income in $', 'Avg_Outstanding_Debt': 'Average Outstanding Debt in $'},
            title=f'Scatter Plot for {selected_occupation}',
            hover_data={'Credit_Score_Probability': ':.2%'},
            size_max=250
        )

        scatter_figure.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            title=f'Scatter Plot for {selected_occupation}',
            annotations=[
                {
                    'x': 0.5,
                    'y': 1.07,
                    'xref': 'paper',
                    'yref': 'paper',
                    'text': 'Bubble size is proportional to the probability of the credit score being \'Poor\'',
                    'showarrow': False,
                    'font': {'size': 14, 'color': colors['text']}
                }
            ],
            height=800
        )

    return scatter_figure


if __name__ == '__main__':
    app.run_server(debug=True)