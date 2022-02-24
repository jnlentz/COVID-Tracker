import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import pandas as pd
import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
from dash.dependencies import Input, Output

df = pd.read_csv('covid_states.csv', error_bad_lines=False)    
sd = pd.read_csv('state_populations.csv', error_bad_lines=False)
gf = df.groupby('state')


def rateOfIncrease(state):
    mean = gf.get_group(state)['positiveIncrease'].agg(np.mean)
    return mean


def toDate(iDate):
    sDate = str(iDate)
    years = int(sDate[0:4])
    months = int(sDate[4:6])
    days = int(sDate[6:8])
    date = datetime.datetime(years, months, days)
    return date

def predict(state):
    Z = gf.get_group(state).sort_index(0)
    Y = Z['positiveIncrease'].values.reshape(-1, 1)
    X = []
    for i in range(len(Z['positiveIncrease'])):
        temp = [i,i]
        X.append(temp)
    linear_regressor = LinearRegression()
    linear_regressor.fit(X, Y)
    Y_pred = linear_regressor.predict(X)
    print(linear_regressor.score(X,Y))
    return(linear_regressor.score(X,Y))
  
    
def graph(state):
    Z = gf.get_group(state).sort_index(0)
    fig = px.line(Z, x='date', y='positiveIncrease')
    return fig

def generate_table(dataframe):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(len(dataframe))
        ])
    ])



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

averageIncrease = []
states = []
for i in sd['State']:
    averageIncrease.append(rateOfIncrease(i))
    states.append(i)


fig1 = px.bar(x=states, y=averageIncrease)

app.layout = html.Div([
    html.H3("COVID-19 Tracker"),
    html.Br(),
    html.Div([dcc.Graph(figure=fig1)]),
    html.Br(),
    html.Div(
        dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        page_action='native',
        style_cell={'textAlign': 'left', 'width':'100px'},
        style_table={'height': '300px', 'minWidth': '50%', 'overflowY': 'auto'})
        ),
    html.Br(),
    html.Div(["State: ",
              dcc.Input(id='input1', value='', type='text')]),
    html.Br(),
    html.Div(id='output3'),
    html.Div(id='output2'),
    html.Br(),
    html.Div(style={'height' : '300px'}, id='output1')

])




@app.callback(
    Output(component_id='output1', component_property='children'),
    [Input(component_id='input1', component_property='value')]
)
def output1(input_value):
    return generate_table(gf.get_group(input_value))

@app.callback(
    Output(component_id='output2', component_property='children'),
    [Input(component_id='input1', component_property='value')]
)
def output2(input_value):
    return 'Slope of trend line: {}'.format(predict(input_value))

@app.callback(
    Output(component_id='output3', component_property='children'),
    [Input(component_id='input1', component_property='value')])
def output3(input_value):
    return 'Mean daily increase: {}'.format(rateOfIncrease(input_value))

if __name__ == '__main__':
    app.run_server(debug=False)
































