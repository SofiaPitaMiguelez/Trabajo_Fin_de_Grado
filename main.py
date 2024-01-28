import dash
from dash import html, dcc, Dash
from dash.dependencies import Input, Output
from map_app_instance import map_app_instance as map_instance_layout
from map_app_instance import map_app_instance_callbacks
from app_instance import app_instance as app_layout
from app_instance import app_instance_callbacks


main = dash.Dash(__name__, suppress_callback_exceptions=True)

new_view_layout = html.Div([
    html.Div([
        html.H1("Visualización de resultados obtenidos en el análisis de la calidad del aire en el Puerto de Almería y su área de afectación", style={'font-weight': 'bold', 'margin-bottom': '20px', 'font-size': '50px'}),
        #html.H2("Bienvenido, en esta página podrás acceder a la visualización de los resultados obtenidos sobre el análisis de calidad del aire del Puerto de Almería y su área de afectación.", style={'margin-bottom': '15px'}),
        html.H2("A continuación, puedes seleccionar la vista a la que quieres acceder:", style={'font-weight': 'normal', 'margin-bottom': '15px'}),
    ], style={'color': 'black', 'padding': '20px', 'border-radius': '10px', 'background-color': 'white', 'width': '80%', 'margin': 'auto'}),
    html.Div([
        dcc.Link("- Gráficas generadas sobre el ICA y los agentes contaminantes", href="/app_instance", style={'font-size': '30px', 'margin-bottom': '10px'}),
        html.H3("Donde podrás visualizar cuales son los agentes más contaminantes en ciertos puntos temporales y espaciales, así como la evolución del Índice de Calidad del Aire (ICA) medida por un sensor a lo largo del mes que selecciones", style={'margin-bottom': '20px'}),
    ], style={'color': 'black', 'font-weight': 'normal', 'padding': '20px', 'border-radius': '10px', 'background-color': 'white', 'width': '80%', 'margin': 'auto', 'margin-top': '20px'}),
    html.Div([
        dcc.Link("- Visualización del mapa del área en estudio", href="/map_app_instance", style={'font-size': '30px', 'margin-bottom': '10px'}),
        html.H3("Donde podrás ver cómo evolucionan los valores de ICA en diferentes puntos del área de estudio a lo largo del período de tiempo que escojas. Además, podrás decidir si quieres que la información esté desagregada o sigua algún tipo de agrupación", style={'margin-bottom': '20px'}),
    ], style={'color': 'black', 'font-weight': 'normal', 'padding': '20px', 'border-radius': '10px', 'background-color': 'white', 'width': '80%', 'margin': 'auto', 'margin-top': '20px'}),
], style={'background-color': '#082255', 'height': '100vh', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'center', 'margin': 'auto', 'margin-top': '50px'})

main.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id="page-content", style={'font-family': 'Arial, sans-serif'}),
    html.Div(style={'width': '10%', 'background-color': 'white'}),
    html.Div(style={'width': '10%', 'background-color': 'white'}),
])

@main.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/app_instance":
        return app_layout.layout
    elif pathname == "/map_app_instance":
        return map_instance_layout.layout
    else:
        return new_view_layout
    
map_app_instance_callbacks(main)    
app_instance_callbacks(main)

    

if __name__ == "__main__":
    main.run_server(debug=True)

