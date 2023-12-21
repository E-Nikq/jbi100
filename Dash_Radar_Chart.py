from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

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
    html.Div(style={'flexgrow':1,'backgroundColor': colors['background']}, children=[
        html.H1(
            children='Radar Chart',
            style={'textAlign': 'center',
                   'color': colors['text'] }
        ),

        html.Div(children='Radar Chart', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        dcc.Graph(
            id='Radar Chart',
            style={'width': '100%', 'Align': 'center'}
        ),

        html.Div(style={'position': 'absolute', 'top': '50px', 'left': '10px', 'backgroundColor': colors['background'],'width': '10%'},
                 children=[
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
                     multi=True)
        ])
    ]),

    html.Div(style={'margin-top': '0px', 'backgroundColor': colors["background"], 'padding-left': '10px','width': '50%'},
             children=[
                 html.Div(style={'width': '80%', 'color': colors['text'], 'backgroundColor':colors["background"]},children=[
                     dcc.Dropdown(value="Num_of_Loan",
                        id="X_axis_option",
                        style={'width': '55%', 'color': colors["text"],
                           'display': 'inline-block'}
                    ),
                    dcc.RadioItems(id='distribution',
                        options=[{'label': 'Hist', 'value': 'Hist'}, {'label': 'None', 'value': 'None'}],
                        value='None', inline=True,
                        style={'color': colors["text"], 'width': '30%', 'display': 'inline-block','float': 'center'}
                    ),
                    dcc.RadioItems(id='X_axis_type',
                        options=[{'label': 'Linear', 'value': 'linear'}, {'label': 'Log', 'value': 'log'}],
                        value='linear',
                        style={'color': colors["text"], 'width': '15%',
                                'display': 'inline-block',
                                'float': 'right'},
                        inline=True,
                    )]),
                dcc.Graph(id="Add_chart")
             ])
])

@app.callback(
    Output('Radar Chart', 'figure'),
    Output('X_axis_option', 'options'),
    [Input('DropdownAttribute', 'value'),
     Input('Multi', 'value')]
)
def update_RadarChart(DropdownAttribute, MultidropdownAttribute):
    Unique_Attribute = df[DropdownAttribute].unique()
    Mean_Multi_All = df[MultidropdownAttribute].mean()
    Std_Multi_Att = df[MultidropdownAttribute].std()

    fig = go.Figure()
    for name_uni in Unique_Attribute:
        Mean_Multi_AttData = df.loc[df[DropdownAttribute] == name_uni,MultidropdownAttribute].mean()
        Z_value_uni = (Mean_Multi_AttData-Mean_Multi_All)/Std_Multi_Att

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
                      transition_duration=500
                      )

    return fig, [{'label': i, 'value' : i} for i in MultidropdownAttribute]

@app.callback(
    Output('X_axis_option', "value"),
    Input("X_axis_option", "value")
)
def set_dist_plots(Current_option):
    return Current_option

@app.callback(Output('Add_chart', 'figure'),
              [Input('DropdownAttribute', "value"),
                Input("X_axis_option","value"),
                Input('X_axis_type', "value"),
                Input("distribution", "value")
               ])
def Update_add_charts(DropdownAttribute, X_axis_option, X_axis_type,Hist_rug_none):
    if Hist_rug_none == "Hist":
        Hist = True
    else:
        Hist = False

    hist_data = []
    for uni_name in df[DropdownAttribute].unique():
        Data_uni_att = df[df[DropdownAttribute] == uni_name][X_axis_option]
        hist_data.append(Data_uni_att)

    fig = ff.create_distplot(hist_data, group_labels=df[DropdownAttribute].unique(), show_hist=Hist,
                             show_rug=False, curve_type='normal')

    fig.update_xaxes(title=X_axis_option,
                     type='linear' if X_axis_type == 'linear' else 'log')

    fig.update_yaxes(title="Frequency")

    fig.update_layout(transition_duration=500,
                      plot_bgcolor=colors['background'],
                      paper_bgcolor=colors['background'],
                      font_color=colors['text'])
    return fig

if __name__ == '__main__':
    app.run(debug=True)


