import pandas as pd
from data_loader import credit_data

# pd.plotting.scatter_matrix(credit_data[["age", "Annual_Income", "Monthly_Inhand_Salary", "Num_Bank_Accounts","Num_Credit_Card", "Interest_Rate", "Num_of_Loan", "Delay_from_due_date",
#                                         "Num_of_Delayed_Payment", "Changed_Credit_Limit", "Num_Credit_Inquiries",
#                                         "Outstanding_Debt", "Credit_Utilization_Ratio", "Total_EMI_per_month",
#                                         "Amount_invested_monthly", "Monthly_Balance"]], diagonal="kde", figsize=(10, 10))

from dash import Dash, html, dcc
from dash import Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# Read the data from csv file
df = pd.read_csv("")

app.layout = html.Div([
    dcc.Dropdown(
        df['Indicator Name'].unique(),
        'Fertility rate, total (births per woman)',
        id='xaxis'
    ),
    dcc.Dropdown(
        df['Indicator Name'].unique(),
        'Life expectancy at birth, total (years)',
        id='yaxis'
    ),
    dcc.Graph(id="scatter_plot"),
    dcc.Slider(
        df['Year'].min(),
        df['Year'].max(),
        step=None,
        value=df['Year'].min(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        id="slider"
    )
])


@app.callback(
    Output("scatter_plot", "figure"),
    Input("slider", "value"),
    Input("xaxis", "value"),
    Input("yaxis", "value")
)
def update_figure(input_year, xaxis, yaxis):
    filter_df = df[df.Year == input_year]

    fig = px.scatter(x=filter_df[filter_df['Indicator Name'] == xaxis]['Value'],
                     y=filter_df[filter_df['Indicator Name'] == yaxis]['Value'],
                     hover_name=filter_df[filter_df['Indicator Name'] == yaxis]['Country Name']
                     )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)