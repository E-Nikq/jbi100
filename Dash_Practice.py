from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

app = Dash(__name__)

df = pd.read_excel('C:/Users/Timo/Documents/School NT/Minor/JBI100 Visualization/final_cleaned_data_new_good.xlsx')

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

Categorical_names = ['Credit_Mix', 'Occupation', 'Payment_of_Min_Amount', 'Month', 'Credit_Score',
                     'Payment_Behaviour']
Numeric_names = ["Age", "Amount_invested_monthly", "Changed_Credit_Limit", "Interest_Rate",
                 "Monthly_Inhand_Salary",
                 "Num_Bank_Accounts", "Num_Credit_Card", "Num_Credit_Inquiries", "Num_of_Delayed_Payment",
                 "Num_of_Loan",
                 "Outstanding_Debt", "Delay_from_due_date", "Credit_Utilization_Ratio", "Credit_History_Age",
                 "Total_EMI_per_month", "Monthly_Balance", "Annual_Income"]
Aggregate_functions = ["mean","count","min","max","median","std"]

app.layout = html.Div([
    html.Div(style={'flex-grow': 1, 'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Radar Chart',
        style={'textAlign': 'center',
            'color': colors['text']
        }

    ),

    html.Div(children='Radar Chart', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='Radar Chart',
        style={'width': '100%', 'Align':'center'}
    ),

    html.Div(style={'position': 'absolute', 'top': '50px', 'left': '10px', 'backgroundColor': colors['background'],
                    'width': '10%'}, children=[
        html.Label("Select the attribute:", style={'color': colors["text"]}),
        dcc.Dropdown(options=[{'label': name, 'value': name} for name in Categorical_names],
                     value='Occupation',
                     id='DropdownAttribute'
                     ),
        html.Br(),
        html.Label("Select attributes to compare:", style={'color': colors["text"]}),
        dcc.Dropdown(options=[{'label': name, 'value': name} for name in Numeric_names],
                     value=['Num_of_Loan', 'Num_Bank_Accounts'],
                     id='Multi',
                     multi=True),
        html.Br(),
        html.Label("Select the aggregate function:", style={'color': colors["text"]}),
        dcc.Dropdown(Aggregate_functions,
                     'mean',
                     id='AggFunDropDown')
    ])
    ]),
    html.Div(style={'width':'49%', 'position': 'absolute','backgroundColor':colors["background"]}, children=[
        dcc.Dropdown(
            Numeric_names,
            "Age",
            id="X_axis_option",
            style={'width':'35%'}
        ),
        dcc.RadioItems(
            options=[{'label': 'Linear', 'value': 'Linear'}, {'label': 'Log', 'value': 'Log'}],
            value='Linear',
            id="X_axis_type",
            labelStyle={'display': 'inline-block', 'marginTop': '5px'},
            style={'backgroundColor': colors["background"], 'color': colors['text'], 'width': '20%'}
        ),

        dcc.Graph(id="Add_chart")
    ])
])


@app.callback(
    Output('Radar Chart', 'figure'),
    [Input('DropdownAttribute', 'value'),
     Input('Multi', 'value'),
     Input('AggFunDropDown','value')]
)
def update_RadarChart(DropdownAttribute, MultidropdownAttribute,Aggfunc):
    attributes = [DropdownAttribute] + MultidropdownAttribute

    df_subset = df[attributes]
    df_avg_sel_att = df_subset.pivot_table(index=DropdownAttribute, aggfunc=Aggfunc)

    fig = go.Figure()

    for name_att in MultidropdownAttribute:
        fig.add_trace(go.Scatterpolar(
            r=df_avg_sel_att[name_att],
            theta=pd.Series(df_subset[DropdownAttribute].unique(),name=DropdownAttribute),
            name=name_att,
            fill='toself'
        ))

    fig.update_layout(showlegend=True,
                      polar=dict(radialaxis=dict(visible=True)),
                      plot_bgcolor=colors['background'],
                      paper_bgcolor=colors['background'],
                      font_color=colors['text'],
                      transition_duration=500
                      )
    return fig

@app.callback(Output('Add_chart', 'figure'),
              [Input('Radar Chart','clickData'),
               Input('X_axis_option','value'),
               Input('X_axis_type','value'),
               Input('DropdownAttribute', 'value')
               ]
              )
def Update_add_charts(clickData,X_axis_option,X_axis_type,DropdownAttribute):
    if clickData is None:
        selected_theta_value = df[DropdownAttribute].unique()[0]
    else:
        selected_theta_value = clickData['points'][0]['x']

    filtered_df = df.loc[df[DropdownAttribute] == selected_theta_value]

    fig = px.scatter(filtered_df, x=X_axis_option, y="Age", color="Occupation")

    fig.update_xaxes(title=X_axis_option, type='linear' if X_axis_type == 'Linear' else 'log')
    fig.update_yaxes(title="Age")
    fig.update_layout(transition_duration=500,
                      plot_bgcolor=colors['background'],
                      paper_bgcolor=colors['background'],
                      font_color=colors['text'])
    return fig

if __name__ == '__main__':
    app.run(debug=True)


