from dash import Dash, html, dcc, callback, Output, Input
import numpy
import pandas as pd
import plotly.express as px
import csv
#test

def read_cs(csvFile):
    data = []
    with open(csvFile, 'r', newline='', encoding='utf-8') as archivo:
        csv_reader = csv.reader(archivo, delimiter=';')
        for fila in csv_reader:
            data.append(int(fila[0]))
    return data

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
ecg_data = read_cs("ECG1.csv")
ecg_time = list(range(0, len(ecg_data), 1))
ecg = {"data": ecg_data, "time": ecg_time}
n_iterations = 0
#test
app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Simulador ECG', style={'textAlign':'center'}),
    #dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    html.Button('Iniciar simulación', id='boton'),
     html.Div([
        "Frecuencia: ",
        dcc.Input(id='my-input', value='Escribe aquí', type='number')
    ]),
    html.Br(),
    html.Div(id='my-output'),
    html.Div(id='resultado'),
    #dcc.Graph(id='graph-content'),
    dcc.Graph(id='ecg-graph'),
])

#@callback(
#    Output('graph-content', 'figure'),
 #   Input('dropdown-selection', 'value')
#)
#def update_graph(value):
#    dff = df[df.country==value]
#    return px.line(dff, x='year', y='pop')

@callback(
    Output('ecg-graph', 'figure'),
    #Input('dropdown-selection', 'value')
)
def update_graph(value):
    fig = px.line(ecg, x="time", y="data")
   # fig.update_xaxes(range=[0, n_iterations])
    return fig

@callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return f'Frecuencia output: {input_value}'

@app.callback(
    Output('resultado', 'children'),
    Input('boton', 'n_clicks')
)
def actualizar_output(n_clicks):
    if n_clicks is None:
        return "Haz clic en el botón."
    else:
        return f"Has hecho clic {n_clicks} veces."

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")