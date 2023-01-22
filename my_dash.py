import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

app = dash.Dash()

x = [1, 2, 3, 4, 5]
y = [2, 3, 4, 5, 6]

trace = go.Scatter(x=x, y=y, mode='lines')
data = [trace]

layout = go.Layout(title='Line Plot Example', xaxis={'title': 'X'}, yaxis={'title': 'Y'})

fig = go.Figure(data=data, layout=layout)

app.layout = html.Div([
    dcc.Graph(id='line-plot', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)